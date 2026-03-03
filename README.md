# GoldBod – End-to-End Gold Price Analytics Pipeline

GoldBod is an end-to-end data analytics platform that ingests gold price data, applies policy pricing logic, stores results in SQL Server, and exposes analytics through Streamlit and Power BI.

---

## Architecture Overview

Pipeline flow:

Yahoo Finance → Python Ingestion → SQL Server → Streamlit Dashboard → Power BI

Project structure:

GoldBod/
│
├─ ingestion/
│   └─ goldbod3.py
│
├─ database/
│   └─ create_tables.sql
│
├─ streamlit/
│   └─ goldbod3_dashboard1.py
│
├─ powerbi/
│   └─ gold_prices_usd.pbix
│
├─ config/
│   └─ .env.example
│
├─ scripts/
│   └─ updategoldbod3.bat
│
├─ requirements.txt
└─ README.md

---

## Features

- Incremental gold price ingestion
- Data validation and anomaly detection
- Policy-based GoldBod pricing layer
- SQL Server storage
- Streamlit operational dashboard
- Power BI semantic reporting model
- Reproducible pipeline execution

---

## Dependencies

Install required packages:

```bash
pip install -r requirements.txt