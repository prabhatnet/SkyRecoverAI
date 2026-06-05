from __future__ import annotations

from typing import Any, Dict

from .base_agent import AgentResult, BaseAgent


class CompensationAgent(BaseAgent):
    name = "compensation"

    def run(self, state: Dict[str, Any]) -> AgentResult:
        disruption_type = state.get("disruption", {}).get("disruption_type", "unknown")
        package = {"meal": 25, "hotel": 0}
        if disruption_type in {"cancellation", "weather", "crew"}:
            package["hotel"] = 150
        return AgentResult(self.name, package)
