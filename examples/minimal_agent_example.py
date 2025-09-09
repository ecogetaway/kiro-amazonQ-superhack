#!/usr/bin/env python3
"""
Minimal OpenAI Agent Example
Just the basics: name, instructions, model
"""

from openai import OpenAI
import os

def create_agent():
    """Create an agent with name, instructions, and model"""
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    agent = client.beta.assistants.create(
        name="My Learning Agent",           # Agent name
        instructions="""                   # Agent instructions
        You are a helpful learning assistant.
        Explain things clearly and provide examples.
        """,
        model="gpt-4o-mini"               # AI model
    )
    
    return agent

def chat(agent_id, message):
    """Chat with the agent"""
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create conversation
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )
    
    # Run agent
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=agent_id
    )
    
    # Wait for response
    import time
    while run.status in ['queued', 'in_progress']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    # Get response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

def main():
    """Main function"""
    
    print("🤖 Minimal OpenAI Agent Example")
    print("=" * 40)
    
    try:
        # Create agent
        agent = create_agent()
        print(f"✅ Agent created: {agent.name}")
        print(f"📋 ID: {agent.id}")
        
        # Test
        response = chat(agent.id, "What is machine learning?")
        print(f"\n🤖 Response: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
