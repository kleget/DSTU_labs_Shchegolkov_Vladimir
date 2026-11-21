@echo off
setlocal

if "%~1"=="" (
    echo Open a C++ source file before running this task.
    exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-cpp.ps1" -Source "%~1" -Workspace "%~2" -Run
exit /b %errorlevel%
