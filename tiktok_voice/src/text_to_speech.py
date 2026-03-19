# Python standard modules
import asyncio
import os
import base64
import json
import re
import sys
from json import load
from pathlib import Path
from typing import Dict, List, Optional

# Downloaded modules
import aiohttp
from playsound import playsound

# Local files
from .voice import Voice

DEFAULT_PRONUNCIATION_OVERRIDES_FILE_NAME = 'pronunciation_overrides.json'

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
    success: bool = False    

    # Iterate over endpoints to find a working one
    for endpoint in endpoint_data:
        # Generate audio bytes from the current endpoint
        audio_bytes: bytes = asyncio.run(_fetch_audio_bytes_async(endpoint, normalized_text, voice))

        if audio_bytes:
            # Save the generated audio to a file
            _save_audio_file(output_file_path, audio_bytes)
        
            # Optionally play the audio file
            if play_sound:
                playsound(output_file_path)
            
            success = True
            # Stop after processing a valid endpoint
            break

    if not success:
        raise Exception("failed to generate audio, all endpoints failed")

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
) -> Optional[bytes]:
    text_chunks: List[str] = _split_text(text)
    audio_chunks: List[str] = [""] * len(text_chunks)

    async def fetch_chunk(
        session: aiohttp.ClientSession,
        index: int,
        text_chunk: str
    ):
        async with session.post(
            endpoint["url"],
            json={"text": text_chunk, "voice": voice.value},
        ) as response:
            response.raise_for_status()
            data = await response.json()
            audio_chunks[index] = data[endpoint["response"]]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_chunk(session, i, chunk) for i, chunk in enumerate(text_chunks)]
        
        try:
            await asyncio.gather(*tasks)
        except:
            return None

    return base64.b64decode("".join(audio_chunks))

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
    
    # Split text into chunks based on punctuation marks
    merged_chunks: List[str] = []
    separated_chunks: List[str] = re.findall(r'.*?[.,!?:;-]|.+', text)
    character_limit: int = 300
    # Further split any chunks longer than 300 characters
    for i, chunk in enumerate(separated_chunks):
        if len(chunk.encode("utf-8")) > character_limit:
            separated_chunks[i:i+1] = re.findall(r'.*?[ ]|.+', chunk) 

    # Combine chunks into segments of 300 characters or less
    current_chunk: str = ""
    for separated_chunk in separated_chunks:
        if len(current_chunk.encode("utf-8")) + len(separated_chunk.encode("utf-8")) <= character_limit:
            current_chunk += separated_chunk
        else:
            merged_chunks.append(current_chunk)
            current_chunk = separated_chunk

    # Append the last chunk
    merged_chunks.append(current_chunk)
    return merged_chunks
