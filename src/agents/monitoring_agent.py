"""
Autonomous Proactive Monitoring Agent
Independently monitors infrastructure, predicts issues, and takes preventive actions
"""

import statistics
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from ..models.alert import Alert, AlertSeverity, AlertStatus
from ..models.correlation_result import MonitoringResult, ConfidenceLevel
from ..data.loader import DataLoader

@dataclass
class MetricAnalysis:
    """Analysis result for a specific metric"""
    metric_name: str
    current_value: float
    threshold_value: float
    is_anomaly: bool
    severity_score: float
    trend: str  # "increasing", "decreasing", "stable"
    prediction: str
    confidence: float

class AutonomousMonitoringAgent:
    """Agent that autonomously monitors infrastructure and makes proactive decisions"""
    
    def __init__(self):
        # ITIL Service Operation standards from steering guidelines
        self.anomaly_threshold = 2.0  # Standard deviations for anomaly detection
        self.critical_threshold = 0.9  # 90% threshold for critical alerts
        self.warning_threshold = 0.8   # 80% threshold for warning alerts
        
        # Agent behavior guidelines
        self.high_confidence_threshold = 0.8  # >80% for autonomous action
        self.low_confidence_threshold = 0.6   # <60% requires human escalation
        
        # Business-critical systems (prioritized per agent behavior guidelines)
        self.critical_systems = [
            "prod-db-01", "prod-web-01", "prod-web-02", 
            "load-balancer", "auth-service"
        ]
        
        # Monitoring state
        self.alerts_generated = []
        self.top_issues = []
        self.performance_history = []
        
        # Learning and adaptation
        self.false_positive_rate = 0.0
        self.accuracy_score = 0.0
        
        self.data_loader = DataLoader()
    
    def analyze_metrics(self, metrics_data: Dict) -> List[MetricAnalysis]:
        """Analyze infrastructure metrics for anomalies and trends"""
        
        analyses = []
        
        for metric_name, data_points in metrics_data.items():
            if not data_points:
                continue
            
            analysis = self._analyze_single_metric(metric_name, data_points)
            analyses.append(analysis)
        
        return analyses
    
    def _analyze_single_metric(self, metric_name: str, data_points: List[Dict]) -> MetricAnalysis:
        """Analyze a single metric for anomalies and trends"""
        
        # Extract values and timestamps
        values = [point['value'] for point in data_points]
        timestamps = [datetime.fromisoformat(point['timestamp']) for point in data_points]
        
        if len(values) < 2:
            return MetricAnalysis(
                metric_name=metric_name,
                current_value=values[0] if values else 0,
                threshold_value=100,
                is_anomaly=False,
                severity_score=0.0,
                trend="stable",
                prediction="Insufficient data",
                confidence=0.0
            )
        
        # Calculate statistics
        current_value = values[-1]
        mean_value = statistics.mean(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        
        # Determine thresholds based on metric type
        threshold_value = self._get_metric_threshold(metric_name)
        
        # Detect anomalies using statistical analysis
        is_anomaly = False
        severity_score = 0.0
        
        if std_dev > 0:
            z_score = abs(current_value - mean_value) / std_dev
            is_anomaly = z_score > self.anomaly_threshold
            severity_score = min(1.0, z_score / 3.0)  # Normalize to 0-1
        
        # Check threshold-based anomalies
        if current_value > threshold_value:
            is_anomaly = True
            severity_score = max(severity_score, current_value / 100.0)
        
        # Analyze trend
        trend = self._analyze_trend(values)
        
        # Generate prediction and confidence
        prediction, confidence = self._generate_prediction(
            metric_name, current_value, trend, severity_score
        )
        
        return MetricAnalysis(
            metric_name=metric_name,
            current_value=current_value,
            threshold_value=threshold_value,
            is_anomaly=is_anomaly,
            severity_score=severity_score,
            trend=trend,
            prediction=prediction,
            confidence=confidence
        )
    
    def _get_metric_threshold(self, metric_name: str) -> float:
        """Get appropriate threshold based on metric type"""
        thresholds = {
            'cpu_utilization': 85.0,
            'memory_usage': 90.0,
            'disk_usage': 85.0,
            'network_throughput': 80.0,
            'error_rate': 5.0,
            'response_time': 2000.0  # milliseconds
        }
        return thresholds.get(metric_name, 80.0)
    
    def _analyze_trend(self, values: List[float]) -> str:
        """Analyze trend in metric values"""
        if len(values) < 3:
            return "stable"
        
        # Simple trend analysis using recent values
        recent_values = values[-5:]  # Last 5 data points
        
        if len(recent_values) < 2:
            return "stable"
        
        # Calculate slope
        x = list(range(len(recent_values)))
        y = recent_values
        
        # Simple linear regression slope
        n = len(x)
        slope = (n * sum(x[i] * y[i] for i in range(n)) - sum(x) * sum(y)) / (n * sum(x[i]**2 for i in range(n)) - sum(x)**2)
        
        if slope > 1.0:
            return "increasing"
        elif slope < -1.0:
            return "decreasing"
        else:
            return "stable"
    
    def _generate_prediction(self, metric_name: str, current_value: float, 
                           trend: str, severity_score: float) -> Tuple[str, float]:
        """Generate prediction and confidence score"""
        
        predictions = {
            'cpu_utilization': {
                'increasing': "CPU usage trending upward - potential performance degradation",
                'decreasing': "CPU usage normalizing - system recovering",
                'stable': "CPU usage stable within normal range"
            },
            'memory_usage': {
                'increasing': "Memory usage climbing - possible memory leak detected",
                'decreasing': "Memory usage decreasing - system optimization effective",
                'stable': "Memory usage stable - no immediate concerns"
            },
            'disk_usage': {
                'increasing': "Disk space consumption accelerating - storage cleanup needed",
                'decreasing': "Disk usage optimized - cleanup activities successful",
                'stable': "Disk usage stable - adequate storage available"
            }
        }
        
        # Get prediction based on metric and trend
        metric_predictions = predictions.get(metric_name, {
            'increasing': f"{metric_name} trending upward - monitoring required",
            'decreasing': f"{metric_name} improving - positive trend",
            'stable': f"{metric_name} stable - no action needed"
        })
        
        prediction = metric_predictions.get(trend, "Unknown trend pattern")
        
        # Calculate confidence based on severity and data quality
        base_confidence = 0.7
        if severity_score > 0.8:
            confidence = min(0.95, base_confidence + 0.2)
        elif severity_score > 0.5:
            confidence = base_confidence + 0.1
        else:
            confidence = base_confidence
        
        return prediction, confidence
    
    def generate_top_issues(self, analyses: List[MetricAnalysis]) -> List[MonitoringResult]:
        """Generate top 3 issues requiring immediate attention"""
        
        # Filter for anomalies and sort by severity
        anomalies = [analysis for analysis in analyses if analysis.is_anomaly]
        anomalies.sort(key=lambda x: x.severity_score, reverse=True)
        
        top_issues = []
        
        for i, analysis in enumerate(anomalies[:3]):  # Top 3 issues
            # Determine alert severity
            if analysis.severity_score >= self.critical_threshold:
                alert_severity = AlertSeverity.CRITICAL
            elif analysis.severity_score >= self.warning_threshold:
                alert_severity = AlertSeverity.WARNING
            else:
                alert_severity = AlertSeverity.INFO
            
            # Generate recommended actions
            recommended_actions = self._generate_recommended_actions(analysis)
            
            # Assess business impact
            business_impact = self._assess_business_impact(analysis)
            
            # Determine confidence level
            if analysis.confidence >= self.high_confidence_threshold:
                confidence_level = ConfidenceLevel.HIGH
            elif analysis.confidence >= self.low_confidence_threshold:
                confidence_level = ConfidenceLevel.MEDIUM
            else:
                confidence_level = ConfidenceLevel.LOW
            
            # Create monitoring result
            result = MonitoringResult(
                alert_id=f"MON-{datetime.now().strftime('%Y%m%d%H%M%S')}-{i+1}",
                anomaly_detected=True,
                severity_score=analysis.severity_score,
                confidence_level=confidence_level,
                recommended_actions=recommended_actions,
                business_impact=business_impact,
                priority_rank=i + 1,
                reasoning=self._generate_monitoring_reasoning(analysis),
                created_at=datetime.now(),
                agent_id="monitoring_agent"
            )
            
            top_issues.append(result)
        
        self.top_issues = top_issues
        return top_issues
    
    def _generate_recommended_actions(self, analysis: MetricAnalysis) -> List[str]:
        """Generate actionable recommendations based on metric analysis"""
        
        actions = {
            'cpu_utilization': [
                "Check for runaway processes using top/htop",
                "Review recent deployments for performance issues",
                "Consider scaling up server resources",
                "Investigate high CPU consuming applications"
            ],
            'memory_usage': [
                "Investigate potential memory leaks in applications",
                "Restart services with high memory consumption",
                "Review application logs for memory-related errors",
                "Consider increasing available memory"
            ],
            'disk_usage': [
                "Clean up temporary files and logs",
                "Archive old data to secondary storage",
                "Review disk usage by directory (du -sh /*)",
                "Plan for additional storage capacity"
            ]
        }
        
        base_actions = actions.get(analysis.metric_name, [
            f"Monitor {analysis.metric_name} closely",
            "Review system logs for related errors",
            "Consider preventive maintenance"
        ])
        
        # Add urgency-based actions
        if analysis.severity_score > 0.9:
            base_actions.insert(0, "URGENT: Immediate investigation required")
        elif analysis.severity_score > 0.8:
            base_actions.insert(0, "HIGH PRIORITY: Address within 1 hour")
        
        return base_actions[:4]  # Return top 4 actions
    
    def _assess_business_impact(self, analysis: MetricAnalysis) -> str:
        """Assess business impact of the detected issue"""
        
        # Check if it affects critical systems
        resource = next((dp.get('resource', '') for dp in [{}]), '')
        is_critical_system = any(critical in resource for critical in self.critical_systems)
        
        if analysis.severity_score >= 0.9:
            if is_critical_system:
                return "Critical - Production services at risk"
            else:
                return "High - Service degradation likely"
        elif analysis.severity_score >= 0.7:
            if is_critical_system:
                return "High - Critical system performance impacted"
            else:
                return "Medium - User experience may be affected"
        else:
            return "Low - Monitoring recommended"
    
    def _generate_monitoring_reasoning(self, analysis: MetricAnalysis) -> str:
        """Generate human-readable reasoning for monitoring decision"""
        
        reasoning_parts = []
        
        # Current state
        reasoning_parts.append(f"{analysis.metric_name} at {analysis.current_value:.1f}%")
        
        # Threshold comparison
        if analysis.current_value > analysis.threshold_value:
            reasoning_parts.append(f"exceeds threshold ({analysis.threshold_value:.1f}%)")
        
        # Trend analysis
        if analysis.trend != "stable":
            reasoning_parts.append(f"trending {analysis.trend}")
        
        # Severity assessment
        if analysis.severity_score > 0.8:
            reasoning_parts.append("high severity detected")
        elif analysis.severity_score > 0.5:
            reasoning_parts.append("moderate severity")
        
        # Prediction
        reasoning_parts.append(f"Prediction: {analysis.prediction}")
        
        return "; ".join(reasoning_parts)
    
    def make_autonomous_decisions(self, top_issues: List[MonitoringResult]) -> List[Dict]:
        """Make autonomous decisions about preventive actions"""
        
        decisions = []
        
        for issue in top_issues:
            decision = {
                'alert_id': issue.alert_id,
                'autonomous_action': False,
                'action_taken': None,
                'reasoning': '',
                'timestamp': datetime.now()
            }
            
            # Autonomous action criteria (agent behavior guidelines)
            if (issue.confidence_level == ConfidenceLevel.HIGH and 
                issue.severity_score >= 0.8):
                
                # Determine autonomous action
                if issue.severity_score >= 0.9:
                    action = "create_critical_incident"
                    decision['reasoning'] = "Critical severity with high confidence - creating incident automatically"
                elif issue.priority_rank <= 2:
                    action = "create_preventive_ticket"
                    decision['reasoning'] = "Top priority issue with high confidence - creating preventive maintenance ticket"
                else:
                    action = "send_alert_notification"
                    decision['reasoning'] = "High confidence anomaly - sending proactive alert"
                
                decision['autonomous_action'] = True
                decision['action_taken'] = action
                issue.auto_executed = True
                
                print(f"🤖 Monitoring Agent: Autonomous action - {action}")
                
            else:
                decision['reasoning'] = f"Confidence {issue.confidence_level.value} - requires human review"
                print(f"👤 Monitoring Agent: Human review required - {issue.alert_id}")
            
            decisions.append(decision)
        
        return decisions
    
    def execute_preventive_actions(self, decisions: List[Dict]) -> List[Dict]:
        """Execute preventive actions (simulation for demo)"""
        
        results = []
        
        for decision in decisions:
            if not decision['autonomous_action']:
                continue
            
            action = decision['action_taken']
            result = {
                'alert_id': decision['alert_id'],
                'action': action,
                'success': True,
                'details': {},
                'timestamp': datetime.now()
            }
            
            if action == "create_critical_incident":
                incident_id = f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                result['details'] = {
                    'incident_id': incident_id,
                    'severity': 'P1',
                    'assigned_team': 'Infrastructure Team',
                    'sla_target': '4 hours'
                }
                print(f"🚨 Created critical incident {incident_id}")
                
            elif action == "create_preventive_ticket":
                ticket_id = f"REQ-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                result['details'] = {
                    'ticket_id': ticket_id,
                    'type': 'Preventive Maintenance',
                    'priority': 'High',
                    'assigned_team': 'Operations Team'
                }
                print(f"🔧 Created preventive maintenance ticket {ticket_id}")
                
            elif action == "send_alert_notification":
                result['details'] = {
                    'notification_sent': True,
                    'recipients': ['ops-team@company.com', 'infrastructure-alerts'],
                    'escalation_scheduled': '30 minutes'
                }
                print(f"📧 Sent proactive alert notification")
            
            results.append(result)
        
        return results
    
    def predict_future_issues(self, metrics_data: Dict, prediction_window_hours: int = 4) -> List[Dict]:
        """Predict potential issues in the next few hours based on current trends"""
        
        predictions = []
        
        for metric_name, data_points in metrics_data.items():
            if len(data_points) < 3:
                continue
            
            # Extract recent values for trend analysis
            recent_values = [point['value'] for point in data_points[-10:]]  # Last 10 points
            
            # Simple linear extrapolation
            if len(recent_values) >= 3:
                # Calculate trend slope
                x = list(range(len(recent_values)))
                y = recent_values
                n = len(x)
                
                if n > 1 and sum(xi**2 for xi in x) != (sum(x)**2 / n):
                    slope = (n * sum(x[i] * y[i] for i in range(n)) - sum(x) * sum(y)) / (n * sum(xi**2 for xi in x) - sum(x)**2)
                    intercept = (sum(y) - slope * sum(x)) / n
                    
                    # Predict future values
                    future_value = slope * (len(recent_values) + prediction_window_hours) + intercept
                    
                    # Check if prediction exceeds thresholds
                    threshold = self._get_metric_threshold(metric_name)
                    
                    if future_value > threshold:
                        risk_level = "HIGH" if future_value > threshold * 1.1 else "MEDIUM"
                        
                        predictions.append({
                            'metric_name': metric_name,
                            'current_value': recent_values[-1],
                            'predicted_value': future_value,
                            'threshold': threshold,
                            'risk_level': risk_level,
                            'time_to_threshold': self._calculate_time_to_threshold(recent_values, slope, intercept, threshold),
                            'confidence': min(0.9, 0.5 + (len(recent_values) / 20)),  # More data = higher confidence
                            'recommended_action': self._get_predictive_action(metric_name, future_value, threshold)
                        })
        
        # Sort by risk level and time to threshold
        predictions.sort(key=lambda x: (x['risk_level'] == 'HIGH', -x['time_to_threshold']))
        
        return predictions
    
    def _calculate_time_to_threshold(self, values: List[float], slope: float, intercept: float, threshold: float) -> float:
        """Calculate estimated time until threshold is reached (in hours)"""
        
        if slope <= 0:
            return float('inf')  # Not trending toward threshold
        
        current_x = len(values) - 1
        current_value = values[-1]
        
        # Solve: slope * x + intercept = threshold
        threshold_x = (threshold - intercept) / slope
        time_to_threshold = max(0, threshold_x - current_x)
        
        return time_to_threshold
    
    def _get_predictive_action(self, metric_name: str, predicted_value: float, threshold: float) -> str:
        """Get recommended preventive action based on prediction"""
        
        actions = {
            'cpu_utilization': 'Scale up compute resources or optimize high-CPU processes',
            'memory_usage': 'Increase memory allocation or restart memory-intensive services',
            'disk_usage': 'Clean up disk space or provision additional storage',
            'network_throughput': 'Optimize network configuration or increase bandwidth',
            'error_rate': 'Review recent deployments and application logs',
            'response_time': 'Optimize database queries and application performance'
        }
        
        return actions.get(metric_name, f'Monitor {metric_name} closely and prepare mitigation plan')
    
    def generate_capacity_recommendations(self, metrics_data: Dict) -> Dict:
        """Generate capacity planning recommendations based on usage trends"""
        
        recommendations = {
            'immediate_actions': [],
            'short_term_planning': [],
            'long_term_planning': [],
            'cost_optimization': []
        }
        
        for metric_name, data_points in metrics_data.items():
            if len(data_points) < 5:
                continue
            
            values = [point['value'] for point in data_points]
            current_value = values[-1]
            avg_value = sum(values) / len(values)
            max_value = max(values)
            
            # Immediate actions (>90% utilization)
            if current_value > 90:
                recommendations['immediate_actions'].append(
                    f"URGENT: {metric_name} at {current_value:.1f}% - immediate capacity increase needed"
                )
            
            # Short-term planning (trending upward, >75%)
            elif current_value > 75 and self._analyze_trend(values) == "increasing":
                recommendations['short_term_planning'].append(
                    f"{metric_name} trending up (current: {current_value:.1f}%) - plan capacity increase within 30 days"
                )
            
            # Long-term planning (average >60%)
            elif avg_value > 60:
                recommendations['long_term_planning'].append(
                    f"{metric_name} average utilization {avg_value:.1f}% - consider capacity planning for next quarter"
                )
            
            # Cost optimization (consistently low usage)
            elif max_value < 30 and avg_value < 20:
                recommendations['cost_optimization'].append(
                    f"{metric_name} underutilized (avg: {avg_value:.1f}%, max: {max_value:.1f}%) - consider downsizing"
                )
        
        return recommendations
    
    def detect_anomaly_patterns(self, metrics_data: Dict) -> List[Dict]:
        """Detect recurring anomaly patterns that might indicate systemic issues"""
        
        patterns = []
        
        for metric_name, data_points in metrics_data.items():
            if len(data_points) < 10:
                continue
            
            values = [point['value'] for point in data_points]
            timestamps = [datetime.fromisoformat(point['timestamp']) for point in data_points]
            
            # Detect periodic spikes
            spikes = []
            threshold = self._get_metric_threshold(metric_name)
            
            for i, value in enumerate(values):
                if value > threshold:
                    spikes.append({
                        'index': i,
                        'value': value,
                        'timestamp': timestamps[i]
                    })
            
            if len(spikes) >= 3:
                # Check for time-based patterns
                spike_hours = [spike['timestamp'].hour for spike in spikes]
                
                # Check if spikes occur at similar times
                from collections import Counter
                hour_counts = Counter(spike_hours)
                most_common_hour, count = hour_counts.most_common(1)[0]
                
                if count >= 2:  # At least 2 spikes at same hour
                    patterns.append({
                        'metric_name': metric_name,
                        'pattern_type': 'time_based_spikes',
                        'description': f'Recurring spikes around {most_common_hour:02d}:00',
                        'frequency': count,
                        'severity': 'HIGH' if count >= 3 else 'MEDIUM',
                        'recommendation': f'Investigate scheduled processes or peak usage at {most_common_hour:02d}:00'
                    })
        
        return patterns
    
    def get_performance_metrics(self) -> Dict:
        """Get agent performance metrics for monitoring"""
        return {
            'alerts_generated': len(self.alerts_generated),
            'top_issues_identified': len(self.top_issues),
            'autonomous_actions': sum(1 for issue in self.top_issues if issue.auto_executed),
            'false_positive_rate': self.false_positive_rate,
            'accuracy_score': self.accuracy_score,
            'critical_threshold': self.critical_threshold,
            'warning_threshold': self.warning_threshold
        }
    
    def run_proactive_analysis(self) -> Dict:
        """Run complete proactive monitoring analysis"""
        
        print("🔍 Monitoring Agent: Starting proactive analysis...")
        
        # Load sample metrics
        metrics_data = self.data_loader.load_metrics()
        
        if not metrics_data:
            print("❌ No metrics data available")
            return {'success': False, 'reason': 'No metrics data'}
        
        # Analyze metrics
        analyses = self.analyze_metrics(metrics_data)
        print(f"📊 Analyzed {len(analyses)} metrics")
        
        # Generate top 3 issues
        top_issues = self.generate_top_issues(analyses)
        print(f"⚠️ Identified {len(top_issues)} top priority issues")
        
        # Make autonomous decisions
        decisions = self.make_autonomous_decisions(top_issues)
        
        # Execute preventive actions
        action_results = self.execute_preventive_actions(decisions)
        
        # Generate predictions and capacity recommendations
        predictions = self.predict_future_issues(metrics_data)
        capacity_recommendations = self.generate_capacity_recommendations(metrics_data)
        anomaly_patterns = self.detect_anomaly_patterns(metrics_data)
        
        print(f"🔮 Generated {len(predictions)} predictions")
        print(f"📈 Found {len(anomaly_patterns)} anomaly patterns")
        
        return {
            'success': True,
            'analyses_count': len(analyses),
            'top_issues_count': len(top_issues),
            'autonomous_actions': len(action_results),
            'top_issues': top_issues,
            'action_results': action_results,
            'predictions': predictions,
            'capacity_recommendations': capacity_recommendations,
            'anomaly_patterns': anomaly_patterns
        }