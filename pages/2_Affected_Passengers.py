"""Page 2 – Affected Passengers."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from ui.components import no_simulation_warning, priority_badge

st.set_page_config(page_title="Affected Passengers · SkyRecoverAI", page_icon="🧳", layout="wide")

st.title("🧳 Affected Passengers")
st.caption("Passenger impact assessment — priority segmentation and profile details.")
st.divider()

sim = st.session_state.get("sim_result")
if not sim:
    no_simulation_warning()
    st.stop()

pax_list = sim["passengers"]

# ── Summary KPIs ──────────────────────────────────────────────────────────────
critical  = sum(1 for p in pax_list if p["priority"] == "Critical")
high      = sum(1 for p in pax_list if p["priority"] == "High")
standard  = sum(1 for p in pax_list if p["priority"] == "Standard")
connected = sum(1 for p in pax_list if p["has_connection"])
with_ssr  = sum(1 for p in pax_list if p["ssr"])

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Passengers",    f"{sim['passenger_count']:,}")
k2.metric("🔴 Critical",         critical)
k3.metric("🟠 High",             high)
k4.metric("⚪ Standard",         standard)
k5.metric("Connections at Risk", connected)

st.divider()

# ── Breakdown tabs ────────────────────────────────────────────────────────────
tab_pri, tab_tier, tab_cls, tab_ssr = st.tabs(
    ["Priority Groups", "Loyalty Tiers", "Ticket Classes", "Special Service Requests"]
)

with tab_pri:
    col_chart, col_note = st.columns([2, 1])
    with col_chart:
        st.bar_chart(
            pd.DataFrame(
                {"Priority": ["Critical", "High", "Standard"], "Passengers": [critical, high, standard]}
            ).set_index("Priority")
        )
    with col_note:
        st.markdown(priority_badge("Critical"), unsafe_allow_html=True)
        st.caption("Score ≥ 80: Business/First + Platinum/Gold + connection risk + SSR")
        st.markdown(priority_badge("High"), unsafe_allow_html=True)
        st.caption("Score 50–79: mixed tier, connection or SSR factor")
        st.markdown(priority_badge("Standard"), unsafe_allow_html=True)
        st.caption("Score < 50: Economy, no loyalty, no connection risk")

with tab_tier:
    tiers  = ["None", "Silver", "Gold", "Platinum"]
    counts = [sum(1 for p in pax_list if p["loyalty_tier"] == t) for t in tiers]
    st.bar_chart(pd.DataFrame({"Tier": tiers, "Passengers": counts}).set_index("Tier"))

with tab_cls:
    classes = ["Economy", "Premium Economy", "Business", "First"]
    counts  = [sum(1 for p in pax_list if p["ticket_class"] == c) for c in classes]
    st.bar_chart(pd.DataFrame({"Class": classes, "Passengers": counts}).set_index("Class"))

with tab_ssr:
    ssr_codes = ["WCHR", "UMNR", "VGML", "BLND", "DEAF"]
    ssr_counts = [sum(1 for p in pax_list if p["ssr"] == code) for code in ssr_codes]
    st.bar_chart(pd.DataFrame({"SSR Code": ssr_codes, "Count": ssr_counts}).set_index("SSR Code"))
    st.caption(
        "WCHR=Wheelchair · UMNR=Unaccompanied Minor · VGML=Vegetarian · "
        "BLND=Visually Impaired · DEAF=Hearing Impaired"
    )

st.divider()

# ── Passenger table with filters ──────────────────────────────────────────────
st.subheader("Passenger Detail")

fc, ft, fl, fp = st.columns([3, 2, 2, 2])
filter_name     = fc.text_input("Search name", placeholder="Type to filter…")
filter_tier     = ft.selectbox("Loyalty tier",   ["All", "None", "Silver", "Gold", "Platinum"])
filter_class    = fl.selectbox("Ticket class",   ["All", "Economy", "Premium Economy", "Business", "First"])
filter_priority = fp.selectbox("Priority",       ["All", "Critical", "High", "Standard"])

df = (
    pd.DataFrame(pax_list)
    [["passenger_id", "full_name", "loyalty_tier", "ticket_class", "priority",
      "has_connection", "ssr", "impact_score"]]
    .rename(columns={
        "passenger_id":  "ID",
        "full_name":     "Name",
        "loyalty_tier":  "Tier",
        "ticket_class":  "Class",
        "priority":      "Priority",
        "has_connection": "Connection",
        "ssr":           "SSR",
        "impact_score":  "Score",
    })
)
df["Connection"] = df["Connection"].map({True: "Yes", False: "No"})
df["SSR"]        = df["SSR"].fillna("—")

if filter_name:
    df = df[df["Name"].str.contains(filter_name, case=False, na=False)]
if filter_tier != "All":
    df = df[df["Tier"] == filter_tier]
if filter_class != "All":
    df = df[df["Class"] == filter_class]
if filter_priority != "All":
    df = df[df["Priority"] == filter_priority]

st.dataframe(
    df.sort_values("Score", ascending=False).reset_index(drop=True),
    use_container_width=True,
    height=420,
    column_config={
        "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d"),
    },
)
st.caption(
    f"Showing {len(df):,} of {sim['passenger_count']:,} passengers · "
    f"{with_ssr} have Special Service Requests · {connected} have onward connections at risk"
)
