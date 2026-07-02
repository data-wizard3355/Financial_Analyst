from crewai import Task
from crew.models import ParsedQuery


def make_query_parsing_task(agent):
    return Task(
        description=(
            'Analyze the following user query:\n\n'
            '"{query}"\n\n'
            "Extract:\n"
            "- Stock symbols\n"
            "- Period\n"
            "- Interval\n"
            "- User intent/action\n"
            "- Charts requested by the user\n\n"
            "Return only the structured ParsedQuery object."
        ),
        expected_output=(
            "ParsedQuery containing:\n"
            "- symbols\n"
            "- period\n"
            "- interval\n"
            "- action\n"
            "- charts"
        ),
        agent=agent,
        output_pydantic=ParsedQuery,
    )


def make_research_task(researcher,execution_plan):
    return Task(
        description=(
    f"""
    Use the following execution plan:

    Symbols: {execution_plan.symbols}
    Period: {execution_plan.period}
    Interval: {execution_plan.interval}
    Action: {execution_plan.action}

    Retrieve all required financial information.

    Prefer:
    - analyze_stock()
    - summarize_stock()
    - calculate_indicators()
    - analyze_correlation()

    Only use get_stock_data() if raw historical data is required.
    Do not generate charts.
    Do not write reports.
    Only retrieve the required financial information.
    """
    ),
    agent=researcher,
    expected_output=(
            "Structured financial analysis for all requested stocks."),
    )


def make_visualization_task(
    visualization_agent,
    execution_plan,
    research_task,
):
    return Task(
        description=f"""
Generate the following charts:

Charts:
{execution_plan.charts}

Symbols:
{execution_plan.symbols}

Period:
{execution_plan.period}

Interval:
{execution_plan.interval}

The planner has already decided which charts must be generated.

For each chart:

- Call generate_chart()
- Use the chart type exactly as provided.
- Use the supplied symbols.
- Use the supplied period.
- Use the supplied interval.

Do not generate additional charts.
Do not skip requested charts.
Do not perform financial analysis.

Return only the generated chart paths.
""",
        agent=visualization_agent,
        context=[research_task],
        expected_output=(
            "List of generated chart paths."
        ),
    )

def make_analysis_task(
    analyst,
    execution_plan,
    research_task,
    visualization_task=None,
):
    return Task(
        description=f"""
Write a professional financial report.

Execution Plan
--------------
Symbols: {execution_plan.symbols}
Period: {execution_plan.period}
Interval: {execution_plan.interval}
Action: {execution_plan.action}
Charts: {execution_plan.charts}

Use:
- Research results
- Generated charts

IMPORTANT:
- Do NOT use Markdown syntax.
- Do NOT use ##, ###, **, *, -, or tables.
- Write clean plain text only.

Structure the report exactly as follows:

Title

Executive Summary
<paragraph>

Trend Analysis
<paragraph>

Key Highs and Lows
<paragraph>

Technical Indicators
<paragraph>

Risks and Observations
<paragraph>

Final Recommendation
<paragraph>

Finally call generate_pdf_report() using:
- title
- report
- charts

Return ONLY the generated PDF path.
""",
        agent=analyst,
        context=[t for t in [research_task, visualization_task] if t is not None],
        expected_output="A generated PDF report containing the financial analysis and charts.",
    )