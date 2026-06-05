# SkyRecoverAI Repository Structure

## Required Folders Overview

### agents
- Responsibility: Implements domain agents and their recovery decisions.
- Design rationale: Strong separation by business capability keeps prompts, logic, and tests isolated.
- Future scalability: Promote each agent into a standalone service with event subscriptions.

### workflows
- Responsibility: Contains LangGraph flow definitions, state contracts, and event progression.
- Design rationale: Separates orchestration from business logic to simplify debugging and replay.
- Future scalability: Versioned workflow definitions and distributed orchestration through message bus.

### services
- Responsibility: Shared technical services such as OpenAI client, config, and JSON persistence helpers.
- Design rationale: Avoids duplicate infrastructure code across agents and workflows.
- Future scalability: Replace local adapters with enterprise implementations without domain rewrites.

### data
- Responsibility: Sample scenario inputs and generated outputs for deterministic demos.
- Design rationale: Database-free MVP with auditable fixtures and repeatable runs.
- Future scalability: Migrate to schema-managed persistence and event stores.

### docs
- Responsibility: Architecture, standards, decisions, and onboarding guides.
- Design rationale: Creates a durable engineering narrative and portfolio quality.
- Future scalability: Expand into ADRs, API contracts, and operational runbooks.

### tests
- Responsibility: Unit, integration, and workflow correctness checks.
- Design rationale: Keeps confidence high as prompt logic and workflow complexity evolve.
- Future scalability: Add contract tests, load tests, and scenario regression packs.
