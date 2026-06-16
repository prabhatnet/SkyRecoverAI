# SkyRecoverAI Hugging Face Demo — Flow Design & Screen Layout

## Overview

This document specifies the ideal 3-minute demo experience for hiring managers, architects, and technical directors. Optimized for high-impact presentation of agentic AI orchestration patterns.

**Duration:** 3 minutes (180 seconds)  
**Entry Point:** `streamlit_hf_demo.py` (Hugging Face Spaces)  
**Scenario:** ATL Thunderstorm (Critical, 284 passengers, 18 flights)

---

## Timeline & Screen-by-Screen Breakdown

### **Screen 1: Title & Intro** (0:00–0:15)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ ✈️ SkyRecoverAI                                             │
│ Agentic AI for Airline Disruption Recovery                 │
│                                                              │
│ A multi-agent LLM workflow that automates passenger        │
│ recovery decisions in real-time.                            │
│                                                              │
│ Demo: 3-minute walkthrough. Simulates a critical           │
│ weather disruption and demonstrates AI-driven recovery     │
│ orchestration for hiring evaluators.                        │
│ ─────────────────────────────────────────────────────────── │
│                                                              │
│ 1️⃣ TRIGGER DISRUPTION SCENARIO                             │
│ Scenario: ATL Thunderstorm — Critical severity,            │
│ 284 passengers affected.                                    │
│                                                              │
│ [🌩️ ATL Thunderstorm]       [CRITICAL]                     │
│ Weather event forced reroute.  Airport: ATL                │
│ 6+ hour delays likely.         Flights: 18                 │
│                                Passengers: 284              │
│                                                              │
│ [▶ START DEMO WORKFLOW]                                    │
└─────────────────────────────────────────────────────────────┘
```

**Talking Point:**  
*"SkyRecoverAI is an agentic AI system that automates airline disruption recovery. It orchestrates 7 specialized LLM agents in a deterministic pipeline, each responsible for a specific recovery step. This ATL thunderstorm scenario is critical severity—284 passengers affected across 18 flights. Let's run the recovery workflow."*

**Presenter Action:**  
Click the **"Start Demo Workflow"** button.

---

### **Screen 2: Agent Pipeline Execution** (0:15–0:45)

**Layout (animated progress bar):**
```
┌─────────────────────────────────────────────────────────────┐
│ [████████░░░░░░░░░░░░░░░░] Running Rebooking Agent…        │
│                                                              │
│ Disruption Agent: Classifying event: Weather, Critical      │
│ Passenger Impact Agent: Ranking 284 passengers by priority  │
│ Rebooking Agent: Searching alternatives: 3 viable          │
│                 itineraries found                           │
│                                                              │
│ ✅ Completed: 3 agents                                      │
│ ⏳ In Progress: Compensation Agent                           │
│ ⏳ Pending: Payment Recovery, Communication, Decision       │
└─────────────────────────────────────────────────────────────┘
```

**What Happens:**
- Progress bar fills from 0–100% (7 steps, 0.4s each = ~2.8s total agent runtime)
- Status message updates: shows current agent name + brief task
- Each agent step is visually marked with emoji (✅ or ⏳)

**Talking Point:**  
*"Behind the scenes, 7 agents execute in sequence. Each agent is independent and contract-based: it receives validated input, processes it, and returns validated output. If an agent times out, there's a deterministic fallback. Let's see what each one did."*

**Presenter Action:**  
Let animation complete (no interaction). ~30 seconds.

---

### **Screen 3: Disruption & Impact Summary** (0:45–1:30)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 2️⃣ DISRUPTION IMPACT ASSESSMENT                             │
│                                                              │
│ ┌──────────┬──────────────┬──────────────┬──────────────┐  │
│ │ Case ID  │ Flights      │ Passengers   │ Duration     │  │
│ │ 4F3084C9 │ 18           │ 284          │ 360 min      │  │
│ └──────────┴──────────────┴──────────────┴──────────────┘  │
│                                                              │
│ PASSENGER PRIORITY DISTRIBUTION                             │
│                                                              │
│ ┌─────────────┬─────────────┬─────────────┐               │
│ │ 🔴 CRITICAL │ 🟠 HIGH     │ ⚪ STANDARD │               │
│ │ 24 (8%)     │ 87 (31%)    │ 173 (61%)   │               │
│ └─────────────┴─────────────┴─────────────┘               │
│                                                              │
│ Passenger Impact Agent output: Ranked by loyalty tier,      │
│ connection risk, and class. Critical tier gets priority     │
│ rebooking and upgraded compensation.                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Talking Points:**

*"The Passenger Impact Agent immediately ranked all 284 passengers into priority groups. Critical: 24 (mostly business class with tight connections). High: 87 (economy with connections or loyalty status). Standard: 173 (local flights, no time pressure). This ranking drives the entire recovery strategy—we can't please everyone equally, so the algorithm focuses on people with the most pressing needs."*

**Presenter Action:**  
Scroll to reveal full passenger distribution. ~15 seconds viewing.

---

### **Screen 4: Rebooking Options** (1:30–2:00)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 3️⃣ RANKED REBOOKING OPTIONS                                 │
│ Agent evaluated 47 available itineraries and ranked by      │
│ passenger preference.                                        │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ⭐ RECOMMENDED                                          │ │
│ │ ✈️ SR810 (ATL → LHR, next available)                    │ │
│ │ Cabin: Business · 14 seats available                    │ │
│ │                                                          │ │
│ │ Score: ████████░░ 88%                                   │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Backup Option 1                                         │ │
│ │ ✈️ SR812 (ATL → LHR +8h via Boston)                     │ │
│ │ Cabin: Premium Economy · 47 seats available             │ │
│ │                                                          │ │
│ │ Score: ███████░░░ 74%                                   │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Talking Points:**

*"The Rebooking Agent scanned 47 available itineraries and ranked them by passenger preference. The top option is SR810—direct ATL to LHR, next available, business class upgrade automatically assigned to critical passengers. Score is 88%: high confidence in passenger acceptance. If that sells out, we fall back to SR812 with 74% confidence. Each option is scored based on delay, class, and passenger tier match."*

**Presenter Action:**  
Scroll to see 1–2 backup options. ~15 seconds viewing.

---

### **Screen 5: Compensation Decision** (2:00–2:30)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 4️⃣ COMPENSATION DECISION                                    │
│ Policy-driven entitlements automatically calculated         │
│ per passenger tier.                                          │
│                                                              │
│ ┌──────────────┬──────────────┬──────────────┬────────────┐ │
│ │ Meal         │ Hotel        │ Refunds      │ Travel     │ │
│ │ Vouchers     │ Vouchers     │              │ Credit     │ │
│ │ $18,200      │ $31,700      │ $26,304      │ $14,012    │ │
│ └──────────────┴──────────────┴──────────────┴────────────┘ │
│                                                              │
│ TOTAL ESTIMATED RECOVERY COST: $90,216                      │
│                                                              │
│ Policy Applied: Meal and Hotel                              │
│ Payment Mode: Travel Credit                                 │
│                                                              │
│ Breakdown Logic:                                             │
│ • 24 Critical passengers: full meal + hotel (tier 1)        │
│ • 87 High passengers: meal + hotel (tier 2)                │
│ • 173 Standard passengers: meal only                        │
│ • Refund + Credit: capped at ticket value × delay factor   │
│                                                              │
│ Confidence: Policy-driven → 100% auditability              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Talking Points:**

*"The Compensation Agent applied policy rules automatically. This is critical for enterprise compliance—no agent makes a guess about what to offer. The rules are:*
- *Critical tier: meal + hotel (we're covering their inconvenience)*
- *High tier: meal + hotel (loyalty reward)*
- *Standard tier: meal only*
- *All tiers get refund or travel credit capped at ticket value plus 25% for delays.*

*Total estimated cost: $90k. This is shown to the airline's operations team for approval before any communication is sent. Policy guardrails prevent the AI from over-committing or under-compensating."*

**Presenter Action:**  
Point to KPI bar, then show the breakdown logic. ~15 seconds viewing.

---

### **Screen 6: Final Decision & Strategy** (2:30–2:50)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 5️⃣ FINAL RECOVERY STRATEGY                                  │
│                                                              │
│ ┌──────────────┬──────────────┬──────────────┐             │
│ │ Strategy     │ Confidence   │ Review Req'd  │             │
│ │ REBOOK +     │ 87%          │ YES          │             │
│ │ MEAL +       │              │ (Critical    │             │
│ │ HOTEL        │              │  Severity)   │             │
│ └──────────────┴──────────────┴──────────────┘             │
│                                                              │
│ Rationale:                                                   │
│ "Strategy balances passenger satisfaction with cost.       │
│ Rebooking via SR810 gets 86% of passengers to              │
│ destination within 6 hours. Meal + hotel covers            │
│ immediate needs. Loyalty tier weighting ensures            │
│ top-tier passengers get cabin upgrades. Policy             │
│ guardrails prevent violations. Human sign-off             │
│ required for critical-severity decisions."                 │
│                                                              │
│ ⚠️ CRITICAL SEVERITY → HUMAN-IN-THE-LOOP REQUIRED          │
│    Before execution, an operations manager must             │
│    approve this decision. Full audit trail provided.        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Talking Points:**

*"The Decision Agent selected the optimal strategy: REBOOK + MEAL + HOTEL, with 87% confidence. Notice the human review flag—because this is critical severity, it doesn't execute automatically. Instead, it goes to an operations manager who sees the full rationale, passenger impact, and cost. They can approve, modify, or reject. That's the enterprise pattern: high-confidence decisions are autonomous, but critical ones have human oversight built in."*

**Presenter Action:**  
Read the rationale aloud. Emphasize human review. ~15 seconds viewing.

---

### **Screen 7: Agent Pipeline Trace** (2:50–3:00)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ 6️⃣ AGENT PIPELINE TRACE                                     │
│                                                              │
│ Total Agents: 7 | Total Latency: 2.8s | Avg Confidence: 88%│
│                                                              │
│ ▼ Step 1: Disruption Agent                    ✅  0.3s     │
│   Confidence: ████████░░ 92%                                │
│                                                              │
│ ▼ Step 2: Passenger Impact Agent              ✅  0.4s     │
│   Confidence: █████████░ 91%                                │
│                                                              │
│ ▼ Step 3: Rebooking Agent                     ✅  0.5s     │
│   Confidence: ████████░░ 88%                                │
│                                                              │
│ [View all 7 steps]                                           │
│                                                              │
│ Full state JSON available for inspection at bottom.          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Talking Points:**

*"Total pipeline execution: 2.8 seconds. Each agent produced confidence scores—disruption agent 92%, passenger impact 91%, rebooking 88%, etc. If any step had low confidence or failed, it would show in the trace. Operations teams can audit the decision trail. This is what we mean by explainability: every choice is traceable."*

**Presenter Action:**  
Scroll to show all 7 agents (optional). End on this screen to show full transparency.

---

### **Screen 8: Closing Message** (3:00 → End)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ ═══════════════════════════════════════════════════════════ │
│ KEY TECHNICAL HIGHLIGHTS                                    │
│ ═══════════════════════════════════════════════════════════ │
│                                                              │
│ ✅ Multi-Agent Orchestration — 7 specialized LLM agents     │
│ ✅ Policy-Driven Decisions — Business rules guard outputs   │
│ ✅ Full Explainability — Every decision traced              │
│ ✅ Graceful Degradation — Fallbacks for LLM failures        │
│ ✅ Enterprise Architecture — Python + Streamlit + LangGraph │
│ ✅ Azure-Ready — Event Grid, Service Bus, Container Apps    │
│                                                              │
│ PORTFOLIO PROJECT: Built to demonstrate agentic AI design   │
│ patterns, multi-step workflow orchestration, and            │
│ production-grade error handling.                             │
│                                                              │
│ Learn more: [GitHub] · [Architecture Docs] · [Agent Design] │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Presenter Closing:**  
*"That's the 3-minute walkthrough. What you saw is a production-ready pattern for multi-step AI workflows in enterprise. Each agent is independent, testable, and upgradeable. Policies prevent violations. Full transparency for auditing. We've designed this to scale on Azure—agents can run on serverless, state lives in durable storage, and workflow orchestration is handled by LangGraph. Questions?"*

---

## Variant: Extended Demo (7–10 Minutes)

If your audience wants deeper dives, branch to the **full multi-page app**:

```bash
streamlit run streamlit_app.py
```

Additional screens:

| Screen | Time | Purpose |
|--------|------|---------|
| Dashboard Hub | 1 min | KPI overview, active cases |
| Affected Passengers (full) | 2 min | Filterable passenger table, tier/class/SSR breakdown |
| Recovery Recommendations (full) | 1.5 min | Comparison table, alternative scenarios |
| Compensation Analysis (full) | 2 min | Cost breakdown by tier, per-passenger estimate |
| Agent Decision Trace (full) | 1.5 min | Full audit trail with step timing |

**Total:** ~8 minutes for full walkthrough with Q&A.

---

## Demo Checklist

### Before You Start
- [ ] `.env` file has `OPENAI_API_KEY` configured (or use mock mode if offline)
- [ ] Virtual environment activated
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Streamlit app launches: `streamlit run streamlit_hf_demo.py`
- [ ] Button click triggers workflow without errors
- [ ] All 6 sections render on a single page

### Presenter Preparation
- [ ] Review talking points above (practice 1-2x)
- [ ] Customize for audience (hiring manager vs. architect focus)
- [ ] Have browser open to documentation links for post-demo Q&A
- [ ] Have GitHub repo ready for code walkthroughs if asked
- [ ] Prepare response to "can this run in production?" (answer: yes, with DB + queue → see docs)

### Timing Notes
- **3-minute target:** Screen 1 (15s) → Trigger (15s) → Agents (30s) → Impact (30s) → Rebooking (30s) → Compensation (30s) → Decision (30s) → Trace (10s) = 180s
- **Buffer time:** Don't count intro/closing in the 3 minutes; those are free
- **If running long:** Skip "Agent Pipeline Trace" and jump to "Final Decision" (saves ~45 seconds)

---

## Q&A Prep

**"How does it handle failures?"**  
Each agent has fallback logic. If the LLM times out, we use deterministic rules. If schema validation fails, we flag low confidence and escalate to human review. No silent failures.

**"What if the LLM is hallucinating?"**  
Policy guards catch violations. If compensation exceeds a threshold, human review is mandatory. Decisions that conflict with known passenger data are rejected.

**"Why multi-agent instead of one big prompt?"**  
One big prompt is unpredictable—it might invent facts, make compliance mistakes, or fail silently. Multi-agent lets us isolate concerns: disruption classification is deterministic, rebooking searches against real data, compensation follows policy rules, decision logic is auditable. Failures are localized.

**"Can this scale?"**  
MVP uses JSON files + Streamlit. Production would use PostgreSQL for state, Azure Service Bus for queues, Container Apps for agents, Event Grid for event routing. We've prepared those boundaries.

**"What's the dev effort to customize?"**  
Each agent is <100 lines of code. To add a new recovery path, you subclass `Agent`, define input/output schema, add to the LangGraph DAG. No monolithic codebase rewrite.

---

## Key Metrics to Highlight

| Metric | Value | Why It Matters |
|--------|-------|---|
| Pipeline latency | 2.8 seconds | Shows real-time decisioning (vs. hours of manual review) |
| Avg. confidence | 88% | Demonstrates high-confidence output (>85% threshold for autonomy) |
| Passengers served | 284 in 1 case | Shows scale (multi-agent pipeline handles bulk decisions) |
| Cost calculated | $90k in policy-driven mode | Compliance: every voucher is auditable, not guessed |
| Agents in DAG | 7 independent agents | Architecture: modular design, each upgradeable |
| Human review required | 1 of 1 critical case | Enterprise: safety guardrails built in |

---

## Deployment Notes

### Hugging Face Spaces
1. Push repo to GitHub
2. Create Hugging Face Space linked to repo
3. Set `streamlit_hf_demo.py` as entry point (if Space doesn't auto-detect)
4. Set `OPENAI_API_KEY` in Space Secrets (or leave blank for mock mode)
5. Space will auto-deploy from main branch

### Local Demo
```bash
git clone <your-repo>
cd SkyRecoverAI
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_hf_demo.py
```

### Offline/Mock Mode
If no OpenAI API key available, the simulation service still generates realistic data deterministically. Demo works in isolation.
