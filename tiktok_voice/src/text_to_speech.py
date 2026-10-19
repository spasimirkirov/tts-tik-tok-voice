# Python standard modules
import asyncio
import os
import base64
import json
import re
import ssl
import sys
from json import load
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Downloaded modules
import aiohttp

# Local files
from .voice import Voice

DEFAULT_PRONUNCIATION_OVERRIDES_FILE_NAME = 'pronunciation_overrides.json'

# Per request: a stuck endpoint gives up in time for the next one to be tried.
REQUEST_TIMEOUT_SECONDS = 12


def _create_ssl_context() -> ssl.SSLContext:
    """Verified TLS. certifi's CA bundle travels inside the PyInstaller exe, where the
    system certificates are not always found (that broke verification in the built exe)."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()

def tts(
    text: str,
    voice: Voice,
    output_file_path: str = "output.mp3",
    play_sound: bool = False
):
    """Main function to convert text to speech and save to a file."""
    
    # Validate input arguments
    _validate_args(text, voice)
    normalized_text = _normalize_text_for_voice(text, voice)

    # Load endpoint data from the endpoints.json file
    endpoint_data: List[Dict[str, str]] = _load_endpoints()
    errors: List[str] = []

    # Iterate over endpoints to find a working one
    for endpoint in endpoint_data:
        # Generate audio bytes from the current endpoint
        audio_bytes, error = asyncio.run(_fetch_audio_bytes_async(endpoint, normalized_text, voice))

        if audio_bytes:
            # Save the generated audio to a file
            _save_audio_file(output_file_path, audio_bytes)

            # Optionally play the audio file (playsound is only needed for --play)
            if play_sound:
                from playsound import playsound
                playsound(output_file_path)

            return

        errors.append(f"{endpoint['url']}: {error}")

    raise Exception("failed to generate audio, all endpoints failed: " + " | ".join(errors))

def _save_audio_file(output_file_path: str, audio_bytes: bytes):
    """Write the audio bytes to a file."""
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
        
    with open(output_file_path, "wb") as file:
        file.write(audio_bytes)

async def _fetch_audio_bytes_async(
    endpoint: Dict[str, str],
    text: str,
    voice: Voice
) -> Tuple[Optional[bytes], Optional[str]]:
    """Audio bytes for the whole text, or (None, reason) when this endpoint failed."""
    text_chunks: List[str] = _split_text(text)
    audio_chunks: List[bytes] = [b""] * len(text_chunks)
    ssl_context = _create_ssl_context()

    async def fetch_chunk(
        session: aiohttp.ClientSession,
        index: int,
        text_chunk: str
    ):
        async with session.post(
            endpoint["url"],
            json={"text": text_chunk, "voice": voice.value},
            ssl=ssl_context
        ) as response:
            response.raise_for_status()
            data = await response.json(content_type=None)
            encoded = data.get(endpoint["response"]) if isinstance(data, dict) else None
            if not encoded:
                raise ValueError(f"no audio in response: {str(data)[:200]}")
            # Each chunk is its own base64 string with its own padding: decode them one by
            # one. Joining the strings first stopped at the first "=" and lost the rest.
            audio_chunks[index] = base64.b64decode(encoded)

    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT_SECONDS)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [fetch_chunk(session, i, chunk) for i, chunk in enumerate(text_chunks)]

        try:
            await asyncio.gather(*tasks)
        except Exception as error:
            return None, f"{type(error).__name__}: {error}"

    return b"".join(audio_chunks), None

def _load_endpoints() -> List[Dict[str, str]]:
    """Load endpoint configurations from a JSON file."""
    package_root = _get_package_root()
    json_file_path = package_root / 'data' / 'config.json'
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return load(file)


def _normalize_text_for_voice(text: str, voice: Voice) -> str:
    replacements = _load_pronunciation_overrides(voice)
    normalized_text = text

    for pattern, replacement in replacements.items():
        normalized_text = re.sub(pattern, replacement, normalized_text, flags=re.IGNORECASE)

    return normalized_text


def _load_pronunciation_overrides(voice: Voice) -> Dict[str, str]:
    override_config = _load_pronunciation_override_config()
    voice_keys = _build_pronunciation_override_keys(voice)
    replacements: Dict[str, str] = {}

    for voice_key in voice_keys:
        replacements.update(override_config.get(voice_key, {}))

    return replacements


def _build_pronunciation_override_keys(voice: Voice) -> List[str]:
    keys = ['default']

    if voice.name.startswith('JP_') or voice.value.startswith('jp_'):
        keys.append('jp')

    keys.append(voice.name)
    return keys


def _load_pronunciation_override_config() -> Dict[str, Dict[str, str]]:
    config: Dict[str, Dict[str, str]] = {}

    for config_path in _get_pronunciation_override_paths():
        if not config_path.exists():
            continue

        with open(config_path, 'r', encoding='utf-8') as file:
            loaded_config = json.load(file)

        if not isinstance(loaded_config, dict):
            continue

        for section, overrides in loaded_config.items():
            if not isinstance(section, str) or not isinstance(overrides, dict):
                continue

            section_overrides = config.setdefault(section, {})
            section_overrides.update({
                pattern: replacement
                for pattern, replacement in overrides.items()
                if isinstance(pattern, str) and isinstance(replacement, str)
            })

    return config


def _get_pronunciation_override_paths() -> List[Path]:
    paths: List[Path] = []
    packaged_config_path = _get_package_root() / 'data' / DEFAULT_PRONUNCIATION_OVERRIDES_FILE_NAME
    paths.append(packaged_config_path)

    for candidate_dir in _get_external_override_directories():
        candidate_path = candidate_dir / DEFAULT_PRONUNCIATION_OVERRIDES_FILE_NAME
        if candidate_path not in paths:
            paths.append(candidate_path)

    return paths


def _get_external_override_directories() -> List[Path]:
    directories: List[Path] = []

    if getattr(sys, 'frozen', False):
        directories.append(Path(sys.executable).resolve().parent)

    directories.append(Path.cwd())
    return directories


def _get_package_root() -> Path:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / 'tiktok_voice'

    return Path(__file__).resolve().parents[1]

def _validate_args(text: str, voice: Voice):
    """Validate the input arguments."""
    
    # Check if the voice is of the correct type
    if not isinstance(voice, Voice):
        raise TypeError("'voice' must be of type Voice")
    
    # Check if the text is not empty
    if not text:
        raise ValueError("text must not be empty")

def _split_text(text: str) -> List[str]:
    """Split text into chunks of 300 characters or less."""
    
    character_limit: int = 300

    # "." does not match a line break: turn breaks into spaces so words across lines stay apart
    text = re.sub(r'\s+', ' ', text).strip()

    # Split text into chunks based on punctuation marks, then split any chunk longer than
    # the limit on spaces (a new list: replacing items while iterating skipped some)
    separated_chunks: List[str] = []
    for chunk in re.findall(r'.*?[.,!?:;-]|.+', text):
        if len(chunk.encode("utf-8")) > character_limit:
            separated_chunks.extend(re.findall(r'.*?[ ]|.+', chunk))
        else:
            separated_chunks.append(chunk)

    # Combine chunks into segments of 300 characters or less
    merged_chunks: List[str] = []
    current_chunk: str = ""
    for separated_chunk in separated_chunks:
        if len(current_chunk.encode("utf-8")) + len(separated_chunk.encode("utf-8")) <= character_limit:
            current_chunk += separated_chunk
        else:
            if current_chunk.strip():
                merged_chunks.append(current_chunk)
            current_chunk = separated_chunk

    # Append the last chunk (never send an empty one: the API rejects it)
    if current_chunk.strip():
        merged_chunks.append(current_chunk)
    return merged_chunks
