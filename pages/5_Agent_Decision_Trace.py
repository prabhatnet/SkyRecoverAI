"""Page 5 – Agent Decision Trace."""
from __future__ import annotations

import streamlit as st

from ui.components import confidence_bar, no_simulation_warning

st.set_page_config(page_title="Agent Decision Trace · SkyRecoverAI", page_icon="🔍", layout="wide")

st.title("🔍 Agent Decision Trace")
st.caption(
    "Full transparency into the AI agent pipeline — every step, confidence score, and decision rationale."
)
st.divider()

sim = st.session_state.get("sim_result")
if not sim:
    no_simulation_warning()
    st.stop()

# ── Case header ───────────────────────────────────────────────────────────────
h1, h2, h3 = st.columns(3)
h1.metric("Case ID",  sim["case_id"])
h2.metric("Scenario", sim["scenario_name"])
h3.metric("Strategy", sim["decision"]["strategy"])
st.divider()

# ── Pipeline timeline ─────────────────────────────────────────────────────────
st.subheader("Agent Pipeline Execution")

trail = sim["audit_trail"]
total_latency = sum(s["latency_s"] for s in trail)
avg_confidence = sum(s["confidence"] for s in trail) / len(trail)

t1, t2, t3 = st.columns(3)
t1.metric("Total Agents",       len(trail))
t2.metric("Total Latency",      f"{total_latency:.1f} s")
t3.metric("Avg. Confidence",    f"{avg_confidence*100:.0f}%")

st.markdown("")

for step in trail:
    expanded = step["step"] <= 2
    with st.expander(
        f"{step['status']}  ·  Step {step['step']}  ·  **{step['agent']}**  ·  `{step['event']}`",
        expanded=expanded,
    ):
        col_left, col_right = st.columns([2, 1])
        with col_left:
            confidence_bar("Agent Confidence", step["confidence"])
        with col_right:
            st.metric("Latency",  f"{step['latency_s']} s")
            st.metric("Status",   step["status"])

        # Per-step summary context
        summaries = {
            1: f"Disruption type **{sim['scenario_type']}** classified. "
               f"Severity **{sim['severity']}** · Root cause **{sim['root_cause']}** · "
               f"Airport **{sim['affected_airport']}**.",
            2: f"**{sim['passenger_count']:,}** passengers assessed. "
               f"Priority groups assigned based on loyalty tier, ticket class, connection risk, and SSR.",
            3: f"**{len(sim['rebooking_options'])}** rebooking options generated and ranked. "
               f"Top option: `{sim['rebooking_options'][0]['flight']}`.",
            4: f"Compensation package computed. "
               f"Policy applied: **{sim['compensation']['hint']}**. "
               f"Total estimated cost: **${sim['compensation']['total']:,.0f}**.",
            5: f"Payment recovery simulated. "
               f"Mode: **{sim['payment_recovery']['recommended_mode']}**. "
               f"Amount: **${sim['payment_recovery']['amount']:,.0f}**.",
            6: "Personalised passenger communication drafted for SMS, email, and push channels.",
            7: f"Final strategy selected: **{sim['decision']['strategy']}**. "
               f"Confidence: **{sim['decision']['confidence']*100:.0f}%**. "
               + ("Human review flagged." if sim["decision"]["human_review_required"] else "Auto-execute approved."),
        }
        st.caption(summaries.get(step["step"], ""))

st.divider()

# ── Confidence summary ────────────────────────────────────────────────────────
st.subheader("Confidence Summary Across All Agents")
for step in trail:
    confidence_bar(f"Step {step['step']} · {step['agent']}", step["confidence"])

st.divider()

# ── Final decision ────────────────────────────────────────────────────────────
st.subheader("Final Decision")
dec = sim["decision"]

d1, d2 = st.columns(2)
d1.metric("Strategy",   dec["strategy"])
d2.metric("Confidence", f"{dec['confidence']*100:.0f}%")
st.markdown(f"**Rationale:** {dec['rationale']}")

if dec["human_review_required"]:
    st.warning(
        "**Human-in-the-Loop required.** This decision cannot be auto-executed. "
        "An operations agent must review and approve.",
        icon="👁️",
    )
else:
    st.success("Decision meets auto-execution threshold. No human review required.", icon="✅")

st.divider()

# ── Full state inspector ──────────────────────────────────────────────────────
st.subheader("Full State Inspector")
with st.expander("View complete workflow state (JSON)", expanded=False):
    display = {k: v for k, v in sim.items() if k != "passengers"}
    display["passengers_summary"] = f"{sim['passenger_count']} passenger records — omitted for display"
    st.json(display, expanded=2)
