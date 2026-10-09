# Implementation notes and report mapping

This source project is a small runnable demonstration of concepts in the report. It does not reproduce a production FinTech system.

| Report concept | Prototype location |
|---|---|
| Synthetic API event data | `data/sample_events.json` |
| Request/behavior feature inputs | `src/app.py` — `PaymentEvent` model |
| Deterministic rules | `src/detector.py` — rule checks for velocity, auth failures, duplicate requests, beneficiary changes |
| Behavioral/anomaly-style score | `src/detector.py` — transparent weighted deviation score |
| Hybrid risk score | `src/detector.py` — weighted rule and behavior combination |
| Risk bands and actions | `src/detector.py` — allow, monitor, step-up, hold/block, block-and-alert |
| API request lifecycle | `src/app.py` — `/score` and `/score/batch` |
| Evaluation limitations | README — synthetic illustrative data and non-production disclaimer |

## Important distinction

The report discusses a possible prototype stack and describes Isolation Forest as a suitable anomaly detection option. This implementation uses transparent heuristic scoring and **does not train or run an Isolation Forest model**. It is provided as an executable starting-point demo, not as proof of the report's illustrative evaluation values. The scoring weights and thresholds are hand-set and require validation on representative, authorized data before any real deployment.
