from __future__ import annotations

from typing import Any, Dict

from .base_agent import AgentResult, BaseAgent


class DisruptionAgent(BaseAgent):
    name = "disruption"

    def run(self, state: Dict[str, Any]) -> AgentResult:
        disruption = state.get("scenario", {}).get("type", "unknown")
        return AgentResult(self.name, {"disruption_type": disruption})
