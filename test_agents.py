#!/usr/bin/env python3
"""
Test runner for AI agents
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_correlation_agent():
    """Test the correlation agent"""
    try:
        from src.agents.correlation_agent import AutonomousCorrelationAgent
        from src.data.loader import DataLoader
        
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
        
        # Get correlation demo data
        demo_incidents = data_loader.get_correlation_demo_data()
        
        if len(demo_incidents) < 2:
            print("❌ Not enough demo incidents for correlation test")
            return
        
        print(f"\n🔍 Testing Correlation on {len(demo_incidents)} demo incidents:")
        print("-" * 50)
        
        # Test correlation between incidents
        target_incident = demo_incidents[0]
        other_incidents = demo_incidents[1:]
        
        print(f"\n📋 Target Incident: {target_incident.title}")
        print(f"   System: {target_incident.affected_system}")
        print(f"   Description: {target_incident.description[:100]}...")
        
        # Find similar incidents
        similar = agent.find_similar_incidents(target_incident, other_incidents)
        
        if similar:
            print(f"\n✅ Found {len(similar)} similar incidents:")
            for i, item in enumerate(similar[:3], 1):
                sim_inc = item['incident']
                score = item['similarity_score']
                reasoning = item['reasoning']
                print(f"\n   {i}. {sim_inc.title}")
                print(f"      Similarity: {score:.2f}")
                print(f"      Reasoning: {reasoning}")
            
            # Make correlation decision
            result = agent.make_correlation_decision(target_incident, similar)
            
            print(f"\n🤖 Autonomous Agent Decision:")
            print(f"   Action: {result.decision.value}")
            print(f"   Confidence: {result.confidence_level.value} ({result.correlation_score:.2f})")
            print(f"   Reasoning: {result.reasoning}")
            
            if result.should_execute_autonomously():
                print(f"\n✅ Executing autonomously (confidence > 80%)")
                action_result = agent.execute_correlation_action(result)
                print(f"   📝 Action completed: {action_result['action_taken']}")
                if action_result['details']:
                    for key, value in action_result['details'].items():
                        print(f"      {key}: {value}")
            else:
                print(f"\n👤 Requires human review (confidence < 80%)")
        else:
            print("\n❌ No similar incidents found")
        
        # Show performance metrics
        print(f"\n📈 Agent Performance Summary:")
        print("-" * 30)
        metrics = agent.get_performance_metrics()
        for key, value in metrics.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n✅ Correlation Agent test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing correlation agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_correlation_agent()