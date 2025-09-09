# OpenAI Agents SDK Tutorial for Beginners

## Table of Contents
1. [Introduction](#introduction)
2. [Basic Concepts](#basic-concepts)
3. [Simple Examples](#simple-examples)
4. [Advanced Patterns](#advanced-patterns)
5. [Integration with Your Project](#integration-with-your-project)
6. [Best Practices](#best-practices)

## Introduction

The OpenAI Agents SDK allows you to create AI agents that can:
- Make autonomous decisions
- Execute tasks independently
- Coordinate with other agents
- Learn from their actions

Think of an agent as a specialized AI assistant that can work on its own to complete specific tasks.

## Basic Concepts

### 1. Agent
An `Agent` is like a specialized worker with:
- **Name**: How you identify the agent
- **Instructions**: What the agent should do and how it should behave
- **Tools**: Functions the agent can call to perform actions
- **Memory**: What the agent remembers from previous interactions

### 2. Runner
A `Runner` executes agents and manages:
- **Synchronous execution**: `run_sync()` - waits for completion
- **Asynchronous execution**: `run_async()` - doesn't block other code
- **Result handling**: Returns structured results with outputs and metadata

### 3. Result
When an agent completes a task, you get a `Result` object containing:
- **final_output**: The main response from the agent
- **messages**: All conversation messages
- **usage**: Token usage statistics
- **metadata**: Additional information about the execution

## Simple Examples

### Example 1: Basic Agent (Your Code)
```python
from agents import Agent, Runner

# Create a simple agent
agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant"
)

# Run the agent synchronously
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Output:
# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
```

**What's happening here:**
1. We create an agent with a name and basic instructions
2. We use `Runner.run_sync()` to execute the agent with a specific task
3. The agent processes the request and returns a result
4. We access the `final_output` to get the agent's response

### Example 2: Agent with Specific Instructions
```python
from agents import Agent, Runner

# Create a specialized agent
math_agent = Agent(
    name="MathTutor",
    instructions="""
    You are a patient math tutor. 
    - Always explain concepts step by step
    - Use simple language for beginners
    - Provide examples for each concept
    - Ask if the student needs clarification
    """
)

# Ask the agent to explain a concept
result = Runner.run_sync(
    math_agent, 
    "Explain what a function is in programming, like I'm 10 years old"
)

print(result.final_output)
```

### Example 3: Agent with Tools
```python
from agents import Agent, Runner, Tool

# Define a tool (function) the agent can use
def calculate_area(length, width):
    """Calculate the area of a rectangle"""
    return length * width

def get_weather(city):
    """Get weather information for a city"""
    # This would normally call a weather API
    return f"Weather in {city}: 72°F, sunny"

# Create tools
tools = [
    Tool(name="calculate_area", function=calculate_area),
    Tool(name="get_weather", function=get_weather)
]

# Create agent with tools
helper_agent = Agent(
    name="Helper",
    instructions="You are a helpful assistant that can calculate areas and check weather",
    tools=tools
)

# The agent can now use these tools
result = Runner.run_sync(
    helper_agent,
    "What's the area of a rectangle that's 5 feet by 3 feet, and what's the weather in New York?"
)

print(result.final_output)
```

## Advanced Patterns

### Example 4: Multiple Agents Working Together
```python
from agents import Agent, Runner

# Create specialized agents
researcher = Agent(
    name="Researcher",
    instructions="You research topics and gather information. Be thorough and accurate."
)

writer = Agent(
    name="Writer", 
    instructions="You write clear, engaging content based on research. Use simple language."
)

editor = Agent(
    name="Editor",
    instructions="You review and improve written content. Check for clarity and flow."
)

# Workflow: Research -> Write -> Edit
topic = "How do solar panels work?"

# Step 1: Research
research_result = Runner.run_sync(researcher, f"Research: {topic}")
research_info = research_result.final_output

# Step 2: Write
writing_result = Runner.run_sync(
    writer, 
    f"Write an article about {topic} using this research: {research_info}"
)
article = writing_result.final_output

# Step 3: Edit
editing_result = Runner.run_sync(
    editor,
    f"Edit and improve this article: {article}"
)
final_article = editing_result.final_output

print("Final Article:")
print(final_article)
```

### Example 5: Agent with Memory and Context
```python
from agents import Agent, Runner

# Create an agent that remembers previous conversations
memory_agent = Agent(
    name="PersonalAssistant",
    instructions="""
    You are a personal assistant that remembers previous conversations.
    - Always greet the user by name if you know it
    - Remember their preferences and interests
    - Reference previous conversations when relevant
    - Be helpful and friendly
    """
)

# First conversation
result1 = Runner.run_sync(
    memory_agent,
    "Hi, I'm Sarah. I love reading science fiction books."
)
print("First response:", result1.final_output)

# Second conversation (agent should remember Sarah and her interests)
result2 = Runner.run_sync(
    memory_agent,
    "Can you recommend a good book for me?"
)
print("Second response:", result2.final_output)
```

### Example 6: Error Handling and Validation
```python
from agents import Agent, Runner

# Create an agent with error handling
safe_agent = Agent(
    name="SafeAgent",
    instructions="""
    You are a careful agent that:
    - Always validates inputs
    - Handles errors gracefully
    - Asks for clarification when needed
    - Never makes assumptions
    """
)

def safe_agent_call(agent, message):
    """Safely call an agent with error handling"""
    try:
        result = Runner.run_sync(agent, message)
        return {
            "success": True,
            "output": result.final_output,
            "usage": result.usage
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": "I encountered an error. Please try again."
        }

# Test with various inputs
test_messages = [
    "What's 2 + 2?",
    "Tell me about quantum physics",
    "",  # Empty message
    "Help me with something very complex that might cause issues"
]

for message in test_messages:
    result = safe_agent_call(safe_agent, message)
    print(f"Input: '{message}'")
    print(f"Success: {result['success']}")
    print(f"Output: {result['output']}")
    print("-" * 50)
```

## Integration with Your Project

### Example 7: ITSM Agent (Based on Your Codebase)
```python
from agents import Agent, Runner, Tool
from datetime import datetime

# Create tools for ITSM operations
def create_incident(title, description, severity="Medium"):
    """Create a new incident"""
    incident_id = f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return {
        "incident_id": incident_id,
        "title": title,
        "description": description,
        "severity": severity,
        "status": "Open",
        "created_at": datetime.now().isoformat()
    }

def get_incident_status(incident_id):
    """Get the status of an incident"""
    # This would normally query a database
    return f"Incident {incident_id} is currently Open and assigned to the Infrastructure team"

def escalate_incident(incident_id, reason):
    """Escalate an incident"""
    return f"Incident {incident_id} has been escalated. Reason: {reason}"

# Create ITSM tools
itsm_tools = [
    Tool(name="create_incident", function=create_incident),
    Tool(name="get_incident_status", function=get_incident_status),
    Tool(name="escalate_incident", function=escalate_incident)
]

# Create ITSM agent
itsm_agent = Agent(
    name="ITSM_Agent",
    instructions="""
    You are an IT Service Management agent that helps with incident management.
    
    Your responsibilities:
    - Create incidents when problems are reported
    - Check incident status
    - Escalate incidents when necessary
    - Provide updates to users
    
    Always be professional and helpful. Ask for clarification if needed.
    """,
    tools=itsm_tools
)

# Example usage
result = Runner.run_sync(
    itsm_agent,
    "A user reported that the website is loading very slowly. Can you help create an incident?"
)

print("ITSM Agent Response:")
print(result.final_output)
```

### Example 8: Monitoring Agent Integration
```python
from agents import Agent, Runner, Tool

# Create monitoring tools
def check_system_health():
    """Check overall system health"""
    return {
        "cpu_usage": "75%",
        "memory_usage": "60%", 
        "disk_usage": "45%",
        "status": "Warning - High CPU usage detected"
    }

def get_alert_history():
    """Get recent alerts"""
    return [
        {"id": "ALERT-001", "message": "High CPU usage on server-01", "severity": "Warning"},
        {"id": "ALERT-002", "message": "Disk space low on server-02", "severity": "Critical"}
    ]

def create_maintenance_ticket(description, priority="Medium"):
    """Create a maintenance ticket"""
    ticket_id = f"MAINT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return {
        "ticket_id": ticket_id,
        "description": description,
        "priority": priority,
        "status": "Open"
    }

# Create monitoring tools
monitoring_tools = [
    Tool(name="check_system_health", function=check_system_health),
    Tool(name="get_alert_history", function=get_alert_history),
    Tool(name="create_maintenance_ticket", function=create_maintenance_ticket)
]

# Create monitoring agent
monitoring_agent = Agent(
    name="Monitoring_Agent",
    instructions="""
    You are a proactive monitoring agent that:
    - Monitors system health
    - Analyzes alerts and patterns
    - Creates maintenance tickets when needed
    - Provides status updates
    
    Be proactive and suggest preventive actions.
    """,
    tools=monitoring_tools
)

# Example usage
result = Runner.run_sync(
    monitoring_agent,
    "Can you check the system health and let me know if there are any issues that need attention?"
)

print("Monitoring Agent Response:")
print(result.final_output)
```

## Best Practices

### 1. Clear Instructions
```python
# Good: Specific and clear
agent = Agent(
    name="CodeReviewer",
    instructions="""
    You are a senior software engineer reviewing code.
    
    Your tasks:
    1. Check for bugs and potential issues
    2. Suggest improvements for readability
    3. Ensure best practices are followed
    4. Provide specific, actionable feedback
    
    Always be constructive and educational.
    """
)

# Bad: Vague and unclear
agent = Agent(
    name="Helper",
    instructions="Help with code"
)
```

### 2. Appropriate Tool Selection
```python
# Good: Tools match the agent's purpose
def analyze_logs(log_data):
    """Analyze system logs for errors"""
    # Implementation here
    pass

def generate_report(analysis):
    """Generate a report from analysis"""
    # Implementation here
    pass

log_agent = Agent(
    name="LogAnalyzer",
    instructions="Analyze logs and generate reports",
    tools=[
        Tool(name="analyze_logs", function=analyze_logs),
        Tool(name="generate_report", function=generate_report)
    ]
)
```

### 3. Error Handling
```python
def safe_run_agent(agent, message, max_retries=3):
    """Safely run an agent with retry logic"""
    for attempt in range(max_retries):
        try:
            result = Runner.run_sync(agent, message)
            return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return None
            time.sleep(1)  # Wait before retry
    return None
```

### 4. Resource Management
```python
# Good: Check usage and manage resources
result = Runner.run_sync(agent, message)

if result.usage:
    print(f"Tokens used: {result.usage.total_tokens}")
    print(f"Cost: ${result.usage.total_cost:.4f}")

# Monitor and limit usage
if result.usage.total_tokens > 1000:
    print("Warning: High token usage detected")
```

## Common Patterns

### Pattern 1: Agent Chain
```python
def run_agent_chain(agents, initial_message):
    """Run multiple agents in sequence"""
    current_message = initial_message
    results = []
    
    for agent in agents:
        result = Runner.run_sync(agent, current_message)
        results.append(result)
        current_message = result.final_output
    
    return results
```

### Pattern 2: Agent Comparison
```python
def compare_agent_responses(agents, message):
    """Get responses from multiple agents and compare"""
    responses = []
    
    for agent in agents:
        result = Runner.run_sync(agent, message)
        responses.append({
            "agent_name": agent.name,
            "response": result.final_output,
            "usage": result.usage
        })
    
    return responses
```

### Pattern 3: Conditional Agent Selection
```python
def route_to_appropriate_agent(message, agents):
    """Route message to the most appropriate agent"""
    # Simple keyword-based routing
    if "math" in message.lower():
        return agents["math_agent"]
    elif "code" in message.lower():
        return agents["code_agent"]
    else:
        return agents["general_agent"]
```

## Next Steps

1. **Start Simple**: Begin with basic agents and gradually add complexity
2. **Experiment**: Try different instructions and see how they affect behavior
3. **Add Tools**: Create custom tools for your specific use cases
4. **Monitor Usage**: Keep track of token usage and costs
5. **Test Thoroughly**: Always test your agents with various inputs

## Resources

- [OpenAI Agents Documentation](https://platform.openai.com/docs/assistants/overview)
- [Agent Best Practices](https://platform.openai.com/docs/assistants/tools)
- [Tool Development Guide](https://platform.openai.com/docs/assistants/tools/function-calling)

Remember: The key to successful agent development is clear instructions, appropriate tools, and thorough testing!
