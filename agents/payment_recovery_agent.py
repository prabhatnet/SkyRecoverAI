from __future__ import annotations

from typing import Any, Dict

from .base_agent import AgentResult, BaseAgent


class PaymentRecoveryAgent(BaseAgent):
    name = "payment_recovery"

    def run(self, state: Dict[str, Any]) -> AgentResult:
        comp = state.get("compensation", {})
        total = int(comp.get("meal", 0)) + int(comp.get("hotel", 0))
        return AgentResult(self.name, {"refund_or_credit_amount": total, "mode": "travel_credit"})
