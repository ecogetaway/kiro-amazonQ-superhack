#!/usr/bin/env python3
"""
Learning OpenAI Agents - General Examples
Pure learning examples for understanding OpenAI agents concepts
"""

from openai import OpenAI
import os
import time

def example_1_basic_agent():
    """Example 1: The simplest possible agent"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Agent")
    print("=" * 60)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create a simple agent
    agent = client.beta.assistants.create(
        name="Simple Helper",
        instructions="You are a helpful assistant. Answer questions clearly and be friendly.",
        model="gpt-4o-mini"
    )
    
    print(f"✅ Created agent: {agent.name}")
    print(f"📋 Agent ID: {agent.id}")
    
    # Test the agent
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="What's the capital of France?"
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=agent.id
    )
    
    # Wait for completion
    while run.status in ['queued', 'in_progress']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    # Get response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value
    
    print(f"🤖 Agent Response: {response}")
    return agent

def example_2_agent_with_personality():
    """Example 2: Agent with specific personality"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Agent with Personality")
    print("=" * 60)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create an agent with personality
    agent = client.beta.assistants.create(
        name="Chef Mario",
        instructions="""
        You are Chef Mario, an enthusiastic Italian chef!
        
        Your personality:
        - Always excited about food and cooking
        - Use Italian expressions (Mamma mia!, Bellissimo!, etc.)
        - Give detailed cooking instructions
        - Share cooking tips and secrets
        - Be warm and encouraging
        """,
        model="gpt-4o-mini"
    )
    
    print(f"✅ Created agent: {agent.name}")
    
    # Test the agent
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="I want to make pasta for dinner. Can you help me?"
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=agent.id
    )
    
    while run.status in ['queued', 'in_progress']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value
    
    print(f"🤖 Chef Mario: {response}")
    return agent

def example_3_agent_with_tools():
    """Example 3: Agent with custom tools"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Agent with Tools")
    print("=" * 60)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create agent with tools
    agent = client.beta.assistants.create(
        name="Calculator Agent",
        instructions="""
        You are a helpful calculator agent.
        You can perform mathematical calculations and provide explanations.
        Always show your work step by step.
        """,
        model="gpt-4o-mini",
        tools=[{"type": "code_interpreter"}]  # This allows the agent to run code
    )
    
    print(f"✅ Created agent: {agent.name}")
    
    # Test the agent
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Calculate the area of a circle with radius 5. Show me the formula and steps."
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=agent.id
    )
    
    while run.status in ['queued', 'in_progress']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value
    
    print(f"🤖 Calculator Agent: {response}")
    return agent

def example_4_different_models():
    """Example 4: Compare different models"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Different Models")
    print("=" * 60)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    agents = {}
    
    # Create agents with different models
    for model in models:
        agent = client.beta.assistants.create(
            name=f"Agent-{model}",
            instructions="You are a helpful assistant. Answer questions clearly and concisely.",
            model=model
        )
        agents[model] = agent
        print(f"✅ Created {agent.name} with model {model}")
    
    # Test all agents with the same question
    question = "Explain quantum computing in simple terms"
    print(f"\n📝 Question: {question}")
    
    for model, agent in agents.items():
        print(f"\n🤖 {agent.name} ({model}):")
        
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )
        
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=agent.id
        )
        
        while run.status in ['queued', 'in_progress']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        
        print(f"Response: {response[:200]}...")  # Show first 200 characters
    
    return agents

def example_5_conversation_flow():
    """Example 5: Multi-turn conversation"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Multi-turn Conversation")
    print("=" * 60)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create a conversational agent
    agent = client.beta.assistants.create(
        name="Conversation Agent",
        instructions="""
        You are a friendly conversational agent.
        Remember what we've talked about and build on previous messages.
        Be engaging and ask follow-up questions when appropriate.
        """,
        model="gpt-4o-mini"
    )
    
    print(f"✅ Created agent: {agent.name}")
    
    # Create a thread for the conversation
    thread = client.beta.threads.create()
    
    # Multi-turn conversation
    conversation = [
        "Hi! I'm learning about AI agents. Can you help me understand what they are?",
        "That's interesting! How do I create my own agent?",
        "What are some common use cases for AI agents?",
        "Thanks! Can you give me a simple example of agent code?"
    ]
    
    print("\n💬 Starting conversation...")
    
    for i, message in enumerate(conversation, 1):
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
            assistant_id=agent.id
        )
        
        # Wait for completion
        while run.status in ['queued', 'in_progress']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        # Get the response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        
        print(f"🤖 Agent: {response}")
        print("-" * 40)
    
    return agent

def main():
    """Run all examples"""
    print("🚀 Learning OpenAI Agents - General Examples")
    print("=" * 60)
    
    try:
        # Check API key
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY not found")
            print("Please set your API key: export OPENAI_API_KEY='your-key'")
            return
        
        # Run examples
        agent1 = example_1_basic_agent()
        agent2 = example_2_agent_with_personality()
        agent3 = example_3_agent_with_tools()
        agents4 = example_4_different_models()
        agent5 = example_5_conversation_flow()
        
        print("\n" + "=" * 60)
        print("🎉 All examples completed!")
        print("=" * 60)
        
        print("\n📋 Created Agents:")
        print(f"- {agent1.name}: {agent1.id}")
        print(f"- {agent2.name}: {agent2.id}")
        print(f"- {agent3.name}: {agent3.id}")
        for model, agent in agents4.items():
            print(f"- {agent.name}: {agent.id}")
        print(f"- {agent5.name}: {agent5.id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have a valid OpenAI API key and sufficient credits.")

if __name__ == "__main__":
    main()
