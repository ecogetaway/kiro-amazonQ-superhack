import streamlit as st
import time
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="AI-Powered ITSM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .agent-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    .success-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .warning-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Sample data
def get_incidents():
    return [
        {"id": "INC-001", "title": "Email server slow response", "system": "prod-mail-01", "severity": "P2", "status": "Open"},
        {"id": "INC-002", "title": "Database connection timeout", "system": "prod-db-01", "severity": "P1", "status": "Open"},
        {"id": "INC-003", "title": "Web server high CPU", "system": "prod-web-01", "severity": "P3", "status": "In Progress"},
        {"id": "INC-004", "title": "Email delivery failure", "system": "prod-mail-01", "severity": "P2", "status": "Open"},
        {"id": "INC-005", "title": "Database slow queries", "system": "prod-db-01", "severity": "P3", "status": "Open"}
    ]

def get_metrics():
    return {
        "CPU Utilization": 75.2,
        "Memory Usage": 82.5,
        "Disk Usage": 91.3,
        "Network Throughput": 45.1
    }

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI-Powered ITSM Solution</h1>
        <p>Autonomous agents with predictive analytics for intelligent IT service management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown("## 🛠️ Navigation")
    page = st.sidebar.selectbox("Select Demo:", ["🏠 Dashboard", "🔗 Correlation", "📊 Monitoring", "🔍 Problem Management"])
    
    # Initialize session state
    if 'incidents' not in st.session_state:
        st.session_state.incidents = get_incidents()
    if 'metrics' not in st.session_state:
        st.session_state.metrics = get_metrics()
    
    # Route to pages
    if page == "🏠 Dashboard":
        dashboard()
    elif page == "🔗 Correlation":
        correlation_page()
    elif page == "📊 Monitoring":
        monitoring_page()
    elif page == "🔍 Problem Management":
        problem_page()

def dashboard():
    st.markdown("## 📈 Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Total Incidents</h3>
            <h2 style="color: #667eea;">5</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🔓 Open Incidents</h3>
            <h2 style="color: #f39c12;">4</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🚨 Critical (P1)</h3>
            <h2 style="color: #e74c3c;">1</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🔍 Problems Created</h3>
            <h2 style="color: #27ae60;">2</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Agent status
    st.markdown("## 🤖 Agent Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="agent-card">
            <h3>🔗 Correlation Agent</h3>
            <p><strong>Status:</strong> <span style="color: green;">🟢 Active</span></p>
            <p><strong>Decisions Made:</strong> 12</p>
            <p><strong>Autonomous Actions:</strong> 8</p>
            <p><strong>Accuracy:</strong> 94%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-card">
            <h3>📊 Monitoring Agent</h3>
            <p><strong>Status:</strong> <span style="color: green;">🟢 Active</span></p>
            <p><strong>Alerts Generated:</strong> 5</p>
            <p><strong>Predictions Made:</strong> 3</p>
            <p><strong>Accuracy:</strong> 91%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="agent-card">
            <h3>🔍 Problem Agent</h3>
            <p><strong>Status:</strong> <span style="color: green;">🟢 Active</span></p>
            <p><strong>Problems Created:</strong> 2</p>
            <p><strong>Patterns Analyzed:</strong> 7</p>
            <p><strong>Auto Creation Rate:</strong> 85%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity
    st.markdown("## 🕒 Recent Activity")
    
    st.markdown("""
    <div class="success-card">
        <strong>🔗 Latest Correlation:</strong> GROUP_INCIDENTS (High Confidence) - 2 minutes ago
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-card">
        <strong>📊 Top Alert:</strong> MON-001 (Severity: 91%) - 5 minutes ago
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-card">
        <strong>🔍 Latest Problem:</strong> PRB-001 (Critical priority) - 10 minutes ago
    </div>
    """, unsafe_allow_html=True)

def correlation_page():
    st.markdown("## 🔗 Incident Correlation Agent")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📋 Incident Analysis")
        
        incidents = st.session_state.incidents
        options = [f"{inc['id']}: {inc['title']}" for inc in incidents]
        selected = st.selectbox("Select incident to analyze:", options)
        
        if selected:
            incident_id = selected.split(":")[0]
            incident = next(inc for inc in incidents if inc['id'] == incident_id)
            
            st.markdown(f"""
            <div class="agent-card">
                <h4>📄 Incident Details</h4>
                <p><strong>ID:</strong> {incident['id']}</p>
                <p><strong>Title:</strong> {incident['title']}</p>
                <p><strong>System:</strong> {incident['system']}</p>
                <p><strong>Severity:</strong> {incident['severity']}</p>
                <p><strong>Status:</strong> {incident['status']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 Analyze Correlations", key="analyze_corr"):
                with st.spinner("🤖 AI analyzing incident correlations..."):
                    time.sleep(2)
                    st.session_state.correlation_done = True
    
    with col2:
        st.markdown("### 📊 Correlation Results")
        
        if hasattr(st.session_state, 'correlation_done'):
            st.markdown("""
            <div class="success-card">
                <h4>✅ Analysis Complete</h4>
                <p><strong>Similar Incidents Found:</strong> 2</p>
                <p><strong>Correlation Score:</strong> 0.87</p>
                <p><strong>Decision:</strong> GROUP_INCIDENTS</p>
                <p><strong>Confidence:</strong> HIGH</p>
                <p><strong>Action:</strong> ✅ Executed Autonomously</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🔗 Similar Incidents")
            st.markdown("""
            - **INC-004**: 0.92 similarity (same system: prod-mail-01)
            - **INC-001**: 0.82 similarity (similar symptoms: email issues)
            """)
            
            st.markdown("""
            <div class="warning-card">
                <strong>⚠️ Escalation Risk:</strong> 75% probability based on historical patterns
            </div>
            """, unsafe_allow_html=True)

def monitoring_page():
    st.markdown("## 📊 Proactive Monitoring Agent")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📈 Current Metrics")
        
        metrics = st.session_state.metrics
        
        for name, value in metrics.items():
            if value > 85:
                color = "#e74c3c"
                icon = "🔴"
            elif value > 75:
                color = "#f39c12"
                icon = "🟡"
            else:
                color = "#27ae60"
                icon = "🟢"
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>{icon} {name}</h4>
                <h2 style="color: {color};">{value:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🔍 Run Proactive Analysis", key="analyze_monitoring"):
            with st.spinner("🤖 AI analyzing system metrics..."):
                time.sleep(3)
                st.session_state.monitoring_done = True
    
    with col2:
        st.markdown("### 🚨 Top 3 Issues")
        
        if hasattr(st.session_state, 'monitoring_done'):
            st.markdown("""
            <div class="warning-card">
                <h4>🔴 #1 Critical Issue - MON-001</h4>
                <p><strong>Metric:</strong> Disk Usage (91.3%)</p>
                <p><strong>Severity:</strong> 91% | <strong>Confidence:</strong> HIGH</p>
                <p><strong>Action:</strong> ✅ Autonomous cleanup initiated</p>
                <p><strong>Business Impact:</strong> High - Storage capacity critical</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="success-card">
                <h4>🟡 #2 Warning - MON-002</h4>
                <p><strong>Metric:</strong> Memory Usage (82.5%)</p>
                <p><strong>Severity:</strong> 82% | <strong>Confidence:</strong> MEDIUM</p>
                <p><strong>Action:</strong> ⚠️ Human review scheduled</p>
                <p><strong>Business Impact:</strong> Medium - Performance may degrade</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🔮 Predictive Analysis")
            st.markdown("""
            - **Disk Usage** will reach 95% in **2.3 hours**
            - **Memory Usage** trending upward, threshold in **4.1 hours**
            - **CPU Utilization** stable, no immediate concerns
            """)

def problem_page():
    st.markdown("## 🔍 Problem Management Agent")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔍 Pattern Analysis")
        
        st.markdown("""
        <div class="agent-card">
            <h4>📊 Analysis Scope</h4>
            <p><strong>Incidents Analyzed:</strong> 5</p>
            <p><strong>Time Window:</strong> Last 24 hours</p>
            <p><strong>Systems Covered:</strong> 3</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Analyze Incident Patterns", key="analyze_patterns"):
            with st.spinner("🤖 AI analyzing incident patterns..."):
                time.sleep(3)
                st.session_state.patterns_done = True
    
    with col2:
        st.markdown("### 📋 Problem Creation Decisions")
        
        if hasattr(st.session_state, 'patterns_done'):
            st.markdown("""
            <div class="success-card">
                <h4>✅ Pattern #1: System Pattern</h4>
                <p><strong>Key:</strong> prod-mail-01</p>
                <p><strong>Incidents:</strong> 2 related incidents</p>
                <p><strong>Confidence:</strong> 0.85</p>
                <p><strong>Decision:</strong> ✅ Problem creation recommended</p>
                <p><strong>Status:</strong> 🤖 Executed autonomously</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Create Problem Record", key="create_problem"):
                st.success("✅ Created problem: PRB-002")
                st.balloons()
            
            st.markdown("#### 🔧 Root Cause Analysis")
            st.markdown("""
            **Hypothesis:** Underlying infrastructure issue with prod-mail-01 causing recurring failures
            
            **Preventive Measures:**
            - Conduct comprehensive health check of prod-mail-01
            - Review configuration and capacity planning
            - Implement enhanced monitoring
            - Schedule preventive maintenance window
            """)
    
    # Show created problems
    st.markdown("---")
    st.markdown("### 📋 Created Problems")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="agent-card">
            <h4>🔍 PRB-001</h4>
            <p><strong>Title:</strong> Recurring email server issues</p>
            <p><strong>Status:</strong> Investigating</p>
            <p><strong>Priority:</strong> Critical</p>
            <p><strong>Related Incidents:</strong> 2</p>
            <p><strong>Auto Created:</strong> Yes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-card">
            <h4>🔍 PRB-002</h4>
            <p><strong>Title:</strong> Database performance degradation</p>
            <p><strong>Status:</strong> New</p>
            <p><strong>Priority:</strong> High</p>
            <p><strong>Related Incidents:</strong> 2</p>
            <p><strong>Auto Created:</strong> Yes</p>
        </div>
        """, unsafe_allow_html=True)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 Hackathon Demo")
st.sidebar.markdown("**AI-Powered ITSM Solution**")
st.sidebar.markdown("Autonomous agents working together")

st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Uptime", "99.9%")
st.sidebar.metric("Incidents Processed", "156")
st.sidebar.metric("Problems Resolved", "23")

if __name__ == "__main__":
    main()