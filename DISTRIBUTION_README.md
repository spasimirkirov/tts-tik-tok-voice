# TikTok Voice TTS Executable

This folder is ready to use. You do not need to install Python.

## Included Files

- `TikTokVoiceTTS.exe`
  The executable used to generate MP3 audio.
- `voices.json`
  Machine-readable list of all available voices.
- `example-input.txt`
  Example text file you can use with `--text-file`.
- `LICENSE.txt`
  License for the bundled TikTok Voice TTS project.
- `pronunciation_overrides.json`
  Editable pronunciation replacements loaded by the executable.
- `manifest.json`
  Pal Engine integration manifest for registering this folder as a TTS addon.

## Requirements

- Windows
- Internet connection

The executable still needs internet access because audio is generated through remote TikTok TTS endpoints.

## Basic Commands

### List available voices

```powershell
.\TikTokVoiceTTS.exe --list-voices
```

### Export voices as JSON again

```powershell
.\TikTokVoiceTTS.exe --export-voices-json .\voices.json
```

### Generate audio from text

```powershell
.\TikTokVoiceTTS.exe --text "Hello from TikTok TTS" --voice US_MALE_1
```

### Generate audio from a text file

```powershell
.\TikTokVoiceTTS.exe --text-file .\example-input.txt --voice US_MALE_1
```

### Set a custom output file

```powershell
.\TikTokVoiceTTS.exe --text "Hello from TikTok TTS" --voice US_MALE_1 --output .\my-audio.mp3
```

### Play the generated file immediately

```powershell
.\TikTokVoiceTTS.exe --text "Hello from TikTok TTS" --voice US_MALE_1 --play
```

## Common Notes

- Voice names must match exactly, for example `US_MALE_1`.
- Use `voices.json` if you want to build your own UI or picker around the available voices.
- When using `--text-file`, save the file as UTF-8 text.
- The generated file format is MP3.
- You can edit `pronunciation_overrides.json` to fix words a voice clips or says badly.

## Troubleshooting

- If generation fails for all voices, first confirm your internet connection is working.
- If a voice name fails validation, run `--list-voices` and copy the exact voice name.
- If audio playback does not start with `--play`, the MP3 may still have been generated successfully. Check the output file.
- For Japanese voices, the default overrides already improve romanized phrases like `Arigatou Sensei` by rewriting them to kana before generation.