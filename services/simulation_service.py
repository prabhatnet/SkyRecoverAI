"""Simulation service that generates rich, self-contained scenario state
for every recovery scenario. No external DB or API required."""
from __future__ import annotations

import random
import uuid
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Scenario catalogue
# ---------------------------------------------------------------------------

SCENARIOS: Dict[str, Dict[str, Any]] = {
    "atl_thunderstorm": {
        "name": "ATL Thunderstorm",
        "type": "weather",
        "icon": "⛈️",
        "description": (
            "Severe thunderstorm cell over Atlanta Hartsfield-Jackson. "
            "FAA issued a ground stop. 18 departures affected."
        ),
        "severity": "Critical",
        "root_cause": "Weather",
        "affected_airport": "ATL",
        "flight_count": 18,
        "passenger_count": 284,
        "delay_minutes": 195,
        "is_cancellation": False,
        "compensation_hint": "MealAndHotel",
    },
    "flight_cancellation": {
        "name": "Flight Cancellation SR110",
        "type": "cancellation",
        "icon": "🚫",
        "description": (
            "SR110 JFK→LHR cancelled due to unscheduled airframe maintenance. "
            "No spare aircraft available at JFK."
        ),
        "severity": "Critical",
        "root_cause": "Technical",
        "affected_airport": "JFK",
        "flight_count": 1,
        "passenger_count": 147,
        "delay_minutes": 0,
        "is_cancellation": True,
        "compensation_hint": "FullRefund",
    },
    "crew_disruption": {
        "name": "Crew Disruption SR245",
        "type": "crew",
        "icon": "👨‍✈️",
        "description": (
            "SR245 LHR→CDG delayed. Inbound crew exceeded FTL duty-time limits. "
            "Reserve crew sourcing in progress."
        ),
        "severity": "Medium",
        "root_cause": "CrewLegalLimit",
        "affected_airport": "LHR",
        "flight_count": 1,
        "passenger_count": 96,
        "delay_minutes": 95,
        "is_cancellation": False,
        "compensation_hint": "MealOnly",
    },
}

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

_LOYALTY_TIERS = ["None", "Silver", "Gold", "Platinum"]
_TIER_WEIGHTS  = [0.58,   0.24,    0.13,   0.05]
_CLASSES       = ["Economy", "Premium Economy", "Business", "First"]
_CLASS_WEIGHTS = [0.62,      0.18,             0.16,       0.04]
_SSR_POOL      = ["WCHR", "UMNR", "VGML", "BLND", "DEAF"]

_FIRST_NAMES = [
    "Emma", "Noah", "Yuki", "Carlos", "Sophie", "James", "Amara", "Lucas",
    "Priya", "Alex", "Fatima", "Oliver", "Zoe", "Ravi", "Maria", "Chen",
    "Isla", "Mateo", "Aisha", "Tom", "Giulia", "Hiroshi", "Chloe", "Omar",
    "Hannah", "Ethan", "Nina", "Samuel", "Layla", "Felix",
]
_LAST_NAMES = [
    "Rodriguez", "Kim", "Tanaka", "Nguyen", "Patel", "Smith", "Okafor",
    "Muller", "Singh", "Garcia", "Hassan", "Chen", "Williams", "Nakamura",
    "Fernandez", "Brooks", "Sato", "Ahmed", "DaSilva", "Weber",
]
_AVG_TICKET = {"Economy": 480, "Premium Economy": 890, "Business": 2200, "First": 4800}

# ---------------------------------------------------------------------------
# Internal builders
# ---------------------------------------------------------------------------

def _impact_score(tier: str, klass: str, connected: bool, has_ssr: bool) -> int:
    s = {"None": 0, "Silver": 15, "Gold": 30, "Platinum": 50}[tier]
    s += {"Economy": 0, "Premium Economy": 10, "Business": 25, "First": 40}[klass]
    if connected:
        s += 20
    if has_ssr:
        s += 15
    return min(s, 100)


def _build_passengers(count: int, seed: int) -> List[Dict[str, Any]]:
    rng = random.Random(seed)
    rows: List[Dict[str, Any]] = []
    for i in range(count):
        tier     = rng.choices(_LOYALTY_TIERS, weights=_TIER_WEIGHTS)[0]
        klass    = rng.choices(_CLASSES, weights=_CLASS_WEIGHTS)[0]
        first    = rng.choice(_FIRST_NAMES)
        last     = rng.choice(_LAST_NAMES)
        has_conn = rng.random() < 0.35
        has_ssr  = rng.random() < 0.12
        ssr      = rng.choice(_SSR_POOL) if has_ssr else None
        score    = _impact_score(tier, klass, has_conn, has_ssr)
        rows.append({
            "passenger_id":   f"PAX-{200001 + i:06d}",
            "full_name":      f"{first} {last}",
            "loyalty_tier":   tier,
            "ticket_class":   klass,
            "has_connection": has_conn,
            "ssr":            ssr,
            "impact_score":   score,
            "priority":       "Critical" if score >= 80 else ("High" if score >= 50 else "Standard"),
            "ticket_value":   _AVG_TICKET[klass],
        })
    return rows


def _build_rebooking(scenario_type: str) -> List[Dict[str, Any]]:
    if scenario_type == "cancellation":
        return [
            {"option_id": "OPT-1", "flight": "SR112  JFK→LHR  +24 h",       "delta_hrs": 24, "seats": 14, "score": 0.91, "cabin": "Business"},
            {"option_id": "OPT-2", "flight": "SR114  JFK→LHR  +48 h",       "delta_hrs": 48, "seats": 28, "score": 0.77, "cabin": "Economy"},
            {"option_id": "OPT-3", "flight": "SR120  JFK→DXB→LHR  +30 h",   "delta_hrs": 30, "seats": 8,  "score": 0.62, "cabin": "Economy"},
        ]
    if scenario_type == "weather":
        return [
            {"option_id": "OPT-1", "flight": "SR410  ATL→ORD  +4 h",     "delta_hrs": 4, "seats": 42, "score": 0.88, "cabin": "Economy"},
            {"option_id": "OPT-2", "flight": "SR412  ATL→ORD  +6 h",     "delta_hrs": 6, "seats": 61, "score": 0.82, "cabin": "Economy"},
            {"option_id": "OPT-3", "flight": "SR420  ATL→DFW→ORD  +5 h", "delta_hrs": 5, "seats": 19, "score": 0.71, "cabin": "Economy"},
        ]
    return [
        {"option_id": "OPT-1", "flight": "SR247  LHR→CDG  +2 h", "delta_hrs": 2, "seats": 55, "score": 0.95, "cabin": "Economy"},
        {"option_id": "OPT-2", "flight": "SR249  LHR→CDG  +4 h", "delta_hrs": 4, "seats": 78, "score": 0.87, "cabin": "Economy"},
    ]


def _build_compensation(hint: str, passengers: List[Dict[str, Any]]) -> Dict[str, Any]:
    meal_pp  = 25  if hint in ("MealOnly", "MealAndHotel", "FullRefund") else 0
    hotel_pp = 150 if hint in ("MealAndHotel", "FullRefund")             else 0
    refund_r = 0.60 if hint == "FullRefund" else 0.0
    credit_r = 0.40 if hint == "FullRefund" else (0.15 if hint == "MealAndHotel" else 0.0)
    n            = len(passengers)
    ticket_total = sum(p["ticket_value"] for p in passengers)
    return {
        "meal_total":   meal_pp * n,
        "hotel_total":  hotel_pp * n,
        "refund_total": round(ticket_total * refund_r),
        "credit_total": round(ticket_total * credit_r),
        "total":        round(meal_pp * n + hotel_pp * n + ticket_total * (refund_r + credit_r)),
        "meal_per_pax":  meal_pp,
        "hotel_per_pax": hotel_pp,
        "hint":          hint,
        "tier_counts": {t: sum(1 for p in passengers if p["loyalty_tier"] == t) for t in _LOYALTY_TIERS},
    }


def _build_audit_trail() -> List[Dict[str, Any]]:
    return [
        {"step": 1, "agent": "DisruptionAgent",      "event": "disruption.assessed",         "confidence": 0.95, "latency_s": 0.4, "status": "✅ Success"},
        {"step": 2, "agent": "PassengerImpactAgent",  "event": "passenger.impact.assessed",   "confidence": 0.92, "latency_s": 1.1, "status": "✅ Success"},
        {"step": 3, "agent": "RebookingAgent",         "event": "rebooking.options.generated", "confidence": 0.88, "latency_s": 2.3, "status": "✅ Success"},
        {"step": 4, "agent": "CompensationAgent",      "event": "compensation.calculated",     "confidence": 0.97, "latency_s": 0.8, "status": "✅ Success"},
        {"step": 5, "agent": "PaymentRecoveryAgent",   "event": "payment.recovery.simulated",  "confidence": 0.91, "latency_s": 0.6, "status": "✅ Success"},
        {"step": 6, "agent": "CommunicationAgent",     "event": "communication.generated",     "confidence": 0.94, "latency_s": 1.7, "status": "✅ Success"},
        {"step": 7, "agent": "DecisionAgent",          "event": "decision.finalized",          "confidence": 0.89, "latency_s": 0.9, "status": "✅ Success"},
    ]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_STRATEGY   = {"weather": "REBOOK + MEAL + HOTEL", "cancellation": "FULL REFUND or REBOOK", "crew": "REBOOK + MEAL"}
_CONFIDENCE = {"weather": 0.87, "cancellation": 0.91, "crew": 0.94}


def run_scenario(key: str) -> Dict[str, Any]:
    """Return a fully-populated simulation result dict for the given scenario key."""
    sc       = SCENARIOS[key]
    pax      = _build_passengers(sc["passenger_count"], seed=abs(hash(key)) % 9999)
    comp     = _build_compensation(sc["compensation_hint"], pax)
    strategy = _STRATEGY.get(sc["type"], "REBOOK + COMPENSATION")

    return {
        "case_id":          f"CASE-{uuid.uuid4().hex[:8].upper()}",
        "scenario_key":     key,
        "scenario_name":    sc["name"],
        "scenario_type":    sc["type"],
        "scenario_icon":    sc["icon"],
        "description":      sc["description"],
        "severity":         sc["severity"],
        "root_cause":       sc["root_cause"],
        "affected_airport": sc["affected_airport"],
        "flights_impacted": sc["flight_count"],
        "delay_minutes":    sc["delay_minutes"],
        "is_cancellation":  sc["is_cancellation"],
        "passengers":       pax,
        "passenger_count":  len(pax),
        "rebooking_options": _build_rebooking(sc["type"]),
        "compensation":     comp,
        "payment_recovery": {
            "recommended_mode": "original_payment" if sc["compensation_hint"] == "FullRefund" else "travel_credit",
            "amount":           comp["total"],
            "settlement_eta":   "3–5 business days",
        },
        "communication": {
            "message": (
                f"Dear Passenger, we sincerely apologise for the {sc['type']} disruption affecting your flight. "
                f"We have prepared personalised recovery options for you including rebooking and compensation. "
                f"Please visit the SkyRecover app or speak to our agents at {sc['affected_airport']}."
            ),
        },
        "decision": {
            "strategy":               strategy,
            "confidence":             _CONFIDENCE.get(sc["type"], 0.88),
            "rationale": (
                f"Disruption severity: {sc['severity']}. "
                f"{len(pax)} passengers impacted at {sc['affected_airport']}. "
                f"Recommended action: {strategy}."
            ),
            "human_review_required": sc["severity"] == "Critical",
        },
        "audit_trail": _build_audit_trail(),
    }
