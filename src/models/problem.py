"""
Problem data model following ITIL problem management standards
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List

class ProblemStatus(Enum):
    """ITIL problem lifecycle states"""
    NEW = "New"
    INVESTIGATING = "Investigating"
    KNOWN_ERROR = "Known Error"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

class ProblemPriority(Enum):
    """Problem priority based on business impact"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

@dataclass
class Problem:
    """Problem record following ITIL standards"""
    
    id: str
    title: str
    description: str
    status: ProblemStatus
    priority: ProblemPriority
    related_incidents: List[str]
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    # Root cause analysis fields
    root_cause: Optional[str] = None
    contributing_factors: List[str] = None
    timeline_of_events: List[str] = None
    
    # Resolution tracking
    preventive_measures: List[str] = None
    assigned_team: Optional[str] = None
    owner: Optional[str] = None
    
    # Agent decision tracking
    auto_created: bool = False
    pattern_confidence: Optional[float] = None
    
    def __post_init__(self):
        """Initialize empty lists if None"""
        if self.contributing_factors is None:
            self.contributing_factors = []
        if self.timeline_of_events is None:
            self.timeline_of_events = []
        if self.preventive_measures is None:
            self.preventive_measures = []
    
    def add_related_incident(self, incident_id: str):
        """Add an incident to this problem"""
        if incident_id not in self.related_incidents:
            self.related_incidents.append(incident_id)
    
    def meets_closure_criteria(self) -> bool:
        """Check if problem meets ITIL closure criteria"""
        return (
            self.status == ProblemStatus.RESOLVED and
            self.root_cause is not None and
            len(self.preventive_measures) > 0 and
            self.resolved_at is not None
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "related_incidents": self.related_incidents,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "root_cause": self.root_cause,
            "contributing_factors": self.contributing_factors,
            "timeline_of_events": self.timeline_of_events,
            "preventive_measures": self.preventive_measures,
            "assigned_team": self.assigned_team,
            "owner": self.owner,
            "auto_created": self.auto_created,
            "pattern_confidence": self.pattern_confidence
        }