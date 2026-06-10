# SkyRecoverAI Realistic Airline Sample Data Design

## Objective

Define production-quality JSON data contracts and sample records for SkyRecoverAI simulation data.

Datasets:
- airports.json
- flights.json
- passengers.json
- bookings.json
- disruptions.json

---

## Required Dataset Sizes

| Dataset | Required Record Count |
|---|---:|
| airports.json | 20 |
| flights.json | 100 |
| passengers.json | 500 |
| bookings.json | 500 |
| disruptions.json | Variable (recommended 30-80) |

Notes:
- The schema files enforce exact sizes for airports, flights, passengers, and bookings.
- Disruptions are event-driven and intentionally variable.

---

## File Locations

### Schemas
- data/schemas/airports.schema.json
- data/schemas/flights.schema.json
- data/schemas/passengers.schema.json
- data/schemas/bookings.schema.json
- data/schemas/disruptions.schema.json

### Sample Records
- data/samples/airports.sample.json
- data/samples/flights.sample.json
- data/samples/passengers.sample.json
- data/samples/bookings.sample.json
- data/samples/disruptions.sample.json

---

## Domain Modeling Rationale

1. Airports as reference master data
- Stable dimension table for flight network realism.
- Includes region and hub status for routing behavior.

2. Flights as operational schedule feed
- Includes ticket class availability and possible connection flights.
- Includes status and aircraft type to simulate disruption propagation.

3. Passengers as traveler profile registry
- Includes passenger name and loyalty tier.
- Includes SSR and language preference for personalization and fairness.

4. Bookings as traveler intent and trip execution layer
- Includes ticket class and detailed flight segment references.
- Includes connection flights and optional disruption details.

5. Disruptions as event log
- Captures disruption type, severity, cause, and affected flights.
- Provides machine-readable details for recovery and compensation logic.

---

## Key Fields Coverage

Required business attributes are explicitly modeled:
- Passenger Name: passengers.first_name, passengers.last_name, passengers.full_name
- Loyalty Tier: passengers.loyalty_tier
- Ticket Class: bookings.ticket_class and flights.ticket_classes_available
- Flight Details: bookings.flight_details and flights core schedule fields
- Connection Flights: flights.connection_flights and bookings.connection_flights
- Disruption Details: disruptions.details and bookings.disruption_details

---

## JSON Schema Example (Excerpt)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SkyRecoverAI Flights Dataset",
  "type": "array",
  "minItems": 100,
  "maxItems": 100,
  "items": {
    "type": "object",
    "required": [
      "flight_id",
      "flight_number",
      "departure_airport",
      "arrival_airport",
      "scheduled_departure_utc",
      "scheduled_arrival_utc",
      "ticket_classes_available",
      "connection_flights"
    ]
  }
}
```

---

## Sample Records (Examples)

### airports.sample.json

```json
{
  "airport_id": "APT-001",
  "iata_code": "JFK",
  "icao_code": "KJFK",
  "name": "John F. Kennedy International Airport",
  "city": "New York",
  "country": "United States",
  "timezone": "America/New_York",
  "latitude": 40.6413,
  "longitude": -73.7781,
  "is_hub": true,
  "terminals": 6,
  "region": "NA"
}
```

### flights.sample.json

```json
{
  "flight_id": "FL-10001",
  "flight_number": "SR110",
  "operating_carrier": "SkyRecover Air",
  "departure_airport": "JFK",
  "arrival_airport": "LHR",
  "scheduled_departure_utc": "2026-06-12T12:30:00Z",
  "scheduled_arrival_utc": "2026-06-12T19:45:00Z",
  "aircraft_type": "B787-9",
  "status": "scheduled",
  "ticket_classes_available": ["Economy", "Premium Economy", "Business"],
  "connection_flights": [
    {
      "next_flight_id": "FL-10077",
      "min_connection_time_minutes": 70
    }
  ]
}
```

### passengers.sample.json

```json
{
  "passenger_id": "PAX-000001",
  "first_name": "Emma",
  "last_name": "Rodriguez",
  "full_name": "Emma Rodriguez",
  "loyalty_tier": "Gold",
  "home_airport": "JFK",
  "preferred_language": "en-US",
  "contact": {
    "email": "emma.rodriguez@example.com",
    "phone": "+12125550101"
  }
}
```

### bookings.sample.json

```json
{
  "booking_id": "BKG-000001",
  "pnr": "AB12CD",
  "passenger_id": "PAX-000001",
  "ticket_class": "Business",
  "booking_status": "Confirmed",
  "flight_details": {
    "primary_flight_id": "FL-10001",
    "departure_airport": "JFK",
    "arrival_airport": "LHR",
    "departure_utc": "2026-06-12T12:30:00Z",
    "arrival_utc": "2026-06-12T19:45:00Z"
  },
  "connection_flights": [
    {
      "flight_id": "FL-10077",
      "connection_airport": "LHR",
      "layover_minutes": 95
    }
  ],
  "disruption_details": {
    "is_disrupted": true,
    "disruption_id": "DIS-000101",
    "impact_type": "MissedConnection"
  }
}
```

### disruptions.sample.json

```json
{
  "disruption_id": "DIS-000101",
  "event_type": "Weather",
  "severity": "High",
  "root_cause": "Weather",
  "flight_id": "FL-10001",
  "affected_flights": ["FL-10001", "FL-10077"],
  "start_utc": "2026-06-12T14:05:00Z",
  "details": {
    "delay_minutes": 115,
    "is_cancellation": false,
    "description": "Thunderstorm cell over transatlantic corridor reduced departure slots.",
    "affected_airports": ["JFK", "LHR"],
    "compensation_hint": "MealAndHotel"
  }
}
```

---

## Data Generation Guidance for Full Counts

To generate the full required datasets:
1. Build exactly 20 airport records across NA, EU, APAC, LATAM, and MEA.
2. Build exactly 100 flights with realistic hub-to-spoke and spoke-to-hub routes.
3. Build exactly 500 passenger records with loyalty tier distribution:
   - None: 58%
   - Silver: 24%
   - Gold: 13%
   - Platinum: 5%
4. Build exactly 500 bookings (1 booking per passenger for MVP baseline).
5. Build 30-80 disruption events with distribution:
   - Delay: 45%
   - Weather: 25%
   - Crew: 20%
   - Cancellation: 10%

Suggested integrity checks:
- Every booking.passenger_id must exist in passengers.json.
- Every flight reference must exist in flights.json.
- Every airport code referenced by flights must exist in airports.json.
- Every disrupted flight in disruptions.json must exist in flights.json.
