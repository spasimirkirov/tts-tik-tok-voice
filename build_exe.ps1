param(
    [switch]$Clean
)

$ErrorActionPreference = 'Stop'

if ($Clean) {
    Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
}

py -m pip install -r requirements.txt
py -m pip install pyinstaller
py -m PyInstaller --clean TikTokVoiceTTS.spec

$exePath = Join-Path $PSScriptRoot 'dist\TikTokVoiceTTS.exe'
$voicesJsonPath = Join-Path $PSScriptRoot 'dist\voices.json'
$distReadmePath = Join-Path $PSScriptRoot 'dist\README.md'
$licensePath = Join-Path $PSScriptRoot 'dist\LICENSE.txt'
$exampleInputPath = Join-Path $PSScriptRoot 'dist\example-input.txt'
$pronunciationOverridesPath = Join-Path $PSScriptRoot 'dist\pronunciation_overrides.json'
$manifestPath = Join-Path $PSScriptRoot 'dist\manifest.json'

& $exePath --export-voices-json $voicesJsonPath

Copy-Item (Join-Path $PSScriptRoot 'DISTRIBUTION_README.md') $distReadmePath -Force
Copy-Item (Join-Path $PSScriptRoot 'tiktok_voice\LICENSE') $licensePath -Force
Copy-Item (Join-Path $PSScriptRoot 'example-input.txt') $exampleInputPath -Force
Copy-Item (Join-Path $PSScriptRoot 'tiktok_voice\data\pronunciation_overrides.json') $pronunciationOverridesPath -Force
Copy-Item (Join-Path $PSScriptRoot 'manifest.json') $manifestPath -Force

Write-Host ''
Write-Host 'Build complete.'
Write-Host 'Executable:' $exePath
Write-Host 'Voices JSON:' $voicesJsonPath
Write-Host 'README:' $distReadmePath
Write-Host 'License:' $licensePath
Write-Host 'Example input:' $exampleInputPath
Write-Host 'Pronunciation overrides:' $pronunciationOverridesPath
Write-Host 'Manifest:' $manifestPath