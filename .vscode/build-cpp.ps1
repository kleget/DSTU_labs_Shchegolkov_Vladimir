[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Source,
    [Parameter(Mandatory = $true)][string]$Workspace,
    [switch]$AllInDirectory,
    [switch]$Run
)

$ErrorActionPreference = 'Stop'

try {
    $sourcePath = (Get-Item -LiteralPath $Source).FullName
    $workspacePath = (Get-Item -LiteralPath $Workspace).FullName.TrimEnd('\', '/')
    $workspacePrefix = $workspacePath + [IO.Path]::DirectorySeparatorChar
    if ([IO.Path]::GetExtension($sourcePath) -ine '.cpp') {
        throw 'Open and save a .cpp file before building.'
    }
    if (-not $sourcePath.StartsWith($workspacePrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'The active .cpp file must be inside this workspace.'
    }

    # Discover the installed toolchain; VS Code need not run from a Developer Prompt.
    $vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
    if (-not (Test-Path -LiteralPath $vswhere)) {
        throw 'Install Visual Studio / Build Tools with the Desktop development with C++ workload and Windows SDK.'
    }
    $vsInstall = & $vswhere -latest -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    if (-not $vsInstall) {
        throw 'MSVC was not found. Install the Desktop development with C++ workload and Windows SDK.'
    }
    Import-Module (Join-Path $vsInstall 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
    Enter-VsDevShell -VsInstallPath $vsInstall -SkipAutomaticLocation -DevCmdArguments '-arch=x64 -host_arch=x64 -no_logo' | Out-Null

    $sourceDirectory = Split-Path -Parent $sourcePath
    $relativeSource = $sourcePath.Substring($workspacePrefix.Length)
    $relativeDirectory = Split-Path -Parent $relativeSource
    $baseName = [IO.Path]::GetFileNameWithoutExtension($sourcePath)
    $outputDirectory = Join-Path (Join-Path (Join-Path $workspacePath 'out\cpp') $relativeDirectory) $baseName
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
    $program = Join-Path $outputDirectory ($baseName + '.exe')
    $symbols = Join-Path $outputDirectory ($baseName + '.pdb')
    $sources = @($sourcePath)
    if ($AllInDirectory) {
        $sources = @(Get-ChildItem -LiteralPath $sourceDirectory -File -Filter '*.cpp' | Sort-Object Name | Select-Object -ExpandProperty FullName)
    }

    # Array arguments preserve spaces and Unicode. All compiler/linker output stays here.
    $compilerArguments = @('/nologo', '/EHsc', '/std:c++17', '/utf-8', '/W4', '/Z7', '/Od', '/RTC1', '/MTd')
    $compilerArguments += $sources
    $compilerArguments += @(('/Fe:' + $program), ('/Fo:' + $outputDirectory + '/'))
    $compilerArguments += @('/link', '/DEBUG:FULL', '/INCREMENTAL:NO', ('/PDB:' + $symbols))
    Push-Location -LiteralPath $outputDirectory
    try {
        & cl.exe @compilerArguments
        $buildResult = $LASTEXITCODE
    } finally {
        Pop-Location
    }
    if ($buildResult -ne 0) { exit $buildResult }
    Write-Host "Built: $program"

    if ($Run) {
        Push-Location -LiteralPath $sourceDirectory
        try {
            & $program
            $runResult = $LASTEXITCODE
        } finally {
            Pop-Location
        }
        exit $runResult
    }
} catch {
    Write-Error $_
    exit 1
}
