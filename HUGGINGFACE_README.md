# SkyRecoverAI on Hugging Face Spaces

Welcome to the **SkyRecoverAI** demo — a production-grade agentic AI system for airline disruption recovery.

## Demo Overview

This is a **3-minute technical walkthrough** designed for hiring managers, architects, and engineering leaders.

**What you'll see:**
1. Real-time disruption event (ATL Thunderstorm)
2. AI agent pipeline: 7 specialized agents orchestrated in sequence
3. Passenger impact assessment and recovery options
4. Policy-driven compensation decisions
5. Final recovery strategy with full explainability

## How to Run

### Local Development
```bash
git clone https://github.com/yourusername/SkyRecoverAI
cd SkyRecoverAI
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
streamlit run streamlit_hf_demo.py
```

### Hugging Face Spaces
This Space is configured to run `streamlit_hf_demo.py` as the entry point.

File structure:
```
SkyRecoverAI/
  streamlit_hf_demo.py        ← HF Spaces entry point
  streamlit_app.py            ← Full multi-page app
  requirements.txt
  services/
    simulation_service.py
    json_store.py
  ui/
    components.py
  pages/
    1_Disruption_Simulator.py
    2_Affected_Passengers.py
    3_Recovery_Recommendations.py
    4_Compensation_Analysis.py
    5_Agent_Decision_Trace.py
  data/
    schemas/
    samples/
  docs/
    agents-architecture.md
    langgraph-workflow-design.md
    sample-data-design.md
    dashboard-wireframes.md
```

## Architecture Highlights

### Agent Pipeline
```
Disruption → Passenger Impact → Rebooking → Compensation → Payment Recovery → Communication → Decision
```

Each agent outputs confidence scores and latency metrics for full auditability.

### Design Principles
- **Single-responsibility agents** with explicit I/O contracts
- **Policy guards** before LLM-assisted reasoning
- **Graceful degradation** on LLM timeouts or schema failures
- **Full traceability** — every decision step persisted with rationale
- **Enterprise-ready** — designed for Azure Container Apps, Service Bus, Event Grid

### Tech Stack
- **Orchestration:** LangGraph
- **LLM:** OpenAI API (gpt-4o-mini recommended)
- **UI:** Streamlit
- **Language:** Python 3.11+
- **Data:** JSON files (MVP) → PostgreSQL + Service Bus (production)

## Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini  # or gpt-4, gpt-4-turbo, etc.
```

For Hugging Face Spaces, set these in the Space Secrets tab.

## Full Application

The demo showcases only one scenario. The full app includes:

- **Dashboard:** Real-time KPI overview
- **Disruption Simulator:** 3 pre-built scenarios + custom event entry
- **Affected Passengers:** Impact segmentation and detailed passenger profiles
- **Recovery Recommendations:** Ranked rebooking options with agent confidence
- **Compensation Analysis:** Cost breakdown, tier analysis, per-passenger entitlements
- **Agent Decision Trace:** Full audit trail with step-by-step confidence scores

Run the full app:
```bash
streamlit run streamlit_app.py
```

## Documentation

- [Agent Architecture](docs/agents-architecture.md) — Detailed spec for all 7 agents
- [LangGraph Workflow Design](docs/langgraph-workflow-design.md) — State model, step contracts, Mermaid diagrams
- [Sample Data Design](docs/sample-data-design.md) — JSON schemas and realistic datasets
- [Dashboard Wireframes](docs/dashboard-wireframes.md) — UI design, user flows, component specs

## Demo Talking Points

**For Hiring Managers:**
- ✅ Production-grade agent orchestration with LangGraph
- ✅ Policy-driven guardrails for financial/legal decisions
- ✅ Multi-step AI workflows with graceful error handling
- ✅ Full observability and explainability (no black-box LLM)
- ✅ Enterprise architecture patterns ready for Kubernetes/Cloud

**For Architects:**
- ✅ Clean separation of concerns: agents, workflows, data, UI
- ✅ Deterministic policy engine + LLM-assisted reasoning
- ✅ Azure integration boundaries prepared (Event Grid, Service Bus, Container Apps)
- ✅ Data contracts with JSON Schema
- ✅ Comprehensive audit trails for compliance and debugging

**For Engineers:**
- ✅ Type hints throughout (Python 3.11+ idioms)
- ✅ Modular agent design: each can be swapped/upgraded independently
- ✅ Simulation service: deterministic data generation for fast demos
- ✅ Streamlit + LangGraph: minimal dependencies, easy to extend
- ✅ Schema validation + validation errors → immediate feedback

## Next Steps

1. Review the [architecture documentation](docs/agents-architecture.md)
2. Inspect the [LangGraph workflow design](docs/langgraph-workflow-design.md)
3. Explore the [full multi-page app](streamlit_app.py) for detailed UX
4. Check out the [sample data contracts](docs/sample-data-design.md) for data model
5. Deploy to Azure Container Apps or Kubernetes using the included patterns

## License

Portfolio project. 

## Contact

Questions about the demo or the system design? Refer to the documentation files or reach out via GitHub issues.

---

**Built with:** Python · Streamlit · LangGraph · OpenAI · JSON  
**Target Deployment:** Hugging Face Spaces · Azure Container Apps · Kubernetes
