# AI-Powered ITSM Solution

A hackathon prototype demonstrating agentic AI capabilities in IT Service Management using Amazon Bedrock AgentCore and AWS services.

## Features

- **Autonomous Incident Correlation**: AI agents that independently group related incidents
- **Proactive Monitoring**: Predictive analysis with "top 3 issues" alerts
- **Problem Management Integration**: Automatic problem creation from incident patterns
- **Multi-Agent Coordination**: Supervisor agent orchestrating specialized agents
- **Real-time Dashboard**: Streamlit interface showing agent decisions and reasoning

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run Demo**
   ```bash
   streamlit run src/demo/dashboard.py
   ```

## Architecture

The solution uses autonomous AI agents that make independent decisions:

- **Correlation Agent**: Groups incidents using ML similarity analysis
- **Monitoring Agent**: Predicts infrastructure issues proactively  
- **Problem Agent**: Creates problems from recurring incident patterns
- **Supervisor Agent**: Coordinates all agents and resolves conflicts

## Project Structure

```
src/
├── agents/           # Autonomous AI agents
├── models/           # Data models
├── demo/            # Streamlit dashboard
└── config.py        # Configuration management
```

## Hackathon Demo

This prototype demonstrates key agentic AI capabilities:
- Autonomous decision-making without human intervention
- Multi-agent coordination and conflict resolution
- Real-time learning and adaptation
- Proactive problem prevention