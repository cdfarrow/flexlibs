#Requires -Version 5.1
<#
.SYNOPSIS
  Download and silently install FieldWorks for CI, or restore registry after a cache hit.
#>
[CmdletBinding()]
param(
    [string]$Version = "9.3.9.1",
    [string]$Build = "1439",
    [string]$InstallerUrl = "",
    [string]$CodeDir = "C:\Program Files\FieldWorks9",
    [string]$ProjectsDir = "C:\ProgramData\SIL\FieldWorks\Projects",
    [string]$DownloadDir = "C:\fw-ci\installer",
    [string]$InstallLog = "C:\fw-ci\fw-install.log",
    [string]$CodeDirOutFile = "C:\fw-ci\fw-code-dir.txt"
)

$ErrorActionPreference = "Stop"

function Ensure-Registry {
    param([string]$CodeDir, [string]$ProjectsDir)

    $regPath = "HKLM:\SOFTWARE\SIL\FieldWorks\9"
    if (-not (Test-Path $regPath)) {
        New-Item -Path $regPath -Force | Out-Null
    }
    New-ItemProperty -Path $regPath -Name "RootCodeDir" -Value $CodeDir -PropertyType String -Force | Out-Null
    New-ItemProperty -Path $regPath -Name "ProjectsDir" -Value $ProjectsDir -PropertyType String -Force | Out-Null
    New-ItemProperty -Path $regPath -Name "Data_Directory" -Value (Split-Path $ProjectsDir -Parent) -PropertyType String -Force | Out-Null
    Write-Host "Registry ready: RootCodeDir=$CodeDir ProjectsDir=$ProjectsDir"
}

function Test-FieldWorksInstalled {
    param([string]$CodeDir)
    if (-not $CodeDir) { return $false }
    return (Test-Path (Join-Path $CodeDir "FieldWorks.exe")) -and (Test-Path (Join-Path $CodeDir "FwUtils.dll"))
}

function Find-FieldWorksCodeDir {
    param([string]$Preferred)

    if (Test-FieldWorksInstalled -CodeDir $Preferred) {
        return $Preferred
    }

    foreach ($hive in @("HKLM:\SOFTWARE\SIL\FieldWorks\9", "HKLM:\SOFTWARE\WOW6432Node\SIL\FieldWorks\9")) {
        if (Test-Path $hive) {
            $fromReg = (Get-ItemProperty -Path $hive -ErrorAction SilentlyContinue).RootCodeDir
            if (Test-FieldWorksInstalled -CodeDir $fromReg) {
                Write-Host "Found FieldWorks via registry $hive => $fromReg"
                return $fromReg
            }
        }
    }

    $searchRoots = @(
        "C:\Program Files\FieldWorks9",
        "C:\Program Files\SIL",
        "C:\Program Files (x86)\SIL",
        "C:\Program Files",
        "C:\Program Files (x86)"
    )
    foreach ($root in $searchRoots) {
        if (-not (Test-Path $root)) { continue }
        $exe = Get-ChildItem -Path $root -Filter "FieldWorks.exe" -Recurse -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($exe) {
            Write-Host "Found FieldWorks.exe at $($exe.FullName)"
            return $exe.DirectoryName
        }
    }
    return $null
}

function Write-Diagnostics {
    Write-Host "---- Diagnostics ----"
    foreach ($p in @(
        "C:\Program Files\FieldWorks9",
        "C:\Program Files\SIL",
        "C:\Program Files (x86)\SIL",
        "C:\ProgramData\SIL"
    )) {
        if (Test-Path $p) {
            Write-Host "Listing $p"
            Get-ChildItem $p -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  $($_.FullName)" }
        } else {
            Write-Host "Missing: $p"
        }
    }
    foreach ($hive in @("HKLM:\SOFTWARE\SIL", "HKLM:\SOFTWARE\WOW6432Node\SIL")) {
        if (Test-Path $hive) {
            Write-Host "Registry under $hive :"
            Get-ChildItem $hive -Recurse -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  $($_.Name)" }
        }
    }
    Get-ChildItem "C:\fw-ci\fw-install*.log" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "---- $($_.Name) (last 40 lines) ----"
        Get-Content $_.FullName -Tail 40
    }
}

function Write-CodeDirOut {
    param([string]$Resolved)

    Set-Content -Path $CodeDirOutFile -Value $Resolved -Encoding UTF8
    if ($env:GITHUB_ENV) {
        Add-Content -Path $env:GITHUB_ENV -Value "FW_CODE_DIR=$Resolved"
    }
}

if (-not $InstallerUrl) {
    $InstallerUrl = "https://downloads.languagetechnology.org/fieldworks/9.3.9/$Build/FieldWorks_${Version}_Offline_x64.exe"
}

New-Item -ItemType Directory -Force -Path $DownloadDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $InstallLog) | Out-Null
New-Item -ItemType Directory -Force -Path $ProjectsDir | Out-Null

$existing = Find-FieldWorksCodeDir -Preferred $CodeDir
if ($existing) {
    Write-Host "FieldWorks already present at $existing (cache hit or prior install)"
    Ensure-Registry -CodeDir $existing -ProjectsDir $ProjectsDir
    Write-CodeDirOut -Resolved $existing
    exit 0
}

$installerName = Split-Path $InstallerUrl -Leaf
$installerPath = Join-Path $DownloadDir $installerName

if (-not (Test-Path $installerPath)) {
    Write-Host "Downloading FieldWorks installer..."
    Write-Host "  URL: $InstallerUrl"
    Write-Host "  To:  $installerPath"
    & curl.exe -L --retry 3 --retry-delay 5 -o $installerPath $InstallerUrl
    if ($LASTEXITCODE -ne 0) {
        throw "Download failed with exit code $LASTEXITCODE"
    }
} else {
    Write-Host "Using cached installer: $installerPath"
}

$sizeMB = [math]::Round((Get-Item $installerPath).Length / 1MB, 1)
Write-Host "Installer size: ${sizeMB} MB"
Write-Host "Silent installing FieldWorks (/quiet /norestart ADDLOCAL=ALL)..."
Write-Host "Log: $InstallLog"

$proc = Start-Process -FilePath $installerPath `
    -ArgumentList @("/quiet", "/norestart", "/log", $InstallLog, "ADDLOCAL=ALL") `
    -Wait -PassThru -NoNewWindow

Write-Host "Installer exit code: $($proc.ExitCode)"
if ($proc.ExitCode -notin @(0, 3010, 1641)) {
    Write-Diagnostics
    throw "FieldWorks installer failed with exit code $($proc.ExitCode)"
}

$resolved = Find-FieldWorksCodeDir -Preferred $CodeDir
if (-not $resolved) {
    Write-Diagnostics
    throw "FieldWorks.exe not found after install (checked Program Files and registry)"
}

Write-Host "Resolved FieldWorks code dir: $resolved"
Ensure-Registry -CodeDir $resolved -ProjectsDir $ProjectsDir
Write-CodeDirOut -Resolved $resolved
Write-Host "FieldWorks install complete."
