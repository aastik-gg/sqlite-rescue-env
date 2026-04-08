---
title: SQLite Rescue Environment
emoji: 🗄️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# SQLite Rescue Environment

## Description
A data engineering environment where an AI agent must clean, normalize, and manipulate a messy SQLite database using raw SQL queries. This simulates the real-world task of data cleaning and database refactoring.

## Action & Observation Spaces
* **Action Space:** The agent submits an SQL `query` (string) to execute, and a `submit` (boolean) flag when they are ready for their final database state to be graded.
* **Observation Space:** The environment returns the current `schema_info` (string), `rows_affected` (int), any SQL execution `error` (string), and a `query_result` (list of dicts) if the action was a SELECT query.

## Tasks
1. **easy_data_cleaning:** Clean inconsistent dates and trailing whitespaces in a single table.
2. **medium_schema_normalization:** Split a denormalized monolithic table into two related tables with a foreign key.
3. **hard_complex_reconciliation:** Write a complex query/view to generate a financial reconciliation report.

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt` (or via pyproject.toml)
2. Generate the starting databases: `python generate_templates.py`
3. Run the baseline: `python inference.py`