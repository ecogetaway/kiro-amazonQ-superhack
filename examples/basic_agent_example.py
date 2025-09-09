#!/usr/bin/env python3
"""
Basic OpenAI Agents SDK Examples
This file demonstrates the fundamental concepts of OpenAI Agents SDK
"""

# Note: This example assumes you have the OpenAI Agents SDK installed
# pip install openai-agents

from agents import Agent, Runner

def example_1_basic_agent():
    """Example 1: The simplest possible agent"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Agent")
    print("=" * 60)
    
    # Create a simple agent
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant"
    )
    
    # Run the agent with a simple task
    result = Runner.run_sync(agent, "Write a haiku about programming")
    
    print(f"Agent Name: {agent.name}")
    print(f"Instructions: {agent.instructions}")
    print(f"Response: {result.final_output}")
    print()

def example_2_specialized_agent():
    """Example 2: Agent with specific instructions"""
    print("=" * 60)
    print("EXAMPLE 2: Specialized Agent")
    print("=" * 60)
    
    # Create a specialized agent
    math_tutor = Agent(
        name="MathTutor",
        instructions="""
        You are a patient math tutor for beginners.
        
        Your approach:
        1. Always explain concepts step by step
        2. Use simple language and avoid jargon
        3. Provide concrete examples
        4. Ask if the student needs clarification
        5. Be encouraging and supportive
        """
    )
    
    # Ask the agent to explain a concept
    result = Runner.run_sync(
        math_tutor,
        "Explain what a variable is in programming, like I'm 8 years old"
    )
    
    print(f"Agent Name: {math_tutor.name}")
    print(f"Response: {result.final_output}")
    print()

def example_3_agent_with_personality():
    """Example 3: Agent with a specific personality"""
    print("=" * 60)
    print("EXAMPLE 3: Agent with Personality")
    print("=" * 60)
    
    # Create an agent with a specific personality
    chef_agent = Agent(
        name="ChefMario",
        instructions="""
        You are Chef Mario, an enthusiastic Italian chef who loves cooking!
        
        Your personality:
        - Always excited about food and cooking
        - Use Italian expressions (Mamma mia!, Bellissimo!, etc.)
        - Give detailed cooking instructions
        - Share cooking tips and secrets
        - Be warm and encouraging
        """
    )
    
    # Ask the chef for cooking advice
    result = Runner.run_sync(
        chef_agent,
        "I want to make pasta for dinner. Can you help me?"
    )
    
    print(f"Agent Name: {chef_agent.name}")
    print(f"Response: {result.final_output}")
    print()

def example_4_agent_memory():
    """Example 4: Agent that remembers context"""
    print("=" * 60)
    print("EXAMPLE 4: Agent with Memory")
    print("=" * 60)
    
    # Create an agent that should remember previous conversations
    personal_assistant = Agent(
        name="PersonalAssistant",
        instructions="""
        You are a personal assistant that remembers previous conversations.
        
        Your capabilities:
        - Remember user preferences and interests
        - Reference previous conversations when relevant
        - Build on past interactions
        - Be helpful and personalized
        """
    )
    
    # First conversation
    print("First conversation:")
    result1 = Runner.run_sync(
        personal_assistant,
        "Hi, I'm Alex. I love reading science fiction and I'm learning Python programming."
    )
    print(f"Response: {result1.final_output}")
    print()
    
    # Second conversation (should remember Alex and their interests)
    print("Second conversation (should remember Alex):")
    result2 = Runner.run_sync(
        personal_assistant,
        "Can you recommend a good book for me?"
    )
    print(f"Response: {result2.final_output}")
    print()

def example_5_error_handling():
    """Example 5: Safe agent execution with error handling"""
    print("=" * 60)
    print("EXAMPLE 5: Error Handling")
    print("=" * 60)
    
    def safe_agent_call(agent, message):
        """Safely call an agent with error handling"""
        try:
            result = Runner.run_sync(agent, message)
            return {
                "success": True,
                "output": result.final_output,
                "usage": result.usage if hasattr(result, 'usage') else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "I encountered an error. Please try again."
            }
    
    # Create a test agent
    test_agent = Agent(
        name="TestAgent",
        instructions="You are a helpful test agent"
    )
    
    # Test with various inputs
    test_cases = [
        "What's 2 + 2?",
        "Tell me a joke",
        "",  # Empty message
        "Help me with something very complex"
    ]
    
    for i, message in enumerate(test_cases, 1):
        print(f"Test Case {i}: '{message}'")
        result = safe_agent_call(test_agent, message)
        print(f"Success: {result['success']}")
        print(f"Output: {result['output']}")
        if result['usage']:
            print(f"Usage: {result['usage']}")
        print("-" * 40)

def example_6_agent_comparison():
    """Example 6: Compare responses from different agents"""
    print("=" * 60)
    print("EXAMPLE 6: Agent Comparison")
    print("=" * 60)
    
    # Create different types of agents
    formal_agent = Agent(
        name="FormalAgent",
        instructions="You are a formal, professional assistant. Always use proper language and be very polite."
    )
    
    casual_agent = Agent(
        name="CasualAgent", 
        instructions="You are a casual, friendly assistant. Use informal language and be relaxed."
    )
    
    technical_agent = Agent(
        name="TechnicalAgent",
        instructions="You are a technical expert. Use precise terminology and provide detailed explanations."
    )
    
    agents = [formal_agent, casual_agent, technical_agent]
    question = "Explain what a database is"
    
    print(f"Question: {question}")
    print()
    
    for agent in agents:
        result = Runner.run_sync(agent, question)
        print(f"{agent.name}:")
        print(f"{result.final_output}")
        print("-" * 40)

def main():
    """Run all examples"""
    print("OpenAI Agents SDK - Basic Examples")
    print("=" * 60)
    print()
    
    try:
        example_1_basic_agent()
        example_2_specialized_agent()
        example_3_agent_with_personality()
        example_4_agent_memory()
        example_5_error_handling()
        example_6_agent_comparison()
        
        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except ImportError:
        print("Error: OpenAI Agents SDK not installed.")
        print("Install it with: pip install openai-agents")
        print()
        print("Note: This is a demonstration file showing how the SDK would be used.")
        print("The actual SDK may have different syntax or requirements.")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("This might be because the OpenAI Agents SDK is not available or configured.")

if __name__ == "__main__":
    main()
