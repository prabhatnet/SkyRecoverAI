"""Page 1 – Disruption Simulator."""
from __future__ import annotations

import time

import streamlit as st

from services.simulation_service import SCENARIOS, run_scenario
from ui.components import severity_badge

st.set_page_config(page_title="Disruption Simulator · SkyRecoverAI", page_icon="⛈️", layout="wide")

st.title("⛈️ Disruption Simulator")
st.caption("Select a disruption scenario and trigger the full AI recovery workflow.")
st.divider()

# ── Scenario selector ─────────────────────────────────────────────────────────
selected_key = st.radio(
    "Choose a disruption scenario",
    options=list(SCENARIOS.keys()),
    format_func=lambda k: f"{SCENARIOS[k]['icon']}  {SCENARIOS[k]['name']}",
    horizontal=True,
)

sc = SCENARIOS[selected_key]
st.divider()

# ── Scenario detail ───────────────────────────────────────────────────────────
col_info, col_stats = st.columns([3, 2])

with col_info:
    st.markdown(f"### {sc['icon']}  {sc['name']}")
    st.markdown(sc["description"])
    st.markdown(f"Severity: {severity_badge(sc['severity'])}", unsafe_allow_html=True)
    st.markdown(f"**Root Cause:** {sc['root_cause']}  ·  **Airport:** `{sc['affected_airport']}`")

with col_stats:
    m1, m2 = st.columns(2)
    m1.metric("Flights Affected",    sc["flight_count"])
    m2.metric("Passengers Affected", f"{sc['passenger_count']:,}")

    if sc["delay_minutes"]:
        st.metric("Estimated Delay", f"{sc['delay_minutes']} min")
    if sc["is_cancellation"]:
        st.error("Flight Cancelled — no same-day recovery", icon="🚫")

    comp_label = sc["compensation_hint"].replace("And", " + ")
    st.metric("Compensation Type", comp_label)

st.divider()

# ── Agent pipeline preview ────────────────────────────────────────────────────
st.subheader("AI Recovery Pipeline")
st.caption("Each step will execute when you run the simulation.")

AGENTS = [
    ("1", "Disruption Agent",      "Classify disruption type and severity"),
    ("2", "Passenger Impact Agent","Identify and rank impacted passengers"),
    ("3", "Rebooking Agent",       "Search and rank alternative itineraries"),
    ("4", "Compensation Agent",    "Calculate entitlements per policy"),
    ("5", "Payment Recovery Agent","Simulate refund / travel-credit path"),
    ("6", "Communication Agent",   "Draft personalised passenger messages"),
    ("7", "Decision Agent",        "Select final recovery strategy"),
]

pipeline_cols = st.columns(len(AGENTS))
for col, (num, name, desc) in zip(pipeline_cols, AGENTS):
    with col:
        st.markdown(
            f'<div style="background:#f0f2f6;border-radius:8px;padding:10px;text-align:center">'
            f'<div style="font-size:1.4rem;font-weight:700;color:#1f77b4">{num}</div>'
            f'<div style="font-size:0.75rem;font-weight:600;margin-top:4px">{name}</div>'
            f'<div style="font-size:0.68rem;color:#6c757d;margin-top:4px">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.divider()

# ── Run button ────────────────────────────────────────────────────────────────
if st.button("🚀  Run AI Recovery Workflow", type="primary", use_container_width=True):
    prog = st.progress(0, text="Initialising workflow…")
    for i, (_, agent_name, _) in enumerate(AGENTS, 1):
        prog.progress(i / len(AGENTS), text=f"Running {agent_name}…")
        time.sleep(0.25)
    prog.progress(1.0, text="Workflow complete ✅")

    result = run_scenario(selected_key)
    st.session_state["sim_result"] = result

    st.success(f"Recovery case **{result['case_id']}** created successfully.", icon="✅")

    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric("Passengers Impacted",  f"{result['passenger_count']:,}")
    res_c2.metric("Strategy",             result["decision"]["strategy"])
    res_c3.metric("Decision Confidence",  f"{result['decision']['confidence']*100:.0f}%")

    if result["decision"]["human_review_required"]:
        st.warning(
            "Critical severity: this case requires **Human-in-the-Loop** review before execution.",
            icon="👁️",
        )

    st.caption("Navigate to the other pages in the sidebar to explore the full recovery analysis.")

# ── Current sim banner ────────────────────────────────────────────────────────
elif st.session_state.get("sim_result"):
    sim = st.session_state["sim_result"]
    st.info(
        f"Active case: **{sim['case_id']}** · {sim['scenario_icon']} {sim['scenario_name']}  "
        f"— re-run the simulation above to replace it.",
        icon="ℹ️",
    )
