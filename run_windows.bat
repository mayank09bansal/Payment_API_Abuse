@echo off
setlocal
if not exist .venv (
  py -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Starting API at http://127.0.0.1:8000/docs
uvicorn src.app:app --reload
