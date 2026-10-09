"""Rule-plus-behavior scoring for the fictional FinPay academic prototype."""

from typing import Any, Dict, List


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def score_request(event: Dict[str, Any]) -> Dict[str, Any]:
    """Return a transparent demo risk score and recommended action.

    The scoring thresholds are illustrative heuristics, not trained model outputs.
    """
    reasons: List[str] = []
    rule_points = 0.0
    behavior_points = 0.0

    rpm = max(0, int(event.get("requests_per_minute", 0)))
    auth_failures = max(0, int(event.get("auth_failures", 0)))
    txn_velocity = max(0, int(event.get("transaction_velocity", 0)))
    amount_deviation = _clamp(float(event.get("amount_deviation", 0.0)))
    endpoint_diversity = max(0, int(event.get("endpoint_diversity", 0)))
    beneficiary_changes = max(0, int(event.get("beneficiary_changes", 0)))
    device_changed = bool(event.get("device_changed", False))
    network_changed = bool(event.get("network_changed", False))
    duplicate_request = bool(event.get("duplicate_request", False))
    endpoint = str(event.get("endpoint", "unknown")).lower()

    # Deterministic rules: each adds a bounded amount to the score.
    if rpm >= 30:
        rule_points += 0.25
        reasons.append("High request velocity")
    elif rpm >= 15:
        rule_points += 0.12
        reasons.append("Elevated request velocity")

    if auth_failures >= 5:
        rule_points += 0.22
        reasons.append("Repeated authentication failures")
    elif auth_failures >= 3:
        rule_points += 0.10
        reasons.append("Several authentication failures")

    if txn_velocity >= 6:
        rule_points += 0.22
        reasons.append("High transaction velocity")
    elif txn_velocity >= 3:
        rule_points += 0.10
        reasons.append("Elevated transaction velocity")

    if duplicate_request:
        rule_points += 0.18
        reasons.append("Duplicate/replay-like request indicator")

    if endpoint == "payment_initiation" and beneficiary_changes >= 2:
        rule_points += 0.16
        reasons.append("Repeated beneficiary changes before payment")

    # Behavioral deviation score is intentionally transparent and explainable.
    behavior_points += min(rpm / 50.0, 0.25)
    behavior_points += min(auth_failures / 15.0, 0.20)
    behavior_points += min(txn_velocity / 12.0, 0.20)
    behavior_points += amount_deviation * 0.15
    behavior_points += min(endpoint_diversity / 12.0, 0.08)

    if device_changed:
        behavior_points += 0.06
        reasons.append("Device context changed")
    if network_changed:
        behavior_points += 0.04
        reasons.append("Network context changed")
    if beneficiary_changes:
        behavior_points += min(beneficiary_changes / 10.0, 0.10)
    if amount_deviation >= 0.75:
        reasons.append("Transaction amount deviates substantially from baseline")

    rule_score = _clamp(rule_points)
    anomaly_score = _clamp(behavior_points)
    # Hybrid combination, similar in concept to the report's weighted risk model.
    risk_score = round(_clamp(0.55 * rule_score + 0.45 * anomaly_score), 3)

    if risk_score >= 0.72 or (duplicate_request and txn_velocity >= 6):
        action = "block_and_alert"
        band = "critical"
    elif risk_score >= 0.55:
        action = "hold_or_block"
        band = "high"
    elif risk_score >= 0.38:
        action = "step_up_authentication"
        band = "elevated"
    elif risk_score >= 0.20:
        action = "allow_and_monitor"
        band = "moderate"
    else:
        action = "allow"
        band = "low"

    if not reasons:
        reasons.append("No configured high-risk indicators detected")

    return {
        "user_id": str(event.get("user_id", "anonymous")),
        "endpoint": endpoint,
        "rule_score": round(rule_score, 3),
        "anomaly_score": round(anomaly_score, 3),
        "risk_score": risk_score,
        "risk_band": band,
        "recommended_action": action,
        "reasons": reasons,
        "disclaimer": "Illustrative academic heuristic; not a production fraud decision.",
    }
