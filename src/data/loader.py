"""
Data loader utility for sample ITSM data
"""

import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path

from ..models.incident import Incident, SeverityLevel, IncidentStatus
from ..models.alert import Alert, AlertSeverity, AlertStatus
from datetime import timedelta

class DataLoader:
    """Loads sample data for demo and testing"""
    
    def __init__(self, data_dir: str = "data"):
        # Handle both local and Streamlit Cloud paths
        import os
        if os.path.exists(data_dir):
            self.data_dir = Path(data_dir)
        else:
            # Try relative to current file
            current_dir = Path(__file__).parent.parent.parent
            self.data_dir = current_dir / data_dir
    
    def load_incidents(self) -> List[Incident]:
        """Load incidents from JSON file"""
        incidents_file = self.data_dir / "sample_incidents.json"
        
        if not incidents_file.exists():
            # Return sample data if file not found
            return self._get_sample_incidents()
        
        with open(incidents_file, 'r') as f:
            incidents_data = json.load(f)
        
        incidents = []
        for data in incidents_data:
            # Convert string enums back to enum objects
            incident = Incident(
                id=data["id"],
                title=data["title"],
                description=data["description"],
                severity=SeverityLevel(data["severity"]),
                status=IncidentStatus(data["status"]),
                affected_system=data["affected_system"],
                user_group=data["user_group"],
                created_at=datetime.fromisoformat(data["created_at"]),
                resolved_at=datetime.fromisoformat(data["resolved_at"]) if data["resolved_at"] else None,
                correlation_group=data.get("correlation_group"),
                problem_id=data.get("problem_id"),
                impact=data.get("impact", "Medium"),
                urgency=data.get("urgency", "Medium"),
                category=data.get("category", "Infrastructure"),
                subcategory=data.get("subcategory", "Server"),
                assigned_to=data.get("assigned_to"),
                correlation_confidence=data.get("correlation_confidence"),
                auto_created=data.get("auto_created", False)
            )
            incidents.append(incident)
        
        return incidents
    
    def load_alerts(self) -> List[Alert]:
        """Load alerts from JSON file"""
        alerts_file = self.data_dir / "sample_alerts.json"
        
        if not alerts_file.exists():
            # Return sample data if file not found
            return self._get_sample_alerts()
        
        with open(alerts_file, 'r') as f:
            alerts_data = json.load(f)
        
        alerts = []
        for data in alerts_data:
            alert = Alert(
                id=data["id"],
                title=data["title"],
                description=data["description"],
                severity=AlertSeverity(data["severity"]),
                status=AlertStatus(data["status"]),
                affected_resources=data["affected_resources"],
                created_at=datetime.fromisoformat(data["created_at"]),
                resolved_at=datetime.fromisoformat(data["resolved_at"]) if data["resolved_at"] else None,
                metric_name=data.get("metric_name", ""),
                threshold_value=data.get("threshold_value"),
                current_value=data.get("current_value"),
                recommended_actions=data.get("recommended_actions", []),
                business_impact=data.get("business_impact", "Medium"),
                priority_rank=data.get("priority_rank"),
                auto_generated=data.get("auto_generated", True),
                confidence_score=data.get("confidence_score")
            )
            alerts.append(alert)
        
        return alerts
    
    def load_metrics(self) -> Dict:
        """Load sample metrics data"""
        metrics_file = self.data_dir / "sample_metrics.json"
        
        if not metrics_file.exists():
            # Return sample data if file not found
            return self._get_sample_metrics()
        
        with open(metrics_file, 'r') as f:
            return json.load(f)
    
    def get_correlation_demo_data(self) -> List[Incident]:
        """Get incidents specifically for correlation demo"""
        incidents = self.load_incidents()
        
        # Filter for incidents that should correlate
        email_incidents = [inc for inc in incidents if "Email" in inc.affected_system]
        db_incidents = [inc for inc in incidents if "Database" in inc.affected_system]
        
        # Return a mix that shows clear correlation opportunities
        demo_incidents = email_incidents[:4] + db_incidents[:3]
        return demo_incidents
    
    def get_top_alerts_demo_data(self) -> List[Alert]:
        """Get top 3 alerts for proactive monitoring demo"""
        alerts = self.load_alerts()
        
        # Sort by priority rank and return top 3
        top_alerts = [alert for alert in alerts if alert.priority_rank is not None]
        top_alerts.sort(key=lambda x: x.priority_rank)
        
        return top_alerts[:3]
    
    def _get_sample_incidents(self) -> List[Incident]:
        """Generate sample incidents when data file is missing"""
        from datetime import datetime, timedelta
        
        sample_data = [
            {
                "id": "INC-001",
                "title": "Email server slow response",
                "description": "Users reporting slow email delivery and timeouts",
                "severity": "P2",
                "status": "Open",
                "affected_system": "prod-mail-01",
                "user_group": "Sales Team",
                "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                "resolved_at": None
            },
            {
                "id": "INC-002",
                "title": "Database connection timeout",
                "description": "Application experiencing database connection timeouts",
                "severity": "P1",
                "status": "Open",
                "affected_system": "prod-db-01",
                "user_group": "All Users",
                "created_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                "resolved_at": None
            },
            {
                "id": "INC-003",
                "title": "Web server high CPU",
                "description": "Web server showing high CPU utilization",
                "severity": "P3",
                "status": "In Progress",
                "affected_system": "prod-web-01",
                "user_group": "External Users",
                "created_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "resolved_at": None
            },
            {
                "id": "INC-004",
                "title": "Email delivery failure",
                "description": "Email messages not being delivered to external recipients",
                "severity": "P2",
                "status": "Open",
                "affected_system": "prod-mail-01",
                "user_group": "Marketing Team",
                "created_at": (datetime.now() - timedelta(minutes=45)).isoformat(),
                "resolved_at": None
            },
            {
                "id": "INC-005",
                "title": "Database slow queries",
                "description": "Database queries taking longer than usual to execute",
                "severity": "P3",
                "status": "Open",
                "affected_system": "prod-db-01",
                "user_group": "Development Team",
                "created_at": (datetime.now() - timedelta(minutes=15)).isoformat(),
                "resolved_at": None
            }
        ]
        
        incidents = []
        for data in sample_data:
            incident = Incident(
                id=data["id"],
                title=data["title"],
                description=data["description"],
                severity=SeverityLevel(data["severity"]),
                status=IncidentStatus(data["status"]),
                affected_system=data["affected_system"],
                user_group=data["user_group"],
                created_at=datetime.fromisoformat(data["created_at"]),
                resolved_at=None
            )
            incidents.append(incident)
        
        return incidents
    
    def _get_sample_alerts(self) -> List[Alert]:
        """Generate sample alerts when data file is missing"""
        return []  # Simplified for now
    
    def _get_sample_metrics(self) -> Dict:
        """Generate sample metrics when data file is missing"""
        return {
            "cpu_utilization": [
                {"timestamp": datetime.now().isoformat(), "value": 75.2},
                {"timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(), "value": 73.1},
                {"timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(), "value": 71.8}
            ],
            "memory_usage": [
                {"timestamp": datetime.now().isoformat(), "value": 82.5},
                {"timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(), "value": 81.2},
                {"timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(), "value": 80.1}
            ],
            "disk_usage": [
                {"timestamp": datetime.now().isoformat(), "value": 91.3},
                {"timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(), "value": 91.1},
                {"timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(), "value": 90.8}
            ]
        }