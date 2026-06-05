from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class RecoveryState(TypedDict, total=False):
    case_id: str
    scenario: Dict[str, Any]
    flights: List[Dict[str, Any]]
    passengers: List[Dict[str, Any]]
    itineraries: List[Dict[str, Any]]
    disruption: Dict[str, Any]
    passenger_impact: Dict[str, Any]
    rebooking: Dict[str, Any]
    compensation: Dict[str, Any]
    payment_recovery: Dict[str, Any]
    communication: Dict[str, Any]
    decision: Dict[str, Any]
