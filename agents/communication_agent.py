from __future__ import annotations

from typing import Any, Dict

from .base_agent import AgentResult, BaseAgent


class CommunicationAgent(BaseAgent):
    name = "communication"

    def run(self, state: Dict[str, Any]) -> AgentResult:
        disruption = state.get("disruption", {}).get("disruption_type", "disruption")
        message = f"We are sorry for the {disruption}. We have prepared recovery options for you."
        return AgentResult(self.name, {"message": message})
