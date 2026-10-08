@echo off
set "PYTHON=%~dp0venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo Python virtual environment not found at "%PYTHON%".
    echo Create the environment and install requirements.txt before starting EventEase.
    exit /b 1
)

"%PYTHON%" "%~dp0manage.py" migrate
if errorlevel 1 exit /b %errorlevel%

"%PYTHON%" "%~dp0manage.py" runserver 127.0.0.1:8000
