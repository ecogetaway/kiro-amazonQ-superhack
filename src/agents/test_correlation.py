"""
Test script for Incident Correlation Agent
Demonstrates autonomous decision-making capabilities
"""

from correlation_agent import AutonomousCorrelationAgent
from ..data.loader import DataLoader

def test_correlation_agent():
    """Test the correlation agent with sample data"""
    
    print("🚀 Testing Autonomous Incident Correlation Agent")
    print("=" * 50)
    
    # Initialize agent and data
    agent = AutonomousCorrelationAgent()
    agent.initialize_model()
    
    data_loader = DataLoader()
    incidents = data_loader.load_incidents()
    
    if not incidents:
        print("❌ No sample data found. Run sample_generator.py first.")
        return
    
    print(f"📊 Loaded {len(incidents)} sample incidents")
    
    # Test correlation on first few incidents
    test_incidents = incidents[:5]
    existing_incidents = incidents[5:]
    
    print("\n🔍 Testing Correlation Analysis:")
    print("-" * 30)
    
    for incident in test_incidents:
        print(f"\n📋 Analyzing: {incident.title}")
        print(f"   System: {incident.affected_system}")
        print(f"   Severity: {incident.severity.value}")
        
        # Find similar incidents
        similar = agent.find_similar_incidents(incident, existing_incidents)
        
        if similar:
            print(f"   Found {len(similar)} similar incidents:")
            for item in similar[:3]:  # Show top 3
                sim_inc = item['incident']
                score = item['similarity_score']
                print(f"     • {sim_inc.title} (similarity: {score:.2f})")
            
            # Make correlation decision
            result = agent.make_correlation_decision(incident, similar)
            
            print(f"\n🤖 Agent Decision:")
            print(f"   Action: {result.decision.value}")
            print(f"   Confidence: {result.confidence_level.value}")
            print(f"   Reasoning: {result.reasoning}")
            
            if result.should_execute_autonomously():
                print("   ✅ Executing autonomously")
                action_result = agent.execute_correlation_action(result)
                print(f"   📝 Result: {action_result['details']}")
            else:
                print("   👤 Requires human review")
        else:
            print("   No similar incidents found")
    
    # Show performance metrics
    print(f"\n📈 Agent Performance Metrics:")
    metrics = agent.get_performance_metrics()
    for key, value in metrics.items():
        print(f"   {key}: {value}")

if __name__ == "__main__":
    test_correlation_agent()