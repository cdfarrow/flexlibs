#Requires -Version 5.1
<#
.SYNOPSIS
  Restore latest SIL NuGet packages into a flat folder for flexlibs overlay tests.

.DESCRIPTION
  Publishes tests/nuget-overlay to .fw-nuget-overlay at the repo root and writes
  versions.txt listing resolved package versions.
#>
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$Project = Join-Path $PSScriptRoot "Overlay.csproj"
$OutDir = Join-Path $RepoRoot ".fw-nuget-overlay"

Write-Host "Publishing NuGet overlay to $OutDir"

if (Test-Path $OutDir) {
    Remove-Item -Recurse -Force $OutDir
}

dotnet publish $Project -c Release -o $OutDir --nologo
if ($LASTEXITCODE -ne 0) {
    throw "dotnet publish failed with exit code $LASTEXITCODE"
}

$DllCount = @(Get-ChildItem -Path $OutDir -Filter "*.dll" -File).Count
if ($DllCount -eq 0) {
    throw "No DLLs published to $OutDir"
}

# Record resolved package versions from the assets file for debugging.
$Assets = Join-Path $PSScriptRoot "obj\project.assets.json"
$VersionsPath = Join-Path $OutDir "versions.txt"
$Lines = New-Object System.Collections.Generic.List[string]
$Lines.Add("Published: $(Get-Date -Format o)")
$Lines.Add("DLL count: $DllCount")
$Lines.Add("")

if (Test-Path $Assets) {
    $Lines.Add("Resolved packages (from project.assets.json):")
    $json = Get-Content -Raw $Assets | ConvertFrom-Json
    $libs = $json.libraries.PSObject.Properties
    foreach ($lib in ($libs | Sort-Object Name)) {
        if ($lib.Name -match '^(SIL\.(LCModel|Core|WritingSystems))') {
            $Lines.Add("  $($lib.Name)")
        }
    }
} else {
    $Lines.Add("(project.assets.json not found; versions unknown)")
}

$Lines | Set-Content -Path $VersionsPath -Encoding UTF8
Write-Host "Wrote $VersionsPath ($DllCount DLLs)"
Write-Host "Set FLEXLIBS_ASSEMBLY_DIR=$OutDir to use this overlay."
