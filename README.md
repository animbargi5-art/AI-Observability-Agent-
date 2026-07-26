<div align="center">

# 🚀 TattvaAI

### AI-Powered Autonomous Incident Investigation Platform

**Transforming observability data into actionable root cause analysis using AI Agents, LangGraph, and SigNoz.**

---

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange?style=for-the-badge)
![SigNoz](https://img.shields.io/badge/SigNoz-Observability-purple?style=for-the-badge)
![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-Tracing-green?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)

---

**Built for AI-powered Observability and Intelligent Incident Investigation**

</div>

---

# 📖 Overview

Modern cloud-native applications generate enormous amounts of telemetry.

Every second, distributed systems emit:

- Millions of traces
- Millions of logs
- Continuous metrics
- Alerts
- Service dependency information

While observability platforms collect this data effectively, engineers are still responsible for manually investigating incidents.

A single production outage often requires engineers to:

- Search traces
- Read thousands of logs
- Compare metrics
- Analyze service dependencies
- Review historical incidents
- Form hypotheses
- Identify root causes
- Recommend corrective actions

This process is time-consuming, repetitive, and highly dependent on individual expertise.

---

# 🎯 What is TattvaAI?

TattvaAI is an AI-powered autonomous incident investigation platform designed to assist Site Reliability Engineers (SREs), DevOps teams, and Platform Engineers.

Instead of simply visualizing telemetry, TattvaAI actively investigates incidents by coordinating multiple specialized AI agents.

Each agent focuses on a specific area of observability and contributes structured evidence to a shared investigation.

The platform combines:

- Distributed Tracing
- Logs
- Metrics
- Alerts
- Service Dependencies
- Historical Incidents

into a unified investigation pipeline that produces:

- Root Cause Analysis
- Confidence Scores
- Evidence Timeline
- Actionable Recommendations
- Investigation Reports

---

# 🚨 The Problem

As modern systems become increasingly distributed, investigating failures has become significantly more difficult.

Engineers often face challenges such as:

## Alert Fatigue

Large organizations may receive hundreds or thousands of alerts each day.

Many alerts are duplicated, correlated, or symptoms of the same underlying issue.

---

## Fragmented Observability

Operational data is distributed across multiple sources:

- Traces
- Logs
- Metrics
- Dashboards
- Alerts

Engineers must manually correlate this information.

---

## Manual Root Cause Analysis

Finding the actual cause of an incident usually requires:

- Comparing traces
- Reading logs
- Checking dashboards
- Reviewing historical incidents
- Understanding service dependencies

This process is slow and error-prone.

---

## Knowledge Silos

Experienced engineers often solve incidents much faster because they remember previous failures.

That knowledge is rarely preserved in a structured way for future investigations.

---

# 💡 Our Solution

TattvaAI introduces an autonomous investigation engine built around specialized AI agents.

Instead of relying on a single monolithic model, the investigation is divided into focused responsibilities.

Each agent independently analyzes one aspect of the incident and contributes structured evidence to a shared investigation state.

The collected evidence is correlated, ranked, and analyzed to determine the most probable root cause.

This approach provides:

- Structured reasoning
- Transparent investigation flow
- Evidence-based conclusions
- Explainable recommendations
- Repeatable incident analysis

---

# ✨ Key Features

## 🤖 Multi-Agent Investigation

Specialized AI agents independently investigate:

- Distributed Traces
- Logs
- Metrics
- Alerts
- Dependencies
- Historical Incidents

---

## 🧠 Evidence-Based Reasoning

Every conclusion is backed by structured evidence rather than opaque AI outputs.

---

## 🔍 Root Cause Analysis

Automatically identifies likely root causes using correlated telemetry.

---

## 📈 Confidence Scoring

Each investigation produces confidence scores based on collected evidence.

---

## 📚 Historical Memory

Past incidents can be reused to improve future investigations.

---

## 🔄 LangGraph Workflow

The complete investigation is orchestrated through a graph-based workflow.

---

## 📡 Native SigNoz Integration

TattvaAI communicates with SigNoz using the Model Context Protocol (MCP).

---

## 📊 Explainable Reports

Final reports include:

- Timeline
- Evidence
- Root Cause
- Recommendations
- Confidence

making every investigation transparent and reproducible.

---

# 🏗️ System Architecture

TattvaAI is built as a modular AI investigation platform where every layer has a single responsibility.

Instead of directly querying telemetry and producing answers with one large model, the system decomposes incident investigation into multiple independent stages.

This architecture makes investigations:

- Explainable
- Modular
- Scalable
- Extensible
- Observable

---

# High-Level Architecture

```text
                                +----------------------+
                                |      React UI        |
                                | Dashboard / Reports  |
                                +----------+-----------+
                                           |
                                           |
                                           ▼
                           +-------------------------------+
                           |        FastAPI Backend        |
                           | REST API + Investigation API |
                           +---------------+--------------+
                                           |
                                           ▼
                           +-------------------------------+
                           |     Incident Coordinator      |
                           +---------------+--------------+
                                           |
                                           ▼
                           +-------------------------------+
                           |      LangGraph Workflow       |
                           +---------------+--------------+
                                           |
             ---------------------------------------------------------
             |         |         |         |        |         |       |
             ▼         ▼         ▼         ▼        ▼         ▼       ▼

      Trace Agent   Logs Agent Metrics Agent Alert Agent Dependency Historical
                                                              Agent     Agent
             |         |         |         |        |         |
             -------------------------------------------------
                               |
                               ▼
                     Correlation Engine
                               |
                               ▼
                     Root Cause Engine
                               |
                               ▼
                 Recommendation Engine
                               |
                               ▼
                      Report Generation
                               |
                               ▼
                  Investigation State Updated
                               |
                               ▼
                           REST Response
```

---

# Investigation Lifecycle

Every investigation follows the same deterministic workflow.

```text
Incident

      │

      ▼

Investigation Request

      │

      ▼

Create Investigation State

      │

      ▼

Launch LangGraph Workflow

      │

      ▼

Collect Telemetry

      │

      ▼

Analyze Evidence

      │

      ▼

Correlate Findings

      │

      ▼

Generate Hypotheses

      │

      ▼

Determine Root Cause

      │

      ▼

Generate Recommendations

      │

      ▼

Create Final Investigation Report
```

---

# Backend Architecture

The backend follows a layered architecture to ensure clear separation of concerns.

```text
API Layer

        │

        ▼

Coordinator Layer

        │

        ▼

Graph Orchestration

        │

        ▼

AI Agents

        │

        ▼

Tools

        │

        ▼

Application Telemetry Service

        │

        ▼

SigNoz Telemetry Service

        │

        ▼

MCP Gateway

        │

        ▼

Official MCP SDK Client

        │

        ▼

SigNoz MCP Server

        │

        ▼

SigNoz
```

Each layer has a single responsibility.

No layer is aware of implementation details below it.

---

# Frontend Architecture

The frontend is built with React and communicates with the backend using REST APIs.

```text
React

│

├── Dashboard

├── Investigation

├── Evidence

├── Timeline

├── Report

└── Settings

        │

        ▼

REST API

        │

        ▼

FastAPI Backend
```

The frontend is responsible only for visualization.

All investigation logic resides in the backend.

---

# AI Investigation Pipeline

The investigation engine is composed of specialized AI agents.

Each agent contributes structured evidence instead of directly producing conclusions.

```text
Incident

     │

     ▼

Trace Agent
     │

Logs Agent
     │

Metrics Agent
     │

Alert Agent
     │

Dependency Agent
     │

Historical Agent

     │

     ▼

Evidence Collection

     │

     ▼

Correlation Engine

     │

     ▼

Root Cause Engine

     │

     ▼

Recommendation Engine

     │

     ▼

Final Report
```

---

# Data Flow

The following diagram illustrates how telemetry moves through the system.

```text
SigNoz

     │

     ▼

MCP Server

     │

     ▼

MCP Gateway

     │

     ▼

Telemetry Service

     │

     ▼

Tools

     │

     ▼

AI Agents

     │

     ▼

Evidence

     │

     ▼

Correlation

     │

     ▼

Investigation Report
```

---

# Investigation State

Throughout the workflow, all agents share a common `InvestigationState`.

This state acts as the central memory of the investigation.

It stores:

- Incident metadata
- Distributed traces
- Logs
- Metrics
- Alerts
- Dependencies
- Historical incidents
- Evidence
- Hypotheses
- Recommendations
- Confidence score
- Timeline
- Final report

Every agent receives the current state, enriches it with new evidence, and passes the updated state to the next stage.

This shared state enables transparent, explainable, and collaborative reasoning across the entire investigation pipeline.

---

# 🤖 AI Investigation Agents

TattvaAI follows a **multi-agent architecture** where each AI agent has a focused responsibility.

Instead of asking one large language model to investigate an entire production incident, the investigation is divided into specialized stages.

Each agent:

- Receives the current `InvestigationState`
- Collects domain-specific evidence
- Updates the shared investigation state
- Passes the enriched state to the next agent

This modular architecture improves explainability, extensibility, and maintainability.

---

# Investigation Workflow

```text
Incident

    │

    ▼

Trace Agent

    │

    ▼

Logs Agent

    │

    ▼

Metrics Agent

    │

    ▼

Dependency Agent

    │

    ▼

Alert Agent

    │

    ▼

Historical Agent

    │

    ▼

Correlation Engine

    │

    ▼

Root Cause Agent

    │

    ▼

Recommendation Agent

    │

    ▼

Report Agent
```

---

# 🔍 Trace Agent

The Trace Agent is responsible for investigating distributed traces collected from SigNoz.

## Responsibilities

- Retrieve traces
- Analyze request latency
- Detect failed spans
- Identify slow operations
- Detect bottlenecks
- Generate evidence

## Input

- Service Name
- Investigation State

## Output

- Normalized Trace models
- Evidence objects

## Example Evidence

```text
Category:
Trace

Severity:
HIGH

Finding:
Checkout service latency increased from
120ms to 4.8 seconds.

Confidence:
92%
```

---

# 📜 Logs Agent

The Logs Agent investigates application logs to identify runtime failures.

## Responsibilities

- Search logs
- Detect exceptions
- Identify recurring errors
- Extract stack traces
- Correlate logs with traces

## Input

- Service Name
- Trace IDs

## Output

- Log Evidence

## Example Evidence

```text
ERROR

Database connection timeout

Occurred

143 times

Last 10 minutes
```

---

# 📈 Metrics Agent

The Metrics Agent analyzes numerical telemetry.

## Responsibilities

- CPU
- Memory
- Network
- Latency
- Error Rate
- Throughput

## Example Findings

```text
CPU

98%

Memory

92%

Latency

+650%

Request Rate

Stable

Error Rate

18%
```

---

# 🔗 Dependency Agent

Modern applications consist of many interconnected services.

The Dependency Agent analyzes service relationships.

## Responsibilities

- Retrieve dependency graph
- Detect cascading failures
- Identify upstream failures
- Detect downstream impact

## Example

```text
Checkout Service

↓

Payment Service

↓

Redis

↓

Timeout

↓

Checkout Failure
```

---

# 🚨 Alert Agent

The Alert Agent investigates active alerts.

## Responsibilities

- Retrieve alerts
- Prioritize severity
- Correlate duplicate alerts
- Remove noisy alerts
- Generate evidence

## Example

```text
Critical

Database Timeout

Active

12 minutes
```

---

# 📚 Historical Agent

One of the most valuable features of TattvaAI is historical reasoning.

Instead of treating every incident as completely new, previous investigations are reused.

## Responsibilities

- Retrieve historical incidents
- Compare previous failures
- Detect recurring incidents
- Increase confidence
- Suggest previous resolutions

## Example

```text
Current Incident

↓

Matches Incident #381

↓

Similarity

94%

↓

Previous Root Cause

Redis Timeout
```

---

# 🧠 Correlation Engine

After every agent contributes evidence, the Correlation Engine combines all findings.

Rather than relying on a single signal, it correlates evidence across multiple telemetry sources.

## Correlated Inputs

- Traces
- Logs
- Metrics
- Alerts
- Dependencies
- Historical Incidents

## Responsibilities

- Merge evidence
- Remove duplicates
- Calculate confidence
- Rank findings
- Generate hypotheses

---

# 🎯 Root Cause Agent

The Root Cause Agent evaluates all collected evidence and determines the most likely explanation.

## Responsibilities

- Evaluate evidence
- Rank hypotheses
- Identify root cause
- Calculate confidence

## Example

```text
Root Cause

Redis latency caused
payment service timeout
which propagated
to checkout failures.

Confidence

96%
```

---

# 💡 Recommendation Agent

Once the root cause has been identified, recommendations are generated.

Recommendations are based on:

- Root Cause
- Previous Incidents
- Service Topology
- Operational Best Practices

## Example Recommendations

- Restart Redis cluster
- Increase timeout threshold
- Add circuit breaker
- Enable connection pooling
- Scale Redis replicas

---

# 📄 Report Agent

The Report Agent produces the final investigation report.

The report is designed to be understandable by engineers, SRE teams, and incident managers.

## Generated Report

The final report includes:

- Incident Summary
- Timeline
- Evidence
- Root Cause
- Confidence Score
- Recommendations
- Supporting Telemetry

---

# 🔄 Shared Investigation State

Every AI agent operates on a common `InvestigationState`.

```text
InvestigationState

├── Incident Information
├── Traces
├── Logs
├── Metrics
├── Alerts
├── Dependencies
├── Historical Incidents
├── Evidence
├── Hypotheses
├── Recommendations
├── Timeline
├── Confidence
└── Final Report
```

This shared state allows agents to collaborate without directly depending on one another, making the workflow modular, extensible, and easy to maintain.

---

# Why a Multi-Agent Architecture?

Traditional AI systems often rely on a single model to answer complex operational questions.

TattvaAI instead distributes responsibilities across specialized agents, providing several advantages:

- **Modularity:** New investigation capabilities can be added as independent agents.
- **Explainability:** Every conclusion is supported by structured evidence.
- **Scalability:** Agents can evolve independently as the platform grows.
- **Maintainability:** Individual components can be tested and improved in isolation.
- **Transparency:** Engineers can inspect each stage of the investigation rather than receiving a single opaque answer.

This architecture enables TattvaAI to perform systematic, evidence-driven investigations while remaining extensible for future capabilities such as security analysis, cost optimization, and predictive incident detection.

# ⚙️ Backend Architecture

The backend is the intelligence layer of TattvaAI.

It is responsible for:

- Receiving investigation requests
- Managing investigation workflows
- Coordinating AI agents
- Collecting telemetry from SigNoz
- Correlating evidence
- Determining root causes
- Generating recommendations
- Producing investigation reports

The backend follows a modular layered architecture where each layer has a single responsibility.

---

# Backend Overview

```text
                   FastAPI REST API
                          │
                          ▼
              Incident Coordinator
                          │
                          ▼
                 LangGraph Workflow
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   Investigation      AI Agents        Memory
       State
        │
        ▼
      Tools
        │
        ▼
Telemetry Service
        │
        ▼
 SigNoz Telemetry Layer
        │
        ▼
    MCP Gateway
        │
        ▼
 Official MCP SDK
        │
        ▼
 SigNoz MCP Server
        │
        ▼
      SigNoz
```

---

# Backend Layers

The backend is organized into independent layers.

Each layer communicates only with the layer directly below it.

---

## 1. API Layer

Directory

```text
app/api/
```

Responsibilities

- Receive HTTP requests
- Validate request parameters
- Create investigation requests
- Return investigation results
- Expose REST APIs

The API layer contains no business logic.

Example

```text
POST

/investigation/start

↓

Incident Coordinator
```

---

## 2. Coordinator Layer

Directory

```text
app/coordinator/
```

Responsibilities

- Initialize investigation state
- Launch LangGraph workflow
- Return completed investigation

The coordinator acts as the entry point into the AI investigation pipeline.

```text
REST API

↓

Coordinator

↓

Graph
```

---

## 3. LangGraph Workflow

Directory

```text
app/graph/
```

The workflow orchestrates the complete investigation.

Instead of calling agents manually, LangGraph manages execution order.

Workflow

```text
Trace

↓

Logs

↓

Metrics

↓

Dependencies

↓

Alerts

↓

Historical

↓

Correlation

↓

Root Cause

↓

Recommendations

↓

Report
```

Each node receives and updates the shared InvestigationState.

---

# Investigation State

Directory

```text
app/models/
```

InvestigationState acts as the central memory of the investigation.

It stores:

```text
Incident

Service

Traces

Logs

Metrics

Dependencies

Historical Incidents

Evidence

Hypotheses

Recommendations

Timeline

Confidence

Report
```

Every graph node updates this object.

---

# AI Agent Layer

Directory

```text
app/agents/
```

Each AI agent specializes in one telemetry domain.

Current agents include:

```text
Trace Agent

Logs Agent

Metrics Agent

Dependency Agent

Alert Agent

Historical Agent

Correlation Engine

Root Cause Agent

Recommendation Agent

Report Agent
```

Each agent is completely independent.

Agents never communicate directly.

All communication occurs through the shared InvestigationState.

---

# Tool Layer

Directory

```text
app/tools/
```

Tools abstract telemetry retrieval.

Agents never communicate directly with SigNoz.

Instead they use tools.

Example

```text
Trace Agent

↓

Trace Tool

↓

Telemetry Service
```

Current tools

```text
Trace Tool

Logs Tool

Metrics Tool

Dependency Tool

Alert Tool

Historical Tool
```

---

# Application Services

Directory

```text
app/services/
```

Application services expose high-level operations.

Example

```python
telemetry.search_traces()

telemetry.search_logs()

telemetry.query_metrics()

telemetry.get_dependencies()
```

The services hide implementation details from agents.

---

# SigNoz Integration Layer

Directory

```text
app/signoz/
```

Responsibilities

- Build queries
- Execute MCP tools
- Parse responses
- Normalize telemetry
- Return application models

Modules

```text
config.py

query_builder.py

mcp_gateway.py

models.py

telemetry_service.py
```

---

# MCP Gateway

The MCP Gateway provides a thin abstraction over the official MCP SDK.

Responsibilities

- Maintain connection
- Execute tools
- Handle retries
- Handle failures
- Return CallToolResult

Architecture

```text
Telemetry Service

↓

MCP Gateway

↓

MCP Client

↓

SigNoz MCP Server
```

---

# Query Builder

Instead of constructing telemetry requests throughout the project, all queries are centralized.

Supported queries

```text
Trace Query

Log Query

Metric Query

Dependency Query

Alert Query

Historical Query

Service Query
```

Advantages

- Consistency
- Reusability
- Easier maintenance

---

# Telemetry Models

Directory

```text
app/signoz/models.py
```

The backend separates raw telemetry from investigation models.

Raw models

```text
TraceRecord

LogRecord

MetricRecord

AlertRecord

DependencyRecord

ServiceRecord
```

These represent data returned by SigNoz.

---

# Domain Models

Directory

```text
app/models/
```

Domain models are independent of SigNoz.

Examples

```text
Trace

Log

Metric

Evidence

Hypothesis

Recommendation

HistoricalIncident

InvestigationState
```

These models are used throughout the investigation pipeline.

---

# Memory Layer

Investigation memory persists information collected during execution.

It stores:

```text
Evidence

Timeline

Hypotheses

Recommendations

Confidence

Final Report
```

Memory enables every agent to build upon previous findings.

---

# Observability

The backend is instrumented using OpenTelemetry.

Collected telemetry includes:

- Request traces
- Application logs
- Metrics
- Agent execution
- Workflow duration

This telemetry is exported to SigNoz for monitoring and analysis.

---

# Backend Folder Structure

```text
backend/

├── app/
│
├── agents/
│   ├── base_agent.py
│   ├── trace_agent.py
│   ├── logs_agent.py
│   ├── metrics_agent.py
│   ├── dependency_agent.py
│   ├── alert_agent.py
│   ├── historical_agent.py
│   ├── correlation_engine.py
│   ├── root_cause_agent.py
│   ├── recommendation_agent.py
│   └── report_agent.py
│
├── api/
│
├── coordinator/
│
├── core/
│
├── graph/
│
├── memory/
│
├── mcp/
│
├── models/
│
├── reports/
│
├── services/
│
├── signoz/
│
├── tools/
│
├── database/
│
├── repositories/
│
└── main.py
```

---

# Design Principles

The backend follows several architectural principles:

### Separation of Concerns

Each module has a single responsibility.

### Layered Architecture

Higher layers do not depend on implementation details of lower layers.

### Dependency Inversion

Agents depend on abstract tools rather than telemetry providers.

### Extensibility

New telemetry sources, tools, or AI agents can be added without modifying existing components.

### Explainability

Every investigation is evidence-driven and every conclusion can be traced back to the telemetry that produced it.

---

# Backend Request Flow

```text
User

↓

React Frontend

↓

FastAPI

↓

Incident Coordinator

↓

LangGraph Workflow

↓

AI Agents

↓

Tools

↓

Telemetry Service

↓

MCP Gateway

↓

SigNoz MCP Server

↓

SigNoz

↓

Telemetry

↓

Evidence

↓

Root Cause

↓

Recommendations

↓

Final Report

↓

Frontend
```

The backend is designed to be modular, observable, and extensible, enabling future enhancements such as additional telemetry providers, new AI agents, and advanced investigation capabilities without major architectural changes.

---

# 📡 Observability Architecture

Observability is the foundation of TattvaAI.

Rather than building another monitoring platform, TattvaAI integrates with an existing observability ecosystem and transforms telemetry into actionable intelligence.

The platform leverages:

- OpenTelemetry
- SigNoz
- Model Context Protocol (MCP)
- AI Investigation Agents

to automate production incident investigations.

---

# Observability Stack

```text
                    Application

                          │

                          ▼

                OpenTelemetry SDK

                          │

                          ▼

             OpenTelemetry Collector

                          │

                          ▼

                     SigNoz

        Traces │ Logs │ Metrics │ Alerts

                          │

                          ▼

                 SigNoz MCP Server

                          │

                          ▼

                 Official MCP SDK

                          │

                          ▼

                    MCP Gateway

                          │

                          ▼

               SigNoz Telemetry Service

                          │

                          ▼

                  AI Investigation Engine
```

---

# Why SigNoz?

TattvaAI is designed to work with modern observability platforms rather than replacing them.

SigNoz provides:

- Distributed Tracing
- Centralized Logging
- Metrics Collection
- Service Maps
- Dependency Graphs
- Dashboards
- Alerts
- OpenTelemetry-native ingestion

By integrating directly with SigNoz, TattvaAI can investigate production incidents using real telemetry data without requiring custom instrumentation.

---

# OpenTelemetry Pipeline

Applications instrumented with OpenTelemetry continuously export telemetry data.

```text
Application

↓

OpenTelemetry SDK

↓

OTLP Exporter

↓

OTLP Collector

↓

SigNoz
```

Collected telemetry includes:

- HTTP Requests
- Database Calls
- External API Calls
- Exceptions
- Logs
- Metrics
- Resource Attributes
- Span Relationships

This telemetry becomes the evidence analyzed by TattvaAI.

---

# Model Context Protocol (MCP)

TattvaAI communicates with SigNoz using the **Model Context Protocol (MCP)**.

Instead of directly calling proprietary APIs, the backend uses MCP tools exposed by the SigNoz MCP Server.

This approach provides:

- Standardized tool execution
- Provider-independent integration
- Structured responses
- Extensible architecture

---

# MCP Communication Flow

```text
AI Agent

      │

      ▼

Telemetry Service

      │

      ▼

MCP Gateway

      │

      ▼

Official MCP Client

      │

      ▼

SigNoz MCP Server

      │

      ▼

SigNoz APIs

      │

      ▼

Telemetry Response
```

---

# MCP Gateway

The MCP Gateway abstracts communication with the SigNoz MCP Server.

Responsibilities include:

- Establishing MCP sessions
- Managing authentication
- Executing MCP tools
- Handling connection lifecycle
- Retrying failed requests
- Returning structured results

The gateway isolates the rest of the backend from transport-specific implementation details.

---

# Query Builder

Instead of constructing telemetry queries throughout the codebase, TattvaAI centralizes query construction.

Supported query types include:

- Trace Queries
- Log Queries
- Metric Queries
- Alert Queries
- Dependency Queries
- Historical Queries
- Service Discovery Queries

Example flow:

```text
Trace Agent

↓

Query Builder

↓

Trace Query Payload

↓

MCP Tool Execution
```

This ensures consistency across all telemetry requests.

---

# Supported Telemetry Sources

TattvaAI currently analyzes multiple categories of telemetry.

## Distributed Traces

Used to identify:

- Slow requests
- Failed spans
- High latency operations
- Bottlenecks
- Service interactions

---

## Logs

Used to detect:

- Exceptions
- Stack traces
- Error patterns
- Runtime failures
- Warning messages

---

## Metrics

Used to analyze:

- CPU utilization
- Memory consumption
- Network traffic
- Request throughput
- Error rates
- Response latency

---

## Alerts

Used to prioritize ongoing production issues and correlate active incidents.

---

## Dependencies

Used to understand relationships between services and identify cascading failures.

---

## Historical Investigations

Used to compare previous incidents and reuse known resolutions where appropriate.

---

# Telemetry Normalization

Raw responses returned by SigNoz are transformed into application-specific domain models before reaching the investigation engine.

```text
SigNoz Response

↓

MCP Response

↓

Telemetry Parser

↓

TraceRecord

↓

Domain Model

↓

Evidence
```

This separation allows the investigation engine to remain independent of the underlying telemetry provider.

---

# Investigation Evidence Flow

Every telemetry source contributes structured evidence.

```text
Distributed Traces

        │

Logs

        │

Metrics

        │

Alerts

        │

Dependencies

        │

Historical Incidents

        │

        ▼

Evidence Objects

        ▼

Correlation Engine

        ▼

Root Cause Analysis
```

The investigation engine never relies on a single signal.

Instead, conclusions are based on correlated evidence across multiple telemetry sources.

---

# OpenTelemetry Instrumentation

The backend itself is instrumented using OpenTelemetry.

This enables monitoring of:

- Incoming API requests
- Agent execution time
- Workflow duration
- Database interactions
- MCP requests
- External service calls

As a result, TattvaAI can observe its own investigation pipeline while simultaneously investigating customer applications.

---

# Advantages of the Architecture

The observability architecture provides several important benefits:

### Vendor Independence

The investigation engine is separated from telemetry providers.

Additional providers can be supported without changing the AI workflow.

---

### Standardized Communication

The Model Context Protocol provides a consistent interface for tool execution.

---

### Explainable Investigations

Every recommendation can be traced back to the underlying telemetry that produced it.

---

### Extensibility

New telemetry sources, MCP tools, or observability platforms can be integrated with minimal changes to the core investigation engine.

---

### Scalability

The architecture supports distributed environments containing hundreds of services and large volumes of telemetry data while maintaining a modular investigation pipeline.

---

# Design Philosophy

TattvaAI is not designed to replace observability platforms.

Instead, it augments them by transforming telemetry into structured investigations.

The observability platform answers:

> **"What happened?"**

TattvaAI extends this by answering:

- Why did it happen?
- Which services were involved?
- What evidence supports the conclusion?
- What is the most likely root cause?
- What actions should be taken next?

This combination of observability and AI-driven reasoning enables faster, more transparent, and evidence-based incident investigations.


# 📂 Project Structure

TattvaAI follows a modular architecture that separates user interfaces, orchestration logic, AI reasoning, telemetry access, and infrastructure concerns.

```
TattvaAI
│
├── backend/
│   │
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── coordinator/
│   │   ├── core/
│   │   ├── database/
│   │   ├── graph/
│   │   ├── mcp/
│   │   ├── memory/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── reports/
│   │   ├── services/
│   │   ├── signoz/
│   │   ├── tools/
│   │   └── main.py
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   ├── assets/
│   │   └── App.tsx
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
│
├── README.md
│
└── docs/
```

---

# 🖥️ Frontend Architecture

The frontend provides an intuitive interface for engineers to investigate incidents and review AI-generated analysis.

The frontend is intentionally lightweight.

All investigation logic resides in the backend.

---

## Frontend Responsibilities

- Start investigations
- Display telemetry
- Display evidence
- Display investigation timeline
- Display root cause analysis
- Display recommendations
- Display confidence score
- Display final report

---

# Frontend Architecture

```
React

│

├── Dashboard

├── Investigation

├── Evidence

├── Timeline

├── Reports

├── Settings

└── Shared Components
```

---

# Component Flow

```
User

↓

Dashboard

↓

API Service

↓

FastAPI Backend

↓

Investigation Result

↓

Visualization Components
```

---

# Dashboard

The dashboard provides a high-level overview of the observability environment.

Example information displayed:

- Active investigations
- Recent incidents
- Service health
- Error rate
- Latency
- Investigation history

---

# Investigation View

The investigation page displays the entire AI reasoning process.

Information includes:

- Timeline
- Evidence
- Traces
- Logs
- Metrics
- Dependencies
- Root Cause
- Recommendations

---

# Evidence Panel

Evidence generated by every AI agent is displayed in chronological order.

Each evidence item includes:

- Source
- Category
- Severity
- Confidence
- Summary
- Timestamp

---

# Timeline View

The timeline visualizes how the investigation evolved.

Example:

```
Trace Agent Completed

↓

Logs Agent Completed

↓

Metrics Agent Completed

↓

Correlation Engine

↓

Root Cause

↓

Recommendations
```

---

# Report View

The report page presents the final investigation.

It includes:

- Executive Summary
- Timeline
- Evidence
- Root Cause
- Confidence Score
- Recommendations

Reports can later be exported as PDF or shared with team members.

---

# ⚙️ REST API

The backend exposes REST APIs used by the frontend.

---

## Start Investigation

```
POST

/investigation/start
```

Example

```json
{
    "service_name": "checkout-service"
}
```

Response

```json
{
    "incident_id": "...",
    "status": "completed",
    "confidence": 92
}
```

---

## Investigation Status

```
GET

/investigation/{incident_id}
```

Returns:

- Timeline
- Evidence
- Root Cause
- Recommendations

---

## Health Check

```
GET

/health
```

Returns backend health status.

---

## OpenAPI Documentation

FastAPI automatically generates interactive API documentation.

Available at:

```
http://localhost:8000/docs
```

---

# 🐳 Running with Docker

The recommended deployment method is Docker Compose.

Start all services:

```bash
docker compose up --build
```

Run in background:

```bash
docker compose up -d
```

Stop containers:

```bash
docker compose down
```

Rebuild containers:

```bash
docker compose up --build
```

---

# 🚀 Local Development

## Backend

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the backend.

```bash
uvicorn app.main:app --reload
```

Backend URL

```
http://localhost:8000
```

---

## Frontend

Navigate to the frontend.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Run the development server.

```bash
npm run dev
```

Frontend URL

```
http://localhost:5173
```

---

# ⚙️ Environment Configuration

Create a `.env` file inside the backend directory.

Example:

```env
APP_NAME=TattvaAI

APP_VERSION=1.0.0

ENVIRONMENT=development

HOST=0.0.0.0

PORT=8000

DEBUG=True

SIGNOZ_URL=http://localhost:3301

SIGNOZ_API_KEY=<YOUR_API_KEY>

SIGNOZ_MCP_SERVER=http://localhost:8001/mcp

OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

OTEL_SERVICE_NAME=tattva-ai-backend
```

---

# 📦 Technology Stack

## Backend

- Python 3.12
- FastAPI
- LangGraph
- LangChain
- Pydantic
- SQLAlchemy
- OpenTelemetry
- MCP SDK

---

## Frontend

- React 19
- TypeScript
- Vite
- PrimeReact
- PrimeFlex

---

## Infrastructure

- Docker
- Docker Compose
- SigNoz
- OpenTelemetry Collector

---

## AI & Observability

- LangGraph
- OpenTelemetry
- SigNoz
- Model Context Protocol (MCP)

---

# 🔧 Development Principles

The project is designed around a few core engineering principles:

- Modular architecture
- Clear separation of concerns
- Evidence-driven AI reasoning
- Explainable investigation workflow
- Extensible telemetry integrations
- Provider-independent observability layer
- Strong typing with Pydantic models
- Containerized development workflow
- OpenTelemetry-native instrumentation


# 🎥 Demo

A complete demonstration showcases how TattvaAI investigates a production incident from start to finish.

The demo highlights:

- Starting a new investigation
- AI agent execution
- Distributed trace analysis
- Log correlation
- Metrics analysis
- Dependency graph analysis
- Historical incident matching
- Root cause identification
- Recommendation generation
- Final investigation report

---

# 📸 Screenshots

> **Note**
>
> Screenshots will be added as the user interface evolves.

Suggested screenshots include:

- Dashboard
- Investigation Timeline
- Evidence Panel
- Root Cause Report
- Dependency Graph
- Service Overview
- Investigation Summary

Example structure:

```
docs/

├── dashboard.png

├── investigation.png

├── evidence.png

├── report.png

└── architecture.png
```

---

# 🧪 Example Investigation

## Scenario

An engineer receives reports that the checkout service is failing.

The engineer starts an investigation.

```
POST

/investigation/start

{
    "service_name": "checkout-service"
}
```

---

### Trace Agent

Findings

```
High latency detected

Payment API

4.8 seconds
```

---

### Logs Agent

Findings

```
Redis timeout

Connection pool exhausted

Multiple retries
```

---

### Metrics Agent

Findings

```
CPU

24%

Memory

42%

Latency

+620%

Error Rate

17%
```

---

### Dependency Agent

Findings

```
Checkout

↓

Payment

↓

Redis

↓

Timeout
```

---

### Historical Agent

Findings

```
Incident matched

Similarity

94%

Previous Cause

Redis timeout
```

---

### Correlation Engine

Correlated Evidence

```
Trace

+

Logs

+

Metrics

+

Dependencies

+

Historical Incident
```

---

### Root Cause

```
Redis latency caused
Payment API timeout,
which propagated
to Checkout Service.
```

Confidence

```
96%
```

---

### Recommendation

- Restart Redis
- Increase connection pool
- Enable circuit breaker
- Monitor latency
- Review retry strategy

---

### Investigation Completed

```
Status

Completed

Confidence

96%

Evidence

14

Recommendations

5
```

---

# 🗺️ Roadmap

The roadmap represents the planned evolution of TattvaAI.

## Phase 1

- Backend Architecture
- LangGraph Workflow
- AI Agents
- SigNoz Integration
- MCP Gateway
- Investigation Pipeline

Status

✅ Completed

---

## Phase 2

- React Dashboard
- Investigation Timeline
- Evidence Visualization
- Root Cause Reports
- Recommendation Dashboard

Status

🚧 In Progress

---

## Phase 3

- Historical Memory
- Investigation Search
- Report Export
- Authentication
- RBAC
- Investigation Persistence

Status

📅 Planned

---

## Phase 4

- Multi-Provider Support
- Prometheus
- Grafana
- Jaeger
- Elastic
- CloudWatch
- Azure Monitor

Status

📅 Planned

---

## Phase 5

- AI Chat Interface
- Conversational Investigation
- Predictive Incident Detection
- Automated Remediation
- Runbook Generation
- Self-Healing Workflows

Status

🔮 Future Vision

---

# 🤝 Contributing

Contributions are welcome.

If you would like to contribute:

1. Fork the repository

2. Create a feature branch

```
git checkout -b feature/my-feature
```

3. Commit your changes

```
git commit -m "Add new feature"
```

4. Push to your fork

```
git push origin feature/my-feature
```

5. Open a Pull Request

---

## Contribution Guidelines

Please:

- Follow the existing project structure.
- Keep components modular.
- Write descriptive commit messages.
- Add documentation for new features.
- Maintain consistent coding style.
- Prefer reusable components over duplication.

---

# 📖 Documentation

Project documentation includes:

- System Architecture
- Backend Architecture
- AI Agents
- LangGraph Workflow
- MCP Integration
- SigNoz Integration
- API Documentation
- Docker Setup

Additional documentation can be placed inside:

```
docs/
```

---

# 🧠 Design Philosophy

TattvaAI is built around a simple principle:

> **Observability platforms collect telemetry. TattvaAI transforms telemetry into understanding.**

Rather than presenting dashboards alone, the platform builds an explainable investigation by collecting evidence, correlating signals, and generating actionable recommendations.

The architecture emphasizes:

- Transparency
- Explainability
- Extensibility
- Modularity
- Evidence-driven reasoning

---

# ⭐ What Makes TattvaAI Different?

Unlike traditional observability tools, TattvaAI focuses on **investigation**, not just visualization.

Key differentiators include:

- Multi-agent AI architecture
- LangGraph-based orchestration
- Shared investigation state
- Evidence-driven reasoning
- Native SigNoz + MCP integration
- Explainable root cause analysis
- Modular backend design
- Provider-independent telemetry layer
- OpenTelemetry-native architecture

---

# 📜 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

# 🙏 Acknowledgements

TattvaAI builds upon several outstanding open-source projects and communities.

Special thanks to:

- FastAPI
- React
- LangChain
- LangGraph
- SigNoz
- OpenTelemetry
- Model Context Protocol (MCP)
- Pydantic
- SQLAlchemy
- Docker

Their work provides the foundation that makes this project possible.

---

# 📬 Contact

If you have questions, ideas, or feedback, feel free to open an issue or start a discussion in the repository.

Future contact links can include:

- GitHub Issues
- GitHub Discussions
- LinkedIn
- Portfolio Website
- Email

---

# 🌟 Vision

TattvaAI aims to evolve from an AI-powered incident investigation platform into a comprehensive operational intelligence system.

Future capabilities may include:

- Autonomous incident response
- Predictive failure detection
- Automated remediation workflows
- Cross-platform observability
- Long-term operational memory
- AI-assisted SRE collaboration

The long-term goal is to help engineering teams spend less time searching through telemetry and more time solving meaningful problems.

---

<div align="center">

# 🚀 TattvaAI

### Transforming Observability into Intelligence

**Built with ❤️ using FastAPI, React, LangGraph, OpenTelemetry, SigNoz, and MCP.**

If you find this project useful, consider giving it a ⭐ on GitHub.

</div>