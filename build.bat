@echo off

set PYTHONOPTIMIZE=1
set RESOURCEPATH=res
set SCRIPTPATH=%~dp0

:: Check installed python
echo | set /p=check installed python3...
@py -3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo FAIL
    echo Python 3 not installed either not in PATH variable
    pause
    exit /b 1
)
echo OK

echo | set /p=check installed pip3...
@where pip3 >nul 2>&1
if %errorlevel% neq 0 (
    echo FAIL
    echo Pip3 not installed either not in PATH variable
    pause
    exit /b 1
)
echo OK

:: Check installed modules
echo | set /p=check installed pypiwin32...
@pip3 show pypiwin32 >nul 2>&1
if %errorlevel% neq 0 (
    echo FAIL
    echo pypiwin32 not installed
    echo write "pip3 install pypiwin32"
    pause
    exit /b 1
)
echo OK

echo | set /p=check installed pyinstaller...
@pip3 show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo FAIL
    echo pyinstaller not installed
    echo write "pip3 install pyinstaller"
    pause
    exit /b 1
)
echo OK

echo run pyinstaller building:
py -3 -m PyInstaller --clean --onefile --name Battleship --windowed --add-binary %SCRIPTPATH%\%RESOURCEPATH%;%RESOURCEPATH% --icon %SCRIPTPATH%\%RESOURCEPATH%\icon.ico %SCRIPTPATH%\src\main.py

pause