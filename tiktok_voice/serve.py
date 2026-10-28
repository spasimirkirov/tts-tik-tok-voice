"""`--serve`: Pal Engine's persistent TTS worker (protocol v1).

The host starts `TikTokVoiceTTS.exe --serve` once and keeps it running, instead of starting the exe
for every sentence (unpacking the one-file exe and importing Python each time costs 0.5-3 s).

    ready:     {"event": "ready"}                                   (stdout, once)
    request:   {"id": "7", "action": "synthesize", "text": "...", "voice_id": "US_FEMALE_1",
                "output": "C:\\...\\x.mp3"}                          (stdin, one per line)
    response:  {"id": "7", "ok": true, "output": "C:\\...\\x.mp3"}
               {"id": "7", "ok": false, "error": "..."}            (stdout, one per line)

Extra fields (speed, pitch) are ignored: TikTok voices have no tuning. One request at a time. Logs
go to stderr, never stdout (tts() prints, so its output is redirected). The worker ends when stdin
closes (the host quit or stopped it).
"""

import contextlib
import json
import sys
from pathlib import Path

from .src.text_to_speech import tts
from .src.voice import Voice


def _send(message: dict) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle(request: dict) -> dict:
    """One request -> one response (never raises)."""
    request_id = request.get("id")
    try:
        if request.get("action", "synthesize") != "synthesize":
            raise ValueError(f"unknown action: {request.get('action')}")
        output = Path(str(request.get("output") or ""))
        if not str(output):
            raise ValueError("output is required")
        voice = Voice.from_string(str(request.get("voice_id") or ""))
        if voice is None:
            raise ValueError(f"invalid voice: {request.get('voice_id')}")
        text = str(request.get("text") or "").strip()
        if not text:
            raise ValueError("text must not be empty")
        output.parent.mkdir(parents=True, exist_ok=True)
        # stdout is the protocol channel: anything tts() prints goes to stderr instead.
        with contextlib.redirect_stdout(sys.stderr):
            tts(text, voice, str(output), False)
        if not output.exists() or output.stat().st_size == 0:
            raise RuntimeError("no audio was written")
        return {"id": request_id, "ok": True, "output": str(output)}
    except Exception as error:  # network, endpoint and file errors
        return {"id": request_id, "ok": False, "error": f"{type(error).__name__}: {error}"}


def serve() -> int:
    # The host writes UTF-8 JSON; the Windows console default would break non-ASCII text.
    # utf-8-sig: a byte-order mark in front of the first line (PowerShell pipes add one) is skipped.
    sys.stdin.reconfigure(encoding="utf-8-sig")
    sys.stdout.reconfigure(encoding="utf-8")
    _send({"event": "ready"})
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except ValueError:
            print(f"serve: not JSON: {line[:80]}", file=sys.stderr)
            continue
        if isinstance(request, dict):
            _send(handle(request))
    return 0
