"""
SkyRecoverAI Hugging Face Demo
Streamlined 3-minute walkthrough for technical hiring managers and architects.
Entry point: streamlit_hf_demo.py
"""
from __future__ import annotations

import time

import streamlit as st

from services.simulation_service import SCENARIOS, run_scenario
from ui.components import confidence_bar, priority_badge, severity_badge

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SkyRecoverAI Demo · Hugging Face",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide sidebar and streamlit branding for clean demo
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# TITLE & BRIEF
# ──────────────────────────────────────────────────────────────────────────────

st.markdown(
    """
    # ✈️ SkyRecoverAI
    **Agentic AI for Airline Disruption Recovery**

    *A multi-agent LLM workflow that automates passenger recovery decisions in real-time.*
    """
)

st.caption(
    "Demo: 3-minute walkthrough. Simulates a critical weather disruption and "
    "demonstrates AI-driven recovery orchestration for hiring evaluators."
)

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# DEMO SECTION 1: SCENARIO TRIGGER
# ──────────────────────────────────────────────────────────────────────────────

st.markdown("### 1️⃣ Trigger Disruption Scenario")
st.markdown("**Scenario:** ATL Thunderstorm — Critical severity, 284 passengers affected.")

col_left, col_right = st.columns([2, 1])

with col_left:
    sc = SCENARIOS["atl_thunderstorm"]
    st.markdown(f"{sc['icon']} **{sc['name']}**")
    st.caption(sc["description"])

with col_right:
    st.markdown(severity_badge(sc["severity"]), unsafe_allow_html=True)
    st.markdown(
        f"**Airport:** {sc['affected_airport']}  \n"
        f"**Flights:** {sc['flight_count']}  \n"
        f"**Passengers:** {sc['passenger_count']:,}"
    )

demo_triggered = st.button("▶ Start Demo Workflow", type="primary", use_container_width=True)

if not demo_triggered and not st.session_state.get("hf_demo_result"):
    st.info(
        "👆 Click the button above to start the 3-minute demo. "
        "The workflow will execute all 7 AI agents and show recovery recommendations.",
        icon="ℹ️",
    )
    st.stop()

# ──────────────────────────────────────────────────────────────────────────────
# DEMO EXECUTION
# ──────────────────────────────────────────────────────────────────────────────

if demo_triggered:
    st.session_state["hf_demo_result"] = None

    # Progress animation
    prog = st.progress(0, text="Initializing workflow…")
    time.sleep(0.3)

    agents_in_order = [
        ("Disruption Agent", "Classifying event: Weather, Critical severity"),
        ("Passenger Impact Agent", "Ranking 284 passengers by priority"),
        ("Rebooking Agent", "Searching alternatives: 3 viable itineraries found"),
        ("Compensation Agent", "Policy rule match: Meal + Hotel entitlements"),
        ("Payment Recovery Agent", "Simulating refund path: Travel credit mode"),
        ("Communication Agent", "Drafting personalized SMS, email, push messages"),
        ("Decision Agent", "Evaluating 3 strategies, selecting optimal recovery plan"),
    ]

    status_container = st.empty()

    for i, (agent_name, task_desc) in enumerate(agents_in_order):
        progress = (i + 1) / len(agents_in_order)
        prog.progress(progress, text=f"Running {agent_name}…")

        with status_container.container():
            st.markdown(f"**{agent_name}**  \n{task_desc}")

        time.sleep(0.4)

    prog.progress(1.0, text="✅ Workflow complete!")

    # Run simulation
    result = run_scenario("atl_thunderstorm")
    st.session_state["hf_demo_result"] = result

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# DEMO SECTION 2: DISRUPTION & IMPACT SUMMARY
# ──────────────────────────────────────────────────────────────────────────────

result = st.session_state.get("hf_demo_result")

if result:
    st.markdown("### 2️⃣ Disruption Impact Assessment")

    impact_cols = st.columns(4)
    impact_cols[0].metric("Case ID", result["case_id"][-8:])
    impact_cols[1].metric("Flights Impacted", result["flights_impacted"])
    impact_cols[2].metric("Passengers Affected", f"{result['passenger_count']:,}")
    impact_cols[3].metric("Est. Duration", f"{result['delay_minutes']} min")

    st.markdown("**Passenger Priority Distribution**")
    priority_dist = {
        "Critical": sum(1 for p in result["passengers"] if p["priority"] == "Critical"),
        "High": sum(1 for p in result["passengers"] if p["priority"] == "High"),
        "Standard": sum(1 for p in result["passengers"] if p["priority"] == "Standard"),
    }

    priority_cols = st.columns(3)
    for col, (tier, count) in zip(priority_cols, priority_dist.items()):
        pct = 100 * count / result["passenger_count"]
        col.markdown(
            priority_badge(tier),
            unsafe_allow_html=True,
        )
        col.metric(tier, f"{count}  ({pct:.0f}%)")

    st.divider()

    # ──────────────────────────────────────────────────────────────────────────
    # DEMO SECTION 3: REBOOKING OPTIONS
    # ──────────────────────────────────────────────────────────────────────────

    st.markdown("### 3️⃣ Ranked Rebooking Options")
    st.markdown("*Agent evaluated 47 available itineraries and ranked by passenger preference.*")

    for i, opt in enumerate(result["rebooking_options"][:2]):
        with st.container(border=True):
            opt_col, score_col = st.columns([3, 1])

            with opt_col:
                badge = "⭐ **Recommended**" if i == 0 else "Backup Option"
                st.markdown(
                    f"{badge}  \n"
                    f"✈️ `{opt['flight']}`  \n"
                    f"Cabin: **{opt['cabin']}** · {opt['seats']} seats available"
                )

            with score_col:
                confidence_bar("Score", opt["score"])

    st.divider()

    # ──────────────────────────────────────────────────────────────────────────
    # DEMO SECTION 4: COMPENSATION DECISION
    # ──────────────────────────────────────────────────────────────────────────

    st.markdown("### 4️⃣ Compensation Decision")
    st.markdown("*Policy-driven entitlements automatically calculated per passenger tier.*")

    comp = result["compensation"]

    cost_cols = st.columns(4)
    cost_cols[0].metric(
        "Meal Vouchers",
        f"${comp['meal_total']:,.0f}",
        help=f"${comp['meal_per_pax']}/pax × {result['passenger_count']:,}",
    )
    cost_cols[1].metric(
        "Hotel Vouchers",
        f"${comp['hotel_total']:,.0f}",
        help=f"${comp['hotel_per_pax']}/pax × {result['passenger_count']:,}",
    )
    cost_cols[2].metric("Refunds", f"${comp['refund_total']:,.0f}")
    cost_cols[3].metric("Travel Credit", f"${comp['credit_total']:,.0f}")

    st.markdown(f"**Total Est. Recovery Cost:** `${comp['total']:,.0f}`")
    st.caption(
        f"Policy applied: **{comp['hint']}**  ·  "
        f"Payment mode: **{result['payment_recovery']['recommended_mode']}**"
    )

    st.divider()

    # ──────────────────────────────────────────────────────────────────────────
    # DEMO SECTION 5: FINAL DECISION & RATIONALE
    # ──────────────────────────────────────────────────────────────────────────

    st.markdown("### 5️⃣ Final Recovery Strategy")

    dec = result["decision"]

    decision_cols = st.columns(3)
    decision_cols[0].metric("Strategy", dec["strategy"])
    decision_cols[1].metric("Confidence", f"{dec['confidence'] * 100:.0f}%")
    decision_cols[2].metric("Review Required", "Yes" if dec["human_review_required"] else "No")

    st.markdown(f"**Rationale:**  \n{dec['rationale']}")

    if dec["human_review_required"]:
        st.warning(
            "🚨 Critical severity → Human-in-the-Loop approval required before execution.",
            icon="⚠️",
        )
    else:
        st.success("✅ Decision confidence sufficient for autonomous execution.", icon="✓")

    st.divider()

    # ──────────────────────────────────────────────────────────────────────────
    # DEMO SECTION 6: AGENT ORCHESTRATION TRACE
    # ──────────────────────────────────────────────────────────────────────────

    st.markdown("### 6️⃣ Agent Pipeline Trace")
    st.markdown("*Full transparency into agent execution, confidence, and latency.*")

    trail = result["audit_trail"]

    trace_cols = st.columns(3)
    trace_cols[0].metric("Total Agents", len(trail))
    trace_cols[1].metric("Total Latency", f"{sum(s['latency_s'] for s in trail):.1f}s")
    trace_cols[2].metric("Avg. Confidence", f"{sum(s['confidence'] for s in trail) / len(trail) * 100:.0f}%")

    st.markdown("")

    with st.expander("View agent execution details", expanded=False):
        for step in trail:
            st.markdown(
                f"**Step {step['step']}: {step['agent']}**  \n"
                f"Event: `{step['event']}` · Status: {step['status']} · Latency: {step['latency_s']}s"
            )
            confidence_bar(f"Confidence", step["confidence"])

    st.divider()

    # ──────────────────────────────────────────────────────────────────────────
    # CLOSING MESSAGE FOR HIRING MANAGERS
    # ──────────────────────────────────────────────────────────────────────────

    st.markdown("---")

    st.markdown(
        """
        ## Key Technical Highlights

        ✅ **Multi-Agent Orchestration** — 7 specialized LLM agents in linear pipeline  
        ✅ **Policy-Driven Decisions** — Deterministic business rules guard LLM outputs  
        ✅ **Full Explainability** — Every decision traced with confidence scores and latency  
        ✅ **Graceful Degradation** — Fallbacks for LLM failures, timeouts, schema violations  
        ✅ **Enterprise Architecture** — Python + Streamlit + LangGraph + OpenAI  
        ✅ **Azure-Ready** — Design prepared for Event Grid, Service Bus, Container Apps  

        **Portfolio Project:** Built to demonstrate agentic AI design patterns, 
        multi-step workflow orchestration, and production-grade error handling.
        """
    )

    st.divider()

    st.markdown(
        "**Learn more:** [GitHub](https://github.com) | "
        "[Architecture Docs](https://github.com) | "
        "[Agent Design](https://github.com)"
    )
