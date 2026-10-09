"""Run the bundled synthetic examples without starting the API server."""
import json
from pathlib import Path
from src.detector import score_request

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "sample_events.json"

def main():
    events = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    for event in events:
        result = score_request(event)
        print("=" * 72)
        print(f"User: {result['user_id']} | Endpoint: {result['endpoint']}")
        print(f"Risk: {result['risk_score']} ({result['risk_band']})")
        print(f"Action: {result['recommended_action']}")
        print("Reasons:")
        for reason in result["reasons"]:
            print(f" - {reason}")
        print(result["disclaimer"])

if __name__ == "__main__":
    main()
