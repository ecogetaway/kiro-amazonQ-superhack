---
inclusion: always
---

# ITIL Standards and Best Practices

This steering document provides ITIL-aligned standards for all AI agents in the ITSM solution.

## Incident Management Standards

### Severity Classification
- **P1 (Critical)**: Complete service outage affecting all users
- **P2 (High)**: Major functionality impacted, affecting multiple users
- **P3 (Medium)**: Minor functionality impacted, affecting few users
- **P4 (Low)**: Cosmetic issues or feature requests

### Response Time SLAs
- P1: 15 minutes initial response, 4 hours resolution target
- P2: 1 hour initial response, 8 hours resolution target
- P3: 4 hours initial response, 24 hours resolution target
- P4: 8 hours initial response, 72 hours resolution target

## Problem Management Standards

### Problem Creation Criteria
- 3+ related incidents within 24 hours
- Single incident affecting >100 users
- Any P1 incident with unknown root cause
- Recurring incidents with same symptoms

### Root Cause Analysis Requirements
- Document timeline of events
- Identify contributing factors
- Propose preventive measures
- Assign ownership for resolution

## Agent Decision-Making Guidelines

### Autonomous Actions Allowed
- Group incidents with >70% similarity confidence
- Create problem records when criteria met
- Generate P3/P4 alerts automatically
- Update incident status based on resolution

### Human Approval Required
- P1/P2 incident escalations
- Problem closure decisions
- SLA breach notifications
- Major system changes

## Communication Standards

### Stakeholder Notifications
- **End Users**: Simple, non-technical language
- **IT Teams**: Technical details and next steps
- **Management**: Business impact and timelines
- **Vendors**: Specific technical requirements

### Escalation Protocols
- Notify team lead for P2 incidents
- Page on-call manager for P1 incidents
- Update stakeholders every 2 hours for active P1/P2
- Send resolution confirmation to all affected parties