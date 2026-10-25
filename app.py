import streamlit as st
import json
from scanner.scanner import audit_target

# Page Configuration
st.set_page_config(
    page_title="DevSite Auditor | Security Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for Cyberpunk / Security Theme Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    .reportview-container {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("🛡️ DevSite Auditor Pro")
st.markdown("Advanced automated security intelligence tool for developers. Inspect headers, cookies, and exposed configurations instantly.")
st.divider()

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Audit Controls")
    target_url = st.text_input("Target URL", "https://example.com")
    run_btn = st.button("🚀 Run Security Audit", type="primary", use_container_width=True)
    
    st.divider()
    st.markdown("### 🔍 About Modules")
    st.markdown("- **Security Headers:** Checks CSP, HSTS, X-Frame-Options, etc.")
    st.markdown("- **Cookie Security:** Analyzes HttpOnly & Secure flags.")
    st.markdown("- **Sensitive Files:** Probes for exposed `.env` or `.git` paths.")

# Main Application Logic
if run_btn:
    if not target_url:
        st.warning("⚠️ Please enter a valid URL first.")
    else:
        with st.spinner(f"⚡ Probing and analyzing {target_url}..."):
            report = audit_target(target_url)
            
        if "error" in report:
            st.error(f"❌ Failed to connect to target: {report['error']}")
        else:
            st.success("✅ Audit analysis complete!")
            
            # Top-Level Scorecard Metrics
            col1, col2, col3, col4 = st.columns(4)
            score = report["score"]
            
            grade = "A+" if score >= 90 else ("B" if score >= 75 else "C/F")
            grade_color = "green" if score >= 90 else ("orange" if score >= 75 else "red")
            
            col1.metric("Security Score", f"{score} / 100")
            col2.metric("Rating Grade", grade)
            col3.metric("Target Analyzed", report["url"])
            col4.download_button(
                label="📥 Export JSON Report",
                data=json.dumps(report, indent=4),
                file_name="security_audit_report.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.divider()
            
            # Detailed Breakdown Tabs
            tab1, tab2, tab3 = st.tabs(["🔒 Security Headers", "🍪 Cookie Auditor", "📁 Sensitive Files"])
            
            with tab1:
                st.subheader("HTTP Response Headers Inspection")
                for header, data in report["headers"].items():
                    if data["status"] == "Pass":
                        st.success(f"**{header}**\n* Status: Pass\n* Value: `{data['value']}`\n* Protection: {data['desc']}")
                    else:
                        st.error(f"**{header}**\n* Status: Missing\n* Purpose: {data['desc']}\n* 💡 *Remediation: Add this header to your server configuration to prevent attacks.*")
                        
            with tab2:
                st.subheader("Session & Authentication Cookie Analysis")
                if report["cookies"]:
                    for cname, cdata in report["cookies"].items():
                        if cdata["secure"]:
                            st.info(f"Cookie **{cname}**: Securely configured with proper flags.")
                        else:
                            st.warning(f"Cookie **{cname}** Vulnerability Risks: {', '.join(cdata['issues'])}\n* 💡 *Remediation: Ensure HttpOnly and Secure flags are enabled on session cookies.*")
                else:
                    st.info("ℹ️ No session or auth cookies detected in the initial response headers.")
                    
            with tab3:
                st.subheader("Exposed Sensitive Files & Directory Probing")
                for path, pdata in report["files"].items():
                    if "CRITICAL" in pdata["status"]:
                        st.error(f"🚨 Path **{path}**: {pdata['status']}\n* 💡 *Remediation: Restrict public access immediately! Do not leave environment files or git repositories exposed on production servers.*")
                    else:
                        st.info(f"🛡️ Path **{path}**: {pdata['status']}")
else:
    st.info("👈 Enter a target URL in the sidebar and click **Run Security Audit** to begin.")
