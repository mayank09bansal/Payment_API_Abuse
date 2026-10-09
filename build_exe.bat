@echo off
setlocal
if not exist .venv (
  echo First create and activate .venv, then install requirements.txt.
  exit /b 1
)
call .venv\Scripts\activate.bat
pip install pyinstaller
pyinstaller --onefile --name payment-api-abuse src\demo.py
echo Build complete. See dist\payment-api-abuse.exe
