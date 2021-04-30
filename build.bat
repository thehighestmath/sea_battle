@echo off

set PYTHONOPTIMIZE=1
set RESOURCEPATH=res
set SCRIPTPATH=%~dp0

:: Check installed python
@py -3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3 not installed
    exit /b 1
)

@where pip3 >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip3 not installed
    exit /b 1
)

:: Check installed modules
@pip3 show pypiwin32 >nul 2>&1
if %errorlevel% neq 0 (
    echo pypiwin32 not installed
    echo write "pip3 install pypiwin32"
    exit /b 1
)

@pip3 show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo pyinstaller not installed
    echo write "pip3 install pyinstaller"
    exit /b 1
)

pyinstaller --clean --onefile --name Battleship --windowed --add-binary %SCRIPTPATH%\%RESOURCEPATH%;%RESOURCEPATH% --icon %SCRIPTPATH%\%RESOURCEPATH%\icon.ico %SCRIPTPATH%\src\main.py
