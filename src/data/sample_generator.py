"""
Sample data generator for hackathon demo
Creates realistic ITSM data following ITIL standards
"""

import json
import random
from datetime import datetime, timedelta
from typing import List
from pathlib import Path

from ..models.incident import Incident, SeverityLevel, IncidentStatus
from ..models.problem import Problem, ProblemStatus, ProblemPriority
from ..models.alert import Alert, AlertSeverity, AlertStatus

class SampleDataGenerator:
    """Generates realistic sample data for demo scenarios"""
    
    def __init__(self):
        self.systems = [
            "Email Server", "Web Application", "Database Server", 
            "File Server", "Network Switch", "Load Balancer",
            "Authentication Service", "Backup System", "Monitoring System"
        ]
        
        self.user_groups = [
            "Sales Team", "Engineering", "Customer Support", 
            "Finance", "HR", "Marketing", "Operations"
        ]
        
        # Sample incident templates for correlation demo
        self.incident_templates = [
            {
                "title": "Email service unavailable",
                "description": "Users unable to send or receive emails through Outlook",
                "system": "Email Server",
                "severity": SeverityLevel.P2
            },
            {
                "title": "Email connection timeout",
                "description": "Email client showing connection timeout errors",
                "system": "Email Server", 
                "severity": SeverityLevel.P3
            },
            {
                "title": "Slow email delivery",
                "description": "Emails taking longer than usual to send and receive",
                "system": "Email Server",
                "severity": SeverityLevel.P3
            },
            {
                "title": "Database connection errors",
                "description": "Application showing database connection failures",
                "system": "Database Server",
                "severity": SeverityLevel.P1
            },
            {
                "title": "Database query timeout",
                "description": "Database queries timing out after 30 seconds",
                "system": "Database Server",
                "severity": SeverityLevel.P2
            },
            {
                "title": "Web application slow response",
                "description": "Web application pages loading slowly for all users",
                "system": "Web Application",
                "severity": SeverityLevel.P2
            }
        ]
    
    def generate_incidents(self, count: int = 20) -> List[Incident]:
        """Generate sample incidents with correlation opportunities"""
        incidents = []
        base_time = datetime.now() - timedelta(days=2)
        
        for i in range(count):
            template = random.choice(self.incident_templates)
            
            # Add some variation to create realistic scenarios
            incident_time = base_time + timedelta(
                hours=random.randint(0, 48),
                minutes=random.randint(0, 59)
            )
            
            incident = Incident(
                id=f"INC-{1000 + i:04d}",
                title=template["title"],
                description=template["description"],
                severity=template["severity"],
                status=random.choice([IncidentStatus.NEW, IncidentStatus.IN_PROGRESS]),
                affected_system=template["system"],
                user_group=random.choice(self.user_groups),
                created_at=incident_time,
                impact=random.choice(["High", "Medium", "Low"]),
                urgency=random.choice(["High", "Medium", "Low"]),
                category="Infrastructure",
                subcategory=template["system"].split()[0]
            )
            
            # Some incidents are resolved for historical data
            if random.random() < 0.3:
                incident.status = IncidentStatus.RESOLVED
                incident.resolved_at = incident_time + timedelta(
                    hours=random.randint(1, incident.get_sla_target_hours())
                )
            
            incidents.append(incident)
        
        return incidents
    
    def generate_alerts(self, count: int = 10) -> List[Alert]:
        """Generate sample monitoring alerts"""
        alerts = []
        base_time = datetime.now() - timedelta(hours=12)
        
        alert_templates = [
            {
                "title": "High CPU Usage Detected",
                "description": "CPU usage on production server exceeded 85% threshold",
                "severity": AlertSeverity.WARNING,
                "metric": "cpu_utilization",
                "resources": ["prod-web-01", "prod-web-02"]
            },
            {
                "title": "Database Connection Pool Exhausted",
                "description": "Database connection pool reached maximum capacity",
                "severity": AlertSeverity.CRITICAL,
                "metric": "db_connections",
                "resources": ["prod-db-01"]
            },
            {
                "title": "Disk Space Low",
                "description": "Available disk space below 10% on file server",
                "severity": AlertSeverity.WARNING,
                "metric": "disk_usage",
                "resources": ["file-server-01"]
            }
        ]
        
        for i in range(count):
            template = random.choice(alert_templates)
            
            alert_time = base_time + timedelta(
                hours=random.randint(0, 12),
                minutes=random.randint(0, 59)
            )
            
            alert = Alert(
                id=f"ALT-{2000 + i:04d}",
                title=template["title"],
                description=template["description"],
                severity=template["severity"],
                status=AlertStatus.ACTIVE,
                affected_resources=template["resources"],
                created_at=alert_time,
                metric_name=template["metric"],
                threshold_value=random.uniform(80, 95),
                current_value=random.uniform(85, 100),
                business_impact=random.choice(["High", "Medium", "Low"]),
                confidence_score=random.uniform(0.7, 0.95)
            )
            
            # Generate recommended actions based on alert type
            if "CPU" in alert.title:
                alert.recommended_actions = [
                    "Check for runaway processes",
                    "Scale up server resources",
                    "Investigate recent deployments"
                ]
            elif "Database" in alert.title:
                alert.recommended_actions = [
                    "Review active connections",
                    "Restart connection pool",
                    "Check for long-running queries"
                ]
            elif "Disk" in alert.title:
                alert.recommended_actions = [
                    "Clean up temporary files",
                    "Archive old log files",
                    "Add additional storage"
                ]
            
            alerts.append(alert)
        
        # Set priority rankings for top 3 issues
        critical_alerts = [a for a in alerts if a.severity == AlertSeverity.CRITICAL]
        warning_alerts = [a for a in alerts if a.severity == AlertSeverity.WARNING]
        
        # Rank top 3 most critical issues
        top_alerts = (critical_alerts + warning_alerts)[:3]
        for i, alert in enumerate(top_alerts):
            alert.priority_rank = i + 1
        
        return alerts
    
    def save_sample_data(self, output_dir: str = "data"):
        """Save generated sample data to JSON files"""
        Path(output_dir).mkdir(exist_ok=True)
        
        # Generate and save incidents
        incidents = self.generate_incidents(25)
        incidents_data = [inc.to_dict() for inc in incidents]
        
        with open(f"{output_dir}/sample_incidents.json", "w") as f:
            json.dump(incidents_data, f, indent=2)
        
        # Generate and save alerts
        alerts = self.generate_alerts(12)
        alerts_data = [alert.to_dict() for alert in alerts]
        
        with open(f"{output_dir}/sample_alerts.json", "w") as f:
            json.dump(alerts_data, f, indent=2)
        
        # Generate sample metrics for monitoring demo
        metrics_data = self.generate_sample_metrics()
        with open(f"{output_dir}/sample_metrics.json", "w") as f:
            json.dump(metrics_data, f, indent=2)
        
        print(f"Sample data generated in {output_dir}/ directory")
        print(f"- {len(incidents)} incidents")
        print(f"- {len(alerts)} alerts")
        print(f"- Metrics data for monitoring demo")
    
    def generate_sample_metrics(self) -> dict:
        """Generate sample CloudWatch-style metrics"""
        base_time = datetime.now() - timedelta(hours=24)
        
        metrics = {
            "cpu_utilization": [],
            "memory_usage": [],
            "disk_usage": [],
            "network_throughput": [],
            "error_rate": []
        }
        
        # Generate 24 hours of hourly metrics
        for hour in range(24):
            timestamp = base_time + timedelta(hours=hour)
            
            # Simulate normal patterns with some anomalies
            cpu_base = 45 + random.uniform(-10, 10)
            if hour in [14, 15, 16]:  # Afternoon spike
                cpu_base += 30
            
            metrics["cpu_utilization"].append({
                "timestamp": timestamp.isoformat(),
                "value": max(0, min(100, cpu_base + random.uniform(-5, 5))),
                "resource": "prod-web-01"
            })
            
            # Memory usage trending upward (potential leak)
            memory_base = 60 + (hour * 1.5) + random.uniform(-5, 5)
            metrics["memory_usage"].append({
                "timestamp": timestamp.isoformat(),
                "value": max(0, min(100, memory_base)),
                "resource": "prod-app-01"
            })
            
            # Disk usage slowly increasing
            disk_base = 75 + (hour * 0.5) + random.uniform(-2, 2)
            metrics["disk_usage"].append({
                "timestamp": timestamp.isoformat(),
                "value": max(0, min(100, disk_base)),
                "resource": "file-server-01"
            })
        
        return metrics

if __name__ == "__main__":
    generator = SampleDataGenerator()
    generator.save_sample_data()