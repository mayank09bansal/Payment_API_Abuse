"""FastAPI endpoints for the fictional FinPay demo."""
from typing import Any, Dict, List
from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.detector import score_request

app = FastAPI(
    title="FinPay Payment API Abuse Detection Prototype",
    description=(
        "Academic demo of rule-based and behavioral risk scoring for synthetic events. "
        "Not for production payment processing."
    ),
    version="1.0.0",
)


class PaymentEvent(BaseModel):
    user_id: str = "demo-user"
    device_id: str = "demo-device"
    endpoint: str = "account_view"
    requests_per_minute: int = Field(default=1, ge=0, le=100000)
    auth_failures: int = Field(default=0, ge=0, le=100000)
    transaction_velocity: int = Field(default=0, ge=0, le=100000)
    amount: float = Field(default=0.0, ge=0)
    amount_deviation: float = Field(default=0.0, ge=0, le=1)
    endpoint_diversity: int = Field(default=1, ge=0, le=100000)
    device_changed: bool = False
    network_changed: bool = False
    beneficiary_changes: int = Field(default=0, ge=0, le=100000)
    duplicate_request: bool = False


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "project": "FinPay Payment API Abuse Detection Prototype",
        "docs": "/docs",
        "health": "/health",
        "score_endpoint": "POST /score",
    }


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "mode": "synthetic-demo"}


@app.post("/score")
def score(event: PaymentEvent) -> Dict[str, Any]:
    """Score one synthetic request and recommend a defensive action."""
    return score_request(event.model_dump())


@app.post("/score/batch")
def score_batch(events: List[PaymentEvent]) -> Dict[str, Any]:
    """Score multiple synthetic events."""
    results = [score_request(event.model_dump()) for event in events]
    return {"count": len(results), "results": results}
