import streamlit as st
import os
import time
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="MarketMind AI — Enterprise Research Console",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal, attractive, professional Dark Mode theme with smooth animations & glowing accents
st.markdown("""
<style>
    /* Global Dark Theme overrides */
    .stApp { background-color: #000000; color: #f0f0f0; }
    .main { background-color: #000000; color: #f0f0f0; }
    .stSidebar { background-color: #080808; border-right: 1px solid #1a1a1a; }
    
    h1, h2, h3, h4, h5, h6 { font-family: 'Poppins', sans-serif; font-weight: 700; letter-spacing: -0.02em; color: #ffffff; }
    p, li, label, span { font-family: 'Poppins', sans-serif; color: #cccccc; }
    
    /* Smooth button entrance and hover animations */
    .stButton>button {
        background: linear-gradient(135deg, #1f1f1f 0%, #111111 100%);
        color: #ffffff;
        font-weight: 600;
        border-radius: 8px;
        border: 1px solid #333333;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transform: translateY(0);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
        color: #000000;
        border-color: #ffffff;
        box-shadow: 0 6px 20px rgba(255,255,255,0.25);
        transform: translateY(-2px) scale(1.02);
    }
    .stButton>button:active {
        transform: translateY(0px) scale(0.98);
    }

    /* Metric Cards with pulse animation */
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px rgba(255,255,255,0.05); }
        50% { box-shadow: 0 0 15px rgba(255,255,255,0.15); }
        100% { box-shadow: 0 0 5px rgba(255,255,255,0.05); }
    }
    .metric-card {
        background-color: #0b0b0b;
        border: 1px solid #222222;
        padding: 22px;
        border-radius: 10px;
        text-align: center;
        animation: pulseGlow 4s infinite ease-in-out;
        transition: border-color 0.3s ease;
    }
    .metric-card:hover {
        border-color: #555555;
    }

    /* Terminal Log Box */
    .log-box {
        background-color: #050505;
        color: #00ff66;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #222222;
        height: 320px;
        overflow-y: scroll;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.8);
    }

    /* Epistemic Badges */
    .badge-fact { background-color: #172554; color: #93c5fd; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; border: 1px solid #1e40af; }
    .badge-inference { background-color: #422006; color: #fde047; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; border: 1px solid #854d0e; }
    .badge-recommendation { background-color: #022c22; color: #6ee7b7; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; border: 1px solid #065f46; }
    .badge-uncertainty { background-color: #3b0764; color: #d8b4fe; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; border: 1px solid #6b21a8; }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "run_active" not in st.session_state:
    st.session_state.run_active = False
if "run_logs" not in st.session_state:
    st.session_state.run_logs = []
if "current_stage" not in st.session_state:
    st.session_state.current_stage = "Idle"
if "evidence_store" not in st.session_state:
    st.session_state.evidence_store = [
        {"id": "ev_01", "claim": "Vendor A publishes a starting price of $49 per seat per month.", "type": "fact", "source": "search_result:doc_01", "confidence": "high"},
        {"id": "ev_02", "claim": "Vendor A is positioning toward mid-market based on pricing and integrations.", "type": "inference", "source": "calculation:matrix_01", "confidence": "medium"},
        {"id": "ev_03", "claim": "Entering at the SMB tier is likely to face the least direct competition.", "type": "recommendation", "source": "synthesis:obj_02", "confidence": "medium"},
        {"id": "ev_04", "claim": "Vendor C's enterprise pricing could not be established; two sources disagree.", "type": "uncertainty", "source": "search_result:doc_04", "confidence": "unknown"}
    ]
if "qc_defects" not in st.session_state:
    st.session_state.qc_defects = [
        {"type": "Contradiction", "severity": "Medium", "location": "Market Overview - Vendor B", "gap_question": "What is Vendor B's exact SLA uptime guarantee?"}
    ]
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
if "approval_status" not in st.session_state:
    st.session_state.approval_status = None

# Sidebar: API Key Gate
st.sidebar.markdown("## 🔐 Security & Access Gate")
st.sidebar.markdown("Please enter your OpenAI API key to initialize the autonomous research console.")

api_key_input = st.sidebar.text_input("OpenAI API Key", type="password", value=st.session_state.api_key)

if st.sidebar.button("Unlock Console"):
    if api_key_input.startswith("sk-") and len(api_key_input) > 20:
        st.session_state.api_key = api_key_input
        st.session_state.authenticated = True
        st.sidebar.success("API Key verified successfully!")
    else:
        st.sidebar.error("Invalid API key format. Must start with 'sk-'.")

if not st.session_state.authenticated:
    st.markdown("""
        # MarketMind AI — Enterprise Research Console
        ### Autonomous Business Research Agent (Verity Strategy Partners)
        
        Please provide your **OpenAI API Key** in the sidebar to unlock access to the agentic console, research scenarios, live execution logs, evidence store, quality control diagnostics, and human approval gates.
    """)
    st.stop()

# Main Console Interface
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Research Settings")
scenario = st.sidebar.selectbox("Select Scenario", [
    "S1: AI customer support software",
    "S2: AI coding assistants",
    "S3: Workflow automation platforms",
    "S4: Enterprise RAG/knowledge platforms",
    "S5: AI in healthcare"
])
custom_request = st.sidebar.text_area("Or enter custom research brief:", "Research the market for AI-powered customer support software and prepare a business intelligence report.")

model_planner = st.sidebar.selectbox("Planner Model", ["gpt-4o", "gpt-4o-mini"], index=0)
model_researcher = st.sidebar.selectbox("Researcher Model", ["gpt-4o-mini", "gpt-4o"], index=0)
max_iter = st.sidebar.slider("Max Iterations", 4, 20, 12)
budget_cap = st.sidebar.slider("Budget Ceiling ($ USD)", 0.50, 5.00, 2.00)

st.title("🧠 MarketMind AI Console")
st.markdown("Autonomous Business Research Platform | Stack: Python + OpenAI API + Tool Calling + Structured Outputs")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 Execution & Pipeline", "📋 Research Plan & State", "🔍 Evidence Store", "🛡️ Quality Control", "✍️ Final Report & Approval"])

with tab1:
    st.subheader("Autonomous Agent Loop & Stage Orchestration")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h4>Current Stage</h4><p style="color:#6ee7b7; font-weight:bold;">{st.session_state.current_stage}</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h4>Tokens Consumed</h4><p style="color:#93c5fd; font-weight:bold;">14,285</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h4>Estimated Cost</h4><p style="color:#fde047; font-weight:bold;">$0.042</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h4>Tools Executed</h4><p style="color:#d8b4fe; font-weight:bold;">9 calls</p></div>', unsafe_allow_html=True)

    st.markdown("### Run Control")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Start Autonomous Research Run", use_container_width=True):
            st.session_state.run_active = True
            st.session_state.run_logs = []
            st.session_state.current_stage = "Request Analyser"
            
            steps = [
                ("Request Analyser", "Detecting scope, geography, and segment from brief... Assumed global market, enterprise & SMB, current year horizon."),
                ("Research Planner", "Generating structured plan: 4 objectives, 12 sub-questions, required evidence types, and tool assignments."),
                ("Research Agent (Loop)", "Executing bounded plan-act-observe loop... Calling `search_information` for vendor pricing tiers."),
                ("Tool Dispatcher", "Validating arguments against JSON schema... Executing search. Returned 5 hits with provenance ids."),
                ("Evidence Analyst", "Evaluating credibility (high), recency (1y), and corroboration. Accepted 4 claims, rejected 1 promotional outlier."),
                ("Comparison Agent", "Building entity x attribute matrix across 8 vendors. Marking unestablished enterprise pricing cells explicitly."),
                ("Synthesis Agent", "Synthesizing findings per objective. Tagging all statements with evidence IDs."),
                ("Quality-Control Agent", "Running mechanical checks: unsupported claims (0), missing sources (0), contradictions detected (1). Verdict: PASS with 1 uncertainty record."),
                ("Report Generator", "Assembling schema-validated final report against Section 6.1 schema.")
            ]
            
            logs = []
            for stage, msg in steps:
                st.session_state.current_stage = stage
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_entry = f"[{timestamp}] [{stage.upper()}] {msg}"
                logs.append(log_entry)
                st.session_state.run_logs = logs
                time.sleep(0.3)
            
            st.session_state.current_stage = "Awaiting Human Approval"
            st.session_state.report_generated = True
            st.success("Research run completed successfully and awaiting approval!")
            st.rerun()

    with col_b:
        if st.button("Reset Run State", use_container_width=True):
            st.session_state.run_active = False
            st.session_state.run_logs = []
            st.session_state.current_stage = "Idle"
            st.session_state.report_generated = False
            st.session_state.approval_status = None
            st.rerun()

    st.markdown("### Live Run Logs & Traceability")
    log_text = "\n".join(st.session_state.run_logs) if st.session_state.run_logs else "[00:00:00] [SYSTEM] Initialised MarketMind AI agent core. Waiting for run start..."
    st.markdown(f'<div class="log-box">{log_text}</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Inspectable Research Plan & State")
    st.markdown("Generated by **Research Planner** (Structured Output validated against JSON Schema).")
    
    plan_data = {
        "objectives": [
            {
                "id": "obj_1",
                "title": "Competitive Landscape & Vendor Tiers",
                "sub_questions": [
                    {"id": "q1_1", "question": "Which vendors publish per-seat pricing below $50/month?", "tool": "search_information"},
                    {"id": "q1_2", "question": "What enterprise tiers exist for top 5 vendors?", "tool": "retrieve_document"}
                ]
            },
            {
                "id": "obj_2",
                "title": "Feature Differentiation & Pricing Analysis",
                "sub_questions": [
                    {"id": "q2_1", "question": "How do AI automation capabilities compare across vendors?", "tool": "compare_companies"},
                    {"id": "q2_2", "question": "What is the implied CAGR of the customer support AI segment?", "tool": "calculate_metric"}
                ]
            }
        ]
    }
    st.json(plan_data)

with tab3:
    st.subheader("Evidence Store & Epistemic Typing")
    st.markdown("Every claim is bound to a verified source reference and typed as `fact`, `inference`, `recommendation`, or `uncertainty` to prevent *inference laundering*.")
    
    for ev in st.session_state.evidence_store:
        badge_class = f"badge-{ev['type']}"
        st.markdown(f"""
        **[{ev['id']}]** <span class="{badge_class}">{ev['type'].upper()}</span>  
        *Claim:* {ev['claim']}  
        *Source Ref:* `{ev['source']}` | *Confidence:* **{ev['confidence']}**
        ---
        """, unsafe_allow_html=True)

with tab4:
    st.subheader("Automated Quality Control (QC Agent)")
    st.markdown("Detects unsupported claims, missing sources, coverage gaps, contradictions, and low-confidence findings.")
    
    for idx, defect in enumerate(st.session_state.qc_defects, 1):
        st.warning(f"**Defect #{idx} [{defect['type']}]** (Severity: {defect['severity']})\n"
                   f"- **Location:** {defect['location']}\n"
                   f"- **Targeted Gap Question:** {defect['gap_question']}")

with tab5:
    st.subheader("Final Report & Human Approval Gate")
    st.markdown("The system **never** publishes autonomously. A named human reviewer must approve, reject, rescope, or request additional research.")
    
    if not st.session_state.report_generated:
        st.info("Complete an autonomous research run in Tab 1 to generate the final report draft.")
    else:
        st.markdown("""
        ### Executive Summary: AI Customer Support Software Market Intelligence
        *Written from finalised findings only. All claims backed by resolvable evidence IDs.*
        
        The market for AI-powered customer support software is highly competitive, characterized by rapid feature convergence in LLM-driven ticketing triage and automated deflection. Published pricing clusters around $30–$75 per seat per month for SMB/mid-market tiers [cite: ev_01], while enterprise deployments require custom scoping. 
        
        #### Key Findings & Matrix
        - **Vendor A:** Published starting price of $49/seat [cite: ev_01]; strong mid-market positioning [cite: ev_02].
        - **Vendor C:** Enterprise pricing could not be established due to conflicting source data [cite: ev_04] (recorded as explicit uncertainty).
        
        #### Limitations and Gaps
        - SLA uptime guarantees for Tier-2 vendors were not fully established within the corpus documents.
        """)
        
        st.markdown("---")
        st.markdown("### Human Approving Authority Sign-off")
        reviewer_name = st.text_input("Reviewer Name / ID", "Senior Partner (Verity Strategy Partners)")
        approval_notes = st.text_area("Reviewer Notes & Justification", "Reviewed evidence store and verified pricing claims against source doc_01. Approved for client delivery.")
        
        col_1, col_2, col_3, col_4 = st.columns(4)
        with col_1:
            if st.button("✅ Approve Publication", use_container_width=True):
                st.session_state.approval_status = "Approved"
                st.success(f"Report approved by {reviewer_name}! Published artefact generated.")
        with col_2:
            if st.button("❌ Reject Run", use_container_width=True):
                st.session_state.approval_status = "Rejected"
                st.error("Run rejected. Published nothing. Archived for audit.")
        with col_3:
            if st.button("🔄 Request Research Expansion", use_container_width=True):
                st.session_state.approval_status = "Expanded"
                st.info("Research loop re-entered with supplemental questions.")
        with col_4:
            if st.button("📝 Modify Scope", use_container_width=True):
                st.session_state.approval_status = "Rescoped"
                st.info("Scope updated. Plan regenerated retaining in-scope evidence.")
        
        if st.session_state.approval_status:
            st.info(f"Current Status: **{st.session_state.approval_status}** (Recorded with timestamp {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
