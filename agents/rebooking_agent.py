from __future__ import annotations

from typing import Any, Dict

from .base_agent import AgentResult, BaseAgent


class RebookingAgent(BaseAgent):
    name = "rebooking"

    def run(self, state: Dict[str, Any]) -> AgentResult:
        options = state.get("itineraries", [])[:3]
        return AgentResult(self.name, {"top_options": options})
