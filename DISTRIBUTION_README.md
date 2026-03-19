# TikTok Voice TTS Executable

This distribution is ready to use. You do not need to install Python.

## Recommended Pal Engine Import

Pal Engine should import the generated zip package, not the unpacked folder.

Primary artifact:

- `TikTokVoiceTTS-<version>.zip`
  Ready-to-import integration package that matches the Pal Engine integration zip layout.

Pal Engine can still inspect the unpacked folder, but the zip is the intended distribution format.

## Included Files

- `TikTokVoiceTTS-<version>.zip`
  Ready-to-import Pal Engine integration package.
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
  Pal Engine integration manifest included in both the folder and the zip package.

## Import Into Pal Engine

1. Open `Settings -> Integrations`
2. Choose `Add Plugin`
3. Select the generated `TikTokVoiceTTS-<version>.zip`
4. Let Pal Engine inspect it
5. Save the integration

Pal Engine will extract the zip into its managed external resources folder and register it from there.

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