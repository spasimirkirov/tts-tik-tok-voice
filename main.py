import argparse
import json
from pathlib import Path

from tiktok_voice import tts, Voice
from tiktok_voice.src.voice import voices_payload

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Generate TikTok voice TTS audio.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument('-t', '--text', help='Text input to speak.')
    input_group.add_argument(
        '-txt',
        '--text-file',
        type=Path,
        help='Path to a UTF-8 text file to speak.',
    )
    input_group.add_argument(
        '--list-voices',
        action='store_true',
        help='Print all supported voice names and exit.',
    )
    input_group.add_argument(
        '--export-voices-json',
        type=Path,
        help='Export available voices metadata as JSON and exit.',
    )

    parser.add_argument('-v', '--voice', help='Voice name, for example US_MALE_1.')
    parser.add_argument('-o', '--output', default='output.mp3', help='Output audio file path.')
    parser.add_argument('-play', '--play', help='Play sound after generating audio.', action='store_true')
    return parser


def _read_text_from_args(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text

    if args.text_file is not None:
        return args.text_file.read_text(encoding='utf-8')

    raise ValueError('Provide either --text or --text-file, or use --list-voices.')


def _print_voices() -> None:
    for voice in Voice:
        print(voice.name)


def _export_voices_json(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(voices_payload(), indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Voices JSON saved to {output_path}')


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_voices:
        _print_voices()
        return 0

    if args.export_voices_json:
        _export_voices_json(args.export_voices_json)
        return 0

    if not args.text and not args.text_file:
        parser.error('one of --text or --text-file is required unless --list-voices or --export-voices-json is used')

    if not args.voice:
        parser.error('--voice is required unless --list-voices or --export-voices-json is used')

    voice = Voice.from_string(args.voice)
    if voice is None:
        parser.error(f'invalid voice: {args.voice}. Use --list-voices to see valid names.')

    text = _read_text_from_args(args)
    tts(text, voice, args.output, args.play)
    print(f'Audio saved to {args.output}')
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
