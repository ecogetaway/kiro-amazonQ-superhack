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
    # Header with emojis and colors
    st.markdown("# 🤖 AI-Powered ITSM Solution")
    st.markdown("### *Autonomous agents with predictive analytics for intelligent IT service management*")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.markdown("# 🛠️ Navigation")
    page = st.sidebar.radio("Select Demo:", ["🏠 Dashboard", "🔗 Correlation", "📊 Monitoring", "🔍 Problem Management", "📚 Knowledge Base"])
    
    # Initialize session state
    if 'incidents' not in st.session_state:
        st.session_state.incidents = get_incidents()
    if 'metrics' not in st.session_state:
        st.session_state.metrics = get_metrics()
    if 'knowledge_agent' not in st.session_state:
        st.session_state.knowledge_agent = "initialized"  # Simplified for demo
    

    
    # Route to pages
    if page == "🏠 Dashboard":
        dashboard()
    elif page == "🔗 Correlation":
        correlation_page()
    elif page == "📊 Monitoring":
        monitoring_page()
    elif page == "🔍 Problem Management":
        problem_page()
    elif page == "📚 Knowledge Base":
        knowledge_page()

def dashboard():
    st.markdown("## 📈 Dashboard Overview")
    
    # Key metrics using Streamlit's metric component
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Incidents", "5", delta="2 today")
    
    with col2:
        st.metric("🔓 Open Incidents", "4", delta="-1 resolved")
    
    with col3:
        st.metric("🚨 Critical (P1)", "1", delta="0 new")
    
    with col4:
        st.metric("📚 Knowledge Articles", "3", delta="1 auto-created")
    
    st.markdown("---")
    
    # Agent status using containers and columns
    st.markdown("## 🤖 Agent Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("### 🔗 Correlation Agent")
            st.success("🟢 Status: Active")
            st.metric("Decisions Made", "12")
            st.metric("Autonomous Actions", "8")
            st.metric("Accuracy", "94%")
    
    with col2:
        with st.container():
            st.markdown("### 📊 Monitoring Agent")
            st.success("🟢 Status: Active")
            st.metric("Alerts Generated", "5")
            st.metric("Predictions Made", "3")
            st.metric("Accuracy", "91%")
    
    with col3:
        with st.container():
            st.markdown("### 📚 Knowledge Agent")
            st.success("🟢 Status: Active")
            st.metric("Articles Available", "3")
            st.metric("Auto-Generated", "3")
            st.metric("Avg Effectiveness", "80%")
    
    # Recent activity using info/warning/error boxes
    st.markdown("## 🕒 Recent Activity")
    
    st.info("🔗 **Latest Correlation:** GROUP_INCIDENTS (High Confidence) - 2 minutes ago")
    st.warning("📊 **Top Alert:** MON-001 (Severity: 91%) - 5 minutes ago")
    st.info("📚 **Knowledge Created:** KB-004 auto-generated from PRB-001 - 5 minutes ago")

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
            
            # Use expander for incident details
            with st.expander("📄 Incident Details", expanded=True):
                st.write(f"**ID:** {incident['id']}")
                st.write(f"**Title:** {incident['title']}")
                st.write(f"**System:** {incident['system']}")
                st.write(f"**Severity:** {incident['severity']}")
                st.write(f"**Status:** {incident['status']}")
            
            if st.button("🔍 Analyze Correlations", type="primary"):
                with st.spinner("🤖 AI analyzing incident correlations..."):
                    time.sleep(2)
                    st.session_state.correlation_done = True
    
    with col2:
        st.markdown("### 📊 Correlation Results")
        
        if hasattr(st.session_state, 'correlation_done'):
            st.success("✅ **Analysis Complete**")
            
            # Use metrics for results
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Similar Incidents", "2")
                st.metric("Correlation Score", "0.87")
            with col_b:
                st.metric("Decision", "GROUP_INCIDENTS")
                st.metric("Confidence", "HIGH")
            
            st.success("✅ **Action:** Executed Autonomously")
            
            st.markdown("#### 🔗 Similar Incidents")
            st.write("• **INC-004**: 0.92 similarity (same system: prod-mail-01)")
            st.write("• **INC-001**: 0.82 similarity (similar symptoms: email issues)")
            
            st.warning("⚠️ **Escalation Risk:** 75% probability based on historical patterns")

def monitoring_page():
    st.markdown("## 📊 Proactive Monitoring Agent")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📈 Current Metrics")
        
        metrics = st.session_state.metrics
        
        for name, value in metrics.items():
            if value > 85:
                st.error(f"🔴 **{name}**: {value:.1f}%")
            elif value > 75:
                st.warning(f"🟡 **{name}**: {value:.1f}%")
            else:
                st.success(f"🟢 **{name}**: {value:.1f}%")
        
        if st.button("🔍 Run Proactive Analysis", type="primary"):
            with st.spinner("🤖 AI analyzing system metrics..."):
                time.sleep(3)
                st.session_state.monitoring_done = True
    
    with col2:
        st.markdown("### 🚨 Top 3 Issues")
        
        if hasattr(st.session_state, 'monitoring_done'):
            # Issue #1
            with st.container():
                st.error("🔴 **#1 Critical Issue - MON-001**")
                st.write("**Metric:** Disk Usage (91.3%)")
                st.write("**Severity:** 91% | **Confidence:** HIGH")
                st.success("✅ **Action:** Autonomous cleanup initiated")
                st.write("**Business Impact:** High - Storage capacity critical")
            
            st.markdown("---")
            
            # Issue #2
            with st.container():
                st.warning("🟡 **#2 Warning - MON-002**")
                st.write("**Metric:** Memory Usage (82.5%)")
                st.write("**Severity:** 82% | **Confidence:** MEDIUM")
                st.info("⚠️ **Action:** Human review scheduled")
                st.write("**Business Impact:** Medium - Performance may degrade")
            
            st.markdown("#### 🔮 Predictive Analysis")
            st.info("• **Disk Usage** will reach 95% in **2.3 hours**")
            st.info("• **Memory Usage** trending upward, threshold in **4.1 hours**")
            st.success("• **CPU Utilization** stable, no immediate concerns")

def problem_page():
    st.markdown("## 🔍 Problem Management Agent")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔍 Pattern Analysis")
        
        with st.container():
            st.markdown("#### 📊 Analysis Scope")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Incidents", "5")
            with col_b:
                st.metric("Time Window", "24h")
            with col_c:
                st.metric("Systems", "3")
        
        if st.button("🔍 Analyze Incident Patterns", type="primary"):
            with st.spinner("🤖 AI analyzing incident patterns..."):
                time.sleep(3)
                st.session_state.patterns_done = True
    
    with col2:
        st.markdown("### 📋 Problem Creation Decisions")
        
        if hasattr(st.session_state, 'patterns_done'):
            st.success("✅ **Pattern #1: System Pattern**")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Key", "prod-mail-01")
                st.metric("Incidents", "2")
            with col_b:
                st.metric("Confidence", "0.85")
                st.success("🤖 Autonomous")
            
            if st.button("🔄 Create Problem Record", type="primary"):
                st.success("✅ Created problem: PRB-002")
                st.balloons()
            
            with st.expander("🔧 Root Cause Analysis"):
                st.write("**Hypothesis:** Underlying infrastructure issue with prod-mail-01 causing recurring failures")
                st.write("**Preventive Measures:**")
                st.write("• Conduct comprehensive health check of prod-mail-01")
                st.write("• Review configuration and capacity planning")
                st.write("• Implement enhanced monitoring")
                st.write("• Schedule preventive maintenance window")
    
    # Show created problems
    st.markdown("---")
    st.markdown("### 📋 Created Problems")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🔍 PRB-001", expanded=True):
            st.write("**Title:** Recurring email server issues")
            st.write("**Status:** Investigating")
            st.write("**Priority:** Critical")
            st.write("**Related Incidents:** 2")
            st.success("**Auto Created:** Yes")
    
    with col2:
        with st.expander("🔍 PRB-002", expanded=True):
            st.write("**Title:** Database performance degradation")
            st.write("**Status:** New")
            st.write("**Priority:** High")
            st.write("**Related Incidents:** 2")
            st.success("**Auto Created:** Yes")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 Hackathon Demo")
st.sidebar.markdown("**AI-Powered ITSM Solution**")
st.sidebar.markdown("*Autonomous agents working together*")

st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Uptime", "99.9%", delta="0.1%")
st.sidebar.metric("Incidents Processed", "156", delta="12 today")
st.sidebar.metric("Knowledge Articles", "3", delta="1 created today")

# Add knowledge base integration hints to existing pages
def add_knowledge_integration():
    """Add knowledge base suggestions to correlation and monitoring results"""
    pass

def knowledge_page():
    st.markdown("## 📚 Knowledge Base Agent")
    
    # Knowledge base search
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔍 Search Knowledge Base")
        
        search_query = st.text_input("Search for solutions:", placeholder="e.g., email slow, database timeout")
        
        if search_query:
            # Simulate knowledge search results
            st.success("✅ Found 3 relevant articles")
            
            with st.expander("📝 #1 Email Server Slow Response - Memory Leak Fix", expanded=True):
                st.write("**Type:** Solution | **Effectiveness:** 90% | **Usage:** 15 times")
                st.markdown("---")
                st.markdown("""
                **Problem:** Email server experiencing slow response times
                
                **Root Cause:** Memory leak in email service process
                
                **Solution:**
                1. Restart email service: `sudo systemctl restart postfix`
                2. Clear memory cache: `sudo sync && echo 3 > /proc/sys/vm/drop_caches`
                3. Monitor memory usage: `free -h`
                
                **Prevention:** Schedule weekly service restarts
                """)
                
                if st.button("Use This Solution #1"):
                    st.success("✅ Solution applied! Saved 30 minutes resolution time.")
            
            with st.expander("📝 #2 Database Connection Timeout - Quick Workaround"):
                st.write("**Type:** Workaround | **Effectiveness:** 70% | **Usage:** 8 times")
                st.markdown("**Quick Fix:** Increase connection pool size and restart app servers")
    
    with col2:
        st.markdown("### 🤖 AI-Powered Suggestions")
        
        incidents = st.session_state.incidents
        incident_options = [f"{inc['id']}: {inc['title']}" for inc in incidents]
        selected_incident = st.selectbox("Select incident for suggestions:", incident_options)
        
        if selected_incident and st.button("🔍 Get AI Suggestions", type="primary"):
            with st.spinner("🤖 AI analyzing incident for knowledge matches..."):
                time.sleep(2)
                st.session_state.kb_suggestions = True
        
        if hasattr(st.session_state, 'kb_suggestions'):
            st.success("✅ Found 2 suggested solutions")
            
            st.info("💡 **Suggested:** Email Server Slow Response Fix")
            st.write("Relevance: 0.9 | Effectiveness: 90%")
            
            st.info("💡 **Suggested:** High CPU Usage Optimization")
            st.write("Relevance: 0.7 | Effectiveness: 80%")
    
    # Knowledge base metrics
    st.markdown("---")
    st.markdown("### 📊 Knowledge Base Analytics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Articles", "3")
    with col2:
        st.metric("Auto-Generated", "3")
    with col3:
        st.metric("Total Usage", "35")
    with col4:
        st.metric("Avg Effectiveness", "80%")
    
    # Auto-create knowledge demo
    st.markdown("---")
    st.markdown("### 🤖 Auto-Create Knowledge Article")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Simulate resolved incident:**")
        
        resolution_notes = st.text_area(
            "Resolution steps:",
            value="1. Restarted email service\n2. Cleared memory cache\n3. Updated configuration\n4. Verified functionality",
            height=100
        )
        
        if st.button("📄 Auto-Create Knowledge Article", type="primary"):
            with st.spinner("🤖 AI creating knowledge article..."):
                time.sleep(2)
                st.session_state.new_article = True
    
    with col2:
        if hasattr(st.session_state, 'new_article'):
            st.success("✅ Created: KB-004")
            
            with st.expander("📝 Email Server Issues - Resolution Guide", expanded=True):
                st.markdown("""
                **Problem:** Email server slow response
                
                **System Affected:** prod-mail-01
                
                **Resolution Steps:**
                1. Restarted email service
                2. Cleared memory cache
                3. Updated configuration
                4. Verified functionality
                
                **Auto-generated from incident:** INC-001
                """)
                st.write("**Keywords:** email, slow, memory, restart")
                st.write("**Auto-generated:** Yes")

if __name__ == "__main__":
    main()