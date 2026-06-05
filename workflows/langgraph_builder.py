from __future__ import annotations

from typing import Any, Dict

from langgraph.graph import END, StateGraph

from agents.communication_agent import CommunicationAgent
from agents.compensation_agent import CompensationAgent
from agents.decision_agent import DecisionAgent
from agents.disruption_agent import DisruptionAgent
from agents.passenger_impact_agent import PassengerImpactAgent
from agents.payment_recovery_agent import PaymentRecoveryAgent
from agents.rebooking_agent import RebookingAgent


def _run_disruption(state: Dict[str, Any]) -> Dict[str, Any]:
    state["disruption"] = DisruptionAgent().run(state).payload
    return state


def _run_impact(state: Dict[str, Any]) -> Dict[str, Any]:
    state["passenger_impact"] = PassengerImpactAgent().run(state).payload
    return state


def _run_rebooking(state: Dict[str, Any]) -> Dict[str, Any]:
    state["rebooking"] = RebookingAgent().run(state).payload
    return state


def _run_compensation(state: Dict[str, Any]) -> Dict[str, Any]:
    state["compensation"] = CompensationAgent().run(state).payload
    return state


def _run_payment_recovery(state: Dict[str, Any]) -> Dict[str, Any]:
    state["payment_recovery"] = PaymentRecoveryAgent().run(state).payload
    return state


def _run_communication(state: Dict[str, Any]) -> Dict[str, Any]:
    state["communication"] = CommunicationAgent().run(state).payload
    return state


def _run_decision(state: Dict[str, Any]) -> Dict[str, Any]:
    state["decision"] = DecisionAgent().run(state).payload
    return state


def build_graph():
    graph = StateGraph(dict)
    graph.add_node("disruption", _run_disruption)
    graph.add_node("impact", _run_impact)
    graph.add_node("rebooking", _run_rebooking)
    graph.add_node("compensation", _run_compensation)
    graph.add_node("payment_recovery", _run_payment_recovery)
    graph.add_node("communication", _run_communication)
    graph.add_node("decision", _run_decision)

    graph.set_entry_point("disruption")
    graph.add_edge("disruption", "impact")
    graph.add_edge("impact", "rebooking")
    graph.add_edge("rebooking", "compensation")
    graph.add_edge("compensation", "payment_recovery")
    graph.add_edge("payment_recovery", "communication")
    graph.add_edge("communication", "decision")
    graph.add_edge("decision", END)

    return graph.compile()
