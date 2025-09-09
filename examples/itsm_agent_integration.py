#!/usr/bin/env python3
"""
ITSM Agent Integration Examples
This file shows how to integrate OpenAI Agents with your existing ITSM project
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents import Agent, Runner, Tool
from datetime import datetime
from typing import Dict, List, Optional

# Import your existing models and classes
from models.incident import Incident, SeverityLevel
from models.alert import Alert, AlertSeverity, AlertStatus
from models.correlation_result import CorrelationResult, CorrelationDecision, ConfidenceLevel
from data.loader import DataLoader

class ITSMAgentIntegration:
    """Integration class showing how to use OpenAI Agents with your ITSM system"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        
    def create_incident_management_agent(self) -> Agent:
        """Create an agent specialized for incident management"""
        
        def create_incident(title: str, description: str, severity: str = "Medium") -> Dict:
            """Create a new incident"""
            incident_id = f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            return {
                "incident_id": incident_id,
                "title": title,
                "description": description,
                "severity": severity,
                "status": "Open",
                "created_at": datetime.now().isoformat(),
                "assigned_team": "Infrastructure Team"
            }
        
        def get_incident_status(incident_id: str) -> Dict:
            """Get the status of an incident"""
            # In a real system, this would query your database
            return {
                "incident_id": incident_id,
                "status": "Open",
                "assigned_team": "Infrastructure Team",
                "last_updated": datetime.now().isoformat(),
                "progress": "Investigation in progress"
            }
        
        def escalate_incident(incident_id: str, reason: str) -> Dict:
            """Escalate an incident"""
            return {
                "incident_id": incident_id,
                "action": "escalated",
                "reason": reason,
                "escalated_to": "Senior Management",
                "timestamp": datetime.now().isoformat()
            }
        
        def search_similar_incidents(description: str) -> List[Dict]:
            """Search for similar incidents"""
            # This would normally use your correlation logic
            return [
                {
                    "incident_id": "INC-20241201001",
                    "title": "Database connection timeout",
                    "similarity_score": 0.85,
                    "status": "Resolved"
                },
                {
                    "incident_id": "INC-20241201002", 
                    "title": "Application server unresponsive",
                    "similarity_score": 0.72,
                    "status": "Open"
                }
            ]
        
        # Create tools for the incident management agent
        tools = [
            Tool(name="create_incident", function=create_incident),
            Tool(name="get_incident_status", function=get_incident_status),
            Tool(name="escalate_incident", function=escalate_incident),
            Tool(name="search_similar_incidents", function=search_similar_incidents)
        ]
        
        return Agent(
            name="IncidentManagementAgent",
            instructions="""
            You are an IT Service Management agent specialized in incident management.
            
            Your responsibilities:
            1. Create incidents when problems are reported
            2. Check incident status and provide updates
            3. Escalate incidents when necessary
            4. Search for similar incidents to help with resolution
            5. Provide professional and helpful service
            
            Always:
            - Ask for clarification if information is unclear
            - Provide incident IDs for tracking
            - Explain what actions you're taking
            - Be empathetic to users experiencing issues
            """,
            tools=tools
        )
    
    def create_monitoring_agent(self) -> Agent:
        """Create an agent specialized for monitoring and alerts"""
        
        def check_system_health() -> Dict:
            """Check overall system health"""
            return {
                "overall_status": "Warning",
                "cpu_usage": "75%",
                "memory_usage": "60%",
                "disk_usage": "45%",
                "network_status": "Normal",
                "alerts": [
                    {"type": "CPU", "severity": "Warning", "message": "High CPU usage detected"},
                    {"type": "Memory", "severity": "Info", "message": "Memory usage within normal range"}
                ]
            }
        
        def get_recent_alerts(hours: int = 24) -> List[Dict]:
            """Get recent alerts"""
            return [
                {
                    "alert_id": "ALERT-001",
                    "message": "High CPU usage on server-01",
                    "severity": "Warning",
                    "timestamp": datetime.now().isoformat(),
                    "status": "Active"
                },
                {
                    "alert_id": "ALERT-002",
                    "message": "Disk space low on server-02",
                    "severity": "Critical",
                    "timestamp": datetime.now().isoformat(),
                    "status": "Active"
                }
            ]
        
        def create_maintenance_ticket(description: str, priority: str = "Medium") -> Dict:
            """Create a maintenance ticket"""
            ticket_id = f"MAINT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            return {
                "ticket_id": ticket_id,
                "description": description,
                "priority": priority,
                "status": "Open",
                "assigned_team": "Operations Team",
                "created_at": datetime.now().isoformat()
            }
        
        def predict_system_issues() -> Dict:
            """Predict potential system issues"""
            return {
                "predictions": [
                    {
                        "issue": "Disk space exhaustion",
                        "probability": "High",
                        "timeframe": "2-3 days",
                        "recommended_action": "Clean up log files and temporary data"
                    },
                    {
                        "issue": "Memory pressure",
                        "probability": "Medium", 
                        "timeframe": "1 week",
                        "recommended_action": "Monitor memory usage and consider scaling"
                    }
                ],
                "confidence": 0.75
            }
        
        # Create tools for the monitoring agent
        tools = [
            Tool(name="check_system_health", function=check_system_health),
            Tool(name="get_recent_alerts", function=get_recent_alerts),
            Tool(name="create_maintenance_ticket", function=create_maintenance_ticket),
            Tool(name="predict_system_issues", function=predict_system_issues)
        ]
        
        return Agent(
            name="MonitoringAgent",
            instructions="""
            You are a proactive monitoring agent for IT infrastructure.
            
            Your responsibilities:
            1. Monitor system health and performance
            2. Analyze alerts and identify patterns
            3. Create maintenance tickets for preventive actions
            4. Predict potential issues before they occur
            5. Provide status updates and recommendations
            
            Always:
            - Be proactive in identifying issues
            - Provide clear explanations of problems
            - Suggest specific actions to resolve issues
            - Prioritize critical issues appropriately
            """,
            tools=tools
        )
    
    def create_correlation_agent(self) -> Agent:
        """Create an agent specialized for incident correlation"""
        
        def correlate_incidents(incident_descriptions: List[str]) -> Dict:
            """Correlate incidents based on descriptions"""
            # This would use your existing correlation logic
            correlations = []
            
            for i, desc1 in enumerate(incident_descriptions):
                for j, desc2 in enumerate(incident_descriptions[i+1:], i+1):
                    # Simple keyword-based correlation for demo
                    common_words = set(desc1.lower().split()) & set(desc2.lower().split())
                    similarity = len(common_words) / max(len(desc1.split()), len(desc2.split()))
                    
                    if similarity > 0.3:  # 30% similarity threshold
                        correlations.append({
                            "incident_1": f"INC-{i+1:03d}",
                            "incident_2": f"INC-{j+1:03d}",
                            "similarity_score": similarity,
                            "common_keywords": list(common_words),
                            "correlation_confidence": "High" if similarity > 0.6 else "Medium"
                        })
            
            return {
                "correlations_found": len(correlations),
                "correlations": correlations,
                "analysis_timestamp": datetime.now().isoformat()
            }
        
        def suggest_problem_creation(correlations: List[Dict]) -> Dict:
            """Suggest creating a problem record from correlations"""
            high_confidence_correlations = [c for c in correlations if c["correlation_confidence"] == "High"]
            
            if len(high_confidence_correlations) >= 2:
                return {
                    "should_create_problem": True,
                    "reason": f"Found {len(high_confidence_correlations)} high-confidence correlations",
                    "suggested_problem_title": "Recurring Infrastructure Issues",
                    "recommended_actions": [
                        "Create problem record",
                        "Assign to infrastructure team",
                        "Schedule root cause analysis"
                    ]
                }
            else:
                return {
                    "should_create_problem": False,
                    "reason": "Insufficient high-confidence correlations",
                    "recommended_actions": ["Continue monitoring", "Gather more incident data"]
                }
        
        # Create tools for the correlation agent
        tools = [
            Tool(name="correlate_incidents", function=correlate_incidents),
            Tool(name="suggest_problem_creation", function=suggest_problem_creation)
        ]
        
        return Agent(
            name="CorrelationAgent",
            instructions="""
            You are an incident correlation specialist.
            
            Your responsibilities:
            1. Analyze incidents to find patterns and relationships
            2. Correlate similar incidents based on descriptions and symptoms
            3. Suggest when to create problem records from correlated incidents
            4. Provide insights into recurring issues
            
            Always:
            - Use data-driven analysis
            - Explain your correlation reasoning
            - Provide confidence levels for correlations
            - Suggest actionable next steps
            """,
            tools=tools
        )
    
    def create_supervisor_agent(self) -> Agent:
        """Create a supervisor agent that coordinates other agents"""
        
        def route_request(request: str, available_agents: List[str]) -> str:
            """Route requests to appropriate agents"""
            request_lower = request.lower()
            
            if any(word in request_lower for word in ["incident", "problem", "issue", "outage"]):
                return "IncidentManagementAgent"
            elif any(word in request_lower for word in ["monitor", "alert", "health", "performance"]):
                return "MonitoringAgent"
            elif any(word in request_lower for word in ["correlate", "pattern", "similar", "related"]):
                return "CorrelationAgent"
            else:
                return "IncidentManagementAgent"  # Default
        
        def coordinate_agents(primary_agent: str, secondary_agents: List[str], task: str) -> Dict:
            """Coordinate multiple agents for complex tasks"""
            return {
                "primary_agent": primary_agent,
                "secondary_agents": secondary_agents,
                "coordination_plan": f"Primary agent handles main task, secondary agents provide support",
                "estimated_completion": "5-10 minutes",
                "coordination_timestamp": datetime.now().isoformat()
            }
        
        # Create tools for the supervisor agent
        tools = [
            Tool(name="route_request", function=route_request),
            Tool(name="coordinate_agents", function=coordinate_agents)
        ]
        
        return Agent(
            name="SupervisorAgent",
            instructions="""
            You are a supervisor agent that coordinates other specialized agents.
            
            Your responsibilities:
            1. Route requests to the most appropriate agent
            2. Coordinate multiple agents for complex tasks
            3. Ensure proper escalation and handoffs
            4. Monitor overall system performance
            
            Always:
            - Choose the most appropriate agent for each request
            - Explain your routing decisions
            - Coordinate effectively between agents
            - Provide clear status updates
            """,
            tools=tools
        )
    
    def demonstrate_agent_workflows(self):
        """Demonstrate various agent workflows"""
        print("=" * 60)
        print("ITSM Agent Integration Examples")
        print("=" * 60)
        
        # Create agents
        incident_agent = self.create_incident_management_agent()
        monitoring_agent = self.create_monitoring_agent()
        correlation_agent = self.create_correlation_agent()
        supervisor_agent = self.create_supervisor_agent()
        
        # Example 1: Incident Management Workflow
        print("\n1. Incident Management Workflow")
        print("-" * 40)
        
        incident_requests = [
            "A user reported that the website is loading very slowly",
            "Can you check the status of incident INC-20241201001?",
            "I need to escalate incident INC-20241201002 because it's affecting production"
        ]
        
        for request in incident_requests:
            print(f"Request: {request}")
            result = Runner.run_sync(incident_agent, request)
            print(f"Response: {result.final_output}")
            print()
        
        # Example 2: Monitoring Workflow
        print("\n2. Monitoring Workflow")
        print("-" * 40)
        
        monitoring_requests = [
            "Can you check the overall system health?",
            "What alerts have we received in the last 24 hours?",
            "Are there any potential issues we should be aware of?"
        ]
        
        for request in monitoring_requests:
            print(f"Request: {request}")
            result = Runner.run_sync(monitoring_agent, request)
            print(f"Response: {result.final_output}")
            print()
        
        # Example 3: Correlation Workflow
        print("\n3. Correlation Workflow")
        print("-" * 40)
        
        correlation_requests = [
            "Can you analyze these incidents for patterns: 'Database timeout', 'Application slow', 'Server unresponsive'?",
            "Should we create a problem record based on recent correlations?"
        ]
        
        for request in correlation_requests:
            print(f"Request: {request}")
            result = Runner.run_sync(correlation_agent, request)
            print(f"Response: {result.final_output}")
            print()
        
        # Example 4: Supervisor Coordination
        print("\n4. Supervisor Coordination")
        print("-" * 40)
        
        supervisor_requests = [
            "We have multiple system issues that need attention",
            "Can you help coordinate a response to a major outage?",
            "I need to understand the relationship between recent incidents"
        ]
        
        for request in supervisor_requests:
            print(f"Request: {request}")
            result = Runner.run_sync(supervisor_agent, request)
            print(f"Response: {result.final_output}")
            print()
    
    def demonstrate_multi_agent_coordination(self):
        """Demonstrate multi-agent coordination for complex scenarios"""
        print("\n" + "=" * 60)
        print("Multi-Agent Coordination Example")
        print("=" * 60)
        
        # Create agents
        incident_agent = self.create_incident_management_agent()
        monitoring_agent = self.create_monitoring_agent()
        correlation_agent = self.create_correlation_agent()
        
        # Scenario: Major system outage
        print("\nScenario: Major System Outage")
        print("-" * 40)
        
        # Step 1: Monitor detects issues
        print("Step 1: Monitoring Agent detects issues")
        monitoring_result = Runner.run_sync(
            monitoring_agent,
            "Check system health and identify any critical issues"
        )
        print(f"Monitoring Response: {monitoring_result.final_output}")
        print()
        
        # Step 2: Create incidents
        print("Step 2: Incident Management Agent creates incidents")
        incident_result = Runner.run_sync(
            incident_agent,
            "Create incidents for the critical issues detected by monitoring"
        )
        print(f"Incident Response: {incident_result.final_output}")
        print()
        
        # Step 3: Correlate incidents
        print("Step 3: Correlation Agent analyzes patterns")
        correlation_result = Runner.run_sync(
            correlation_agent,
            "Analyze the incidents for correlation and suggest if we need a problem record"
        )
        print(f"Correlation Response: {correlation_result.final_output}")
        print()
        
        # Step 4: Coordinated response
        print("Step 4: Coordinated Response")
        print("All agents have provided their analysis. The system can now:")
        print("- Create appropriate incidents")
        print("- Escalate critical issues")
        print("- Create problem records if needed")
        print("- Coordinate response teams")

def main():
    """Run the ITSM agent integration examples"""
    try:
        integration = ITSMAgentIntegration()
        integration.demonstrate_agent_workflows()
        integration.demonstrate_multi_agent_coordination()
        
        print("\n" + "=" * 60)
        print("ITSM Agent Integration Examples Completed!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Make sure you have the required dependencies installed:")
        print("pip install openai-agents")
        print()
        print("Note: This example shows how to integrate OpenAI Agents with your existing ITSM system.")
        print("The actual integration would require proper configuration and API keys.")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("This might be because the OpenAI Agents SDK is not available or configured.")

if __name__ == "__main__":
    main()
