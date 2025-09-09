#!/usr/bin/env python3
"""
Basic OpenAI Agent Creation
Simple example showing how to create an agent with name, instructions, and model
"""

from openai import OpenAI
import os

def create_basic_agent():
    """Create a basic OpenAI agent"""
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create agent with name, instructions, and model
    agent = client.beta.assistants.create(
        name="My ITSM Agent",                    # Agent name
        instructions="""                        # Agent instructions
        You are a helpful IT Service Management assistant.
        Help users with incident management and IT support.
        Be professional and provide clear solutions.
        """,
        model="gpt-4o-mini"                     # AI model to use
    )
    
    return agent

def chat_with_agent(agent_id, message):
    """Chat with the agent"""
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create a conversation thread
    thread = client.beta.threads.create()
    
    # Add user message
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
    
    # Wait for response
    import time
    while run.status in ['queued', 'in_progress']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    # Get the response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value
    
    return response

def main():
    """Main function"""
    
    print("🤖 Creating Basic OpenAI Agent")
    print("=" * 40)
    
    try:
        # Create agent
        agent = create_basic_agent()
        print(f"✅ Agent created: {agent.name}")
        print(f"📋 Agent ID: {agent.id}")
        
        # Test the agent
        print("\n💬 Testing agent...")
        response = chat_with_agent(
            agent.id, 
            "Help me create an incident for a slow database server"
        )
        
        print(f"🤖 Agent Response: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
