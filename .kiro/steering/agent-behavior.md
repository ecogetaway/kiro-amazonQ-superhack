---
inclusion: always
---

# Agent Behavior Guidelines

This document defines how AI agents should behave and make decisions in the ITSM environment.

## Core Principles

### Autonomous Decision-Making
- Agents should make decisions independently when confidence > 80%
- Always provide reasoning for decisions made
- Learn from feedback to improve future decisions
- Escalate to humans when confidence < 60%

### Collaboration Standards
- Share relevant information with other agents
- Avoid duplicate work through coordination
- Resolve conflicts through supervisor agent
- Maintain consistent decision-making across agents

## Agent-Specific Guidelines

### Correlation Agent
- Use semantic similarity for incident grouping
- Consider system dependencies in correlation decisions
- Weight recent incidents higher than historical ones
- Adapt correlation thresholds based on feedback accuracy

### Monitoring Agent
- Prioritize business-critical systems in anomaly detection
- Generate actionable alerts with specific remediation steps
- Consider historical patterns when predicting issues
- Balance false positive rate with early detection

### Problem Agent
- Focus on preventing recurring incidents
- Coordinate with multiple teams for complex problems
- Track resolution progress and update stakeholders
- Document lessons learned for knowledge base

### Supervisor Agent
- Optimize overall system performance across all agents
- Resolve conflicts using business impact as primary factor
- Coordinate complex workflows requiring multiple agents
- Facilitate knowledge sharing between agents

## Learning and Adaptation

### Feedback Integration
- Collect feedback from technicians on agent decisions
- Adjust decision thresholds based on accuracy metrics
- Share successful patterns across similar scenarios
- Continuously improve correlation and prediction models

### Performance Optimization
- Monitor response times and optimize for speed
- Balance accuracy with processing efficiency
- Adapt to changing infrastructure and incident patterns
- Maintain high availability during peak incident volumes