# SkyRecoverAI Agent Architecture

## Overview

This document defines the seven core agents in SkyRecoverAI and standardizes their architecture for the MVP and future enterprise evolution.

### Design Principles
- Single-responsibility agents with explicit contracts.
- Deterministic policy checks before LLM-assisted reasoning.
- Traceable decisions with explainability artifacts.
- Graceful degradation when external dependencies fail.
- Azure-ready integration boundaries via adapters.

---

## 1. Disruption Agent

### Purpose
Detect and normalize disruption events such as cancellation, delay, weather impact, or crew constraints, and assign severity for downstream recovery.

### Inputs
- Scenario payload from UI or event source.
- Flight schedule records.
- Operational attributes: delay duration, airport status, crew status.
- Historical disruption thresholds from policy configuration.

### Outputs
- Normalized disruption object:
  - disruption_type
  - severity_level
  - affected_flights
  - disruption_confidence
- Event marker: disruption.assessed

### Decision Logic
1. Validate disruption payload schema.
2. Classify disruption category.
3. Compute severity using deterministic rules:
   - Delay bands, route criticality, onward connection impact.
4. Set confidence score:
   - High if payload is complete and deterministic rule coverage is strong.
5. Persist decision trace to shared workflow state.

### Prompt Design
- Prompt objective: classify ambiguous disruption context and summarize operational constraints.
- Prompt style: short, schema-constrained output in JSON.
- Guardrails:
  - Must not infer unavailable facts.
  - Must return unknown fields as null, not fabricated values.
- Few-shot examples include weather and crew edge cases.

### Failure Handling
- Invalid payload: route to validation error queue and stop chain.
- Missing critical fields: mark disruption_confidence low and continue with fallback defaults.
- LLM timeout: execute deterministic-only classification.
- Retries: exponential backoff with capped attempts.

### Future Azure Integration
- Input source: Azure Event Grid for operational events.
- Event emission: Azure Service Bus topic disruption.assessed.
- Hosting: Azure Container Apps.
- Telemetry: Application Insights with correlation IDs.

---

## 2. Passenger Impact Agent

### Purpose
Determine which passengers are affected, segment priority groups, and estimate recovery urgency.

### Inputs
- Normalized disruption output.
- Passenger manifest and itinerary records.
- Loyalty tier, special service requests, connection metadata.
- Policy rules for vulnerable-passenger prioritization.

### Outputs
- passenger_impact object:
  - impacted_passenger_ids
  - impact_score_by_passenger
  - priority_groups
  - missed_connection_risk
- Event marker: passenger.impact.assessed

### Decision Logic
1. Join disruption scope with passenger itineraries.
2. Identify direct and downstream impacts.
3. Score passenger impact:
   - Time sensitivity, family group, SSR, loyalty tier.
4. Assign priority buckets:
   - Critical, high, standard.
5. Produce ranked passenger recovery list.

### Prompt Design
- Prompt objective: explain impact rationale and edge-case ordering.
- Required output format: strict JSON list of passenger decisions.
- Constraints:
  - Preserve deterministic score ordering.
  - LLM may add rationale but cannot change base risk inputs.

### Failure Handling
- Missing passenger file: return empty impact list and fail case as data-unavailable.
- Partial manifests: process available records and flag completeness_ratio.
- Inconsistent data keys: apply mapping adapter, then re-validate.

### Future Azure Integration
- Data retrieval via FastAPI service backed by PostgreSQL.
- Event publication to Service Bus topic passenger.impact.assessed.
- Optional cache in Azure Cache for Redis for large manifest lookups.

---

## 3. Rebooking Agent

### Purpose
Generate and rank alternate itineraries that satisfy passenger and policy constraints.

### Inputs
- passenger_impact output.
- Available itinerary inventory (MVP JSON, future live source).
- Rebooking policies: max stops, cabin constraints, protected connections.
- Optional price and schedule metadata.

### Outputs
- rebooking_options object:
  - candidate_options
  - ranked_options
  - policy_violations
  - rebooking_confidence
- Event marker: rebooking.options.generated

### Decision Logic
1. Filter itineraries by feasibility.
2. Compute ranking score using weighted formula:
   - arrival_delta
   - stop_count
   - connection_reliability
   - policy_compliance_penalty
3. Build top-N options per passenger segment.
4. Generate concise rationale for the top choice.

### Prompt Design
- Prompt objective: generate passenger-friendly rationale for selected options.
- Prompt constraints:
  - Do not invent itineraries.
  - Explain trade-offs between top options.
- Output schema includes option_id, score, reason.

### Failure Handling
- No available itineraries: emit no_rebooking_available and trigger compensation-heavy path.
- Corrupt itinerary payload: quarantine record and continue with remaining options.
- LLM unavailable: keep deterministic ranking and omit narrative text.

### Future Azure Integration
- Inventory adapter to airline PSS or partner APIs.
- Publish and consume with Service Bus.
- Persist option snapshots in PostgreSQL or Cosmos DB.
- Scale-out compute via Container Apps jobs for burst disruptions.

---

## 4. Compensation Agent

### Purpose
Compute passenger entitlements for meal, hotel, refund, and travel-credit options based on policy and disruption context.

### Inputs
- disruption output.
- passenger_impact output.
- policies.json compensation rules.
- Jurisdiction flags for regulatory compliance.

### Outputs
- compensation_package object:
  - meal_voucher
  - hotel_voucher
  - refund_eligibility
  - travel_credit_offer
  - compliance_notes
- Event marker: compensation.calculated

### Decision Logic
1. Determine eligibility from rule matrix.
2. Evaluate disruption cause and controllability.
3. Apply passenger-priority modifiers.
4. Produce package with compliance annotation.
5. Flag manual review when high-liability thresholds are exceeded.

### Prompt Design
- Prompt objective: summarize compensation rationale in plain language.
- Constraint model:
  - Policy rules are source-of-truth.
  - LLM cannot increase monetary values beyond computed caps.
- Structured output with entitlement and explanation fields.

### Failure Handling
- Missing policy rules: halt compensation step and escalate as configuration error.
- Conflicting rules: apply highest-precedence rule and emit warning.
- Unknown jurisdiction: default to conservative baseline package and flag review.

### Future Azure Integration
- Policy service hosted in FastAPI with rule versioning.
- Immutable compensation audit stream in Event Grid or Service Bus.
- Compliance logging to Azure Monitor and Log Analytics.

---

## 5. Payment Recovery Agent

### Purpose
Simulate or execute financial recovery actions such as refund route, travel-credit issuance, and settlement timing.

### Inputs
- compensation_package output.
- passenger payment profile (method token, currency, channel).
- payment policy: refund windows, credit validity rules.

### Outputs
- payment_recovery_plan object:
  - recommended_mode
  - amount
  - estimated_settlement_time
  - fallback_mode
- Event marker: payment.recovery.simulated

### Decision Logic
1. Calculate total eligible amount.
2. Choose preferred recovery mode:
   - Original payment method refund when eligible.
   - Travel credit fallback for unsupported channels.
3. Estimate settlement timeline by channel.
4. Attach reversible action token for future execution.

### Prompt Design
- Prompt objective: generate customer-facing explanation of payment path.
- Strict constraints:
  - Use computed amount only.
  - Never include payment-sensitive details in response.
- Output fields: summary_text, timeline_text.

### Failure Handling
- Missing payment profile: default to travel credit and flag missing profile.
- Currency mismatch: normalize using configured FX table or fail-safe default currency.
- Execution provider timeout: keep simulation status and retry asynchronously.

### Future Azure Integration
- Integration with payment microservice via FastAPI.
- Command dispatch over Service Bus queue payment.recovery.command.
- Secret handling via Azure Key Vault.

---

## 6. Communication Agent

### Purpose
Compose personalized, channel-ready messages with actionable recovery options and clear next steps.

### Inputs
- rebooking_options output.
- compensation_package output.
- payment_recovery_plan output.
- Passenger profile and language preference.
- Communication templates.

### Outputs
- communication_bundle object:
  - sms_message
  - email_message
  - app_notification
  - tone_profile
  - localization_status
- Event marker: communication.generated

### Decision Logic
1. Select channel strategy by passenger preference and urgency.
2. Build message payload from approved templates.
3. Insert personalized option details.
4. Apply readability and policy checks.
5. Emit delivery-ready communication package.

### Prompt Design
- Prompt objective: concise, empathetic, action-oriented communication.
- Content controls:
  - No legal promises beyond policy outputs.
  - No fabricated option IDs or amounts.
- Format variants for SMS, email, and push notification.

### Failure Handling
- Missing localization template: fallback to English template with indicator.
- Oversized SMS content: auto-trim to channel-safe length.
- LLM refusal or failure: use deterministic template rendering only.

### Future Azure Integration
- Delivery via Azure Communication Services or third-party providers.
- Event tracking through Event Grid notification events.
- Template management backed by centralized content service.

---

## 7. Decision Agent

### Purpose
Select the final, case-level recovery strategy by combining outputs from all agents and enforcing policy constraints.

### Inputs
- disruption output.
- passenger_impact output.
- rebooking_options output.
- compensation_package output.
- payment_recovery_plan output.
- communication_bundle output.
- Policy and confidence thresholds.

### Outputs
- final_decision object:
  - selected_strategy
  - confidence
  - decision_rationale
  - required_human_review
- Event marker: decision.finalized

### Decision Logic
1. Validate completeness of upstream agent outputs.
2. Compute strategy candidates:
   - Rebook-first
   - Compensation-first
   - Hybrid rebook-plus-compensation
3. Score candidates on:
   - passenger outcome
   - compliance risk
   - operational feasibility
4. Pick highest valid score under policy constraints.
5. Trigger human review for low confidence or high liability.

### Prompt Design
- Prompt objective: compare strategy candidates and produce transparent rationale.
- Mandatory fields: strategy, confidence, top_risks, why_not_alternatives.
- Constraint: cannot select strategy with unresolved critical policy violations.

### Failure Handling
- Missing upstream outputs: stop finalization and emit dependency_missing.
- Tie score between strategies: apply deterministic tie-break rules.
- Low confidence: auto-route to manual review queue.

### Future Azure Integration
- Enterprise orchestration with LangGraph service workers on Container Apps.
- Decision events published to Service Bus topic decision.finalized.
- Human review workflow integrated with React operations console and FastAPI backend.

---

## Cross-Agent Standards

### Common Input Contract
- case_id
- correlation_id
- event_timestamp
- schema_version
- trace_context

### Common Output Contract
- agent_name
- status
- confidence
- payload
- diagnostics

### Observability Requirements
- Structured logs for each agent step.
- Latency and failure metrics per agent.
- End-to-end trace from scenario.started to decision.finalized.

### Security and Governance
- Redact PII in logs and prompts.
- Use policy guards before financial or legal outputs.
- Persist explainability artifacts for every case decision.
