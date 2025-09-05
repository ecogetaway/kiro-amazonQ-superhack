"""
Autonomous Problem Management Agent
Independently identifies root causes, creates problem records, and orchestrates resolution
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from collections import defaultdict, Counter

from ..models.incident import Incident, SeverityLevel, IncidentStatus
from ..models.problem import Problem, ProblemStatus, ProblemPriority
from ..models.correlation_result import ProblemAnalysisResult, ConfidenceLevel
from ..data.loader import DataLoader

class AutonomousProblemAgent:
    """Agent that autonomously manages problems and coordinates resolution activities"""
    
    def __init__(self):
        # ITIL Problem Management standards from steering guidelines
        self.pattern_threshold = 3  # Minimum incidents to identify pattern (ITIL standard)
        self.confidence_threshold = 0.8  # High confidence for autonomous problem creation
        self.time_window_hours = 24  # Time window for pattern analysis
        
        # Problem creation criteria (ITIL standards)
        self.auto_create_criteria = {
            'min_incidents': 3,
            'high_severity_threshold': 2,  # 2+ P1/P2 incidents
            'user_impact_threshold': 100,  # 100+ users affected
            'recurring_pattern_confidence': 0.8
        }
        
        # Agent behavior tracking
        self.problems_created = []
        self.patterns_analyzed = []
        self.resolution_activities = []
        
        self.data_loader = DataLoader()
    
    def analyze_incident_patterns(self, incidents: List[Incident]) -> List[Dict]:
        """Analyze incidents for recurring patterns that indicate underlying problems"""
        
        if len(incidents) < self.pattern_threshold:
            return []
        
        patterns = []
        
        # Group incidents by various criteria for pattern analysis
        system_patterns = self._analyze_system_patterns(incidents)
        symptom_patterns = self._analyze_symptom_patterns(incidents)
        temporal_patterns = self._analyze_temporal_patterns(incidents)
        
        patterns.extend(system_patterns)
        patterns.extend(symptom_patterns)
        patterns.extend(temporal_patterns)
        
        # Filter patterns that meet ITIL criteria
        significant_patterns = [p for p in patterns if self._meets_problem_criteria(p)]
        
        return significant_patterns
    
    def _analyze_system_patterns(self, incidents: List[Incident]) -> List[Dict]:
        """Analyze patterns by affected system"""
        
        system_groups = defaultdict(list)
        
        # Group incidents by affected system
        for incident in incidents:
            system_groups[incident.affected_system].append(incident)
        
        patterns = []
        
        for system, system_incidents in system_groups.items():
            if len(system_incidents) >= self.pattern_threshold:
                pattern = self._create_pattern_analysis(
                    pattern_type="system",
                    pattern_key=system,
                    incidents=system_incidents,
                    description=f"Multiple incidents affecting {system}"
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_symptom_patterns(self, incidents: List[Incident]) -> List[Dict]:
        """Analyze patterns by common symptoms/keywords"""
        
        # Extract key symptoms from incident descriptions
        symptom_keywords = [
            'timeout', 'connection', 'slow', 'error', 'failure', 
            'unavailable', 'crash', 'memory', 'cpu', 'disk'
        ]
        
        symptom_groups = defaultdict(list)
        
        for incident in incidents:
            description_lower = incident.description.lower()
            title_lower = incident.title.lower()
            
            for symptom in symptom_keywords:
                if symptom in description_lower or symptom in title_lower:
                    symptom_groups[symptom].append(incident)
        
        patterns = []
        
        for symptom, symptom_incidents in symptom_groups.items():
            if len(symptom_incidents) >= self.pattern_threshold:
                pattern = self._create_pattern_analysis(
                    pattern_type="symptom",
                    pattern_key=symptom,
                    incidents=symptom_incidents,
                    description=f"Multiple incidents with '{symptom}' symptoms"
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_temporal_patterns(self, incidents: List[Incident]) -> List[Dict]:
        """Analyze patterns by timing (recurring incidents)"""
        
        # Sort incidents by creation time
        sorted_incidents = sorted(incidents, key=lambda x: x.created_at)
        
        patterns = []
        
        # Look for clusters of incidents within time windows
        for i in range(len(sorted_incidents) - self.pattern_threshold + 1):
            window_incidents = []
            start_time = sorted_incidents[i].created_at
            
            for j in range(i, len(sorted_incidents)):
                incident = sorted_incidents[j]
                time_diff = (incident.created_at - start_time).total_seconds() / 3600
                
                if time_diff <= self.time_window_hours:
                    window_incidents.append(incident)
                else:
                    break
            
            if len(window_incidents) >= self.pattern_threshold:
                pattern = self._create_pattern_analysis(
                    pattern_type="temporal",
                    pattern_key=f"{self.time_window_hours}h_cluster",
                    incidents=window_incidents,
                    description=f"{len(window_incidents)} incidents within {self.time_window_hours} hours"
                )
                patterns.append(pattern)
        
        return patterns
    
    def _create_pattern_analysis(self, pattern_type: str, pattern_key: str, 
                               incidents: List[Incident], description: str) -> Dict:
        """Create a pattern analysis result"""
        
        # Calculate pattern confidence based on various factors
        confidence = self._calculate_pattern_confidence(incidents, pattern_type)
        
        # Determine severity based on incident severities
        severity_counts = Counter(inc.severity for inc in incidents)
        high_severity_count = (severity_counts.get(SeverityLevel.P1, 0) + 
                             severity_counts.get(SeverityLevel.P2, 0))
        
        # Estimate user impact
        unique_user_groups = set(inc.user_group for inc in incidents)
        estimated_users_affected = len(unique_user_groups) * 50  # Rough estimate
        
        return {
            'pattern_id': f"{pattern_type}_{pattern_key}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'pattern_type': pattern_type,
            'pattern_key': pattern_key,
            'description': description,
            'incidents': incidents,
            'incident_count': len(incidents),
            'confidence': confidence,
            'high_severity_count': high_severity_count,
            'estimated_users_affected': estimated_users_affected,
            'time_span': self._calculate_time_span(incidents),
            'affected_systems': list(set(inc.affected_system for inc in incidents)),
            'created_at': datetime.now()
        }
    
    def _calculate_pattern_confidence(self, incidents: List[Incident], pattern_type: str) -> float:
        """Calculate confidence score for pattern recognition"""
        
        base_confidence = 0.5
        
        # More incidents = higher confidence
        incident_boost = min(0.3, len(incidents) * 0.05)
        base_confidence += incident_boost
        
        # High severity incidents boost confidence
        high_severity_count = sum(1 for inc in incidents 
                                if inc.severity in [SeverityLevel.P1, SeverityLevel.P2])
        severity_boost = min(0.2, high_severity_count * 0.1)
        base_confidence += severity_boost
        
        # Recent incidents boost confidence
        recent_incidents = sum(1 for inc in incidents 
                             if (datetime.now() - inc.created_at).total_seconds() < 86400)
        recency_boost = min(0.15, recent_incidents * 0.05)
        base_confidence += recency_boost
        
        # Pattern type specific boosts
        if pattern_type == "system":
            base_confidence += 0.1  # System patterns are more reliable
        elif pattern_type == "temporal":
            base_confidence += 0.05  # Temporal clustering is significant
        
        return min(1.0, base_confidence)
    
    def _calculate_time_span(self, incidents: List[Incident]) -> float:
        """Calculate time span of incidents in hours"""
        if len(incidents) < 2:
            return 0.0
        
        times = [inc.created_at for inc in incidents]
        return (max(times) - min(times)).total_seconds() / 3600
    
    def _meets_problem_criteria(self, pattern: Dict) -> bool:
        """Check if pattern meets ITIL problem creation criteria"""
        
        criteria = self.auto_create_criteria
        
        # Must have minimum incidents
        if pattern['incident_count'] < criteria['min_incidents']:
            return False
        
        # High confidence required
        if pattern['confidence'] < criteria['recurring_pattern_confidence']:
            return False
        
        # Check for high severity incidents or high user impact
        meets_severity = pattern['high_severity_count'] >= criteria['high_severity_threshold']
        meets_impact = pattern['estimated_users_affected'] >= criteria['user_impact_threshold']
        
        return meets_severity or meets_impact
    
    def make_problem_creation_decision(self, pattern: Dict) -> ProblemAnalysisResult:
        """Make autonomous decision about creating a problem record"""
        
        should_create = self._meets_problem_criteria(pattern)
        confidence_level = (
            ConfidenceLevel.HIGH if pattern['confidence'] >= 0.8 else
            ConfidenceLevel.MEDIUM if pattern['confidence'] >= 0.6 else
            ConfidenceLevel.LOW
        )
        
        # Generate root cause hypothesis
        root_cause = self._generate_root_cause_hypothesis(pattern)
        
        # Generate preventive measures
        preventive_measures = self._generate_preventive_measures(pattern)
        
        # Create reasoning
        reasoning = self._generate_problem_decision_reasoning(pattern, should_create)
        
        result = ProblemAnalysisResult(
            pattern_id=pattern['pattern_id'],
            related_incidents=[inc.id for inc in pattern['incidents']],
            pattern_confidence=pattern['confidence'],
            should_create_problem=should_create,
            root_cause_hypothesis=root_cause,
            preventive_measures=preventive_measures,
            reasoning=reasoning,
            created_at=datetime.now(),
            agent_id="problem_agent"
        )
        
        # Execute autonomously if criteria met
        if result.meets_problem_creation_criteria():
            result.auto_executed = True
            print(f"🔍 Problem Agent: Autonomous problem creation - {pattern['description']}")
        else:
            print(f"👤 Problem Agent: Human review required - {pattern['description']}")
        
        self.patterns_analyzed.append(result)
        return result
    
    def _generate_root_cause_hypothesis(self, pattern: Dict) -> str:
        """Generate root cause hypothesis based on pattern analysis"""
        
        pattern_type = pattern['pattern_type']
        pattern_key = pattern['pattern_key']
        
        if pattern_type == "system":
            return f"Underlying infrastructure issue with {pattern_key} causing recurring failures"
        
        elif pattern_type == "symptom":
            symptom_causes = {
                'timeout': 'Network latency or resource contention issues',
                'connection': 'Network connectivity or service availability problems',
                'slow': 'Performance degradation due to resource constraints',
                'memory': 'Memory leak or insufficient memory allocation',
                'cpu': 'CPU bottleneck or inefficient processing',
                'disk': 'Storage capacity or I/O performance issues'
            }
            return symptom_causes.get(pattern_key, f"Recurring {pattern_key} issues indicate systemic problem")
        
        elif pattern_type == "temporal":
            return "Time-clustered incidents suggest common trigger event or cascading failure"
        
        else:
            return "Pattern analysis indicates underlying systemic issue requiring investigation"
    
    def _generate_preventive_measures(self, pattern: Dict) -> List[str]:
        """Generate preventive measures based on pattern analysis"""
        
        measures = []
        pattern_type = pattern['pattern_type']
        pattern_key = pattern['pattern_key']
        
        if pattern_type == "system":
            measures = [
                f"Conduct comprehensive health check of {pattern_key}",
                f"Review {pattern_key} configuration and capacity planning",
                f"Implement enhanced monitoring for {pattern_key}",
                "Schedule preventive maintenance window"
            ]
        
        elif pattern_type == "symptom":
            symptom_measures = {
                'timeout': [
                    "Review and optimize timeout configurations",
                    "Implement connection pooling and retry logic",
                    "Monitor network latency and bandwidth"
                ],
                'memory': [
                    "Implement memory leak detection tools",
                    "Review application memory management",
                    "Schedule regular service restarts"
                ],
                'cpu': [
                    "Optimize high-CPU processes and queries",
                    "Implement CPU usage monitoring and alerting",
                    "Consider horizontal scaling options"
                ]
            }
            measures = symptom_measures.get(pattern_key, [
                f"Implement monitoring for {pattern_key} symptoms",
                "Conduct root cause analysis",
                "Develop standard operating procedures"
            ])
        
        else:
            measures = [
                "Implement comprehensive incident correlation monitoring",
                "Review change management processes",
                "Enhance system dependency mapping",
                "Develop incident response playbooks"
            ]
        
        return measures
    
    def _generate_problem_decision_reasoning(self, pattern: Dict, should_create: bool) -> str:
        """Generate reasoning for problem creation decision"""
        
        if should_create:
            return (f"Pattern meets ITIL problem creation criteria: "
                   f"{pattern['incident_count']} incidents, "
                   f"{pattern['high_severity_count']} high-severity, "
                   f"~{pattern['estimated_users_affected']} users affected, "
                   f"confidence: {pattern['confidence']:.2f}")
        else:
            return (f"Pattern does not meet autonomous creation criteria: "
                   f"{pattern['incident_count']} incidents (need {self.auto_create_criteria['min_incidents']}), "
                   f"confidence: {pattern['confidence']:.2f} (need {self.auto_create_criteria['recurring_pattern_confidence']})")
    
    def create_and_manage_problem(self, analysis_result: ProblemAnalysisResult) -> Problem:
        """Create problem record and manage its lifecycle"""
        
        problem_id = f"PRB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Determine priority based on incident severity and impact
        incidents = self.data_loader.load_incidents()
        related_incidents = [inc for inc in incidents if inc.id in analysis_result.related_incidents]
        
        high_severity_count = sum(1 for inc in related_incidents 
                                if inc.severity in [SeverityLevel.P1, SeverityLevel.P2])
        
        if high_severity_count >= 2:
            priority = ProblemPriority.CRITICAL
        elif high_severity_count >= 1:
            priority = ProblemPriority.HIGH
        else:
            priority = ProblemPriority.MEDIUM
        
        # Create problem record
        problem = Problem(
            id=problem_id,
            title=f"Recurring incidents: {analysis_result.root_cause_hypothesis}",
            description=f"Problem created from pattern analysis of {len(analysis_result.related_incidents)} related incidents",
            status=ProblemStatus.INVESTIGATING,
            priority=priority,
            related_incidents=analysis_result.related_incidents,
            created_at=datetime.now(),
            root_cause=analysis_result.root_cause_hypothesis,
            preventive_measures=analysis_result.preventive_measures,
            assigned_team="Infrastructure Team",
            owner="Problem Manager",
            auto_created=True,
            pattern_confidence=analysis_result.pattern_confidence
        )
        
        self.problems_created.append(problem)
        
        print(f"📋 Created problem record {problem_id}")
        print(f"   Priority: {priority.value}")
        print(f"   Related incidents: {len(analysis_result.related_incidents)}")
        print(f"   Root cause hypothesis: {analysis_result.root_cause_hypothesis}")
        
        return problem
    
    def orchestrate_resolution_activities(self, problem: Problem) -> Dict:
        """Orchestrate resolution activities across teams (simulation for demo)"""
        
        activities = {
            'problem_id': problem.id,
            'status': problem.status.value,
            'activities_initiated': [],
            'teams_notified': [],
            'timeline': []
        }
        
        # Simulate orchestration activities
        if problem.priority in [ProblemPriority.CRITICAL, ProblemPriority.HIGH]:
            activities['teams_notified'] = [
                'Infrastructure Team',
                'Application Team', 
                'Network Team',
                'Management'
            ]
            
            activities['activities_initiated'] = [
                'Emergency response team assembled',
                'Root cause analysis initiated',
                'Stakeholder communication started',
                'Preventive measures planning begun'
            ]
        else:
            activities['teams_notified'] = ['Infrastructure Team']
            activities['activities_initiated'] = [
                'Investigation assigned to team',
                'Root cause analysis scheduled'
            ]
        
        # Create timeline
        activities['timeline'] = [
            f"{datetime.now().strftime('%H:%M')} - Problem record created",
            f"{(datetime.now() + timedelta(minutes=5)).strftime('%H:%M')} - Teams notified",
            f"{(datetime.now() + timedelta(minutes=15)).strftime('%H:%M')} - Investigation started",
            f"{(datetime.now() + timedelta(hours=2)).strftime('%H:%M')} - Root cause analysis in progress"
        ]
        
        self.resolution_activities.append(activities)
        
        print(f"🎯 Orchestrating resolution for {problem.id}")
        for team in activities['teams_notified']:
            print(f"   📧 Notified: {team}")
        for activity in activities['activities_initiated']:
            print(f"   🔄 {activity}")
        
        return activities
    
    def get_performance_metrics(self) -> Dict:
        """Get agent performance metrics"""
        return {
            'problems_created': len(self.problems_created),
            'patterns_analyzed': len(self.patterns_analyzed),
            'resolution_activities': len(self.resolution_activities),
            'pattern_threshold': self.pattern_threshold,
            'confidence_threshold': self.confidence_threshold,
            'auto_creation_rate': sum(1 for p in self.patterns_analyzed if p.auto_executed) / max(1, len(self.patterns_analyzed))
        }