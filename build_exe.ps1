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

$manifestSourcePath = Join-Path $PSScriptRoot 'manifest.json'
$manifestData = Get-Content $manifestSourcePath -Raw | ConvertFrom-Json
$packageVersion = if ($manifestData.version) { [string]$manifestData.version } else { '0.0.0' }
$zipFileName = "TikTokVoiceTTS-$packageVersion.zip"

$exePath = Join-Path $PSScriptRoot 'dist\TikTokVoiceTTS.exe'
$voicesJsonPath = Join-Path $PSScriptRoot 'dist\voices.json'
$distReadmePath = Join-Path $PSScriptRoot 'dist\README.md'
$licensePath = Join-Path $PSScriptRoot 'dist\LICENSE.txt'
$exampleInputPath = Join-Path $PSScriptRoot 'dist\example-input.txt'
$pronunciationOverridesPath = Join-Path $PSScriptRoot 'dist\pronunciation_overrides.json'
$manifestPath = Join-Path $PSScriptRoot 'dist\manifest.json'
$zipOutputPath = Join-Path $PSScriptRoot ("dist\" + $zipFileName)

& $exePath --export-voices-json $voicesJsonPath

Copy-Item (Join-Path $PSScriptRoot 'DISTRIBUTION_README.md') $distReadmePath -Force
Copy-Item (Join-Path $PSScriptRoot 'tiktok_voice\LICENSE') $licensePath -Force
Copy-Item (Join-Path $PSScriptRoot 'example-input.txt') $exampleInputPath -Force
Copy-Item (Join-Path $PSScriptRoot 'tiktok_voice\data\pronunciation_overrides.json') $pronunciationOverridesPath -Force
Copy-Item $manifestSourcePath $manifestPath -Force

if (Test-Path $zipOutputPath) {
    Remove-Item $zipOutputPath -Force
}

$packageFiles = @(
    'TikTokVoiceTTS.exe',
    'voices.json',
    'README.md',
    'LICENSE.txt',
    'example-input.txt',
    'pronunciation_overrides.json',
    'manifest.json'
)

Push-Location (Join-Path $PSScriptRoot 'dist')
try {
    Compress-Archive -Path $packageFiles -DestinationPath $zipOutputPath -CompressionLevel Optimal
} finally {
    Pop-Location
}

Write-Host ''
Write-Host 'Build complete.'
Write-Host 'Executable:' $exePath
Write-Host 'Voices JSON:' $voicesJsonPath
Write-Host 'README:' $distReadmePath
Write-Host 'License:' $licensePath
Write-Host 'Example input:' $exampleInputPath
Write-Host 'Pronunciation overrides:' $pronunciationOverridesPath
Write-Host 'Manifest:' $manifestPath
Write-Host 'Plugin zip:' $zipOutputPath