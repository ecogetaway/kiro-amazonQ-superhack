"""
Autonomous Incident Correlation Agent
Independently analyzes, correlates, and groups incidents while making autonomous decisions
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import math

from ..models.incident import Incident, SeverityLevel
from ..models.correlation_result import CorrelationResult, CorrelationDecision, ConfidenceLevel
from ..data.loader import DataLoader

class AutonomousCorrelationAgent:
    """Agent that autonomously correlates incidents and makes grouping decisions"""
    
    def __init__(self):
        # ITIL standards from steering guidelines (adjusted for demo)
        self.correlation_threshold = 0.4  # Lowered for demo to show more correlations
        self.high_confidence_threshold = 0.8  # >80% for autonomous action
        self.low_confidence_threshold = 0.6   # <60% requires human escalation
        
        # Learning and adaptation
        self.learning_rate = 0.1
        self.feedback_history = []
        
        # Text similarity model for semantic analysis
        self.similarity_model = None
        self.data_loader = DataLoader()
        
        # Agent behavior tracking
        self.decisions_made = []
        self.accuracy_score = 0.0
        
        # Critical systems for escalation logic
        self.critical_systems = [
            "prod-db-01", "prod-web-01", "prod-web-02", 
            "load-balancer", "auth-service", "payment-gateway"
        ]
        
    def initialize_model(self):
        """Initialize the text similarity model (using fallback for demo)"""
        # For hackathon demo, use keyword-based similarity
        self.similarity_model = None
        print("📝 Correlation Agent: Using keyword-based similarity for demo")
    
    def analyze_incident_similarity(self, incident1: Incident, incident2: Incident) -> float:
        """Analyze semantic similarity between two incidents"""
        
        # Combine title and description for analysis
        text1 = f"{incident1.title} {incident1.description}"
        text2 = f"{incident2.title} {incident2.description}"
        
        # Use keyword-based similarity for hackathon demo
        similarity = self._keyword_similarity(text1, text2)
        
        # Boost similarity for same affected system (ITIL best practice)
        if incident1.affected_system == incident2.affected_system:
            similarity += 0.2
        
        # Boost for same user group (indicates common impact)
        if incident1.user_group == incident2.user_group:
            similarity += 0.1
        
        # Weight recent incidents higher (agent behavior guideline)
        time_diff = abs((incident1.created_at - incident2.created_at).total_seconds())
        if time_diff < 3600:  # Within 1 hour
            similarity += 0.1
        elif time_diff < 86400:  # Within 24 hours
            similarity += 0.05
        
        return min(1.0, similarity)  # Cap at 1.0
    
    def _keyword_similarity(self, text1: str, text2: str) -> float:
        """Enhanced keyword-based similarity calculation for demo"""
        
        # Enhanced technical terms with weights
        technical_terms = {
            # High-weight terms (critical system components)
            'database': 0.4, 'server': 0.4, 'network': 0.4, 'authentication': 0.4,
            # Medium-weight terms (common issues)
            'timeout': 0.3, 'connection': 0.3, 'slow': 0.3, 'error': 0.3, 'failure': 0.3,
            'unavailable': 0.3, 'memory': 0.3, 'cpu': 0.3, 'disk': 0.3,
            # Lower-weight terms (specific symptoms)
            'email': 0.2, 'login': 0.2, 'backup': 0.2, 'storage': 0.2, 'application': 0.2,
            'performance': 0.2, 'latency': 0.2, 'crash': 0.2, 'restart': 0.2
        }
        
        words1 = set(word.lower() for word in text1.split())
        words2 = set(word.lower() for word in text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        # Basic Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        base_similarity = len(intersection) / len(union) if union else 0.0
        
        # Weighted boost for technical terms
        tech_boost = 0.0
        for word in words1.intersection(words2):
            if word in technical_terms:
                tech_boost += technical_terms[word]
        
        base_similarity += tech_boost
        
        # Boost for exact phrase matches
        if any(phrase in text1.lower() and phrase in text2.lower() 
               for phrase in ['connection timeout', 'slow response', 'server error', 
                            'database error', 'email delivery', 'login failed']):
            base_similarity += 0.2
        
        return min(1.0, base_similarity)
    
    def find_similar_incidents(self, target_incident: Incident, 
                             existing_incidents: List[Incident]) -> List[Dict]:
        """Find incidents similar to the target incident"""
        
        similar_incidents = []
        
        for incident in existing_incidents:
            # Skip resolved/closed incidents and self
            if (incident.id == target_incident.id or 
                incident.status.value in ['Resolved', 'Closed']):
                continue
            
            similarity_score = self.analyze_incident_similarity(target_incident, incident)
            
            if similarity_score >= self.correlation_threshold:
                similar_incidents.append({
                    'incident': incident,
                    'similarity_score': similarity_score,
                    'reasoning': self._generate_similarity_reasoning(
                        target_incident, incident, similarity_score
                    )
                })
        
        # Sort by similarity score (highest first)
        similar_incidents.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similar_incidents
    
    def _generate_similarity_reasoning(self, incident1: Incident, incident2: Incident, 
                                     score: float) -> str:
        """Generate human-readable reasoning for correlation decision"""
        reasons = []
        
        if incident1.affected_system == incident2.affected_system:
            reasons.append(f"same affected system ({incident1.affected_system})")
        
        if incident1.user_group == incident2.user_group:
            reasons.append(f"same user group ({incident1.user_group})")
        
        # Check for common keywords
        words1 = set(incident1.description.lower().split())
        words2 = set(incident2.description.lower().split())
        common_words = words1.intersection(words2)
        
        if len(common_words) > 2:
            key_words = [w for w in common_words if len(w) > 4][:3]
            if key_words:
                reasons.append(f"common symptoms: {', '.join(key_words)}")
        
        time_diff = abs((incident1.created_at - incident2.created_at).total_seconds())
        if time_diff < 3600:
            reasons.append("occurred within 1 hour")
        elif time_diff < 86400:
            reasons.append("occurred within 24 hours")
        
        base_reason = f"Text similarity: {score:.2f}"
        if reasons:
            return f"{base_reason} ({'; '.join(reasons)})"
        else:
            return base_reason
    
    def make_correlation_decision(self, target_incident: Incident, 
                                similar_incidents: List[Dict]) -> CorrelationResult:
        """Makes autonomous decisions about correlation strength and actions"""
        
        if not similar_incidents:
            return CorrelationResult(
                incident_id=target_incident.id,
                similar_incidents=[],
                correlation_score=0.0,
                confidence_level=ConfidenceLevel.HIGH,
                decision=CorrelationDecision.NO_ACTION,
                reasoning="No similar incidents found",
                created_at=datetime.now(),
                agent_id="correlation_agent"
            )
        
        # Get the highest similarity score
        max_similarity = similar_incidents[0]['similarity_score']
        similar_incident_ids = [item['incident'].id for item in similar_incidents]
        
        # Determine confidence level based on agent behavior guidelines
        if max_similarity >= self.high_confidence_threshold:
            confidence = ConfidenceLevel.HIGH
        elif max_similarity >= self.low_confidence_threshold:
            confidence = ConfidenceLevel.MEDIUM
        else:
            confidence = ConfidenceLevel.LOW
        
        # Make decision based on ITIL standards and confidence
        decision = self._determine_correlation_action(
            target_incident, similar_incidents, confidence
        )
        
        # Generate escalation prediction
        escalation_prediction = self.predict_incident_escalation(target_incident, similar_incidents)
        
        # Generate reasoning
        reasoning = self._generate_decision_reasoning(
            target_incident, similar_incidents, decision, max_similarity
        )
        
        # Add escalation info to reasoning if significant
        if escalation_prediction['escalation_probability'] > 0.5:
            reasoning += f" | Escalation risk: {escalation_prediction['escalation_probability']:.1%}"
        
        result = CorrelationResult(
            incident_id=target_incident.id,
            similar_incidents=similar_incident_ids,
            correlation_score=max_similarity,
            confidence_level=confidence,
            decision=decision,
            reasoning=reasoning,
            created_at=datetime.now(),
            agent_id="correlation_agent"
        )
        
        # Store escalation prediction in result for later use
        result.escalation_prediction = escalation_prediction
        
        # Execute autonomously if confidence is high enough
        if result.should_execute_autonomously():
            result.auto_executed = True
            print(f"🤖 Correlation Agent: Autonomous action - {decision.value}")
            
            # Add escalation warning if needed
            if hasattr(result, 'escalation_prediction') and result.escalation_prediction['escalation_probability'] > 0.7:
                print(f"⚠️  High escalation risk detected: {result.escalation_prediction['escalation_probability']:.1%}")
        else:
            print(f"👤 Correlation Agent: Human review required - {decision.value}")
        
        self.decisions_made.append(result)
        return result
    
    def _determine_correlation_action(self, target_incident: Incident, 
                                    similar_incidents: List[Dict], 
                                    confidence: ConfidenceLevel) -> CorrelationDecision:
        """Determine what action to take based on correlation analysis"""
        
        if not similar_incidents:
            return CorrelationDecision.NO_ACTION
        
        # Count incidents by severity for escalation decisions
        high_severity_count = sum(1 for item in similar_incidents 
                                if item['incident'].severity in [SeverityLevel.P1, SeverityLevel.P2])
        
        total_similar = len(similar_incidents)
        
        # ITIL Problem Management: 3+ related incidents suggests a problem
        if total_similar >= 3 and confidence == ConfidenceLevel.HIGH:
            return CorrelationDecision.CREATE_PROBLEM
        
        # Also create problem if 2+ incidents affecting critical systems
        critical_incidents = sum(1 for item in similar_incidents 
                               if any(critical in item['incident'].affected_system 
                                     for critical in self.critical_systems))
        if critical_incidents >= 2 and confidence != ConfidenceLevel.LOW:
            return CorrelationDecision.CREATE_PROBLEM
        
        # Escalate severity if multiple high-severity incidents
        if (high_severity_count >= 2 and 
            target_incident.severity in [SeverityLevel.P3, SeverityLevel.P4]):
            return CorrelationDecision.ESCALATE_SEVERITY
        
        # Default: group incidents
        return CorrelationDecision.GROUP_INCIDENTS
    
    def _generate_decision_reasoning(self, target_incident: Incident, 
                                   similar_incidents: List[Dict],
                                   decision: CorrelationDecision, 
                                   max_similarity: float) -> str:
        """Generate reasoning for the correlation decision"""
        
        count = len(similar_incidents)
        
        if decision == CorrelationDecision.CREATE_PROBLEM:
            return (f"Found {count} similar incidents with {max_similarity:.2f} similarity. "
                   f"Meets ITIL criteria for problem creation (3+ related incidents).")
        
        elif decision == CorrelationDecision.ESCALATE_SEVERITY:
            high_sev_count = sum(1 for item in similar_incidents 
                               if item['incident'].severity in [SeverityLevel.P1, SeverityLevel.P2])
            return (f"Found {high_sev_count} high-severity similar incidents. "
                   f"Recommending severity escalation for broader impact.")
        
        elif decision == CorrelationDecision.GROUP_INCIDENTS:
            return (f"Found {count} similar incidents with {max_similarity:.2f} similarity. "
                   f"Grouping for coordinated response.")
        
        else:
            return "No correlation action required."
    
    def execute_correlation_action(self, result: CorrelationResult) -> Dict:
        """Execute the correlation decision (simulation for demo)"""
        
        action_result = {
            'success': True,
            'action_taken': result.decision.value,
            'timestamp': datetime.now(),
            'details': {}
        }
        
        if result.decision == CorrelationDecision.GROUP_INCIDENTS:
            # Simulate grouping incidents
            group_id = f"GRP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            action_result['details'] = {
                'group_id': group_id,
                'incidents_grouped': len(result.similar_incidents) + 1,
                'notification_sent': True
            }
            print(f"📋 Grouped {len(result.similar_incidents) + 1} incidents under {group_id}")
        
        elif result.decision == CorrelationDecision.CREATE_PROBLEM:
            # Simulate problem record creation
            problem_id = f"PRB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            action_result['details'] = {
                'problem_id': problem_id,
                'related_incidents': len(result.similar_incidents) + 1,
                'assigned_team': 'Infrastructure Team'
            }
            print(f"🔍 Created problem record {problem_id} for recurring incidents")
        
        elif result.decision == CorrelationDecision.ESCALATE_SEVERITY:
            # Simulate severity escalation
            action_result['details'] = {
                'original_severity': 'P3',
                'new_severity': 'P2',
                'escalation_reason': 'Multiple related high-severity incidents'
            }
            print(f"⬆️ Escalated incident severity due to correlation pattern")
        
        return action_result
    
    def learn_from_feedback(self, result: CorrelationResult, feedback: Dict):
        """Learn from technician feedback to improve future decisions"""
        
        feedback_entry = {
            'result': result,
            'feedback': feedback,
            'timestamp': datetime.now()
        }
        
        self.feedback_history.append(feedback_entry)
        
        # Adjust thresholds based on feedback
        if feedback.get('correct', False):
            # Positive feedback - slightly lower threshold for similar cases
            if result.confidence_level == ConfidenceLevel.MEDIUM:
                self.correlation_threshold = max(0.6, self.correlation_threshold - 0.02)
        else:
            # Negative feedback - raise threshold to be more conservative
            if result.confidence_level == ConfidenceLevel.HIGH:
                self.correlation_threshold = min(0.8, self.correlation_threshold + 0.02)
        
        # Update accuracy score
        correct_decisions = sum(1 for entry in self.feedback_history 
                              if entry['feedback'].get('correct', False))
        self.accuracy_score = correct_decisions / len(self.feedback_history)
        
        print(f"📈 Correlation Agent: Updated accuracy score to {self.accuracy_score:.2f}")
    
    def batch_correlation_analysis(self, incidents: List[Incident]) -> Dict:
        """Perform batch analysis of all incidents for comprehensive correlation mapping"""
        
        print("🔍 Correlation Agent: Running batch analysis...")
        
        correlation_matrix = {}
        incident_groups = []
        
        # Create correlation matrix
        for i, incident1 in enumerate(incidents):
            correlation_matrix[incident1.id] = {}
            
            for j, incident2 in enumerate(incidents):
                if i != j:
                    similarity = self.analyze_incident_similarity(incident1, incident2)
                    correlation_matrix[incident1.id][incident2.id] = similarity
        
        # Find incident clusters using similarity threshold
        processed_incidents = set()
        
        for incident in incidents:
            if incident.id in processed_incidents:
                continue
            
            # Find all incidents similar to this one
            group = [incident]
            processed_incidents.add(incident.id)
            
            for other_incident in incidents:
                if (other_incident.id not in processed_incidents and 
                    correlation_matrix[incident.id].get(other_incident.id, 0) >= self.correlation_threshold):
                    group.append(other_incident)
                    processed_incidents.add(other_incident.id)
            
            if len(group) > 1:
                incident_groups.append({
                    'group_id': f"GRP-{len(incident_groups)+1}",
                    'incidents': group,
                    'size': len(group),
                    'avg_similarity': sum(correlation_matrix[group[0].id].get(inc.id, 0) for inc in group[1:]) / max(1, len(group)-1)
                })
        
        return {
            'correlation_matrix': correlation_matrix,
            'incident_groups': incident_groups,
            'total_incidents': len(incidents),
            'grouped_incidents': sum(len(group['incidents']) for group in incident_groups),
            'ungrouped_incidents': len(incidents) - sum(len(group['incidents']) for group in incident_groups)
        }
    
    def predict_incident_escalation(self, incident: Incident, similar_incidents: List[Dict]) -> Dict:
        """Predict if incident is likely to escalate based on historical patterns"""
        
        if not similar_incidents:
            return {
                'escalation_probability': 0.0,
                'confidence': 0.0,
                'reasoning': 'No historical data available'
            }
        
        # Analyze escalation patterns in similar incidents
        escalated_count = 0
        total_similar = len(similar_incidents)
        
        for item in similar_incidents:
            similar_inc = item['incident']
            # Consider P1/P2 as escalated incidents
            if similar_inc.severity in [SeverityLevel.P1, SeverityLevel.P2]:
                escalated_count += 1
        
        escalation_probability = escalated_count / total_similar
        
        # Adjust based on current incident characteristics
        if incident.affected_system in self.critical_systems:
            escalation_probability += 0.2
        
        if incident.severity in [SeverityLevel.P3, SeverityLevel.P4] and escalation_probability > 0.6:
            escalation_probability += 0.1
        
        escalation_probability = min(1.0, escalation_probability)
        
        # Calculate confidence based on sample size and similarity scores
        avg_similarity = sum(item['similarity_score'] for item in similar_incidents) / total_similar
        confidence = min(0.95, avg_similarity * (total_similar / 10))  # More similar incidents = higher confidence
        
        reasoning = f"Based on {escalated_count}/{total_similar} similar incidents that escalated (avg similarity: {avg_similarity:.2f})"
        
        return {
            'escalation_probability': escalation_probability,
            'confidence': confidence,
            'reasoning': reasoning,
            'similar_escalations': escalated_count,
            'total_similar': total_similar
        }
    
    def get_performance_metrics(self) -> Dict:
        """Get agent performance metrics for monitoring"""
        return {
            'decisions_made': len(self.decisions_made),
            'accuracy_score': self.accuracy_score,
            'correlation_threshold': self.correlation_threshold,
            'autonomous_actions': sum(1 for d in self.decisions_made if d.auto_executed),
            'feedback_received': len(self.feedback_history)
        }