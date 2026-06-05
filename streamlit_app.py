from __future__ import annotations

import streamlit as st

from services.json_store import load_json, save_json
from workflows.langgraph_builder import build_graph

st.set_page_config(page_title="SkyRecoverAI", layout="wide")
st.title("SkyRecoverAI")
st.caption("Flight disruption recovery simulation with agentic workflow")

scenario_type = st.selectbox(
    "Scenario",
    ["cancellation", "delay", "weather", "crew"],
)

if st.button("Run Recovery Simulation"):
    flights = load_json("data/flights.json")
    passengers = load_json("data/passengers.json")
    itineraries = load_json("data/itineraries.json")

    initial_state = {
        "case_id": "case-demo-001",
        "scenario": {"type": scenario_type},
        "flights": flights,
        "passengers": passengers,
        "itineraries": itineraries,
    }

    app = build_graph()
    final_state = app.invoke(initial_state)

    st.subheader("Decision")
    st.json(final_state.get("decision", {}))

    st.subheader("Communication Draft")
    st.write(final_state.get("communication", {}).get("message", "N/A"))

    save_json("data/output/cases_output.json", final_state)
    st.success("Simulation completed and output saved to data/output/cases_output.json")
