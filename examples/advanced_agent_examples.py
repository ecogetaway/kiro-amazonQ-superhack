#!/usr/bin/env python3
"""
Advanced OpenAI Agents SDK Examples
This file demonstrates advanced patterns and multi-agent workflows
"""

from agents import Agent, Runner, Tool
from datetime import datetime
import json

def example_1_agent_with_tools():
    """Example 1: Agent with custom tools"""
    print("=" * 60)
    print("EXAMPLE 1: Agent with Tools")
    print("=" * 60)
    
    # Define custom tools
    def calculate_area(length, width):
        """Calculate the area of a rectangle"""
        return length * width
    
    def get_weather(city):
        """Get weather information for a city (simulated)"""
        weather_data = {
            "New York": "72°F, partly cloudy",
            "London": "65°F, rainy", 
            "Tokyo": "78°F, sunny",
            "Paris": "68°F, overcast"
        }
        return weather_data.get(city, f"Weather data not available for {city}")
    
    def create_todo_item(task, priority="Medium"):
        """Create a todo item"""
        todo_id = f"TODO-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {
            "id": todo_id,
            "task": task,
            "priority": priority,
            "status": "Pending",
            "created_at": datetime.now().isoformat()
        }
    
    # Create tools
    tools = [
        Tool(name="calculate_area", function=calculate_area),
        Tool(name="get_weather", function=get_weather),
        Tool(name="create_todo_item", function=create_todo_item)
    ]
    
    # Create agent with tools
    helper_agent = Agent(
        name="HelperAgent",
        instructions="""
        You are a helpful assistant with access to various tools.
        
        You can:
        - Calculate areas of rectangles
        - Check weather for cities
        - Create todo items
        
        Always use the appropriate tool when the user asks for something you can do.
        Be helpful and explain what you're doing.
        """,
        tools=tools
    )
    
    # Test the agent with different requests
    requests = [
        "What's the area of a rectangle that's 5 feet by 3 feet?",
        "What's the weather like in Tokyo?",
        "Create a todo item for 'Buy groceries' with high priority"
    ]
    
    for request in requests:
        print(f"Request: {request}")
        result = Runner.run_sync(helper_agent, request)
        print(f"Response: {result.final_output}")
        print("-" * 40)

def example_2_multi_agent_workflow():
    """Example 2: Multiple agents working together"""
    print("=" * 60)
    print("EXAMPLE 2: Multi-Agent Workflow")
    print("=" * 60)
    
    # Create specialized agents
    researcher = Agent(
        name="Researcher",
        instructions="""
        You are a research specialist. Your job is to:
        - Gather comprehensive information on topics
        - Organize information clearly
        - Identify key points and facts
        - Be thorough and accurate
        """
    )
    
    writer = Agent(
        name="Writer",
        instructions="""
        You are a content writer. Your job is to:
        - Take research and turn it into engaging content
        - Use clear, accessible language
        - Structure information logically
        - Make content interesting and readable
        """
    )
    
    editor = Agent(
        name="Editor",
        instructions="""
        You are an editor. Your job is to:
        - Review and improve written content
        - Check for clarity and flow
        - Ensure proper structure
        - Make final improvements
        """
    )
    
    # Workflow: Research -> Write -> Edit
    topic = "How do solar panels work?"
    print(f"Topic: {topic}")
    print()
    
    # Step 1: Research
    print("Step 1: Research")
    research_result = Runner.run_sync(researcher, f"Research: {topic}")
    research_info = research_result.final_output
    print(f"Research: {research_info[:200]}...")
    print()
    
    # Step 2: Write
    print("Step 2: Writing")
    writing_result = Runner.run_sync(
        writer,
        f"Write an article about {topic} using this research: {research_info}"
    )
    article = writing_result.final_output
    print(f"Article: {article[:200]}...")
    print()
    
    # Step 3: Edit
    print("Step 3: Editing")
    editing_result = Runner.run_sync(
        editor,
        f"Edit and improve this article: {article}"
    )
    final_article = editing_result.final_output
    print(f"Final Article: {final_article[:200]}...")
    print()

def example_3_agent_chain():
    """Example 3: Agent chain pattern"""
    print("=" * 60)
    print("EXAMPLE 3: Agent Chain")
    print("=" * 60)
    
    def run_agent_chain(agents, initial_message):
        """Run multiple agents in sequence"""
        current_message = initial_message
        results = []
        
        for i, agent in enumerate(agents):
            print(f"Step {i+1}: {agent.name}")
            result = Runner.run_sync(agent, current_message)
            results.append(result)
            current_message = result.final_output
            print(f"Output: {result.final_output[:100]}...")
            print()
        
        return results
    
    # Create a chain of agents
    analyzer = Agent(
        name="Analyzer",
        instructions="Analyze the given problem and break it down into components"
    )
    
    planner = Agent(
        name="Planner",
        instructions="Create a step-by-step plan based on the analysis"
    )
    
    executor = Agent(
        name="Executor",
        instructions="Provide specific actions to implement the plan"
    )
    
    agents = [analyzer, planner, executor]
    problem = "I want to learn Python programming but don't know where to start"
    
    print(f"Problem: {problem}")
    print()
    
    results = run_agent_chain(agents, problem)
    
    print("Final Result:")
    print(results[-1].final_output)

def example_4_conditional_routing():
    """Example 4: Route to appropriate agent based on input"""
    print("=" * 60)
    print("EXAMPLE 4: Conditional Agent Routing")
    print("=" * 60)
    
    def route_to_agent(message, agents):
        """Route message to the most appropriate agent"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["math", "calculate", "number", "equation"]):
            return agents["math_agent"]
        elif any(word in message_lower for word in ["code", "program", "function", "debug"]):
            return agents["code_agent"]
        elif any(word in message_lower for word in ["cook", "recipe", "food", "kitchen"]):
            return agents["cooking_agent"]
        else:
            return agents["general_agent"]
    
    # Create specialized agents
    agents = {
        "math_agent": Agent(
            name="MathAgent",
            instructions="You are a math expert. Help with calculations, equations, and mathematical concepts."
        ),
        "code_agent": Agent(
            name="CodeAgent", 
            instructions="You are a programming expert. Help with coding, debugging, and software development."
        ),
        "cooking_agent": Agent(
            name="CookingAgent",
            instructions="You are a cooking expert. Help with recipes, cooking techniques, and food preparation."
        ),
        "general_agent": Agent(
            name="GeneralAgent",
            instructions="You are a general assistant. Help with a wide variety of topics."
        )
    }
    
    # Test different types of questions
    questions = [
        "What's 15 * 23?",
        "How do I write a Python function?",
        "What's a good recipe for chocolate cake?",
        "Tell me about the weather"
    ]
    
    for question in questions:
        print(f"Question: {question}")
        selected_agent = route_to_agent(question, agents)
        print(f"Selected Agent: {selected_agent.name}")
        
        result = Runner.run_sync(selected_agent, question)
        print(f"Response: {result.final_output}")
        print("-" * 40)

def example_5_agent_feedback_loop():
    """Example 5: Agent with feedback and improvement"""
    print("=" * 60)
    print("EXAMPLE 5: Agent Feedback Loop")
    print("=" * 60)
    
    # Create an agent that learns from feedback
    learning_agent = Agent(
        name="LearningAgent",
        instructions="""
        You are a learning agent that improves based on feedback.
        
        Your approach:
        1. Provide your best response
        2. Ask for feedback if needed
        3. Learn from corrections
        4. Improve future responses
        """
    )
    
    # Simulate a learning conversation
    conversation = [
        ("What's the capital of France?", "Paris"),
        ("That's correct! Now, what's the capital of Japan?", "Tokyo"),
        ("Perfect! What's the capital of Australia?", "Sydney"),
        ("Actually, it's Canberra. Can you remember that for next time?", "Yes, I'll remember that Canberra is the capital of Australia.")
    ]
    
    for i, (question, expected) in enumerate(conversation, 1):
        print(f"Round {i}:")
        print(f"Question: {question}")
        
        result = Runner.run_sync(learning_agent, question)
        print(f"Agent Response: {result.final_output}")
        print(f"Expected: {expected}")
        print("-" * 40)

def example_6_agent_monitoring():
    """Example 6: Monitor agent performance and usage"""
    print("=" * 60)
    print("EXAMPLE 6: Agent Monitoring")
    print("=" * 60)
    
    def monitor_agent_call(agent, message):
        """Monitor agent calls and collect metrics"""
        start_time = datetime.now()
        
        try:
            result = Runner.run_sync(agent, message)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            metrics = {
                "success": True,
                "duration_seconds": duration,
                "response_length": len(result.final_output),
                "usage": result.usage if hasattr(result, 'usage') else None,
                "timestamp": start_time.isoformat()
            }
            
            return result, metrics
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            metrics = {
                "success": False,
                "error": str(e),
                "duration_seconds": duration,
                "timestamp": start_time.isoformat()
            }
            
            return None, metrics
    
    # Create a test agent
    test_agent = Agent(
        name="TestAgent",
        instructions="You are a test agent for monitoring"
    )
    
    # Test with various messages
    test_messages = [
        "Hello, how are you?",
        "What's 2 + 2?",
        "Tell me a short story",
        "Explain quantum physics in simple terms"
    ]
    
    all_metrics = []
    
    for message in test_messages:
        print(f"Testing: {message}")
        result, metrics = monitor_agent_call(test_agent, message)
        
        print(f"Success: {metrics['success']}")
        print(f"Duration: {metrics['duration_seconds']:.2f} seconds")
        print(f"Response Length: {metrics['response_length']} characters")
        
        if result:
            print(f"Response: {result.final_output[:100]}...")
        
        all_metrics.append(metrics)
        print("-" * 40)
    
    # Summary statistics
    successful_calls = [m for m in all_metrics if m['success']]
    avg_duration = sum(m['duration_seconds'] for m in successful_calls) / len(successful_calls)
    avg_response_length = sum(m['response_length'] for m in successful_calls) / len(successful_calls)
    
    print("Summary Statistics:")
    print(f"Total Calls: {len(all_metrics)}")
    print(f"Successful Calls: {len(successful_calls)}")
    print(f"Average Duration: {avg_duration:.2f} seconds")
    print(f"Average Response Length: {avg_response_length:.0f} characters")

def main():
    """Run all advanced examples"""
    print("OpenAI Agents SDK - Advanced Examples")
    print("=" * 60)
    print()
    
    try:
        example_1_agent_with_tools()
        example_2_multi_agent_workflow()
        example_3_agent_chain()
        example_4_conditional_routing()
        example_5_agent_feedback_loop()
        example_6_agent_monitoring()
        
        print("=" * 60)
        print("All advanced examples completed successfully!")
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
