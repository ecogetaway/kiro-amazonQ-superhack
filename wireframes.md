# 📱 Wireframes & Mock Diagrams

## Dashboard Wireframe

```
┌─────────────────────────────────────────────────────────────────┐
│  🤖 AI-Powered ITSM Solution                    [Settings] [⚙️] │
├─────────────────────────────────────────────────────────────────┤
│  📊 Dashboard | 🔗 Correlation | 📈 Monitoring | 🔍 Problems    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   Total     │ │    Open     │ │  Critical   │ │  Problems   │ │
│  │ Incidents   │ │ Incidents   │ │    (P1)     │ │  Created    │ │
│  │    156      │ │     23      │ │      4      │ │      7      │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│                                                                 │
│  🤖 Agent Status                                                │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │ 🔗 Correlation  │ │ 📊 Monitoring   │ │ 🔍 Problem      │   │
│  │ Agent: Active   │ │ Agent: Active   │ │ Agent: Active   │   │
│  │ Decisions: 45   │ │ Alerts: 12      │ │ Problems: 7     │   │
│  │ Autonomous: 38  │ │ Predictions: 8  │ │ Patterns: 15    │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│                                                                 │
│  🕒 Recent Activity                                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 🔗 Latest Correlation: GROUP_INCIDENTS (High Confidence)   │ │
│  │ ⚠️ Escalation Risk: 75% for INC-2024-001                  │ │
│  │ 📊 Top Alert: MON-001 (Severity: 85%)                     │ │
│  │ 🔮 Prediction: CPU will exceed threshold in 2.3h          │ │
│  │ 🔍 Latest Problem: PRB-001 (Critical priority)            │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Correlation Agent Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  🔗 Incident Correlation Agent                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Incident Analysis              │  Correlation Results          │
│  ┌─────────────────────────────┐ │ ┌─────────────────────────────┐ │
│  │ Select Incident:            │ │ │ Found 3 similar incidents   │ │
│  │ [INC-001: Email server...▼] │ │ │ Score: 0.87                 │ │
│  │                             │ │ │ Decision: GROUP_INCIDENTS   │ │
│  │ ID: INC-001                 │ │ │ Confidence: HIGH            │ │
│  │ Title: Email server slow    │ │ │ ✅ Action executed auto     │ │
│  │ System: prod-mail-01        │ │ │                             │ │
│  │                             │ │ │ 🔴 Escalation Risk: 75%     │ │
│  │ [🔍 Analyze Correlations]   │ │ │ Based on 2/3 similar        │ │
│  │                             │ │ │ incidents that escalated    │ │
│  └─────────────────────────────┘ │ │                             │ │
│                                 │ │ Similar Incidents:          │ │
│  🔮 Advanced Analysis           │ │ • INC-002: 0.92 (same sys) │ │
│  ┌─────────────────────────────┐ │ │ • INC-005: 0.85 (symptoms) │ │
│  │ [📋 Batch Analysis]         │ │ │ • INC-008: 0.78 (timing)   │ │
│  │                             │ │ │                             │ │
│  │ Groups Found: 4             │ │ │ [Execute Action]            │ │
│  │ Grouped Incidents: 18       │ │ └─────────────────────────────┘ │
│  └─────────────────────────────┘ │                               │
└─────────────────────────────────────────────────────────────────┘
```

## Monitoring Agent Interface

```
┌──────────────────────────────────���──────────────────────────────┐
│  📊 Proactive Monitoring Agent                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Current Metrics                │  Top 3 Issues                │
│  ┌─────────────────────────────┐ │ ┌─────────────────────────────┐ │
│  │ 🟢 CPU Utilization: 65.2%  │ │ │ #1 🔴 MON-001               │ │
│  │ 🟡 Memory Usage: 78.5%     │ │ │ Severity: 85% | High Conf   │ │
│  │ 🔴 Disk Usage: 91.3%       │ │ │ ✅ Autonomous action taken  │ │
│  │ 🟢 Network: 45.1%          │ │ │                             │ │
│  │                             │ │ │ #2 🟡 MON-002               │ │
│  │ [🔍 Run Analysis]           │ │ │ Severity: 72% | Medium Conf │ │
│  │                             │ │ │ ⚠️ Human review required    │ │
│  └─────────────────────────────┘ │ │                             │ │
│                                 │ │ #3 🟡 MON-003               │ │
│  🔮 Predictive Analysis         │ │ Severity: 68% | High Conf   │ │
│  ┌─────────────────────────────┐ │ │ ✅ Autonomous action taken  │ │
│  │ 🔴 disk_usage               │ │ └─────────────────────────────┘ │
│  │ Predicted: 95.2% (90% max)  │ │                               │
│  │ Time to threshold: 2.3h     │ │  📈 Capacity Planning         │
│  │ Action: Clean disk space    │ │ ┌─────────────────────────────┐ │
│  │                             │ │ │ ⚠️ Immediate Actions        │ │
│  │ 🟡 memory_usage             │ │ │ • Disk at 91% - cleanup    │ │
│  │ Predicted: 85.1% (90% max)  │ │ │                             │ │
│  │ Time to threshold: 4.1h     │ │ │ 📅 Short-term (30 days)     │ │
│  │ Action: Restart services    │ │ │ • Memory trending up        │ │
│  └─────────────────────────────┘ │ └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Problem Management Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 Problem Management Agent                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Pattern Analysis               │  Problem Creation Decisions   │
│  ┌─────────────────────────────┐ │ ┌─────────────────────────────┐ │
│  │ Analyzing 156 incidents     │ │ │ Pattern #1: System          │ │
│  │ for patterns...             │ │ │ Key: prod-mail-01 | Inc: 5  │ │
│  │                             │ │ │ Confidence: 0.85            │ │
│  │ [🔍 Analyze Patterns]       │ │ │ ✅ Problem creation rec     │ │
│  │                             │ │ │ 🤖 Executed autonomously    │ │
│  │ ✅ Found 3 significant      │ │ │ [🔄 Create Problem #1]      │ │
│  │    patterns                 │ │ │                             │ │
│  └─────────────────────────────┘ │ │ Pattern #2: Symptom         │ │
│                                 │ │ Key: timeout | Inc: 4       │ │
│  📊 Pattern Insights            │ │ Confidence: 0.72            │ │
│  ┌─────────────────────────────┐ │ │ ⚠️ Does not meet criteria   │ │
│  │ System Patterns: 2          │ │ │                             │ │
│  │ Symptom Patterns: 1         │ │ │ Pattern #3: Temporal        │ │
│  │ Temporal Patterns: 0        │ │ │ Key: 24h_cluster | Inc: 6   │ │
│  │ Avg Confidence: 0.79        │ │ │ Confidence: 0.91            │ │
│  └─────────────────────────────┘ │ │ ✅ Problem creation rec     │ │
│                                 │ │ 🤖 Executed autonomously    │ │
│  📋 Created Problems            │ │ [🔄 Create Problem #3]      │ │
│  ┌─────────────────────────────┐ │ └─────────────────────────────┘ │
│  │ PRB-001: Email server       │ │                               │
│  │ Status: Investigating       │ │                               │
│  │ Priority: Critical          │ │                               │
│  │ Related Inc: 5              │ │                               │
│  │ Auto Created: Yes           │ │                               │
│  │ Confidence: 0.85            │ │                               │
│  │                             │ │                               │
│  │ Resolution Status:          │ │                               │
│  │ • Teams notified            │ │                               │
│  │ • Investigation started     │ │                               │
│  └─────────────────────────────┘ │                               │
└─────────────────────────────────────────────────────────────────┘
```

## Mobile Interface Mockup

```
┌─────────────────┐
│ 🤖 ITSM AI      │
├─────────────────┤
│ 📊 Dashboard    │
│ 🔗 Correlation  │
│ 📈 Monitoring   │ 
│ 🔍 Problems     │
├─────────────────┤
│ 📊 Overview     │
│ ┌─────────────┐ │
│ │ Incidents   │ │
│ │    156      │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │ Problems    │ │
│ │     7       │ │
│ └─────────────┘ │
│                 │
│ 🚨 Alerts       │
│ • High CPU      │
│ • Disk Full     │
│ • Memory Leak   │
│                 │
│ 🤖 Agents       │
│ 🟢 All Active   │
│                 │
│ [Refresh]       │
└─────────────────┘
```