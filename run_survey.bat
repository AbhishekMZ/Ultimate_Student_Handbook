@echo off
echo Starting Student Survey...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.x and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "student_survey.py" (
    echo Error: student_survey.py not found
    pause
    exit /b 1
)

if not exist "students.csv" (
    echo Error: students.csv not found
    pause
    exit /b 1
)

REM Run the survey
python student_survey.py

pause
