from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AgentResult:
    name: str
    payload: Dict[str, Any]


class BaseAgent:
    name = "base"

    def run(self, state: Dict[str, Any]) -> AgentResult:
        raise NotImplementedError("Agents must implement run().")
