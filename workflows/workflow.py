from __future__ import annotations

from typing import Any, Dict

from agents.communication_agent import CommunicationAgent
from agents.compensation_agent import CompensationAgent
from agents.decision_agent import DecisionAgent
from agents.disruption_agent import DisruptionAgent
from agents.passenger_impact_agent import PassengerImpactAgent
from agents.payment_recovery_agent import PaymentRecoveryAgent
from agents.rebooking_agent import RebookingAgent


def run_recovery_workflow(state: Dict[str, Any]) -> Dict[str, Any]:
    state["disruption"] = DisruptionAgent().run(state).payload
    state["passenger_impact"] = PassengerImpactAgent().run(state).payload
    state["rebooking"] = RebookingAgent().run(state).payload
    state["compensation"] = CompensationAgent().run(state).payload
    state["payment_recovery"] = PaymentRecoveryAgent().run(state).payload
    state["communication"] = CommunicationAgent().run(state).payload
    state["decision"] = DecisionAgent().run(state).payload
    return state
