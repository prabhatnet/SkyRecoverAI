"""Page 4 – Compensation Analysis."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from ui.components import no_simulation_warning

st.set_page_config(page_title="Compensation Analysis · SkyRecoverAI", page_icon="💰", layout="wide")

st.title("💰 Compensation Analysis")
st.caption("Entitlement breakdown, cost projections, and payment recovery plan.")
st.divider()

sim = st.session_state.get("sim_result")
if not sim:
    no_simulation_warning()
    st.stop()

comp = sim["compensation"]
pax  = sim["passengers"]

# ── Cost KPI bar ──────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Est. Cost",  f"${comp['total']:,.0f}")
k2.metric("Meal Vouchers",    f"${comp['meal_total']:,.0f}",    help=f"${comp['meal_per_pax']} per passenger")
k3.metric("Hotel Vouchers",   f"${comp['hotel_total']:,.0f}",   help=f"${comp['hotel_per_pax']} per passenger")
k4.metric("Refunds",          f"${comp['refund_total']:,.0f}")
k5.metric("Travel Credit",    f"${comp['credit_total']:,.0f}")

st.divider()

# ── Analysis tabs ─────────────────────────────────────────────────────────────
tab_breakdown, tab_tier, tab_pax = st.tabs(
    ["Cost Breakdown", "By Loyalty Tier", "Per-Passenger Estimate"]
)

with tab_breakdown:
    df_b = pd.DataFrame({
        "Category": ["Meal Vouchers", "Hotel Vouchers", "Refunds", "Travel Credit"],
        "Amount ($)": [
            comp["meal_total"],
            comp["hotel_total"],
            comp["refund_total"],
            comp["credit_total"],
        ],
    }).set_index("Category")
    df_b = df_b[df_b["Amount ($)"] > 0]
    st.bar_chart(df_b)
    st.caption(f"Compensation policy applied: **{comp['hint']}**")

with tab_tier:
    tiers  = ["None", "Silver", "Gold", "Platinum"]
    counts = [comp["tier_counts"][t] for t in tiers]
    voucher_cost = [c * (comp["meal_per_pax"] + comp["hotel_per_pax"]) for c in counts]

    df_t = pd.DataFrame({
        "Tier":                    tiers,
        "Passengers":              counts,
        "Est. Voucher Cost ($)":   voucher_cost,
    }).set_index("Tier")
    st.dataframe(df_t, use_container_width=True)
    st.caption("Voucher costs only. Refunds and credits are based on individual ticket values.")

with tab_pax:
    refund_r  = 0.60 if comp["hint"] == "FullRefund"    else 0.0
    credit_r  = 0.40 if comp["hint"] == "FullRefund"    else (0.15 if comp["hint"] == "MealAndHotel" else 0.0)
    rows = []
    for p in pax[:150]:
        meal   = comp["meal_per_pax"]
        hotel  = comp["hotel_per_pax"]
        refund = round(p["ticket_value"] * refund_r)
        credit = round(p["ticket_value"] * credit_r)
        rows.append({
            "Name":       p["full_name"],
            "Tier":       p["loyalty_tier"],
            "Class":      p["ticket_class"],
            "Priority":   p["priority"],
            "Meal ($)":   meal,
            "Hotel ($)":  hotel,
            "Refund ($)": refund,
            "Credit ($)": credit,
            "Total ($)":  meal + hotel + refund + credit,
        })

    st.dataframe(
        pd.DataFrame(rows).set_index("Name"),
        use_container_width=True,
        height=420,
    )
    if sim["passenger_count"] > 150:
        st.caption(f"Showing first 150 of {sim['passenger_count']:,} passengers.")

st.divider()

# ── Payment recovery plan ─────────────────────────────────────────────────────
st.subheader("Payment Recovery Plan")
pr = sim["payment_recovery"]

p1, p2, p3 = st.columns(3)
p1.metric("Recommended Mode", pr["recommended_mode"].replace("_", " ").title())
p2.metric("Total Amount",     f"${pr['amount']:,.0f}")
p3.metric("Settlement ETA",   pr["settlement_eta"])

st.caption(
    "Payment mode is determined by the Payment Recovery Agent based on compensation type "
    "and passenger payment profile availability."
)
