"""
Alert data model for proactive monitoring
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List

class AlertSeverity(Enum):
    """Alert severity levels for proactive monitoring"""
    CRITICAL = "Critical"
    WARNING = "Warning"
    INFO = "Info"

class AlertStatus(Enum):
    """Alert lifecycle states"""
    ACTIVE = "Active"
    ACKNOWLEDGED = "Acknowledged"
    RESOLVED = "Resolved"
    SUPPRESSED = "Suppressed"

@dataclass
class Alert:
    """Proactive monitoring alert following ITIL service operation standards"""
    
    id: str
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    affected_resources: List[str]
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    # Monitoring specific fields
    metric_name: str = ""
    threshold_value: Optional[float] = None
    current_value: Optional[float] = None
    
    # Agent recommendations
    recommended_actions: List[str] = None
    business_impact: str = "Medium"
    priority_rank: Optional[int] = None  # For "top 3 issues" ranking
    
    # Agent decision tracking
    auto_generated: bool = True
    confidence_score: Optional[float] = None
    
    def __post_init__(self):
        """Initialize empty lists if None"""
        if self.recommended_actions is None:
            self.recommended_actions = []
    
    def is_top_priority(self) -> bool:
        """Check if this alert should be in top 3 issues"""
        return (
            self.severity == AlertSeverity.CRITICAL and
            self.status == AlertStatus.ACTIVE and
            self.priority_rank is not None and
            self.priority_rank <= 3
        )
    
    def get_escalation_required(self) -> bool:
        """Determine if alert requires immediate escalation"""
        critical_conditions = [
            self.severity == AlertSeverity.CRITICAL,
            "production" in self.description.lower(),
            any("database" in resource.lower() for resource in self.affected_resources),
            self.current_value and self.threshold_value and 
            self.current_value > (self.threshold_value * 1.5)
        ]
        return any(critical_conditions)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "status": self.status.value,
            "affected_resources": self.affected_resources,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "metric_name": self.metric_name,
            "threshold_value": self.threshold_value,
            "current_value": self.current_value,
            "recommended_actions": self.recommended_actions,
            "business_impact": self.business_impact,
            "priority_rank": self.priority_rank,
            "auto_generated": self.auto_generated,
            "confidence_score": self.confidence_score
        }