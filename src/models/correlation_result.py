"""
Data models for agent decision results and correlation analysis
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum

class CorrelationDecision(Enum):
    """Agent decision types for incident correlation"""
    GROUP_INCIDENTS = "group_incidents"
    CREATE_PROBLEM = "create_problem"
    ESCALATE_SEVERITY = "escalate_severity"
    NO_ACTION = "no_action"

class ConfidenceLevel(Enum):
    """Confidence levels for agent decisions following behavior guidelines"""
    HIGH = "high"      # >80% - autonomous action allowed
    MEDIUM = "medium"  # 60-80% - human review recommended
    LOW = "low"        # <60% - escalate to human

@dataclass
class CorrelationResult:
    """Result of incident correlation analysis by autonomous agent"""
    
    incident_id: str
    similar_incidents: List[str]
    correlation_score: float
    confidence_level: ConfidenceLevel
    decision: CorrelationDecision
    reasoning: str
    created_at: datetime
    
    # Agent decision tracking
    agent_id: str = "correlation_agent"
    auto_executed: bool = False
    human_feedback: Optional[str] = None
    
    def should_execute_autonomously(self) -> bool:
        """Check if agent should execute decision autonomously per behavior guidelines"""
        return (
            self.confidence_level == ConfidenceLevel.HIGH and
            self.correlation_score > 0.7  # ITIL standard from steering
        )
    
    def requires_human_approval(self) -> bool:
        """Check if decision requires human approval per ITIL standards"""
        escalation_decisions = [
            CorrelationDecision.ESCALATE_SEVERITY,
            CorrelationDecision.CREATE_PROBLEM
        ]
        return (
            self.decision in escalation_decisions or
            self.confidence_level == ConfidenceLevel.LOW
        )

@dataclass
class MonitoringResult:
    """Result of proactive monitoring analysis"""
    
    alert_id: str
    anomaly_detected: bool
    severity_score: float
    confidence_level: ConfidenceLevel
    recommended_actions: List[str]
    business_impact: str
    priority_rank: Optional[int]  # For top 3 issues
    reasoning: str
    created_at: datetime
    
    # Agent decision tracking
    agent_id: str = "monitoring_agent"
    auto_executed: bool = False
    
    def is_top_priority_issue(self) -> bool:
        """Check if this should be in top 3 issues list"""
        return (
            self.anomaly_detected and
            self.severity_score > 0.8 and
            self.confidence_level == ConfidenceLevel.HIGH
        )

@dataclass
class ProblemAnalysisResult:
    """Result of problem management analysis"""
    
    pattern_id: str
    related_incidents: List[str]
    pattern_confidence: float
    should_create_problem: bool
    root_cause_hypothesis: Optional[str]
    preventive_measures: List[str]
    reasoning: str
    created_at: datetime
    
    # Agent decision tracking
    agent_id: str = "problem_agent"
    auto_executed: bool = False
    
    def meets_problem_creation_criteria(self) -> bool:
        """Check if pattern meets ITIL problem creation criteria"""
        return (
            len(self.related_incidents) >= 3 and  # ITIL standard from steering
            self.pattern_confidence > 0.8 and
            self.should_create_problem
        )