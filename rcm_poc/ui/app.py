"""
AI Regulatory Change Management (RCM) Analyst
E2E POC - Streamlit GUI Application
Mirrors the UI shown in the architecture screenshots
"""

import streamlit as st
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.regulations import SAMPLE_REGULATIONS, BANK_PROFILES
from agents.rcm_agent import RCMAnalystAgent

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RCM Analyst | AI-Powered",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Dark Navy Theme */
  .stApp { background-color: #0a1628; color: #e0e6f0; }
  .stSidebar { background-color: #0d1f3c !important; }
  .stSidebar .stMarkdown { color: #e0e6f0; }

  /* Header */
  .rcm-header {
    background: linear-gradient(135deg, #0d1f3c 0%, #1a3a6c 100%);
    border-bottom: 2px solid #00b4d8;
    padding: 1rem 2rem;
    margin: -1rem -1rem 1.5rem -1rem;
    display: flex; align-items: center; gap: 1rem;
  }
  .rcm-header h1 { color: white; font-size: 1.6rem; font-weight: 700; margin: 0; }
  .rcm-header span { color: #00b4d8; font-size: 0.85rem; }

  /* Sidebar reg cards */
  .reg-card {
    background: #112240;
    border-left: 3px solid #1a5276;
    border-radius: 6px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  .reg-card:hover { border-left-color: #00b4d8; background: #1a3a6c; }
  .reg-card.active { border-left-color: #00ff88; background: #1a4a3c; }
  .reg-card .reg-title { font-size: 0.78rem; font-weight: 600; color: #e0e6f0; line-height: 1.3; }
  .reg-card .reg-date { font-size: 0.68rem; color: #7fa3c0; margin-top: 0.3rem; }
  .reg-card .reg-badge { font-size: 0.65rem; background: #1a3a6c; color: #00b4d8;
    border-radius: 3px; padding: 1px 5px; display: inline-block; margin-top: 0.3rem; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
    background: #0d1f3c;
    border-bottom: 1px solid #1a3a6c;
    gap: 0;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7fa3c0;
    font-size: 0.82rem;
    padding: 0.6rem 1.2rem;
    border-bottom: 2px solid transparent;
  }
  .stTabs [aria-selected="true"] {
    color: #00b4d8 !important;
    border-bottom-color: #00b4d8 !important;
    background: transparent !important;
  }

  /* Metric cards */
  .metric-card {
    background: #112240;
    border: 1px solid #1a3a6c;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
  }
  .metric-card .metric-val { font-size: 2rem; font-weight: 700; color: #00b4d8; }
  .metric-card .metric-label { font-size: 0.75rem; color: #7fa3c0; margin-top: 0.3rem; }

  /* Section headers */
  .section-header {
    font-size: 1rem; font-weight: 700; color: #00b4d8;
    border-bottom: 1px solid #1a3a6c;
    padding-bottom: 0.4rem; margin-bottom: 1rem;
  }

  /* Status badges */
  .badge-high { background: #4a0f0f; color: #ff6b6b; border: 1px solid #ff6b6b;
    border-radius: 4px; padding: 2px 8px; font-size: 0.72rem; font-weight: 600; }
  .badge-medium { background: #4a3000; color: #ffa500; border: 1px solid #ffa500;
    border-radius: 4px; padding: 2px 8px; font-size: 0.72rem; font-weight: 600; }
  .badge-low { background: #0a3a2a; color: #00ff88; border: 1px solid #00ff88;
    border-radius: 4px; padding: 2px 8px; font-size: 0.72rem; font-weight: 600; }
  .badge-applicable { background: #0a3a2a; color: #00ff88; border: 1px solid #00ff88;
    border-radius: 4px; padding: 3px 10px; font-size: 0.78rem; font-weight: 600; }
  .badge-na { background: #4a0f0f; color: #ff6b6b; border: 1px solid #ff6b6b;
    border-radius: 4px; padding: 3px 10px; font-size: 0.78rem; font-weight: 600; }

  /* Action item cards */
  .action-card {
    background: #112240; border: 1px solid #1a3a6c; border-radius: 6px;
    padding: 0.8rem 1rem; margin-bottom: 0.6rem;
  }
  .action-card .action-id { color: #00b4d8; font-size: 0.7rem; font-weight: 700; }
  .action-card .action-title { color: #e0e6f0; font-size: 0.88rem; font-weight: 600; margin: 0.2rem 0; }
  .action-card .action-desc { color: #7fa3c0; font-size: 0.78rem; }

  /* Gap/impact rows */
  .impact-row {
    background: #112240; border-left: 3px solid #1a5276;
    border-radius: 0 6px 6px 0; padding: 0.7rem 1rem; margin-bottom: 0.5rem;
  }
  .impact-row.new { border-left-color: #ff6b6b; }
  .impact-row.amend { border-left-color: #ffa500; }
  .impact-row.ok { border-left-color: #00ff88; }

  /* Info boxes */
  .info-box {
    background: #0d2a4a; border: 1px solid #1a5276;
    border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 1rem;
  }

  /* Status indicator */
  .status-dot { width: 8px; height: 8px; border-radius: 50%;
    display: inline-block; margin-right: 5px; }
  .status-dot.active { background: #00ff88; box-shadow: 0 0 6px #00ff88; }

  /* Progress bar custom */
  .stProgress > div > div { background-color: #00b4d8; }

  /* Button styling */
  .stButton > button {
    background: linear-gradient(135deg, #0066cc, #0099cc);
    color: white; border: none; border-radius: 6px;
    font-weight: 600; padding: 0.5rem 1.5rem;
    transition: all 0.2s;
  }
  .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,180,216,0.3); }

  /* Expander */
  .streamlit-expanderHeader { background: #112240 !important; color: #e0e6f0 !important; }
  .streamlit-expanderContent { background: #0a1628 !important; border: 1px solid #1a3a6c !important; }

  /* Tables */
  .stDataFrame { border: 1px solid #1a3a6c !important; }

  /* Mandate item */
  .mandate-item {
    background: #112240; border-radius: 6px; padding: 0.6rem 1rem;
    margin-bottom: 0.4rem; font-size: 0.82rem; color: #c0d4e8;
    border-left: 3px solid #00b4d8;
  }
  .mandate-id { color: #00b4d8; font-weight: 700; font-size: 0.72rem; }

  .sidebar-label {
    font-size: 0.7rem; color: #7fa3c0; text-transform: uppercase;
    letter-spacing: 0.08em; margin: 1rem 0 0.4rem 0;
  }

  .system-status {
    background: #0a2a1a; border: 1px solid #00ff88;
    border-radius: 6px; padding: 0.4rem 0.8rem;
    font-size: 0.72rem; color: #00ff88; margin-bottom: 1rem;
  }
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ────────────────────────────────────────────────────────
if 'results_cache' not in st.session_state:
    st.session_state.results_cache = {}
if 'selected_reg' not in st.session_state:
    st.session_state.selected_reg = SAMPLE_REGULATIONS[1]['id']  # default
if 'selected_bank' not in st.session_state:
    st.session_state.selected_bank = "HSBC"
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0


# ─── Helper Functions ─────────────────────────────────────────────────────────
def get_badge(level: str) -> str:
    level_lower = level.lower() if level else ''
    if level_lower == 'high' or level_lower == 'critical':
        return f'<span class="badge-high">{level}</span>'
    elif level_lower == 'medium':
        return f'<span class="badge-medium">{level}</span>'
    else:
        return f'<span class="badge-low">{level}</span>'

def get_impact_class(impact_type: str) -> str:
    t = impact_type.lower() if impact_type else ''
    if 'new' in t: return 'new'
    if 'amend' in t or 'strengthen' in t or 'update' in t: return 'amend'
    return 'ok'

def cache_key(reg_id, bank_name):
    return f"{reg_id}|{bank_name}"


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1rem 0;">
        <div style="font-size:1.5rem;">🏦</div>
        <div style="font-size:1rem; font-weight:700; color:#e0e6f0;">RCM Analyst</div>
        <div style="font-size:0.7rem; color:#00b4d8;">AI-Powered Regulatory Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="system-status">
        <span class="status-dot active"></span>
        System Active: {len(SAMPLE_REGULATIONS)} Incoming Regulations
    </div>
    """, unsafe_allow_html=True)

    # Bank selector
    st.markdown('<div class="sidebar-label">Select Bank</div>', unsafe_allow_html=True)
    selected_bank = st.selectbox(
        "", list(BANK_PROFILES.keys()), label_visibility="collapsed",
        key="bank_selector",
        index=list(BANK_PROFILES.keys()).index(st.session_state.selected_bank)
    )
    st.session_state.selected_bank = selected_bank

    # API key
    st.markdown('<div class="sidebar-label">Anthropic API Key</div>', unsafe_allow_html=True)
    api_key = st.text_input("", type="password", label_visibility="collapsed",
                             placeholder="sk-ant-...", key="api_key")

    # Regulatory Feed
    st.markdown('<div class="sidebar-label">📡 Regulatory Feed</div>', unsafe_allow_html=True)

    for reg in SAMPLE_REGULATIONS:
        is_active = reg['id'] == st.session_state.selected_reg
        active_class = "active" if is_active else ""

        if st.button(
            f"{'🟢 ' if is_active else ''}{reg['title'][:45]}...\n{reg['date']}",
            key=f"reg_btn_{reg['id']}",
            use_container_width=True
        ):
            st.session_state.selected_reg = reg['id']
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.65rem; color:#4a6580; text-align:center;">
    Agentic RAG Architecture<br>
    Gap Analyzer Agent v1.0<br>
    Powered by Claude AI
    </div>
    """, unsafe_allow_html=True)


# ─── Get Selected Data ─────────────────────────────────────────────────────────
selected_reg = next((r for r in SAMPLE_REGULATIONS if r['id'] == st.session_state.selected_reg),
                     SAMPLE_REGULATIONS[0])
bank_profile = BANK_PROFILES[st.session_state.selected_bank]

# ─── Main Header ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="rcm-header">
  <span style="font-size:1.8rem;">🏛️</span>
  <div>
    <h1>Regulatory Change Management Analyst</h1>
    <span>Bank: {bank_profile['name']} &nbsp;|&nbsp; {selected_reg['regulator']} &nbsp;|&nbsp;
    {selected_reg['date']}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏦 Bank Profile",
    "📋 Regulation Summary",
    "✅ Applicability Assessment",
    "📊 Compliance Assessment",
    "🎯 Action Plan"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: BANK PROFILE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f"## 🏦 Bank Profile Summary — {bank_profile['name']}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">{bank_profile.get('total_assets','N/A')}</div>
            <div class="metric-label">Total Assets</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">{bank_profile.get('retail_deposits','N/A')}</div>
            <div class="metric-label">Retail Deposits</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">{len(bank_profile['policies'])}</div>
            <div class="metric-label">Active Policies</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">{len(bank_profile['internal_controls'])}</div>
            <div class="metric-label">Internal Controls</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-header">📦 Products & Services Offered</div>',
                    unsafe_allow_html=True)
        for category, products in bank_profile['products_services'].items():
            with st.expander(f"**{category}** ({len(products)} products)", expanded=False):
                for p in products:
                    st.markdown(f"• {p}")

        st.markdown('<div class="section-header" style="margin-top:1.5rem;">🏛️ Regulators</div>',
                    unsafe_allow_html=True)
        for reg_name in bank_profile.get('regulators', []):
            st.markdown(f"""<div class="mandate-item">{reg_name}</div>""",
                        unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-header">📜 Active Policies</div>',
                    unsafe_allow_html=True)
        for policy in bank_profile['policies']:
            st.markdown(f"""<div class="mandate-item">{policy}</div>""",
                        unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:1.5rem;">🔒 Internal Controls</div>',
                    unsafe_allow_html=True)
        for ctrl in bank_profile['internal_controls']:
            st.markdown(f"""<div class="mandate-item">{ctrl}</div>""",
                        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: REGULATION SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"## 📋 {selected_reg['title']}")

    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.info(f"**Regulator:** {selected_reg['regulator']}\n\n**Type:** {selected_reg['type']}")
    with info_col2:
        st.info(f"**Date:** {selected_reg['date']}\n\n**ID:** {selected_reg['id']}")
    with info_col3:
        st.info(f"**Mandates:** {len(selected_reg['mandates'])}\n\n**Source:** {selected_reg['source_url']}")

    ck = cache_key(selected_reg['id'], st.session_state.selected_bank)

    if ck in st.session_state.results_cache and 'summary' in st.session_state.results_cache[ck]:
        summary = st.session_state.results_cache[ck]['summary']
        _show_summary(summary, selected_reg)
    else:
        st.markdown('<div class="section-header">📌 Regulation Mandates (Raw)</div>',
                    unsafe_allow_html=True)
        for i, m in enumerate(selected_reg['mandates'], 1):
            st.markdown(f"""<div class="mandate-item">
                <span class="mandate-id">M-{i:03d}</span><br>{m}</div>""",
                unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("*Run the full AI analysis to get plain English interpretation and mandate decomposition*")

        with st.expander("📄 View Full Regulation Text"):
            st.text(selected_reg['full_text'])


def _show_summary(summary, reg):
    st.markdown('<div class="section-header">🌐 Plain English Summary</div>',
                unsafe_allow_html=True)
    st.markdown(f"""<div class="info-box">{summary.get('plain_english_summary','')}</div>""",
                unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="section-header">🎯 Key Themes</div>', unsafe_allow_html=True)
        for theme in summary.get('key_themes', []):
            st.markdown(f"• {theme}")

        st.markdown('<div class="section-header" style="margin-top:1rem;">👥 Who Is Affected</div>',
                    unsafe_allow_html=True)
        st.markdown(summary.get('who_is_affected', ''))

    with col_r:
        st.markdown('<div class="section-header">📅 Key Dates</div>', unsafe_allow_html=True)
        dates = summary.get('key_dates', {})
        for phase, detail in dates.items():
            if detail:
                st.markdown(f"**{phase.replace('_', ' ').title()}:** {detail}")

        st.markdown('<div class="section-header" style="margin-top:1rem;">⚠️ Penalty Risk</div>',
                    unsafe_allow_html=True)
        st.warning(summary.get('penalty_risk', ''))

    st.markdown('<div class="section-header" style="margin-top:1rem;">📜 Mandate Breakdown</div>',
                unsafe_allow_html=True)
    for m in summary.get('mandates', []):
        with st.expander(f"**{m['mandate_id']}** — {m['mandate_title']} [{m['mandate_type']}]"):
            st.markdown(f"**Original:** {m['mandate_text']}")
            st.markdown(f"**Plain English:** {m['plain_english']}")
            if m.get('sub_mandates'):
                st.markdown("**Sub-requirements:**")
                for s in m['sub_mandates']:
                    st.markdown(f"  - {s}")


# Patch tab2 to show summary if cached
with tab2:
    ck = cache_key(selected_reg['id'], st.session_state.selected_bank)
    if ck in st.session_state.results_cache and 'summary' in st.session_state.results_cache[ck]:
        summary = st.session_state.results_cache[ck]['summary']
        _show_summary(summary, selected_reg)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: APPLICABILITY ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f"## ✅ Applicability Assessment")
    st.markdown(f"*Regulation: **{selected_reg['title']}** | Bank: **{bank_profile['name']}***")

    ck = cache_key(selected_reg['id'], st.session_state.selected_bank)

    if ck in st.session_state.results_cache and 'applicability' in st.session_state.results_cache[ck]:
        app = st.session_state.results_cache[ck]['applicability']

        # Top-line verdict
        is_app = app.get('is_applicable', False)
        score = app.get('applicability_score', 0)
        risk = app.get('regulatory_risk_rating', 'Medium')

        verdict_col, score_col, risk_col = st.columns([2, 1, 1])
        with verdict_col:
            badge = '<span class="badge-applicable">✓ APPLICABLE</span>' if is_app else '<span class="badge-na">✗ NOT APPLICABLE</span>'
            st.markdown(f"### Verdict: {badge}", unsafe_allow_html=True)
            st.markdown(app.get('applicability_rationale', ''))
        with score_col:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-val" style="color:{'#00ff88' if score > 70 else '#ffa500'}">{score}%</div>
                <div class="metric-label">Applicability Score</div></div>""", unsafe_allow_html=True)
        with risk_col:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-val" style="color:{'#ff6b6b' if risk=='High' else '#ffa500' if risk=='Medium' else '#00ff88'}">{risk}</div>
                <div class="metric-label">Risk Rating</div></div>""", unsafe_allow_html=True)

        st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-header">🟢 In-Scope Business Units</div>',
                        unsafe_allow_html=True)
            for bu in app.get('in_scope_business_units', []):
                st.markdown(f"""<div class="mandate-item" style="border-left-color:#00ff88;">✓ {bu}</div>""",
                            unsafe_allow_html=True)

            st.markdown('<div class="section-header" style="margin-top:1rem;">👨‍💼 Assigned SME Functions</div>',
                        unsafe_allow_html=True)
            for sme in app.get('assigned_sme', []):
                st.markdown(f"• {sme}")

        with c2:
            st.markdown('<div class="section-header">🔴 Out-of-Scope Business Units</div>',
                        unsafe_allow_html=True)
            for bu in app.get('out_of_scope_business_units', []):
                st.markdown(f"""<div class="mandate-item" style="border-left-color:#4a6580;">✗ {bu}</div>""",
                            unsafe_allow_html=True)

            st.markdown('<div class="section-header" style="margin-top:1rem;">📅 Compliance Timeline</div>',
                        unsafe_allow_html=True)
            timeline = app.get('compliance_timeline', {})
            for phase, detail in timeline.items():
                if detail:
                    icon = "🔴" if "immediate" in phase else "🟡" if "short" in phase else "🟢"
                    st.markdown(f"{icon} **{phase.replace('_', ' ').title()}:** {detail}")

        st.markdown('<div class="section-header" style="margin-top:1rem;">📌 Key Applicability Criteria</div>',
                    unsafe_allow_html=True)
        for crit in app.get('key_applicability_criteria', []):
            st.markdown(f"""<div class="mandate-item">• {crit}</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="info-box" style="margin-top:1rem;">
            <strong>⚠️ Risk Rationale:</strong> {app.get('rationale_for_rating','')}
        </div>""", unsafe_allow_html=True)

    else:
        st.info("👆 Run the AI Analysis to see applicability assessment results")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: COMPLIANCE ASSESSMENT (Impact + Gaps)
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## 📊 Compliance Impact Assessment & Gap Analysis")

    ck = cache_key(selected_reg['id'], st.session_state.selected_bank)

    if ck in st.session_state.results_cache and 'impact' in st.session_state.results_cache[ck]:
        impact = st.session_state.results_cache[ck]['impact']

        if impact is None:
            st.success("✅ This regulation is NOT applicable to this bank — no impact assessment required.")
        else:
            # Summary metrics
            policy_impacts = impact.get('policy_impacts', [])
            control_impacts = impact.get('control_impacts', [])
            new_controls = impact.get('new_controls_required', [])
            overall = impact.get('overall_impact_level', 'Medium')

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-val" style="color:{'#ff6b6b' if overall=='High' else '#ffa500'}">{overall}</div>
                    <div class="metric-label">Overall Impact</div></div>""", unsafe_allow_html=True)
            with m2:
                new_p = len([p for p in policy_impacts if 'new' in p.get('impact_type','').lower()])
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-val">{len(policy_impacts)}</div>
                    <div class="metric-label">Policies Impacted ({new_p} New)</div></div>""",
                    unsafe_allow_html=True)
            with m3:
                gap_c = len([c for c in control_impacts if 'no change' not in c.get('impact_type','').lower()])
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-val">{gap_c}</div>
                    <div class="metric-label">Control Gaps</div></div>""", unsafe_allow_html=True)
            with m4:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-val">{len(new_controls)}</div>
                    <div class="metric-label">New Controls Required</div></div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="info-box" style="margin:1rem 0;">
                <strong>📋 Impact Summary:</strong> {impact.get('impact_summary','')}
                <br><br><strong>⏱️ Estimated Effort:</strong> {impact.get('estimated_total_effort','')}
            </div>""", unsafe_allow_html=True)

            # Policy impacts
            st.markdown('<div class="section-header">📜 Policy Impact Analysis</div>',
                        unsafe_allow_html=True)
            for pi in policy_impacts:
                imp_class = get_impact_class(pi.get('impact_type', ''))
                with st.expander(
                    f"**{pi.get('impact_type','').upper()}** — {pi.get('policy_name','')} | Effort: {pi.get('effort_estimate','')}",
                    expanded=pi.get('impact_type','') != 'No Change'
                ):
                    st.markdown(f"**Description:** {pi.get('impact_description','')}")
                    if pi.get('mandates_triggering'):
                        st.markdown(f"**Triggered by:** {', '.join(pi['mandates_triggering'])}")

            # Control gaps
            st.markdown('<div class="section-header" style="margin-top:1.5rem;">🔒 Control Gap Analysis</div>',
                        unsafe_allow_html=True)
            for ci in control_impacts:
                imp_class = get_impact_class(ci.get('impact_type', ''))
                with st.expander(
                    f"**{ci.get('impact_type','').upper()}** — {ci.get('control_name','')} | Effort: {ci.get('effort_estimate','')}",
                    expanded=ci.get('impact_type','') != 'No Change'
                ):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**Current State:** {ci.get('current_state','')}")
                    with col_b:
                        st.markdown(f"**Required State:** {ci.get('required_state','')}")
                    if ci.get('gap_description'):
                        st.warning(f"**Gap:** {ci.get('gap_description','')}")

            # New controls required
            if new_controls:
                st.markdown('<div class="section-header" style="margin-top:1.5rem;">🆕 New Controls Required</div>',
                            unsafe_allow_html=True)
                for nc in new_controls:
                    st.markdown(f"""<div class="action-card">
                        <div class="action-id">NEW CONTROL | Complexity: {nc.get('implementation_complexity','')}</div>
                        <div class="action-title">{nc.get('control_name','')}</div>
                        <div class="action-desc">{nc.get('control_description','')}</div>
                        <div class="action-desc" style="margin-top:0.3rem;color:#00b4d8;">
                            Mandate: {nc.get('mandate_triggering','')}
                        </div>
                    </div>""", unsafe_allow_html=True)

            # Risks if non-compliant
            st.markdown('<div class="section-header" style="margin-top:1.5rem;">⚠️ Risks if Non-Compliant</div>',
                        unsafe_allow_html=True)
            for risk in impact.get('risks_if_non_compliant', []):
                st.error(f"• {risk}")

    else:
        st.info("👆 Run the AI Analysis to see compliance impact assessment")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: ACTION PLAN
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("## 🎯 Action Plan & Remediation Roadmap")

    ck = cache_key(selected_reg['id'], st.session_state.selected_bank)

    if ck in st.session_state.results_cache and 'action_plan' in st.session_state.results_cache[ck]:
        plan = st.session_state.results_cache[ck]['action_plan']

        if plan is None:
            st.success("✅ No action plan required — regulation not applicable.")
        else:
            # Header metrics
            actions = plan.get('critical_actions', [])
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-val">{plan.get('total_actions', len(actions))}</div>
                    <div class="metric-label">Total Actions</div></div>""", unsafe_allow_html=True)
            with m2:
                critical = len([a for a in actions if a.get('priority','').lower() == 'critical'])
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-val" style="color:#ff6b6b">{critical}</div>
                    <div class="metric-label">Critical Actions</div></div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-val" style="font-size:1rem">{plan.get('estimated_cost_impact','TBD')}</div>
                    <div class="metric-label">Estimated Cost Impact</div></div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="info-box">
                <strong>📋 Executive Summary:</strong> {plan.get('executive_summary','')}
            </div>""", unsafe_allow_html=True)

            # Roadmap
            st.markdown('<div class="section-header">🗺️ Implementation Roadmap</div>',
                        unsafe_allow_html=True)
            roadmap = plan.get('implementation_roadmap', {})
            phase_cols = st.columns(3)
            phase_colors = ['#ff6b6b', '#ffa500', '#00ff88']
            for idx, (phase_key, phase_data) in enumerate(roadmap.items()):
                with phase_cols[idx]:
                    label = phase_data.get('label', phase_key)
                    phase_actions = phase_data.get('actions', [])
                    st.markdown(f"""<div style="background:#112240; border-top: 3px solid {phase_colors[idx]};
                        border-radius: 6px; padding: 0.8rem; min-height: 100px;">
                        <div style="color:{phase_colors[idx]}; font-weight:700; font-size:0.8rem; margin-bottom:0.5rem;">{label}</div>
                        {''.join([f'<div style="font-size:0.75rem; color:#c0d4e8; margin-bottom:0.3rem;">• {a}</div>' for a in phase_actions]) if phase_actions else '<div style="color:#4a6580;font-size:0.75rem;">No actions</div>'}
                    </div>""", unsafe_allow_html=True)

            # Action Items
            st.markdown('<div class="section-header" style="margin-top:1.5rem;">📋 Action Items</div>',
                        unsafe_allow_html=True)

            priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
            sorted_actions = sorted(actions,
                key=lambda x: priority_order.get(x.get('priority','medium').lower(), 2))

            for action in sorted_actions:
                p = action.get('priority', 'Medium')
                p_color = '#ff6b6b' if p.lower() == 'critical' else '#ffa500' if p.lower() == 'high' else '#00b4d8' if p.lower() == 'medium' else '#7fa3c0'

                with st.expander(
                    f"[{action.get('action_id','ACT')}] {action.get('action_title','')} | Priority: {p} | Due: {action.get('due_date','')}",
                    expanded=p.lower() in ['critical', 'high']
                ):
                    c_l, c_r = st.columns([3,1])
                    with c_l:
                        st.markdown(f"**Description:** {action.get('action_description','')}")
                        st.markdown(f"**Owner:** {action.get('owner','')}")
                        st.markdown(f"**Success Criteria:** {action.get('success_criteria','')}")
                    with c_r:
                        st.markdown(f"""<div class="metric-card" style="padding:0.5rem;">
                            <div style="font-size:1.5rem; font-weight:700; color:{p_color}">{p}</div>
                            <div style="font-size:0.65rem; color:#7fa3c0">Priority</div>
                            <div style="font-size:1.2rem; font-weight:700; color:#00b4d8; margin-top:0.5rem">{action.get('effort_days',0)}d</div>
                            <div style="font-size:0.65rem; color:#7fa3c0">Effort</div>
                        </div>""", unsafe_allow_html=True)

                    if action.get('dependencies'):
                        st.markdown(f"**Dependencies:** {', '.join(action['dependencies'])}")

            # Resources
            if plan.get('resource_requirements'):
                st.markdown('<div class="section-header" style="margin-top:1rem;">👥 Resource Requirements</div>',
                            unsafe_allow_html=True)
                for r in plan['resource_requirements']:
                    st.markdown(f"""<div class="mandate-item">• {r}</div>""", unsafe_allow_html=True)

            # Delivery risks
            if plan.get('key_risks_to_delivery'):
                st.markdown('<div class="section-header" style="margin-top:1rem;">⚠️ Key Risks to Delivery</div>',
                            unsafe_allow_html=True)
                for r in plan['key_risks_to_delivery']:
                    st.warning(f"• {r}")

    else:
        st.info("👆 Run the AI Analysis to see action plan")


# ═══════════════════════════════════════════════════════════════════════════════
# BOTTOM ACTION BAR — Run Analysis
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")

ck = cache_key(selected_reg['id'], st.session_state.selected_bank)
already_run = ck in st.session_state.results_cache

col_run1, col_run2, col_run3 = st.columns([2, 2, 2])

with col_run1:
    if st.button(
        f"🚀 Run AI Analysis — {selected_bank} × {selected_reg['id']}",
        use_container_width=True,
        type="primary"
    ):
        if not api_key:
            st.error("⚠️ Please enter your Anthropic API key in the sidebar to run analysis")
        else:
            try:
                agent = RCMAnalystAgent(api_key=api_key)
                progress_bar = st.progress(0)
                status_text = st.empty()

                def update_progress(pct, msg):
                    progress_bar.progress(pct)
                    status_text.markdown(f"*{msg}*")

                results = agent.run_full_analysis(
                    selected_reg, bank_profile, progress_callback=update_progress
                )

                st.session_state.results_cache[ck] = results
                progress_bar.empty()
                status_text.empty()
                st.success("✅ Analysis complete! Navigate the tabs to explore results.")
                st.rerun()

            except Exception as e:
                st.error(f"Error running analysis: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

with col_run2:
    if st.button(
        "🔄 Run All Banks × All Regulations",
        use_container_width=True,
        help="Batch mode: runs analysis for every bank against every regulation"
    ):
        if not api_key:
            st.error("⚠️ Please enter your Anthropic API key in the sidebar")
        else:
            total = len(BANK_PROFILES) * len(SAMPLE_REGULATIONS)
            batch_progress = st.progress(0)
            batch_status = st.empty()
            done = 0

            try:
                agent = RCMAnalystAgent(api_key=api_key)
                for bank_name, bank_prof in BANK_PROFILES.items():
                    for reg in SAMPLE_REGULATIONS:
                        bk = cache_key(reg['id'], bank_name)
                        batch_status.markdown(f"*Analyzing: **{bank_name}** × **{reg['id']}**...*")
                        if bk not in st.session_state.results_cache:
                            results = agent.run_full_analysis(reg, bank_prof)
                            st.session_state.results_cache[bk] = results
                        done += 1
                        batch_progress.progress(done / total)

                batch_progress.empty()
                batch_status.empty()
                st.success(f"✅ Batch complete! Analysed {total} combinations.")
                st.rerun()
            except Exception as e:
                st.error(f"Batch error: {str(e)}")

with col_run3:
    if already_run:
        if st.button("🗑️ Clear Results", use_container_width=True):
            if ck in st.session_state.results_cache:
                del st.session_state.results_cache[ck]
            st.rerun()

        # Export results
        results_data = st.session_state.results_cache.get(ck, {})
        st.download_button(
            label="⬇️ Export Results (JSON)",
            data=json.dumps(results_data, indent=2),
            file_name=f"rcm_analysis_{selected_reg['id']}_{selected_bank}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

# Footer
st.markdown("""
<div style="text-align:center; color:#4a6580; font-size:0.7rem; margin-top:2rem; padding-top:1rem; border-top:1px solid #1a3a6c;">
  AI in RCM POC | Agentic RAG Architecture | Gap Analyzer Agent v1.0 | Powered by Anthropic Claude
</div>
""", unsafe_allow_html=True)
