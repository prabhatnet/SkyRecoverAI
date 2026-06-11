"""Shared UI helper components for all SkyRecoverAI pages."""
from __future__ import annotations

import streamlit as st

SEVERITY_COLORS = {
    "Critical": "#dc3545",
    "High":     "#fd7e14",
    "Medium":   "#ffc107",
    "Low":      "#198754",
}
PRIORITY_COLORS = {
    "Critical": "#dc3545",
    "High":     "#fd7e14",
    "Standard": "#6c757d",
}


def severity_badge(severity: str) -> str:
    color = SEVERITY_COLORS.get(severity, "#6c757d")
    return (
        f'<span style="background:{color};color:white;padding:3px 12px;'
        f'border-radius:12px;font-size:0.8rem;font-weight:700">{severity}</span>'
    )


def priority_badge(priority: str) -> str:
    color = PRIORITY_COLORS.get(priority, "#6c757d")
    return (
        f'<span style="background:{color};color:white;padding:3px 12px;'
        f'border-radius:12px;font-size:0.8rem;font-weight:700">{priority}</span>'
    )


def no_simulation_warning() -> None:
    st.warning(
        "No simulation has been run yet. "
        "Go to **Disruption Simulator** in the sidebar to launch a scenario.",
        icon="⚠️",
    )


def confidence_bar(label: str, value: float) -> None:
    """Render a labelled horizontal confidence progress bar."""
    color = "#198754" if value >= 0.9 else ("#ffc107" if value >= 0.75 else "#dc3545")
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">'
        f'<span style="min-width:220px;font-size:0.88rem">{label}</span>'
        f'<div style="flex:1;background:#e9ecef;border-radius:6px;height:14px">'
        f'<div style="background:{color};width:{value*100:.0f}%;height:14px;border-radius:6px"></div>'
        f'</div>'
        f'<span style="font-weight:700;color:{color};min-width:44px;text-align:right">'
        f'{value*100:.0f}%</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = "") -> None:
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)
