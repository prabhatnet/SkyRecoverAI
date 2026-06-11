"""Page 3 – Recovery Recommendations."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from ui.components import confidence_bar, no_simulation_warning

st.set_page_config(page_title="Recovery Recommendations · SkyRecoverAI", page_icon="🔁", layout="wide")

st.title("🔁 Recovery Recommendations")
st.caption("Ranked rebooking options and final agent strategy for the active disruption case.")
st.divider()

sim = st.session_state.get("sim_result")
if not sim:
    no_simulation_warning()
    st.stop()

# ── Communication banner ──────────────────────────────────────────────────────
st.info(sim["communication"]["message"], icon="💬")
st.divider()

# ── Rebooking option cards ────────────────────────────────────────────────────
st.subheader("Ranked Rebooking Options")
options = sim["rebooking_options"]

for i, opt in enumerate(options):
    is_best = i == 0
    with st.container(border=True):
        hdr_col, stat_col, score_col = st.columns([3, 2, 2])

        with hdr_col:
            badge = "⭐ **Best Option**" if is_best else f"Option {i + 1}"
            st.markdown(badge)
            st.markdown(f"✈️  `{opt['flight']}`")
            st.markdown(f"Cabin: **{opt['cabin']}**")

        with stat_col:
            s1, s2 = st.columns(2)
            s1.metric("Seats Available", opt["seats"])
            s2.metric("Arrival Delay",   f"+{opt['delta_hrs']} hrs")

        with score_col:
            st.markdown("**Option Score**")
            confidence_bar("", opt["score"])

st.divider()

# ── Options comparison table ──────────────────────────────────────────────────
st.subheader("Comparison Table")
df = pd.DataFrame(options).rename(columns={
    "option_id":  "Option",
    "flight":     "Flight",
    "delta_hrs":  "Delay (hrs)",
    "seats":      "Seats",
    "score":      "Score",
    "cabin":      "Cabin",
})
df["Score"] = (df["Score"] * 100).round(1)

st.dataframe(
    df.set_index("Option"),
    use_container_width=True,
    column_config={
        "Score": st.column_config.ProgressColumn("Score (%)", min_value=0, max_value=100, format="%.1f"),
    },
)
st.divider()

# ── Agent decision ────────────────────────────────────────────────────────────
st.subheader("Agent Strategy Decision")
dec = sim["decision"]

d1, d2 = st.columns(2)
d1.metric("Selected Strategy",   dec["strategy"])
d2.metric("Decision Confidence", f"{dec['confidence'] * 100:.0f}%")

st.markdown(f"**Rationale:** {dec['rationale']}")

if dec["human_review_required"]:
    st.warning(
        "This decision is flagged for **Human-in-the-Loop** review "
        "before execution due to Critical severity.",
        icon="👁️",
    )
else:
    st.success("Decision confidence is sufficient for automated execution.", icon="✅")
