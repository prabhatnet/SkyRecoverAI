# Tests Folder

## Responsibility
Contains automated tests for agents, workflow orchestration, and shared services.

## Design Rationale
- Encourages fast regression detection for frequent prompt and policy changes.
- Aligns tests with architecture boundaries (agent/service/workflow).
- Supports contributor confidence and CI readiness.

## Future Scalability Considerations
- Add scenario replay tests from production-like disruption datasets.
- Add contract tests for future FastAPI endpoints.
- Add performance tests for batch disruption spikes.
