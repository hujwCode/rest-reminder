@echo off
cd /d "%~dp0"
echo ====================================
echo     Rest Reminder Tool - Starting...
echo ====================================
echo.

echo Checking Python...
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Found python command
    echo.
    echo Starting program...
    python rest_reminder.py
    goto :end
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    echo Found py command
    echo.
    echo Starting program...
    py rest_reminder.py
    goto :end
)

where python3 >nul 2>&1
if %errorlevel% equ 0 (
    echo Found python3 command
    echo.
    echo Starting program...
    python3 rest_reminder.py
    goto :end
)

echo.
echo ========================================
echo [ERROR] Python not found!
echo ========================================
echo.
echo Possible reasons:
echo 1. Python is not installed
echo 2. Python is not in system PATH
echo.
echo Solution:
echo - Visit https://www.python.org/downloads/
echo - Check "Add Python to PATH" when installing
echo.
echo ========================================
pause
exit /b 1

:end
if errorlevel 1 (
    echo.
    echo ========================================
    echo [ERROR] Program failed!
    echo ========================================
    echo.
    pause
)
