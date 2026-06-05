from workflows.workflow import run_recovery_workflow


def test_workflow_smoke() -> None:
    state = {
        "scenario": {"type": "cancellation"},
        "passengers": [{"passenger_id": "P1"}],
        "itineraries": [{"option_id": "OPT1"}],
    }

    result = run_recovery_workflow(state)
    assert "decision" in result
    assert result["decision"]["strategy"] == "rebook_plus_compensation"
