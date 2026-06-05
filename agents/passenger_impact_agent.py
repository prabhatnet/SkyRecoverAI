from __future__ import annotations

from typing import Any, Dict

from .base_agent import AgentResult, BaseAgent


class PassengerImpactAgent(BaseAgent):
    name = "passenger_impact"

    def run(self, state: Dict[str, Any]) -> AgentResult:
        passengers = state.get("passengers", [])
        return AgentResult(self.name, {"impacted_count": len(passengers)})
