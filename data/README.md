# Data Folder

## Responsibility
Stores static sample inputs and generated case outputs for the MVP.

## Design Rationale
- Keeps the MVP database-free while preserving reproducible scenarios.
- Makes demos deterministic and easy to reset.
- Enables transparent review of business assumptions.

## Future Scalability Considerations
- Replace JSON files with repository/service interfaces backed by PostgreSQL.
- Add schema validation and versioning for event and case records.
- Archive historical runs into partitioned storage for analytics.

## Data Contracts
- JSON Schemas: [schemas](schemas)
- Sample records: [samples](samples)

Key references:
- [Airports Schema](schemas/airports.schema.json)
- [Flights Schema](schemas/flights.schema.json)
- [Passengers Schema](schemas/passengers.schema.json)
- [Bookings Schema](schemas/bookings.schema.json)
- [Disruptions Schema](schemas/disruptions.schema.json)
