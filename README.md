# TikTok Voice TTS

This repository is a fork of [mark-rez/TikTok-Voice-TTS](https://github.com/mark-rez/TikTok-Voice-TTS) adapted to make Windows builds and command-line usage simpler.

The main goal of this fork is to let a user build a small standalone `.exe` that can be used easily from Command Prompt, PowerShell, batch files, or other scripts without requiring a separate Python install on the target machine.

This project is only for fun. It is not associated with TikTok in any way.

## Windows Executable

### Build
Run:

`powershell -ExecutionPolicy Bypass -File .\build_exe.ps1`

The main output file is:

`dist\TikTokVoiceTTS.exe`

The build also generates or copies these helper files into `dist`:

- `voices.json`
- `README.md`
- `LICENSE.txt`
- `example-input.txt`
- `pronunciation_overrides.json`
- `manifest.json`

The executable still requires an internet connection because audio is generated through remote TikTok TTS endpoints.

The generated `manifest.json` matches the Pal Engine Integrations format, so the built `dist` folder can be registered directly as a TTS addon.

## Executable Usage

### List voices
Run `TikTokVoiceTTS.exe --list-voices`

### Export voices as JSON
Run `TikTokVoiceTTS.exe --export-voices-json .\voices.json`

### Create audio from file
1. Put your text in a UTF-8 text file.
2. Run `TikTokVoiceTTS.exe --text-file FILENAME.txt --voice VOICENAME`

### Create audio from argument
1. Run `TikTokVoiceTTS.exe --text TEXT --voice VOICENAME`

### Set output file
Run `TikTokVoiceTTS.exe --text "Hello world" --voice US_MALE_1 --output my-audio.mp3`

### Play after generating
Run `TikTokVoiceTTS.exe --text "Hello world" --voice US_MALE_1 --play`

### Pronunciation overrides
If a voice clips or mispronounces a word, you can edit `pronunciation_overrides.json`.

The executable loads the bundled defaults first, then merges any `pronunciation_overrides.json` found next to the `.exe` or in the current working directory.

This fork ships default Japanese overrides so romanized inputs such as `Arigatou Sensei` can be rewritten to kana before they are sent to TTS.

## Voices
List of every voice and its designation:

| Name                 |
| ----------------------------- |
| GHOSTFACE                     |
| CHEWBACCA                     |
| C3PO                          |
| STITCH                        |
| STORMTROOPER                  |
| ROCKET                        |
| MADAME_LEOTA                  |
| GHOST_HOST                    |
| PIRATE                        |
| AU_FEMALE_1                   |
| AU_MALE_1                     |
| UK_MALE_1                     |
| UK_MALE_2                     |
| US_FEMALE_1                   |
| US_FEMALE_2                   |
| US_MALE_1                     |
| US_MALE_2                     |
| US_MALE_3                     |
| US_MALE_4                     |
| MALE_JOMBOY                   |
| MALE_CODY                     |
| FEMALE_SAMC                   |
| FEMALE_MAKEUP                 |
| FEMALE_RICHGIRL               |
| MALE_GRINCH                   |
| MALE_DEADPOOL                 |
| MALE_JARVIS                   |
| MALE_ASHMAGIC                 |
| MALE_OLANTERKKERS             |
| MALE_UKNEIGHBOR               |
| MALE_UKBUTLER                 |
| FEMALE_SHENNA                 |
| FEMALE_PANSINO                |
| MALE_TREVOR                   |
| FEMALE_BETTY                  |
| MALE_CUPID                    |
| FEMALE_GRANDMA                |
| MALE_XMXS_CHRISTMAS           |
| MALE_SANTA_NARRATION          |
| MALE_SING_DEEP_JINGLE         |
| MALE_SANTA_EFFECT             |
| FEMALE_HT_NEYEAR              |
| MALE_WIZARD                   |
| FEMALE_HT_HALLOWEEN           |
| FR_MALE_1                     |
| FR_MALE_2                     |
| DE_FEMALE                     |
| DE_MALE                       |
| ES_MALE                       |
| ES_MX_MALE                    |
| BR_FEMALE_1                   |
| BR_FEMALE_2                   |
| BR_FEMALE_3                   |
| BR_MALE                       |
| BP_FEMALE_IVETE               |
| BP_FEMALE_LUDMILLA            |
| PT_FEMALE_LHAYS               |
| PT_FEMALE_LAIZZA              |
| PT_MALE_BUENO                 |
| ID_FEMALE                     |
| JP_FEMALE_1                   |
| JP_FEMALE_2                   |
| JP_FEMALE_3                   |
| JP_MALE                       |
| KR_MALE_1                     |
| KR_FEMALE                     |
| KR_MALE_2                     |
| JP_FEMALE_FUJICOCHAN          |
| JP_FEMALE_HASEGAWARIONA       |
| JP_MALE_KEIICHINAKANO         |
| JP_FEMALE_OOMAEAIIKA          |
| JP_MALE_YUJINCHIGUSA          |
| JP_FEMALE_SHIROU              |
| JP_MALE_TAMAWAKAZUKI          |
| JP_FEMALE_KAORISHOJI          |
| JP_FEMALE_YAGISHAKI           |
| JP_MALE_HIKAKIN               |
| JP_FEMALE_REI                 |
| JP_MALE_SHUICHIRO             |
| JP_MALE_MATSUDAKE             |
| JP_FEMALE_MACHIKORIIITA       |
| JP_MALE_MATSUO                |
| JP_MALE_OSADA                 |
| SING_FEMALE_ALTO              |
| SING_MALE_TENOR               |
| SING_FEMALE_WARMY_BREEZE      |
| SING_MALE_SUNSHINE_SOON       |
| SING_FEMALE_GLORIOUS          |
| SING_MALE_IT_GOES_UP          |
| SING_MALE_CHIPMUNK            |
| SING_FEMALE_WONDERFUL_WORLD   |
| SING_MALE_FUNNY_THANKSGIVING  |
| MALE_NARRATION                |
| MALE_FUNNY                    |
| FEMALE_EMOTIONAL              |

## License
```
MIT License

Copyright (c) 2024 Mark Reznikov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```