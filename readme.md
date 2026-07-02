# 📈 Financial Analyst AI

> A deterministic multi-agent financial analysis platform built with CrewAI, MCP (Model Context Protocol), Gemini, and Python.

---

## Overview

Financial Analyst AI is an intelligent financial research assistant capable of transforming natural language investment queries into professional financial reports.

Instead of relying on a single Large Language Model (LLM) to perform every task, the system separates responsibilities into specialized AI agents coordinated through a deterministic execution planner.

This hybrid architecture combines the flexibility of LLMs with the reliability and predictability of traditional software engineering.

---

## Key Features

✅ Natural language financial queries

✅ Multi-stock comparison

✅ Technical analysis

✅ Correlation analysis

✅ Automatic chart generation

✅ Professional PDF reports

✅ Deterministic workflow planning

✅ CrewAI multi-agent architecture

✅ Model Context Protocol (MCP)

---

# Architecture Philosophy

Modern AI applications often allow a Large Language Model to both understand a request **and decide how the application should execute it.**

Although this provides flexibility, it also introduces several production challenges:

- inconsistent workflows
- hallucinated tool usage
- higher token consumption
- unpredictable execution
- difficult debugging

This project follows a different philosophy.

The LLM is responsible only for understanding natural language.

Once the user's request has been converted into structured data, deterministic Python code takes over and decides exactly how the application should execute the request.

This hybrid architecture combines the strengths of AI with deterministic software engineering.

---

# Overall Architecture

```text
                            User Query
                                 │
                                 ▼
                   ┌────────────────────────┐
                   │ Query Parser Crew      │
                   │ (LLM)                  │
                   └────────────────────────┘
                                 │
                                 ▼
                        ParsedQuery (Pydantic)
                                 │
                                 ▼
                 ┌─────────────────────────────┐
                 │ Deterministic Planner       │
                 │ (Pure Python Business Rules)│
                 └─────────────────────────────┘
                                 │
                                 ▼
                      ExecutionPlan (Pydantic)
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
  Research Agent       Visualization Agent      Analyst Agent
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 ▼
                    Professional PDF Report
```

---

# Why Two Crews?

The application intentionally separates **language understanding** from **workflow execution**.

## Crew 1 — Query Parser

The first CrewAI workflow contains a single agent.

Its only responsibility is understanding the user's natural language request.

It extracts:

- stock symbols
- period
- interval
- analysis type
- requested charts
- requested metrics
- PDF requirement

It produces:

```python
ParsedQuery(...)
```

No financial tools are executed during this stage.

This crew exists purely to transform natural language into structured data.

---

## ParsedQuery

ParsedQuery represents **what the user asked for.**

It acts as the interface between the LLM and deterministic software.

Example

```python
ParsedQuery(
    symbols=["AAPL","MSFT"],
    action="comparison",
    period="5y",
    interval="1d",
    chart_requests=[...],
    metric_requests=[...]
)
```

---

# Deterministic Execution Planner

Between the two crews sits the Execution Planner.

Unlike the agents, the planner is **not an LLM.**

It is ordinary Python code.

Its job is to convert the ParsedQuery into an ExecutionPlan.

This stage applies business rules such as:

- selecting default charts
- expanding chart requests
- determining visualization requirements
- enabling PDF generation

Given the same ParsedQuery, the planner will always produce the same ExecutionPlan.

This guarantees reproducible execution.

---

## ExecutionPlan

ParsedQuery describes:

> What the user wants.

ExecutionPlan describes:

> What the application will execute.

For example:

```python
ExecutionPlan(
    symbols=["AAPL","MSFT"],
    charts=[
        ChartPlan(...),
        ChartPlan(...)
    ],
    generate_pdf=True
)
```

Every downstream agent receives the exact same execution plan.

No downstream agent needs to reinterpret the user's request.

---

# Crew 2 — Execution

The second Crew performs the actual financial analysis.

Unlike Crew 1, it never interprets natural language.

Instead, every agent receives the ExecutionPlan and performs one specialized responsibility.

---

## Research Agent

Responsibilities

- Retrieve stock information
- Compute financial metrics
- Calculate technical indicators
- Retrieve historical data
- Correlation analysis

Tools

- analyze_stock()
- summarize_stock()
- calculate_indicators()
- analyze_correlation()
- get_stock_data()

The Research Agent never generates charts.

---

## Visualization Agent

Responsibilities

- Generate charts
- Execute visualization requests
- Reuse downloaded data

Supported Charts

- Price
- Volume
- Moving Average
- Candlestick
- Comparison
- Heatmap
- Returns
- RSI
- MACD
- Volatility
- Drawdown

The Visualization Agent never performs financial analysis.

---

## Analyst Agent

Responsibilities

- Interpret research results
- Combine charts
- Write professional report
- Generate PDF

Tool

generate_pdf_report()

---

# Why ActionType is Constrained

The system intentionally limits the primary analysis workflow to a predefined set of supported actions.

```python
analysis
technical_analysis
comparison
correlation
volume_analysis
```

This **does not restrict natural language.**

Instead, the LLM maps many different user queries into one standardized business action.

Examples

| User Query | Action |
|------------|--------|
| Analyze Apple | analysis |
| Compare Apple and Microsoft | comparison |
| Show RSI and MACD | technical_analysis |
| Correlation between Tesla and Nvidia | correlation |

Constraining ActionType allows the deterministic planner to build predictable workflows.

---

# Why Not Let the LLM Decide Everything?

Many modern agent systems allow the LLM to decide:

- which tools to call
- which workflow to execute
- which charts to create

While flexible, this introduces:

- hallucinated workflows
- inconsistent execution
- increased token usage
- difficult debugging

This project intentionally separates:

LLM → Semantic Understanding

Python → Workflow Orchestration

This hybrid design produces deterministic execution while preserving natural language flexibility.

---

# Model Context Protocol (MCP)

The project uses Model Context Protocol (MCP) as the communication layer between AI agents and external tools.

```text
Agent
   │
   ▼
MCP Tool
   │
   ▼
Financial Function
   │
   ▼
Yahoo Finance / Python
   │
   ▼
Structured Result
```

Implemented MCP tools include:

Research

- analyze_stock()
- summarize_stock()
- calculate_indicators()
- analyze_correlation()
- get_stock_data()

Visualization

- generate_chart()

Reporting

- generate_pdf_report()

---

# Project Structure

```text
financial-analyst-ai/
│
├── crew/
│   ├── agents.py
│   ├── tasks.py
│   ├── planner.py
│   ├── task_builder.py
│   ├── financial_crew.py
│   ├── models.py
│   └── llm.py
│
├── server/
│   ├── server.py
│   ├── research.py
│   ├── visualization.py
│   ├── pdf.py
│
├── charts/
├── reports/
├── stock_data/
│
├── requirements.txt
└── README.md
```

---

# Technologies

- Python
- CrewAI
- Google Gemini
- MCP (Model Context Protocol)
- Pydantic v2
- pandas
- yfinance
- matplotlib
- ReportLab

---

# Example Query

```text
Compare Apple, Microsoft and Nvidia over the last five years.

Generate:

• Price comparison
• Moving averages
• Volatility
• Returns

Analyze:

• Technical indicators
• Historical performance
• Risks

Recommend the best long-term investment.

Generate the final PDF report.
```

---

# Outputs

```
reports/
    financial_report.pdf

charts/
    comparison.png
    volatility.png
    moving_average.png
    returns.png
```

---

# Future Improvements

- Portfolio optimization
- Risk-adjusted recommendations
- News sentiment analysis
- Fundamental analysis
- Real-time streaming market data
- Agent memory
- Interactive dashboard
- Web deployment
- Multi-model support (Gemini, OpenAI, Groq, SambaNova)
