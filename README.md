---
title: SQLite Rescue Environment
emoji: 🗄️
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# 🗄️ SQLite Rescue Environment

## 📖 What is this project?
This is an **Agentic Evaluation Environment** designed to test how well Large Language Models (LLMs) can perform real-world data engineering tasks. 

Instead of just answering trivia, an AI agent is dropped into a messy SQLite database. Its job is to explore the schema, write raw SQL queries to clean and normalize the data, and submit its final work. The environment acts as a secure sandbox, executing the queries, providing feedback (or errors) back to the agent, and automatically grading the AI's final database state.

## ⚙️ How It Works
1. **The Sandbox Manager:** When the `/reset` API endpoint is called, the environment creates a fresh, isolated temporary database from a messy template.
2. **The Observation Loop:** The AI agent sends raw SQL queries as actions. The environment executes them safely and returns the results, row counts, or syntax errors, allowing the agent to "see" the database state.
3. **The Automated Judge:** When the agent sets the `submit` flag to `True`, custom Python grader scripts analyze the final database state and assign a reward score (0.0 to 1.0) based on how accurately the data was fixed.

## 🕹️ Action & Observation Spaces
* **Action Space:** The agent submits an SQL `query` (string) to execute, and a `submit` (boolean) flag when they are ready for their final database state to be graded.
* **Observation Space:** The environment returns the current `schema_info` (string), `rows_affected` (int), any SQL execution `error` (string), and a `query_result` (list of dicts) if the action was a `SELECT` query.

## 📋 Evaluation Tasks
1. **easy_data_cleaning:** Clean inconsistent dates and trailing whitespaces in a single table.
2. **medium_schema_normalization:** Split a denormalized monolithic table into two related tables with a foreign key.
3. **hard_complex_reconciliation:** Write a complex query/view to generate a financial reconciliation report.

## 🚀 Setup & Execution
This project uses modern Python packaging via `pyproject.toml`, eliminating the need for a legacy `requirements.txt`.

**1. Install dependencies:**
```bash
pip install .
# Or, if you are using uv: uv pip install .