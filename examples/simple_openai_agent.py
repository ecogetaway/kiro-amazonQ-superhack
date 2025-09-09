#!/usr/bin/env python3
"""
Simple OpenAI Agent Example
Creating an agent with name, instructions, and model
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_simple_agent():
    """Create a simple OpenAI agent with name, instructions, and model"""
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create an agent (Assistant in OpenAI terminology)
    agent = client.beta.assistants.create(
        name="ITSM Helper Agent",
        instructions="""
        You are an IT Service Management (ITSM) specialist agent.
        
        Your role:
        - Help with incident management
        - Provide guidance on ITIL best practices
        - Assist with problem resolution
        - Give technical support advice
        
        Always be:
        - Professional and helpful
        - Clear in your explanations
        - Proactive in suggesting solutions
        - Empathetic to users experiencing issues
        """,
        model="gpt-4o-mini",  # You can use gpt-4, gpt-4-turbo, gpt-3.5-turbo, etc.
        tools=[{"type": "code_interpreter"}],  # Optional: add tools
    )
    
    return agent

def run_agent_conversation(agent_id):
    """Run a conversation with the agent"""
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create a thread (conversation)
    thread = client.beta.threads.create()
    
    # Example conversation
    messages = [
        "Hi! I'm having issues with our database server. Can you help?",
        "The server is responding slowly and users are complaining about timeouts.",
        "What should I do to troubleshoot this?"
    ]
    
    print("🤖 ITSM Helper Agent Conversation")
    print("=" * 50)
    
    for i, message in enumerate(messages, 1):
        print(f"\n👤 User: {message}")
        
        # Add message to thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )
        
        # Run the agent
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=agent_id
        )
        
        # Wait for completion
        import time
        while run.status in ['queued', 'in_progress', 'requires_action']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        # Get the response
        messages_response = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        # Print the latest assistant message
        assistant_message = messages_response.data[0]
        if assistant_message.role == "assistant":
            print(f"🤖 Agent: {assistant_message.content[0].text.value}")
        
        print("-" * 30)

def create_advanced_agent():
    """Create an advanced agent with more specific instructions"""
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    agent = client.beta.assistants.create(
        name="Incident Correlation Expert",
        instructions="""
        You are an expert in incident correlation and IT service management.
        
        Your expertise includes:
        1. Analyzing incident patterns and similarities
        2. Identifying root causes from multiple incidents
        3. Suggesting correlation strategies
        4. Recommending problem management actions
        
        When analyzing incidents:
        - Look for common symptoms, systems, or time patterns
        - Consider business impact and user experience
        - Suggest preventive measures
        - Provide clear reasoning for your recommendations
        
        Always structure your responses with:
        - Summary of the situation
        - Analysis of patterns
        - Specific recommendations
        - Next steps
        """,
        model="gpt-4o",  # Using GPT-4 for more complex reasoning
        tools=[
            {"type": "code_interpreter"},
            {"type": "file_search"}
        ]
    )
    
    return agent

def create_monitoring_agent():
    """Create a monitoring and alerting agent"""
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    agent = client.beta.assistants.create(
        name="Proactive Monitoring Agent",
        instructions="""
        You are a proactive monitoring and alerting specialist.
        
        Your responsibilities:
        1. Analyze system metrics and performance data
        2. Identify anomalies and potential issues
        3. Predict future problems based on trends
        4. Recommend preventive actions
        
        When monitoring systems:
        - Focus on business-critical metrics
        - Consider seasonal patterns and trends
        - Prioritize issues by business impact
        - Suggest capacity planning improvements
        
        Provide actionable insights with:
        - Current status assessment
        - Trend analysis
        - Risk predictions
        - Recommended actions with priorities
        """,
        model="gpt-4o-mini",
        tools=[{"type": "code_interpreter"}]
    )
    
    return agent

def main():
    """Main function to demonstrate agent creation"""
    
    print("🚀 Creating OpenAI Agents")
    print("=" * 50)
    
    try:
        # Check if API key is available
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY not found in environment variables")
            print("Please set your OpenAI API key:")
            print("export OPENAI_API_KEY='your-api-key-here'")
            return
        
        # Create different types of agents
        print("\n1. Creating Simple ITSM Helper Agent...")
        simple_agent = create_simple_agent()
        print(f"✅ Created agent: {simple_agent.name} (ID: {simple_agent.id})")
        
        print("\n2. Creating Incident Correlation Expert...")
        correlation_agent = create_advanced_agent()
        print(f"✅ Created agent: {correlation_agent.name} (ID: {correlation_agent.id})")
        
        print("\n3. Creating Proactive Monitoring Agent...")
        monitoring_agent = create_monitoring_agent()
        print(f"✅ Created agent: {monitoring_agent.name} (ID: {monitoring_agent.id})")
        
        # Run a conversation with the simple agent
        print("\n4. Running conversation with ITSM Helper Agent...")
        run_agent_conversation(simple_agent.id)
        
        print("\n🎉 All agents created successfully!")
        print("\nAgent IDs (save these for future use):")
        print(f"- ITSM Helper: {simple_agent.id}")
        print(f"- Correlation Expert: {correlation_agent.id}")
        print(f"- Monitoring Agent: {monitoring_agent.id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Valid OpenAI API key")
        print("2. Sufficient API credits")
        print("3. Internet connection")

if __name__ == "__main__":
    main()
