# Agents Folder

## Responsibility
Contains domain-specific AI agents that each own one business capability in passenger recovery.

## Design Rationale
- Enforces single responsibility per agent.
- Keeps prompts, tools, and decision logic isolated for maintainability.
- Enables independent testing and replacement of each agent implementation.

## Future Scalability Considerations
- Split each agent into its own deployable service when moving to distributed runtime.
- Add async message handlers per agent for event bus integration.
- Add model-routing policy to choose specialized models per agent class.
