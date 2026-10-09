# Detecting and Preventing Payment API Abuse in FinTech Systems: A Case Study of Automated Attacks on Transaction APIs

**Academic prototype for Cyber Security CA-2 | Group 16**

This project demonstrates a defensive, local prototype inspired by the report *Detecting and Preventing Payment API Abuse in FinTech Systems: A Case Study of Automated Attacks on Transaction APIs*.

> **Scope and limitations:** FinPay is fictional. The sample events and risk outputs are illustrative. This is an academic demonstration, not a production payment gateway, a real fraud detector, or a substitute for security review. No real customer or payment data is included.

## Project contents

- `src/app.py` — small REST API and hybrid risk-decision logic
- `src/detector.py` — feature extraction, rule scoring, anomaly scoring, and action mapping
- `data/sample_events.json` — example normal and suspicious requests
- `tests/test_detector.py` — basic automated tests
- `requirements.txt` — Python dependencies
- `run_windows.bat` — Windows setup and launch helper
- `run_unix.sh` — macOS/Linux setup and launch helper
- `build_exe.bat` — optional Windows executable build helper (requires PyInstaller)
- `.env.example` — example environment configuration
- `IMPLEMENTATION_NOTES.md` — implementation-to-report mapping

## Requirements

- Python 3.10 or newer
- Internet access only for the first dependency installation, unless dependencies are already cached
- Windows, macOS, or Linux

## Run on Windows

Open Command Prompt or PowerShell in this project folder.

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn src.app:app --reload
```

Open `http://127.0.0.1:8000/docs` in your browser to try the API.

You can also run `run_windows.bat`; it creates the virtual environment if needed, installs dependencies, and starts the API.

## Run on macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn src.app:app --reload
```

Or run:

```bash
chmod +x run_unix.sh
./run_unix.sh
```

## Try the API

### 1. Health check

```bash
curl http://127.0.0.1:8000/health
```

### 2. Score a normal-looking request

```bash
curl -X POST "http://127.0.0.1:8000/score" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"user-demo-01\",\"device_id\":\"device-a\",\"endpoint\":\"account_view\",\"requests_per_minute\":4,\"auth_failures\":0,\"transaction_velocity\":0,\"amount\":0,\"amount_deviation\":0.1,\"endpoint_diversity\":2,\"device_changed\":false,\"network_changed\":false,\"beneficiary_changes\":0,\"duplicate_request\":false}"
```

### 3. Score a suspicious request

```bash
curl -X POST "http://127.0.0.1:8000/score" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"user-demo-02\",\"device_id\":\"device-new\",\"endpoint\":\"payment_initiation\",\"requests_per_minute\":38,\"auth_failures\":7,\"transaction_velocity\":9,\"amount\":48000,\"amount_deviation\":0.95,\"endpoint_diversity\":8,\"device_changed\":true,\"network_changed\":true,\"beneficiary_changes\":4,\"duplicate_request\":true}"
```

The response includes the rule score, anomaly score, combined risk score, action, and reasons. Scores are demo heuristics, not calibrated probabilities.

### 4. Score the sample data

```bash
python -m src.demo
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Project and endpoint information |
| `GET` | `/health` | Basic health check |
| `POST` | `/score` | Score one request and return a decision |
| `POST` | `/score/batch` | Score a list of requests |

FastAPI's interactive API documentation is available at `/docs`.

## Run tests

With the virtual environment activated:

```bash
python -m unittest discover -s tests -v
```

## Build a Windows `.exe` (optional)

The ZIP contains the source code and a helper script; a compiled `.exe` is not included because Windows executables should be built and tested on a Windows environment.

On Windows, activate the virtual environment, then run:

```bat
pip install pyinstaller
build_exe.bat
```

The generated executable will be placed under `dist\payment-api-abuse.exe`. This bundles the command-line demo, not the FastAPI server. For the API server, use the Python/uvicorn launch steps above.

## GitHub repository

**Repository URL:** `https://github.com/<your-username>/payment-api-abuse-detection`

This is a placeholder, not a live repository link. Create a GitHub repository, push this project, and replace the placeholder with the actual URL before submitting. Example:

```bash
git init
git add .
git commit -m "Add payment API abuse detection prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/payment-api-abuse-detection.git
git push -u origin main
```

## Security and privacy notes

- Use only synthetic test events.
- Do not submit real credentials, access tokens, payment card data, or personal data.
- The prototype uses a simple in-memory demonstration and does not persist real payment transactions.
- Production deployment would require authenticated access to the scoring API, secure secrets management, robust authorization, privacy review, load testing, monitoring, and independent security testing.
