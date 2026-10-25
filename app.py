import streamlit as st
import json
import time
from datetime import datetime
from scanner.scanner import audit_target

# --- Page Configuration ---
st.set_page_config(
    page_title="DevSite Auditor Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling & Cybersecurity Theme ---
st.markdown("""
<style>
    .stApp {
        background-color: #080D18;
        color: #F1F5F9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #0D1423;
        border-right: 1px solid rgba(71, 118, 255, 0.15);
        padding-top: 20px;
    }
    .cyber-card {
        background-color: #111B2D;
        border: 1px solid rgba(71, 118, 255, 0.15);
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .metric-card {
        background-color: #111B2D;
        border: 1px solid rgba(71, 118, 255, 0.15);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #00D4FF;
        margin-top: 6px;
    }
    .metric-label {
        font-size: 13px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .grade-badge-a {
        background-color: rgba(34, 197, 94, 0.15);
        color: #22C55E;
        border: 1px solid #22C55E;
        padding: 6px 16px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 20px;
    }
    .grade-badge-other {
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid #FBBF24;
        padding: 6px 16px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 20px;
    }
    h1, h2, h3 { color: #F1F5F9; font-weight: 600; }
    p, span, label { color: #94A3B8; }
    .stTextInput input {
        background-color: #080D18 !important;
        color: #F1F5F9 !important;
        border: 1px solid rgba(71, 118, 255, 0.3) !important;
        border-radius: 8px !important;
    }
    /* Exact Pure Red Button Matching Your Screenshot */
    .stButton button {
        background: #FF0000 !important;
        color: #FFFFFF !important;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 14px rgba(255, 0, 0, 0.4);
        transition: all 0.2s ease-in-out;
    }
    .stButton button:hover {
        background: #E60000 !important;
        opacity: 1;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Function for Letter Grades ---
def get_grade(score):
    if score >= 90: return "A+"
    elif score >= 80: return "A"
    elif score >= 70: return "B"
    elif score >= 60: return "C"
    elif score >= 50: return "D"
    return "F"

# --- Session State ---
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []
if "current_result" not in st.session_state:
    st.session_state.current_result = None

# --- Sidebar Controls ---
st.sidebar.markdown("""
<div style="margin-bottom: 20px;">
    <h3 style="color: #00D4FF; font-size: 18px; margin-bottom: 4px;">🛡️ Audit Controls</h3>
</div>
""", unsafe_allow_html=True)

target_url = st.sidebar.text_input("Target URL", placeholder="https://example.com")
run_scan_clicked = st.sidebar.button("🚀 Run Security Audit", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 12px; color: #94A3B8;">
    <p style="font-weight: bold; color: #F1F5F9; margin-bottom: 6px;">About Modules</p>
    <p style="margin: 0 0 6px 0;">• <b>Security Headers:</b> Checks CSP, HSTS, X-Frame-Options, etc.</p>
    <p style="margin: 0 0 6px 0;">• <b>Cookie Security:</b> Analyzes HttpOnly & Secure flags.</p>
    <p style="margin: 0;">• <b>Sensitive Files:</b> Probes for exposed .env or .git paths.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 11px; color: #94A3B8;">
    <p style="margin: 0 0 3px 0;">🟢 <b>Status:</b> Operational</p>
    <p style="margin: 0 0 3px 0;">💻 <b>Developer:</b> Waseem Abbas</p>
    <p style="margin: 0;">🐙 <b>GitHub:</b> waseemabbas530</p>
</div>
""", unsafe_allow_html=True)

# --- Handle Scan Execution ---
if run_scan_clicked:
    if not target_url.strip():
        st.error("Please enter a valid target URL in the sidebar.")
    else:
        with st.spinner("Executing multi-vector security audit..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Validating target URL & fetching headers...")
            progress_bar.progress(30)
            time.sleep(0.3)
            
            status_text.text("Auditing cookies & probing sensitive paths...")
            progress_bar.progress(70)
            time.sleep(0.3)
            
            result = audit_target(target_url)
            result["grade"] = get_grade(result.get("score", 0))
            result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            
            st.session_state.current_result = result
            st.session_state.scan_history.insert(0, result)
            st.success(f"Audit completed successfully for {target_url}!")

# --- Main Dashboard Area ---
st.markdown("""
<div>
    <h1 style="font-size: 28px; margin-bottom: 2px;">🛡️ DevSite Auditor Pro</h1>
    <p style="color: #94A3B8; font-size: 14px; margin-bottom: 20px;">Advanced automated security intelligence tool for developers. Inspect headers, cookies, and exposed configurations instantly.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.current_result:
    res = st.session_state.current_result
    score = res.get("score", 0)
    grade = res.get("grade", "F")
    headers = res.get("headers", {})
    cookies = res.get("cookies", {})
    files = res.get("files", {})
    
    passed_headers = sum(1 for h, data in headers.items() if data.get("status") == "Pass")
    total_headers = len(headers)
    
    col_score, col_metrics = st.columns([1, 2])
    
    with col_score:
        st.markdown('<div class="cyber-card" style="text-align: center; height: 100%;">', unsafe_allow_html=True)
        st.markdown("<p class='metric-label'>Security Score</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size: 54px; color: #00D4FF; margin: 10px 0;'>{score}<span style='font-size: 24px; color: #94A3B8;'>/100</span></h1>", unsafe_allow_html=True)
        
        grade_class = "grade-badge-a" if grade in ["A+", "A"] else "grade-badge-other"
        st.markdown(f'<span class="{grade_class}">Grade: {grade}</span>', unsafe_allow_html=True)
        st.markdown("<p style='font-size: 12px; margin-top: 15px; color: #94A3B8;'>Calculated from live header & config inspection</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_metrics:
        st.markdown("#### 📊 Core Metrics")
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Security Headers</div>
                <div class="metric-value">{passed_headers}/{total_headers}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            cookie_count = len([c for c in cookies if c != "info"])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Cookies Audited</div>
                <div class="metric-value">{cookie_count}</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            exposed_files = sum(1 for f, data in files.items() if data.get("exposed"))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Exposed Paths</div>
                <div class="metric-value" style="color: {'#F43F5E' if exposed_files > 0 else '#22C55E'};">{exposed_files}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Audit Status</div>
                <div class="metric-value" style="font-size: 20px; color: #22C55E; margin-top: 10px;">Completed</div>
            </div>
            """, unsafe_allow_html=True)

    tab_headers, tab_cookies, tab_paths, tab_json = st.tabs(["🛡️ Security Headers", "🍪 Cookie Security", "📂 Sensitive Paths", "📄 JSON Export"])
    
    with tab_headers:
        st.markdown("#### HTTP Security Headers Evaluation")
        for header, data in headers.items():
            status = data.get("status")
            status_icon = "✅" if status == "Pass" else "❌"
            color = "#22C55E" if status == "Pass" else "#F43F5E"
            st.markdown(f"""
            <div style="background-color: #0D1423; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid {color};">
                <b>{status_icon} {header}</b> ({data.get('desc')}): <span style="color: #94A3B8;">Status: {status}</span>
            </div>
            """, unsafe_allow_html=True)
            
    with tab_cookies:
        st.markdown("#### Authentication Cookie Analysis")
        if not cookies or ("info" in cookies):
            st.info("No session or authentication cookies detected in initial response.")
        else:
            for c_name, c_data in cookies.items():
                st.markdown(f"""
                <div style="background-color: #0D1423; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px;">
                    <b>🍪 {c_name}</b> — Secure: <code>{c_data.get('secure')}</code> | Issues: {c_data.get('issues')}
                </div>
                """, unsafe_allow_html=True)
                
    with tab_paths:
        st.markdown("#### Sensitive File & Directory Probing")
        for path, p_data in files.items():
            exposed = p_data.get('exposed', False)
            color = "#F43F5E" if exposed else "#22C55E"
            st.markdown(f"""
            <div style="background-color: #0D1423; padding: 10px 16px; border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between;">
                <span><code>{path}</code></span>
                <span style="color: {color}; font-weight: bold;">{p_data.get('status')}</span>
            </div>
            """, unsafe_allow_html=True)
            
    with tab_json:
        st.markdown("#### Raw Audit Report (JSON)")
        json_str = json.dumps(res, indent=4)
        st.download_button(
            label="📥 Download Full JSON Report",
            data=json_str,
            file_name=f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        st.code(json_str, language="json")

else:
    st.markdown("""
    <div class="cyber-card" style="text-align: center; padding: 30px;">
        <p style="color: #00D4FF; font-size: 15px; margin: 0;">👉 Enter a target URL in the sidebar and click <b>Run Security Audit</b> to begin.</p>
    </div>
    """, unsafe_allow_html=True)
