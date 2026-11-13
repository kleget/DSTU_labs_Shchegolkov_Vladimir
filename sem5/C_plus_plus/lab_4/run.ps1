$ErrorActionPreference = 'Stop'
$env:Path = "C:\msys64\ucrt64\bin;" + $env:Path

Push-Location $PSScriptRoot
try {
    & g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o lab4.exe
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & .\lab4.exe
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
