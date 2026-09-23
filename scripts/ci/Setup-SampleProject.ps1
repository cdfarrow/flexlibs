#Requires -Version 5.1
<#
.SYNOPSIS
  Download a sample FieldWorks backup and extract it into the projects directory.
#>
[CmdletBinding()]
param(
    [string]$ProjectsDir = "C:\ProgramData\SIL\FieldWorks\Projects",
    [string]$BackupUrl = "https://downloads.languagetechnology.org/fieldworks/9.0.4/Sena%202%202026-06-09%201659.fwbackup",
    [string]$ProjectName = "Sena 2",
    [string]$DownloadDir = "C:\fw-ci\samples"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression.FileSystem

New-Item -ItemType Directory -Force -Path $DownloadDir | Out-Null
New-Item -ItemType Directory -Force -Path $ProjectsDir | Out-Null

$projectDir = Join-Path $ProjectsDir $ProjectName
$fwdata = Join-Path $projectDir ($ProjectName + ".fwdata")
if (Test-Path $fwdata) {
    Write-Host "Sample project already present: $fwdata"
    exit 0
}

$backupPath = Join-Path $DownloadDir ($ProjectName + ".fwbackup")
if (-not (Test-Path $backupPath)) {
    Write-Host "Downloading sample project backup..."
    Write-Host "  URL: $BackupUrl"
    & curl.exe -L --retry 3 --retry-delay 5 -o $backupPath $BackupUrl
    if ($LASTEXITCODE -ne 0) {
        throw "Sample project download failed with exit code $LASTEXITCODE"
    }
}

if (Test-Path $projectDir) {
    Remove-Item -Recurse -Force $projectDir
}
New-Item -ItemType Directory -Force -Path $projectDir | Out-Null

Write-Host "Extracting $backupPath -> $projectDir"
[System.IO.Compression.ZipFile]::ExtractToDirectory($backupPath, $projectDir)

# fwbackup often has ProjectName.fwdata at the archive root
if (-not (Test-Path $fwdata)) {
    $found = Get-ChildItem -Path $projectDir -Filter "*.fwdata" -Recurse | Select-Object -First 1
    if (-not $found) {
        throw "No .fwdata found after extracting sample project"
    }
    if ($found.DirectoryName -ne $projectDir) {
        Move-Item -Force $found.FullName (Join-Path $projectDir $found.Name)
    }
    if ($found.Name -ne ($ProjectName + ".fwdata")) {
        Rename-Item -Force (Join-Path $projectDir $found.Name) ($ProjectName + ".fwdata")
    }
}

if (-not (Test-Path $fwdata)) {
    throw "Expected project file missing: $fwdata"
}

Write-Host "Sample project ready: $fwdata"
