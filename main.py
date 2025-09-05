#!/usr/bin/env python3
import streamlit as st
import time
from datetime import datetime
from src.agents.correlation_agent import AutonomousCorrelationAgent
from src.agents.monitoring_agent import AutonomousMonitoringAgent
from src.agents.problem_agent import AutonomousProblemAgent
from src.data.loader import DataLoader
from src.models.incident import Incident, SeverityLevel, IncidentStatus
from src.models.problem import Problem, ProblemStatus, ProblemPriority

st.set_page_config(page_title="AI-Powered ITSM", page_icon="🤖", layout="wide")

def init():
    if 'correlation_agent' not in st.session_state:
        st.session_state.correlation_agent = AutonomousCorrelationAgent()
        st.session_state.correlation_agent.initialize_model()
    if 'monitoring_agent' not in st.session_state:
        st.session_state.monitoring_agent = AutonomousMonitoringAgent()
    if 'problem_agent' not in st.session_state:
        st.session_state.problem_agent = AutonomousProblemAgent()
    if 'data_loader' not in st.session_state:
        st.session_state.data_loader = DataLoader()

def correlation_demo():
    st.header("🔗 Incident Correlation Agent")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Incident Analysis")
        incidents = st.session_state.data_loader.load_incidents()
        if not incidents:
            st.error("No data")
            return
        
        options = {f"{inc.id}: {inc.title}": inc for inc in incidents[:5]}
        selected = st.selectbox("Select incident:", list(options.keys()))
        target = options[selected]
        
        st.markdown(f"**ID:** {target.id}\n**Title:** {target.title}\n**System:** {target.affected_system}")
        
        if st.button("🔍 Analyze Correlations"):
            with st.spinner("Analyzing correlations..."):
                time.sleep(2)
                similar = st.session_state.correlation_agent.find_similar_incidents(target, incidents)
                result = st.session_state.correlation_agent.make_correlation_decision(target, similar)
                
                st.session_state.correlation_result = result
                st.session_state.similar_incidents = similar
    
    with col2:
        st.subheader("Correlation Results")
        if hasattr(st.session_state, 'correlation_result'):
            result = st.session_state.correlation_result
            similar = st.session_state.similar_incidents
            
            if similar:
                st.success(f"Found {len(similar)} similar incidents")
                st.markdown(f"**Score:** {result.correlation_score:.2f}\n**Decision:** {result.decision.value}")
                st.markdown(f"**Confidence:** {result.confidence_level.value}")
                
                if result.auto_executed:
                    st.success("✅ Action executed autonomously")
                else:
                    st.warning("⚠️ Human review required")
                
                with st.expander("Similar Incidents"):
                    for item in similar[:3]:
                        st.markdown(f"- **{item['incident'].id}**: {item['similarity_score']:.2f}")
                        st.markdown(f"  *{item['reasoning']}*")
                
                # Show escalation prediction if available
                if hasattr(result, 'escalation_prediction'):
                    pred = result.escalation_prediction
                    if pred['escalation_probability'] > 0.3:
                        risk_color = "🔴" if pred['escalation_probability'] > 0.7 else "🟡"
                        st.markdown(f"**{risk_color} Escalation Risk:** {pred['escalation_probability']:.1%}")
                        st.markdown(f"*{pred['reasoning']}*")
                
                # Execute action if autonomous
                if result.auto_executed and st.button("Execute Action"):
                    action_result = st.session_state.correlation_agent.execute_correlation_action(result)
                    st.json(action_result)
            else:
                st.info("No similar incidents found")
    
    # Performance metrics
    with st.expander("Agent Performance"):
        metrics = st.session_state.correlation_agent.get_performance_metrics()
        col1, col2, col3 = st.columns(3)
        col1.metric("Decisions Made", metrics['decisions_made'])
        col2.metric("Autonomous Actions", metrics['autonomous_actions'])
        col3.metric("Accuracy Score", f"{metrics['accuracy_score']:.2f}")

def monitoring_demo():
    st.header("📊 Proactive Monitoring Agent")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Current Metrics")
        metrics = st.session_state.data_loader.load_metrics()
        if metrics:
            for name, data in metrics.items():
                if data:
                    current_val = data[-1]['value']
                    # Color code based on thresholds
                    if current_val > 85:
                        st.error(f"🔴 {name.replace('_', ' ').title()}: {current_val:.1f}%")
                    elif current_val > 75:
                        st.warning(f"🟡 {name.replace('_', ' ').title()}: {current_val:.1f}%")
                    else:
                        st.success(f"🟢 {name.replace('_', ' ').title()}: {current_val:.1f}%")
        
        if st.button("🔍 Run Proactive Analysis"):
            with st.spinner("Running proactive analysis..."):
                time.sleep(3)
                result = st.session_state.monitoring_agent.run_proactive_analysis()
                st.session_state.monitoring_result = result
    
    with col2:
        st.subheader("Top 3 Issues")
        if hasattr(st.session_state, 'monitoring_result'):
            result = st.session_state.monitoring_result
            
            if result['success'] and result['top_issues']:
                for i, issue in enumerate(result['top_issues'], 1):
                    severity_color = "🔴" if issue.severity_score > 0.8 else "🟡" if issue.severity_score > 0.6 else "🟢"
                    
                    with st.container():
                        st.markdown(f"**#{i} {severity_color} {issue.alert_id}**")
                        st.markdown(f"Severity: {issue.severity_score:.1%} | Confidence: {issue.confidence_level.value}")
                        
                        if issue.auto_executed:
                            st.success("✅ Autonomous action taken")
                        else:
                            st.warning("⚠️ Human review required")
                        
                        with st.expander(f"Details - Issue #{i}"):
                            st.markdown(f"**Reasoning:** {issue.reasoning}")
                            st.markdown(f"**Business Impact:** {issue.business_impact}")
                            st.markdown("**Recommended Actions:**")
                            for action in issue.recommended_actions:
                                st.markdown(f"- {action}")
                        
                        st.divider()
            else:
                st.info("No critical issues detected")
    
    # Performance metrics
    with st.expander("Agent Performance"):
        metrics = st.session_state.monitoring_agent.get_performance_metrics()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Alerts Generated", metrics['alerts_generated'])
        col2.metric("Top Issues", metrics['top_issues_identified'])
        col3.metric("Autonomous Actions", metrics['autonomous_actions'])
        col4.metric("Accuracy Score", f"{metrics['accuracy_score']:.2f}")

def problem_management_demo():
    st.header("🔍 Problem Management Agent")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Pattern Analysis")
        incidents = st.session_state.data_loader.load_incidents()
        if not incidents:
            st.error("No incident data available")
            return
        
        st.info(f"Analyzing {len(incidents)} incidents for patterns...")
        
        if st.button("🔍 Analyze Incident Patterns"):
            with st.spinner("Analyzing patterns..."):
                time.sleep(3)
                patterns = st.session_state.problem_agent.analyze_incident_patterns(incidents)
                st.session_state.patterns = patterns
                
                if patterns:
                    st.success(f"Found {len(patterns)} significant patterns")
                    
                    # Analyze each pattern for problem creation
                    problem_analyses = []
                    for pattern in patterns:
                        analysis = st.session_state.problem_agent.make_problem_creation_decision(pattern)
                        problem_analyses.append(analysis)
                    
                    st.session_state.problem_analyses = problem_analyses
                else:
                    st.info("No significant patterns detected")
    
    with col2:
        st.subheader("Problem Creation Decisions")
        if hasattr(st.session_state, 'patterns') and hasattr(st.session_state, 'problem_analyses'):
            patterns = st.session_state.patterns
            analyses = st.session_state.problem_analyses
            
            for i, (pattern, analysis) in enumerate(zip(patterns, analyses)):
                with st.container():
                    st.markdown(f"**Pattern #{i+1}: {pattern['pattern_type'].title()}**")
                    st.markdown(f"Key: {pattern['pattern_key']} | Incidents: {pattern['incident_count']}")
                    st.markdown(f"Confidence: {pattern['confidence']:.2f}")
                    
                    if analysis.should_create_problem:
                        st.success("✅ Problem creation recommended")
                        if analysis.auto_executed:
                            st.info("🤖 Executed autonomously")
                        
                        if st.button(f"Create Problem #{i+1}", key=f"create_{i}"):
                            problem = st.session_state.problem_agent.create_and_manage_problem(analysis)
                            st.session_state.problem_agent.orchestrate_resolution_activities(problem)
                            st.success(f"Created problem: {problem.id}")
                    else:
                        st.warning("⚠️ Does not meet creation criteria")
                    
                    with st.expander(f"Pattern Details #{i+1}"):
                        st.markdown(f"**Description:** {pattern['description']}")
                        st.markdown(f"**Root Cause Hypothesis:** {analysis.root_cause_hypothesis}")
                        st.markdown(f"**Reasoning:** {analysis.reasoning}")
                        st.markdown("**Preventive Measures:**")
                        for measure in analysis.preventive_measures:
                            st.markdown(f"- {measure}")
                    
                    st.divider()
    
    # Show created problems
    st.subheader("📋 Created Problems")
    created_problems = st.session_state.problem_agent.problems_created
    if created_problems:
        for problem in created_problems[-3:]:  # Show last 3
            with st.expander(f"Problem: {problem.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Title:** {problem.title}")
                    st.markdown(f"**Status:** {problem.status.value}")
                    st.markdown(f"**Priority:** {problem.priority.value}")
                    st.markdown(f"**Related Incidents:** {len(problem.related_incidents)}")
                with col2:
                    st.markdown(f"**Root Cause:** {problem.root_cause}")
                    st.markdown(f"**Assigned Team:** {problem.assigned_team}")
                    st.markdown(f"**Auto Created:** {'Yes' if problem.auto_created else 'No'}")
                    st.markdown(f"**Confidence:** {problem.pattern_confidence:.2f}")
    else:
        st.info("No problems created yet")
    
    # Performance metrics
    with st.expander("Agent Performance"):
        metrics = st.session_state.problem_agent.get_performance_metrics()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Problems Created", metrics['problems_created'])
        col2.metric("Patterns Analyzed", metrics['patterns_analyzed'])
        col3.metric("Resolution Activities", metrics['resolution_activities'])
        col4.metric("Auto Creation Rate", f"{metrics['auto_creation_rate']:.1%}")

def dashboard():
    st.header("📈 AI-Powered ITSM Dashboard")
    
    # Load data
    incidents = st.session_state.data_loader.load_incidents()
    if not incidents:
        st.error("No data available")
        return
    
    # Key metrics
    total = len(incidents)
    open_inc = len([i for i in incidents if i.status not in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED]])
    critical = len([i for i in incidents if i.severity == SeverityLevel.P1])
    problems_created = len(st.session_state.problem_agent.problems_created)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Incidents", total)
    col2.metric("Open Incidents", open_inc)
    col3.metric("Critical (P1)", critical)
    col4.metric("Problems Created", problems_created)
    
    # Agent status
    st.subheader("🤖 Agent Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔗 Correlation Agent**")
        corr_metrics = st.session_state.correlation_agent.get_performance_metrics()
        st.metric("Decisions Made", corr_metrics['decisions_made'])
        st.metric("Autonomous Actions", corr_metrics['autonomous_actions'])
    
    with col2:
        st.markdown("**📊 Monitoring Agent**")
        mon_metrics = st.session_state.monitoring_agent.get_performance_metrics()
        st.metric("Alerts Generated", mon_metrics['alerts_generated'])
        st.metric("Top Issues", mon_metrics['top_issues_identified'])
    
    with col3:
        st.markdown("**🔍 Problem Agent**")
        prob_metrics = st.session_state.problem_agent.get_performance_metrics()
        st.metric("Problems Created", prob_metrics['problems_created'])
        st.metric("Patterns Analyzed", prob_metrics['patterns_analyzed'])
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    
    # Show recent correlation decisions
    if st.session_state.correlation_agent.decisions_made:
        recent_decision = st.session_state.correlation_agent.decisions_made[-1]
        st.info(f"🔗 Latest Correlation: {recent_decision.decision.value} (Confidence: {recent_decision.confidence_level.value})")
    
    # Show recent monitoring alerts
    if st.session_state.monitoring_agent.top_issues:
        recent_alert = st.session_state.monitoring_agent.top_issues[0]
        st.warning(f"📊 Top Alert: {recent_alert.alert_id} (Severity: {recent_alert.severity_score:.1%})")
    
    # Show recent problems
    if st.session_state.problem_agent.problems_created:
        recent_problem = st.session_state.problem_agent.problems_created[-1]
        st.error(f"🔍 Latest Problem: {recent_problem.id} ({recent_problem.priority.value} priority)")

def main():
    st.title("🤖 AI-Powered ITSM Solution")
    st.markdown("*Autonomous agents with predictive analytics for intelligent IT service management*")
    
    # Show key capabilities
    with st.expander("✨ Key Capabilities"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🔗 **Correlation Agent**")
            st.markdown("- Incident similarity analysis")
            st.markdown("- Escalation prediction")
            st.markdown("- Batch correlation mapping")
        with col2:
            st.markdown("📊 **Monitoring Agent**")
            st.markdown("- Proactive issue detection")
            st.markdown("- Future issue prediction")
            st.markdown("- Capacity planning")
        with col3:
            st.markdown("🔍 **Problem Agent**")
            st.markdown("- Pattern recognition")
            st.markdown("- Autonomous problem creation")
            st.markdown("- Resolution orchestration")
    
    init()
    
    # Sidebar navigation
    st.sidebar.title("🛠️ Navigation")
    page = st.sidebar.selectbox("Select Demo:", ["Dashboard", "Correlation", "Monitoring", "Problem Management"])
    
    # Agent configuration
    with st.sidebar.expander("⚙️ Agent Settings"):
        st.markdown("**Correlation Agent**")
        st.slider("Correlation Threshold", 0.1, 1.0, 0.4, key="corr_threshold")
        
        st.markdown("**Monitoring Agent**")
        st.slider("Critical Threshold", 0.5, 1.0, 0.9, key="mon_threshold")
        
        st.markdown("**Problem Agent**")
        st.slider("Pattern Threshold", 2, 10, 3, key="prob_threshold")
    
    # Main content
    if page == "Dashboard":
        dashboard()
    elif page == "Correlation":
        correlation_demo()
    elif page == "Monitoring":
        monitoring_demo()
    elif page == "Problem Management":
        problem_management_demo()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("🏆 **Hackathon Demo**")
    st.sidebar.markdown("Autonomous AI agents for ITSM")

if __name__ == "__main__":
    main()
