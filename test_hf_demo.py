#!/usr/bin/env python
"""Quick validation that HF demo dependencies work."""
from services.simulation_service import run_scenario

result = run_scenario("atl_thunderstorm")
assert result["case_id"], "Missing case_id"
assert result["passenger_count"] == 284, f"Expected 284 passengers, got {result['passenger_count']}"
assert result["decision"]["strategy"], "Missing strategy"
assert "rebooking_options" in result, "Missing rebooking_options"
assert "compensation" in result, "Missing compensation"

print(f"✅ HF Demo validation passed!")
print(f"   Case: {result['case_id']}")
print(f"   Passengers: {result['passenger_count']}")
print(f"   Strategy: {result['decision']['strategy']}")
print(f"   Confidence: {result['decision']['confidence']:.0%}")
print(f"   Rebooking Options: {len(result['rebooking_options'])}")
print(f"   Total Comp Cost: ${result['compensation']['total']:,.0f}")
