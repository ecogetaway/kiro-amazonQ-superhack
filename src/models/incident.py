"""
Incident data model following ITIL standards
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List

class SeverityLevel(Enum):
    """ITIL-aligned severity levels"""
    P1 = "P1"  # Critical: Complete service outage affecting all users
    P2 = "P2"  # High: Major functionality impacted, affecting multiple users
    P3 = "P3"  # Medium: Minor functionality impacted, affecting few users
    P4 = "P4"  # Low: Cosmetic issues or feature requests

class IncidentStatus(Enum):
    """Standard incident lifecycle states"""
    NEW = "New"
    IN_PROGRESS = "In Progress"
    PENDING = "Pending"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

@dataclass
class Incident:
    """Core incident model following ITIL standards"""
    
    id: str
    title: str
    description: str
    severity: SeverityLevel
    status: IncidentStatus
    affected_system: str
    user_group: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    correlation_group: Optional[str] = None
    problem_id: Optional[str] = None
    
    # ITIL-specific fields
    impact: str = "Medium"  # High/Medium/Low
    urgency: str = "Medium"  # High/Medium/Low
    category: str = "Infrastructure"
    subcategory: str = "Server"
    assigned_to: Optional[str] = None
    
    # Agent decision tracking
    correlation_confidence: Optional[float] = None
    auto_created: bool = False
    
    def get_sla_target_hours(self) -> int:
        """Get resolution target based on ITIL SLA standards"""
        sla_targets = {
            SeverityLevel.P1: 4,   # 4 hours resolution target
            SeverityLevel.P2: 8,   # 8 hours resolution target
            SeverityLevel.P3: 24,  # 24 hours resolution target
            SeverityLevel.P4: 72   # 72 hours resolution target
        }
        return sla_targets.get(self.severity, 24)
    
    def is_sla_at_risk(self) -> bool:
        """Check if incident is at risk of SLA breach"""
        if self.status in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED]:
            return False
            
        hours_elapsed = (datetime.now() - self.created_at).total_seconds() / 3600
        target_hours = self.get_sla_target_hours()
        
        # At risk if 75% of SLA time has elapsed
        return hours_elapsed > (target_hours * 0.75)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "status": self.status.value,
            "affected_system": self.affected_system,
            "user_group": self.user_group,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "correlation_group": self.correlation_group,
            "problem_id": self.problem_id,
            "impact": self.impact,
            "urgency": self.urgency,
            "category": self.category,
            "subcategory": self.subcategory,
            "assigned_to": self.assigned_to,
            "correlation_confidence": self.correlation_confidence,
            "auto_created": self.auto_created
        }