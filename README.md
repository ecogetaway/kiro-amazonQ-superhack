# AI-Powered ITSM Solution

A hackathon prototype demonstrating agentic AI capabilities in IT Service Management using Amazon Bedrock AgentCore and AWS services.

## Features

- **Autonomous Incident Correlation**: AI agents that independently group related incidents
- **Proactive Monitoring**: Predictive analysis with "top 3 issues" alerts
- **Problem Management Integration**: Automatic problem creation from incident patterns
- **Knowledge Base Integration**: AI-powered solution suggestions and auto-creation
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
- **Knowledge Agent**: Provides AI-powered solution suggestions and auto-creates articles
- **Supervisor Agent**: Coordinates all agents and resolves conflicts

## Project Structure

```
src/
├── agents/           # Autonomous AI agents
│   ├── correlation_agent.py
│   ├── monitoring_agent.py
│   ├── problem_agent.py
│   └── knowledge_agent.py
├── models/           # Data models
│   ├── incident.py
│   ├── problem.py
│   └── knowledge_base.py
├── data/            # Data loading and samples
└── config.py        # Configuration management

app.py               # Main Streamlit application
COMPLETE_DOCUMENTATION.md  # Full documentation with diagrams
```

## Hackathon Demo

This prototype demonstrates key agentic AI capabilities:
- Autonomous decision-making without human intervention
- Multi-agent coordination and conflict resolution
- Real-time learning and adaptation
- Proactive problem prevention
- Intelligent knowledge management and auto-creation

## Live Demo

- **GitHub Repository**: https://github.com/ecogetaway/kiro-amazonQ-superhack
- **Streamlit Demo**: Available via Streamlit Cloud
- **Complete Documentation**: See `COMPLETE_DOCUMENTATION.md` for full details

## Demo Features

### 🏠 Dashboard
- Real-time agent status and performance metrics
- Autonomous decision tracking
- Knowledge base analytics

### 🔗 Correlation Agent
- Interactive incident analysis
- AI-powered similarity scoring
- Autonomous grouping decisions

### 📊 Monitoring Agent
- Proactive issue detection
- Predictive analytics with timelines
- Top 3 critical issues identification

### 🔍 Problem Management
- Pattern-based problem creation
- Root cause analysis
- ITIL-compliant automation

### 📚 Knowledge Base
- Intelligent search capabilities
- AI-powered solution suggestions
- Auto-creation from incident resolutions
- Effectiveness tracking and analytics