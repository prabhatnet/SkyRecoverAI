# SkyRecoverAI Architecture (MVP - Python + Streamlit)

## Executive Summary

SkyRecoverAI is a portfolio project that simulates how a major airline handles passenger recovery during disruption events. The MVP is intentionally simple, local-first, and fully executable without cloud infrastructure or databases.

The system uses a multi-agent workflow built with LangGraph and OpenAI API, exposed through a Streamlit interface. It ingests JSON sample data for flights, passengers, and policies, then orchestrates specialized agents to produce rebooking, compensation, payment recovery, and communication decisions.

### MVP Outcomes
- Demonstrate end-to-end disruption handling for cancellation, delay, weather, and crew scenarios.
- Show agent collaboration and auditable decisioning.
- Keep architecture cleanly evolvable into enterprise stack components later.

### Hard Constraints Applied
- Python only.
- Streamlit UI.
- LangGraph orchestration.
- OpenAI API.
- JSON sample data only.
- Hugging Face deployment target.
- No cloud dependencies in runtime architecture.
- No Azure dependencies.
- No database for MVP.

---

## Solution Architecture

### Functional Scope
- Detect and classify disruption type.
- Identify impacted passengers and connection risk.
- Generate alternative itinerary options from sample schedules.
- Calculate compensation and payment recovery recommendations.
- Produce personalized passenger messages.
- Select final strategy via Decision Agent.

### Architecture Style
- Single deployable Streamlit app for MVP.
- Internal event-style workflow using LangGraph state transitions.
- JSON files act as source-of-truth and state snapshots.
- Deterministic policy logic + LLM-assisted reasoning.

---

## Context Diagram

```mermaid
flowchart LR
    USER[Ops Analyst / Demo User] --> UI[Streamlit Web App]
    UI --> ORCH[LangGraph Orchestrator]

    ORCH --> AGENTS[Recovery Agents]
    ORCH --> OPENAI[OpenAI API]
    ORCH --> DATA[JSON Sample Data\nflights, passengers, policies]

    AGENTS --> OUT[Recovery Recommendation\nrebook, compensation, payment, communication]
    OUT --> UI
```

### Context Notes
- User triggers disruption scenarios through Streamlit controls.
- All input data is loaded from local JSON files.
- OpenAI API is the only external runtime dependency.

---

## Component Diagram

```mermaid
flowchart TB
    subgraph Presentation[Presentation Layer]
      ST[Streamlit App]
      DASH[Scenario Dashboard]
      TRACE[Decision Trace View]
    end

    subgraph Orchestration[Orchestration Layer]
      LG[LangGraph Workflow]
      STATE[Shared Recovery State]
      RULES[Policy Rules Module]
    end

    subgraph Agents[Agent Layer]
      A1[Disruption Agent]
      A2[Passenger Impact Agent]
      A3[Rebooking Agent]
      A4[Compensation Agent]
      A5[Payment Recovery Agent]
      A6[Communication Agent]
      A7[Decision Agent]
    end

    subgraph Data[Data Layer]
      J1[flights.json]
      J2[passengers.json]
      J3[itineraries.json]
      J4[policies.json]
      J5[cases_output.json]
    end

    subgraph AI[AI Layer]
      OAI[OpenAI API]
      PROMPTS[Prompt Templates]
    end

    ST --> DASH
    ST --> TRACE
    ST --> LG

    LG --> STATE
    LG --> RULES

    LG --> A1
    LG --> A2
    LG --> A3
    LG --> A4
    LG --> A5
    LG --> A6
    LG --> A7

    A1 --> J1
    A2 --> J2
    A3 --> J3
    A4 --> J4
    A5 --> J4
    A6 --> J2
    A7 --> J5

    A3 --> OAI
    A6 --> OAI
    A7 --> OAI
    OAI --> PROMPTS
```

---

## Agent Interaction Diagram

```mermaid
sequenceDiagram
    autonumber
    participant UI as Streamlit UI
    participant LG as LangGraph Orchestrator
    participant D as Disruption Agent
    participant P as Passenger Impact Agent
    participant R as Rebooking Agent
    participant C as Compensation Agent
    participant PR as Payment Recovery Agent
    participant M as Communication Agent
    participant DEC as Decision Agent

    UI->>LG: Start scenario (cancel/delay/weather/crew)
    LG->>D: Classify disruption
    D-->>LG: disruption profile

    LG->>P: Assess impacted passengers
    P-->>LG: impact assessment

    LG->>R: Generate rebooking options
    R-->>LG: ranked alternatives

    LG->>C: Calculate compensation
    C-->>LG: compensation package

    LG->>PR: Simulate payment recovery
    PR-->>LG: payment action plan

    LG->>M: Draft personalized communication
    M-->>LG: channel-ready messages

    LG->>DEC: Select final recommendation
    DEC-->>UI: final recovery decision + rationale
```

---

## Sequence Diagram (Cancellation Example)

```mermaid
sequenceDiagram
    autonumber
    participant U as Ops User
    participant S as Streamlit App
    participant G as LangGraph
    participant D as Disruption Agent
    participant P as Passenger Impact Agent
    participant R as Rebooking Agent
    participant C as Compensation Agent
    participant PR as Payment Recovery Agent
    participant M as Communication Agent
    participant DE as Decision Agent

    U->>S: Select "Flight Cancellation" scenario
    S->>G: build initial case state from JSON

    G->>D: analyze flight disruption
    D-->>G: cancellation severity and constraints

    G->>P: identify affected passenger segments
    P-->>G: impact list and priority groups

    G->>R: search alternate routes
    R-->>G: ranked itineraries

    G->>C: evaluate entitlement policy
    C-->>G: meal/hotel/refund/travel-credit options

    G->>PR: simulate payment recovery path
    PR-->>G: refund timeline and method

    G->>M: generate customer message set
    M-->>G: personalized comms drafts

    G->>DE: choose final strategy
    DE-->>S: recommendation, confidence, explanation
    S-->>U: dashboard output + decision trace
```

---

## Event Model (MVP Internal Events)

```mermaid
flowchart LR
    E1[scenario.started] --> E2[disruption.assessed]
    E2 --> E3[passenger.impact.assessed]
    E3 --> E4[rebooking.options.generated]
    E3 --> E5[compensation.calculated]
    E5 --> E6[payment.recovery.simulated]
    E4 --> E7[decision.requested]
    E6 --> E7
    E7 --> E8[communication.generated]
    E8 --> E9[case.completed]
```

### Event Semantics
- Events are represented as state transitions in LangGraph nodes.
- Each transition appends to an in-memory audit trail.
- Final state is optionally persisted to cases_output.json.

---

## Folder Structure (GitHub Ready)

```text
SkyRecoverAI/
  README.md
  requirements.txt
  .env.example
  app.py

  docs/
    architecture.md
    prompts.md

  data/
    flights.json
    passengers.json
    itineraries.json
    policies.json
    scenarios/
      cancellation_case.json
      delay_case.json
      weather_case.json
      crew_case.json
    output/
      cases_output.json

  src/
    graph/
      workflow.py
      state.py
      events.py

    agents/
      disruption_agent.py
      passenger_impact_agent.py
      rebooking_agent.py
      compensation_agent.py
      payment_recovery_agent.py
      communication_agent.py
      decision_agent.py

    services/
      openai_client.py
      policy_engine.py
      itinerary_service.py
      recommendation_service.py

    ui/
      pages/
        1_Scenario_Simulator.py
        2_Decision_Trace.py
      components/
        case_summary.py
        recommendation_panel.py

    models/
      domain.py
      dto.py

    utils/
      json_store.py
      logger.py
      config.py

  tests/
    test_agents.py
    test_workflow.py
    test_policy_engine.py

  deployment/
    huggingface/
      README.md
      app_hf.py
```

---

## Hugging Face Deployment (MVP)

### Target
- Deploy as a Streamlit Space on Hugging Face.

### Packaging Approach
- Keep dependencies minimal in requirements.txt.
- Use .env for OPENAI_API_KEY in local dev.
- In Hugging Face Spaces, configure OPENAI_API_KEY as repository secret.
- Load JSON sample data from repository paths.

### Runtime Characteristics
- Stateless app behavior for demo sessions.
- Output snapshots written to data/output/cases_output.json if writable.
- If write access is constrained, keep outputs in session state only.

---

## Future Enterprise Architecture (Evolution Path)

The MVP is intentionally modular so each layer can be replaced without rewriting agent business logic.

### Target Evolution Stack
- Frontend: React.
- API: FastAPI.
- Persistence: PostgreSQL.
- LLM provider: Azure OpenAI.
- Messaging backbone: Azure Service Bus + Event Grid.

### Evolution Diagram

```mermaid
flowchart TB
    subgraph MVPNow[MVP - Portfolio]
      M1[Streamlit UI]
      M2[LangGraph in-process orchestration]
      M3[JSON sample data]
      M4[OpenAI API]
    end

    subgraph EnterpriseLater[Enterprise Target]
      E1[React Frontend]
      E2[FastAPI BFF + Agent APIs]
      E3[PostgreSQL]
      E4[Azure OpenAI]
      E5[Azure Service Bus + Event Grid]
    end

    M1 --> E1
    M2 --> E2
    M3 --> E3
    M4 --> E4
    M2 --> E5
```

### Migration Strategy
1. Extract Streamlit orchestration endpoints into FastAPI while keeping LangGraph graphs unchanged.
2. Replace JSON storage adapters with PostgreSQL repositories.
3. Externalize internal events to Service Bus topics and Event Grid.
4. Move Decision Trace view from Streamlit to React operations console.
5. Swap OpenAI client configuration from public API to Azure OpenAI endpoint.

### Architecture Guardrails for Easy Migration
- Keep agents framework-agnostic and UI-agnostic.
- Use interfaces for data store, message bus, and LLM client.
- Keep domain event contracts versioned from day one.
- Centralize policy logic outside prompts.

---

## Summary

SkyRecoverAI MVP delivers a complete local-first simulation of airline disruption recovery using Python, Streamlit, LangGraph, OpenAI API, and JSON data. It demonstrates seven-agent orchestration with auditable decisioning and provides a clean migration path to React, FastAPI, PostgreSQL, and Azure messaging/LLM services when scaling to enterprise architecture.
