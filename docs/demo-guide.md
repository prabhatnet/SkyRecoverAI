# SkyRecoverAI Demo Guide for Hiring Evaluators

## Quick Demo (3 Minutes)

This guide is for evaluators using the Hugging Face Spaces demo or running locally.

### Before You Start
- Environment: Python 3.11+, all dependencies installed
- OpenAI API key configured in `.env` or environment
- Run: `streamlit run streamlit_hf_demo.py`

### Demo Flow

| Time | Step | What to Say | What to Show |
|---|---|---|---|
| 0:00–0:15 | **Intro** | "SkyRecoverAI is an agentic AI system that automates airline disruption recovery. It's built with LangGraph and orchestrates 7 specialized LLM agents." | Title, brief description, scenario selector |
| 0:15–0:45 | **Trigger** | "This ATL thunderstorm scenario is critical severity: 284 passengers affected, 18 flights impacted. Let's start the recovery workflow." | Click "Start Demo Workflow" button |
| 0:45–1:30 | **Pipeline** | "Behind the scenes, 7 agents execute in sequence. Each one is responsible for a specific recovery step: disruption classification, passenger impact assessment, rebooking options, compensation policy, payment recovery simulation, communication drafting, and final strategy selection." | Watch progress animation as agents run (auto-plays) |
| 1:30–2:00 | **Impact** | "284 passengers were assessed and ranked into priority groups. 24 are Critical (business class, loyal, connections at risk), 87 are High, 173 are Standard. This ranking drives the recovery strategy." | Show passenger priority distribution (bars) |
| 2:00–2:30 | **Recovery** | "The Rebooking Agent found 3 viable alternatives. The top option gets passengers to their destination +4 hours with high passenger preference score (88%)." | Show top 2 rebooking options with confidence bars |
| 2:30–2:50 | **Cost** | "The Compensation Agent applied policy rules automatically. Meal + hotel vouchers total $49,700 based on disruption severity and passenger tier breakdown. Payment is routed through travel credit mode." | Show cost KPI bar and breakdown |
| 2:50–3:00 | **Decision** | "The Decision Agent selected the optimal strategy: REBOOK + MEAL + HOTEL, with 87% confidence. Because severity is Critical, human review is flagged before execution — full auditability and control." | Show final strategy, confidence, human review flag |

### Talking Points

#### For Hiring Managers
- **Agentic AI:** Each agent is independently testable and updatable. You can swap GPT-4 for Claude, adjust prompts, or retrain without touching other agents.
- **Explainability:** Every decision is traced. You see which agent made which call, how confident it was, and how long it took. No black boxes.
- **Business Value:** Reduces manual decision time from hours to seconds. Policy guardrails ensure no compliance violations. Passenger satisfaction up, costs down.

#### For Architects
- **Orchestration:** Clean LangGraph state machine. Each agent receives a contract-validated input and returns a contract-validated output. Errors are caught at boundaries.
- **Scalability:** Stateless agent functions → can run on serverless. Workflow state stored in durable store. Integrates with Azure Service Bus, Event Grid, Container Apps.
- **Design Patterns:** This is a reference implementation of multi-step AI workflows. Deterministic policy engine + LLM-assisted reasoning is the enterprise pattern.

#### For Senior Engineers
- **Code Quality:** Type hints throughout. Modular design: each agent is <100 LOC. Simulation service is deterministic — same input, same output. Tests can mock agents independently.
- **Production Readiness:** Error handling for timeouts, schema violations, missing data. Fallback strategies (e.g., deterministic rebooking if LLM fails). Audit trails for compliance.
- **Extensibility:** To add a new recovery path, you subclass `Agent`, define input/output schema, add to workflow DAG. No monolithic codebase changes.

### If Someone Asks…

**"How does it handle failures?"**  
Each agent has fallback logic. If the LLM times out, we revert to deterministic classification. If a schema validation fails, we mark low confidence and escalate to human review. No silent failures.

**"Can this run in production?"**  
This MVP is designed to scale. Replace JSON files with PostgreSQL. Replace Streamlit with FastAPI. Deploy agents to Container Apps. Workflow state lives in Service Bus. We've prepared the abstraction boundaries.

**"What if the LLM is wrong?"**  
Policy guards catch violations before execution. If compensation exceeds a threshold, human review is mandatory. The Decision Agent flags high-risk decisions automatically. And yes, we log everything for post-mortems.

**"How is this different from just prompting GPT-4?"**  
This is multi-step orchestration with checkpoints. A single prompt to GPT-4 might hallucinate passenger names or invent itineraries. Here, each agent validates its output against schema. Agents can't invent data — only synthesize from given facts. Plus, if one agent fails, others continue with graceful degradation.

### Full Application Tour

If you want to show the **full multi-page app** (not the 3-min demo):

```bash
streamlit run streamlit_app.py
```

This gives you:
- **Dashboard:** Live KPI overview + quick-launch scenarios
- **Disruption Simulator:** Custom event entry, full pipeline visualization
- **Affected Passengers:** Filterable passenger table, tier/class/SSR analysis
- **Recovery Recommendations:** Ranked options, comparison table, strategy rationale
- **Compensation Analysis:** Cost breakdown by tier, per-passenger entitlements
- **Agent Decision Trace:** Full audit trail with step-by-step confidence scores

**Time required:** ~10 minutes for full walkthrough

---

## Demo Checklist

- [ ] `.env` file created with `OPENAI_API_KEY` set
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Streamlit app launches without errors: `streamlit run streamlit_hf_demo.py`
- [ ] Button click triggers workflow successfully
- [ ] All 6 sections render correctly
- [ ] Talking points reviewed and personalized for your audience
