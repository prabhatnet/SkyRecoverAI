"""SkyRecoverAI — Dashboard home page."""
from __future__ import annotations

import streamlit as st

from services.simulation_service import SCENARIOS, run_scenario
from ui.components import severity_badge

st.set_page_config(
    page_title="SkyRecoverAI · Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Branding ──────────────────────────────────────────────────────────────────
st.title("✈️ SkyRecoverAI")
st.caption("Agentic AI platform for airline disruption recovery · Portfolio Demo")
st.divider()

# ── Top KPI bar ───────────────────────────────────────────────────────────────
sim = st.session_state.get("sim_result")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Active Disruptions",  "1"                                        if sim else "—")
c2.metric("Flights Impacted",    str(sim["flights_impacted"])                if sim else "—")
c3.metric("Passengers Impacted", f"{sim['passenger_count']:,}"               if sim else "—")
c4.metric("Est. Recovery Cost",  f"${sim['compensation']['total']:,.0f}"     if sim else "—")

st.divider()

# ── Active case banner ────────────────────────────────────────────────────────
if sim:
    dec = sim["decision"]
    with st.container(border=True):
        col_l, col_r = st.columns([3, 1])
        with col_l:
            st.markdown(
                f"**Active Case** · `{sim['case_id']}`  ·  "
                f"{sim['scenario_icon']} {sim['scenario_name']}  ·  "
                f"Airport: **{sim['affected_airport']}**"
            )
            st.caption(sim["description"])
        with col_r:
            st.markdown(
                f"**Strategy:** `{dec['strategy']}`  \n"
                f"**Confidence:** `{dec['confidence']*100:.0f}%`"
            )
            if dec["human_review_required"]:
                st.warning("Human review required", icon="👁️")

    st.divider()

# ── Scenario quick-launch ─────────────────────────────────────────────────────
st.subheader("Quick Launch Scenarios")
st.caption("Trigger a full AI recovery workflow with one click.")

cols = st.columns(3)
for col, (key, sc) in zip(cols, SCENARIOS.items()):
    with col:
        with st.container(border=True):
            st.markdown(f"### {sc['icon']} {sc['name']}")
            st.caption(sc["description"])
            st.markdown(
                f"Severity: ",
                unsafe_allow_html=False,
            )
            st.markdown(severity_badge(sc["severity"]), unsafe_allow_html=True)
            st.markdown(
                f"Airport **{sc['affected_airport']}** · "
                f"Flights **{sc['flight_count']}** · "
                f"Passengers **{sc['passenger_count']:,}**"
            )
            if st.button("▶ Run Simulation", key=f"qs_{key}", use_container_width=True):
                with st.spinner(f"Running AI recovery workflow…"):
                    st.session_state["sim_result"] = run_scenario(key)
                st.rerun()

# ── Help footer ───────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Use the **sidebar** to navigate: Disruption Simulator · Affected Passengers · "
    "Recovery Recommendations · Compensation Analysis · Agent Decision Trace"
)
