#!/usr/bin/env python3
import streamlit as st
import time
from datetime import datetime, timedelta
from enum import Enum

# Simple data models
class SeverityLevel(Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"

class IncidentStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

class Incident:
    def __init__(self, id, title, description, severity, status, affected_system, user_group, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.severity = severity
        self.status = status
        self.affected_system = affected_system
        self.user_group = user_group
        self.created_at = created_at

# Sample data
def get_sample_incidents():
    return [
        Incident("INC-001", "Email server slow response", "Users reporting slow email delivery", 
                SeverityLevel.P2, IncidentStatus.OPEN, "prod-mail-01", "Sales Team", datetime.now() - timedelta(hours=2)),
        Incident("INC-002", "Database connection timeout", "Application experiencing timeouts", 
                SeverityLevel.P1, IncidentStatus.OPEN, "prod-db-01", "All Users", datetime.now() - timedelta(hours=1)),
        Incident("INC-003", "Web server high CPU", "High CPU utilization detected", 
                SeverityLevel.P3, IncidentStatus.IN_PROGRESS, "prod-web-01", "External Users", datetime.now() - timedelta(minutes=30)),
        Incident("INC-004", "Email delivery failure", "Messages not being delivered", 
                SeverityLevel.P2, IncidentStatus.OPEN, "prod-mail-01", "Marketing Team", datetime.now() - timedelta(minutes=45)),
        Incident("INC-005", "Database slow queries", "Queries taking longer than usual", 
                SeverityLevel.P3, IncidentStatus.OPEN, "prod-db-01", "Development Team", datetime.now() - timedelta(minutes=15))
    ]

def get_sample_metrics():
    return {
        "cpu_utilization": [{"timestamp": datetime.now().isoformat(), "value": 75.2}],
        "memory_usage": [{"timestamp": datetime.now().isoformat(), "value": 82.5}],
        "disk_usage": [{"timestamp": datetime.now().isoformat(), "value": 91.3}]
    }

# Simple correlation logic
def find_similar_incidents(target, incidents):
    similar = []
    for inc in incidents:
        if inc.id != target.id and inc.affected_system == target.affected_system:
            score = 0.8 if "email" in target.title.lower() and "email" in inc.title.lower() else 0.6
            similar.append({"incident": inc, "similarity_score": score, "reasoning": f"Same system: {inc.affected_system}"})
    return similar

st.set_page_config(page_title="AI-Powered ITSM", page_icon="🤖", layout="wide")

def main():
    st.title("🤖 AI-Powered ITSM Solution")
    st.markdown("*Autonomous agents with predictive analytics for intelligent IT service management*")
    
    # Initialize session state
    if 'incidents' not in st.session_state:
        st.session_state.incidents = get_sample_incidents()
    if 'metrics' not in st.session_state:
        st.session_state.metrics = get_sample_metrics()
    
    # Sidebar navigation
    st.sidebar.title("🛠️ Navigation")
    page = st.sidebar.selectbox("Select Demo:", ["Dashboard", "Correlation", "Monitoring", "Problem Management"])
    
    if page == "Dashboard":
        dashboard()
    elif page == "Correlation":
        correlation_demo()
    elif page == "Monitoring":
        monitoring_demo()
    elif page == "Problem Management":
        problem_demo()

def dashboard():
    st.header("📈 AI-Powered ITSM Dashboard")
    
    incidents = st.session_state.incidents
    total = len(incidents)
    open_inc = len([i for i in incidents if i.status in [IncidentStatus.OPEN, IncidentStatus.IN_PROGRESS]])
    critical = len([i for i in incidents if i.severity == SeverityLevel.P1])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Incidents", total)
    col2.metric("Open Incidents", open_inc)
    col3.metric("Critical (P1)", critical)
    col4.metric("Problems Created", 2)
    
    st.subheader("🤖 Agent Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔗 Correlation Agent**")
        st.metric("Decisions Made", 12)
        st.metric("Autonomous Actions", 8)
    
    with col2:
        st.markdown("**📊 Monitoring Agent**")
        st.metric("Alerts Generated", 5)
        st.metric("Top Issues", 3)
    
    with col3:
        st.markdown("**🔍 Problem Agent**")
        st.metric("Problems Created", 2)
        st.metric("Patterns Analyzed", 7)

def correlation_demo():
    st.header("🔗 Incident Correlation Agent")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Incident Analysis")
        incidents = st.session_state.incidents
        
        options = {f"{inc.id}: {inc.title}": inc for inc in incidents}
        selected = st.selectbox("Select incident:", list(options.keys()))
        target = options[selected]
        
        st.markdown(f"**ID:** {target.id}")
        st.markdown(f"**Title:** {target.title}")
        st.markdown(f"**System:** {target.affected_system}")
        
        if st.button("🔍 Analyze Correlations"):
            with st.spinner("Analyzing correlations..."):
                time.sleep(2)
                similar = find_similar_incidents(target, incidents)
                st.session_state.correlation_result = similar
    
    with col2:
        st.subheader("Correlation Results")
        if hasattr(st.session_state, 'correlation_result'):
            similar = st.session_state.correlation_result
            
            if similar:
                st.success(f"Found {len(similar)} similar incidents")
                st.markdown(f"**Score:** {similar[0]['similarity_score']:.2f}")
                st.markdown("**Decision:** GROUP_INCIDENTS")
                st.markdown("**Confidence:** HIGH")
                st.success("✅ Action executed autonomously")
                
                with st.expander("Similar Incidents"):
                    for item in similar:
                        st.markdown(f"- **{item['incident'].id}**: {item['similarity_score']:.2f}")
                        st.markdown(f"  *{item['reasoning']}*")
            else:
                st.info("No similar incidents found")

def monitoring_demo():
    st.header("📊 Proactive Monitoring Agent")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Metrics")
        metrics = st.session_state.metrics
        
        for name, data in metrics.items():
            if data:
                current_val = data[0]['value']
                if current_val > 85:
                    st.error(f"🔴 {name.replace('_', ' ').title()}: {current_val:.1f}%")
                elif current_val > 75:
                    st.warning(f"🟡 {name.replace('_', ' ').title()}: {current_val:.1f}%")
                else:
                    st.success(f"🟢 {name.replace('_', ' ').title()}: {current_val:.1f}%")
        
        if st.button("🔍 Run Proactive Analysis"):
            with st.spinner("Running analysis..."):
                time.sleep(3)
                st.session_state.monitoring_done = True
    
    with col2:
        st.subheader("Top 3 Issues")
        if hasattr(st.session_state, 'monitoring_done'):
            st.markdown("**#1 🔴 MON-001**")
            st.markdown("Severity: 91% | Confidence: HIGH")
            st.success("✅ Autonomous action taken")
            
            st.markdown("**#2 🟡 MON-002**")
            st.markdown("Severity: 82% | Confidence: MEDIUM")
            st.warning("⚠️ Human review required")
            
            with st.expander("Details - Issue #1"):
                st.markdown("**Reasoning:** Disk usage at 91.3% exceeds threshold (85%)")
                st.markdown("**Business Impact:** High - Storage capacity critical")
                st.markdown("**Recommended Actions:**")
                st.markdown("- Clean up temporary files and logs")
                st.markdown("- Archive old data to secondary storage")

def problem_demo():
    st.header("🔍 Problem Management Agent")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pattern Analysis")
        incidents = st.session_state.incidents
        st.info(f"Analyzing {len(incidents)} incidents for patterns...")
        
        if st.button("🔍 Analyze Incident Patterns"):
            with st.spinner("Analyzing patterns..."):
                time.sleep(3)
                st.session_state.patterns_found = True
                st.success("Found 2 significant patterns")
    
    with col2:
        st.subheader("Problem Creation Decisions")
        if hasattr(st.session_state, 'patterns_found'):
            st.markdown("**Pattern #1: System**")
            st.markdown("Key: prod-mail-01 | Incidents: 2")
            st.markdown("Confidence: 0.85")
            st.success("✅ Problem creation recommended")
            st.info("🤖 Executed autonomously")
            
            if st.button("🔄 Create Problem #1"):
                st.success("Created problem: PRB-001")
                st.balloons()
            
            with st.expander("Pattern Details #1"):
                st.markdown("**Description:** Multiple incidents affecting prod-mail-01")
                st.markdown("**Root Cause Hypothesis:** Underlying infrastructure issue with prod-mail-01")
                st.markdown("**Preventive Measures:**")
                st.markdown("- Conduct comprehensive health check of prod-mail-01")
                st.markdown("- Review prod-mail-01 configuration and capacity planning")

if __name__ == "__main__":
    main()