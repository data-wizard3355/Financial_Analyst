Architecture Philosophy

Modern AI applications often rely on Large Language Models (LLMs) to both understand user requests and decide how an application should execute them. While this approach offers flexibility, it can also lead to inconsistent workflows, unnecessary reasoning, higher token consumption, and unpredictable behavior.

This project follows a hybrid architecture that separates language understanding from workflow orchestration.

The LLM is responsible for interpreting natural language and extracting structured information from the user's query. Once the query has been converted into a structured format, deterministic Python code takes over to decide exactly how the system should execute the request.

This separation combines the strengths of AI with traditional software engineering, resulting in a system that is more predictable, easier to debug, and better suited for production environments.

Why Two Crews?

The project is intentionally divided into two independent CrewAI workflows.

Crew 1 — Query Parsing

The first crew exists solely to understand the user's request.

Its responsibilities include:

Identifying stock ticker symbols
Determining the requested time period
Identifying the type of financial analysis
Extracting requested charts
Extracting requested financial metrics

The output of this crew is a structured ParsedQuery object.

No financial tools are executed during this stage.

This crew focuses entirely on language understanding, making it responsible only for interpreting the user's intent.

Deterministic Execution Planner

Between the two crews sits the Execution Planner.

The planner is not an AI agent.

Instead, it is a deterministic Python module that converts the parsed query into an execution plan by applying predefined business rules.

Its responsibilities include:

Selecting default charts when none are requested
Expanding chart requests into individual chart-generation tasks
Determining which execution tasks are required
Preparing instructions for downstream agents
Creating the final execution workflow

Since this stage contains no LLM calls, the workflow is completely reproducible.

Crew 2 — Execution

The second crew performs the actual financial analysis.

Unlike the first crew, its agents do not need to interpret the user's request again.

Instead, every agent receives the already prepared ExecutionPlan and focuses only on its own specialized responsibility.

The execution crew contains three agents:

Research Agent — retrieves financial information and technical indicators.
Visualization Agent — generates financial charts.
Analyst Agent — prepares the final report and generates the PDF.

Each agent performs one well-defined task without making workflow decisions.

Execution Pipeline

The complete workflow consists of three distinct stages.

User Query
      │
      ▼
Query Parser Crew
      │
      ▼
ParsedQuery
      │
      ▼
Execution Planner
      │
      ▼
ExecutionPlan
      │
      ▼
Execution Crew
      │
      ▼
PDF Report

Each stage has a single responsibility.

This design follows the software engineering principle of separation of concerns, where each component focuses on one specific task.

ParsedQuery

ParsedQuery is the structured representation of the user's natural language request.

It is produced by the Query Parser Agent and serves as the interface between natural language understanding and deterministic planning.

A ParsedQuery contains information such as:

Stock symbols
Historical period
Data interval
Requested analysis type
Requested charts
Requested financial metrics
Whether a PDF report should be generated

For example:

ParsedQuery(
    symbols=["AAPL", "MSFT"],
    action="comparison",
    period="5y",
    interval="1d",
    chart_requests=[...],
    metric_requests=[...]
)
ExecutionPlan

The ExecutionPlan is the deterministic representation of how the system should execute the user's request.

Unlike ParsedQuery, which represents what the user asked for, the ExecutionPlan represents what the application should do.

It specifies:

Which stocks should be analyzed
Which metrics should be computed
Which charts should be generated
Which tasks should be executed
Whether a PDF should be produced

Every downstream agent receives the same execution plan, ensuring all agents operate on identical instructions.

Deterministic Planning

The planner converts a ParsedQuery into an ExecutionPlan.

During this process it applies business rules that are intentionally kept outside the LLM.

Examples include:

Adding default charts when none are requested
Expanding comparison charts into multi-stock chart tasks
Creating separate technical charts for individual stocks
Deciding whether visualization tasks are required
Enabling PDF generation

Because this stage is implemented entirely in Python, identical inputs always produce identical execution plans.

Why is ActionType Constrained?

The system limits the primary analysis type to a predefined set of supported actions:

analysis
technical_analysis
comparison
correlation
volume_analysis

This does not restrict the user's ability to ask questions in natural language.

Instead, the LLM is responsible for mapping many different ways of expressing a request into one of these standardized business actions.

For example:

User Query	Detected Action
"Analyze Apple"	analysis
"Compare Apple and Microsoft"	comparison
"Show RSI and MACD"	technical_analysis
"How correlated are Tesla and Nvidia?"	correlation

Constraining the action type simplifies downstream planning and ensures every supported workflow follows a predictable execution path.

Why Not Let the LLM Decide the Entire Workflow?

Many agent-based systems allow the LLM to determine which tools should be called and which steps should be executed at runtime.

While this increases flexibility, it can also introduce:

Hallucinated workflows
Inconsistent execution
Higher token usage
Difficult debugging
Reduced reproducibility

This project instead adopts a hybrid strategy.

The LLM is responsible only for semantic understanding and report generation.

Python is responsible for workflow orchestration and business logic.

This design provides the flexibility of natural language interfaces while maintaining the predictability of traditional software systems.

Model Context Protocol (MCP)

The project uses the Model Context Protocol (MCP) as the communication layer between AI agents and external tools.

Rather than embedding business logic directly inside the agents, MCP exposes financial operations as reusable tools.

Examples include:

Stock analysis
Historical data retrieval
Technical indicator calculation
Chart generation
PDF generation

Agents simply invoke MCP tools whenever external computation or data retrieval is required, making the system modular and easy to extend with additional capabilities.