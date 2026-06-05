from __future__ import annotations

from typing import Any, Dict

from .base_agent import AgentResult, BaseAgent


class DecisionAgent(BaseAgent):
    name = "decision"

    def run(self, _state: Dict[str, Any]) -> AgentResult:
        return AgentResult(
            self.name,
            {
                "strategy": "rebook_plus_compensation",
                "confidence": 0.86,
            },
        )
