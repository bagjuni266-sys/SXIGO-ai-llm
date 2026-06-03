@echo off
REM DEL.bat - start the DLT SXIGO Ollama proxy server on Windows
SETLOCAL
echo Starting DLT SXIGO server...
if exist "%~dp0\.venv\Scripts\activate.bat" (
  call "%~dp0\.venv\Scripts\activate.bat"
) else (
  echo Warning: virtualenv activate not found. Ensure Python environment and dependencies installed.
)
python -m pip install -r "%~dp0requirements_server.txt"
python -m uvicorn SEVERDEL:APP --host 0.0.0.0 --port 11435 --reload
ENDLOCAL
