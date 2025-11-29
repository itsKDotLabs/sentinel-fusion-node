# Source: GDELT Data Contract

## 1. Purpose
- Use GDELT as the primary **global events** feed.
- Support questions like:
  - "How many events happened in each country per time bucket?"
  - "What’s the average tone (sentiment) of events by region over time?"
  - "What type of events occurs most in given country?"
  - "Any possibility of potential spread to surrounding areas due to nature of events in those said areas?"


## 2. Ingestion Details
- Ingestion mode:  **scheduled batch**
- Frequency: **daily**
- Access method:
  - Download CSV from GDELT v2 events feed via HTTP
- Storage path (raw): `data/raw/gdelt/`
- File naming pattern:
  - `gdelt_events_YYYYMMDD_HHMM.csv`

## 3. Schema (Raw → Canonical)
Decide which raw fields you care about and how you map them to your canonical schema.

Start a table and fill in:

| Raw Field Name   | Canonical Field | Type      | Required? | Description / Notes |
|------------------|-----------------|-----------|-----------|----------------------|
| <raw_timestamp>  | ts_utc          | datetime  | yes       | Event timestamp in UTC. You decide which raw field to use. |
| <raw_id>         | event_id        | string    | yes       | Unique ID (maybe a hash from several fields). |
| <raw_country>    | country_code    | string    | yes       | 2 or 3 letter code, normalized. |
| <raw_lat>        | lat             | float     | maybe     | Latitude of event (if available). |
| <raw_lon>        | lon             | float     | maybe     | Longitude of event. |
| <raw_category>   | category        | string    | yes       | Type of event(conflict, protest, etc.). |
| <raw_tone>       | tone            | float     | yes       | Negative/positive context. |
| <raw_text>       | keywords        | text      | no        | Topic/nature of event. |


## 4. Quality & Validation Rules
List concrete rules, for example:

- `ts_utc` must be parseable; invalid rows are:
  - logged and skipped
- `country_code` must be in your allowed list.
- `tone` must be between -10 and +10 
- Max % of missing `lat/lon` ≤ 30% of rows missing coords

## 5. Volume & Limits
- Expected rows per run:
  - Will revisit after inital run
- Any known size concerns:
  - If a file exceeds N MB, what do you do? Will revisit after initial run

## 6. Failure & Retry Strategy
- How many retries for the HTTP call? ≤ 25
- How long to wait between retries? 30 secounds
- When to give up and log failure?


## 7. Lineage & Metadata
Every row should at least have:
- `source = "gdelt"`
- `ingested_at` (UTC timestamp)
- `run_id` (string; maybe the time bucket label)

(You define the exact formats.)
