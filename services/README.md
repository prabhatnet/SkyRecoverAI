# Services Folder

## Responsibility
Contains reusable technical services and integration adapters used by agents and workflows.

## Design Rationale
- Separates infrastructure concerns from business logic.
- Allows isolated mocking in tests.
- Keeps API clients and utility logic consistent across agents.

## Future Scalability Considerations
- Split each service adapter into dedicated packages for independent release cadence.
- Introduce retry, circuit-breaker, and bulkhead policies for external integrations.
- Support multi-provider strategies (OpenAI, Azure OpenAI, model routers).
