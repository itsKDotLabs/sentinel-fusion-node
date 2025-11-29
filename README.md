# 🛰️ Sentinel Fusion Node

## Project Overview
Sentinel Fusion Node is an open-source intelligence pipeline that ingests global event data and social chatter, normalizes it, enriches it, and prepares it for analytic or SOC-driven detection workflows.

The goal is to simulate an early-stage **mission-ready data fusion node**—the kind used in defense, threat intelligence, and security operations environments.

This project blends **data engineering, security analytics, and OSINT fusion** into one unified system.


## ✅ Current Status (Early Stage)
✔️ GDELT ingestion pipeline implemented

✔️ Tab-delimited parsing + full GDELT schema assignment (61 fields)

✔️ Normalization to SOC-friendly schema (15-column structured output)

✔️ Processed output generated (CSV + Parquet)


## 🚧 In Progress/Next Milestones
🔄 Initial analytics notebook (actor activity, country spikes, tone distributions)

🔄 Geo-enrichment + actor classification

🔄 OSINT-to-SOC linkage (event anomalies, high-impact signals)

🔄 Sysmon/SOC log intake for fusion layer

🔄 Dashboards + reporting (security intelligence overlays)

## 📂 Project Structure
``` text
sentinel-fusion-node/
│
├── data/
│   ├── raw/          # Raw OSINT data sources (GDELT, Reddit, etc.)
│   └── processed/    # Cleaned + normalized datasets (CSV + Parquet)
│
├── scripts/
│   ├── extract/      # Ingestion pipelines (GDELT loader, more coming)
│   ├── transform/    # Normalization + enrichment
│   └── load/         # Storage + interface layers (future)
│
├── docs/             # Data dictionaries + source documentation
└── notebooks/        # Analytics + anomaly detection (coming)
```

## 🎯 Mission
Build a modular, transparent, and extensible intelligence pipeline that demonstrates:

* Python data engineering skills
* Security analysis + threat-enrichment workflow
* Ability to handle irregular real-world datasets
* Awareness of SOC detection context
* Readiness for cleared-sector analytics or DE roles

## 🔎 Current Intelligence Insights (Sample GDELT Window)

The first end-to-end run of Sentinel Fusion Node generated a set of early-warning indicators
based on negative-tone event clustering across global regions.

### Key Countries Flagged (High Negative Volume + High Negative Ratio)

- **Turkey (TU)** — 116/120 events negative (96.7%), AvgTone −4.73  
- **Syria (SY)** — 63/65 negative (96.9%), AvgTone −4.63  
- **Egypt (EG)** — 50/50 negative (100%), AvgTone −5.65  
- **Sudan (SD)** — 50/50 negative (100%), AvgTone −4.77  
- **Serbia (RS)** — 34/34 negative (100%), AvgTone −4.12  
- **Pakistan (PK)** — 29/29 negative (100%), AvgTone −3.05  
- **South Africa (ZA)** — 43/46 negative (~93%), AvgTone −2.93  

These countries exhibit sustained negative sentiment in global reporting during this analysis window,
suggesting patterns consistent with:

- political unrest  
- conflict activity  
- governance instability  
- civil demonstrations  

This represents the first automated **Sentinel Fusion Alert**, demonstrating the platform’s ability
to convert raw OSINT data into structured, SOC-ready intelligence signals.
