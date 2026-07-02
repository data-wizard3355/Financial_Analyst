from crewai import Agent
from crewai.mcp import MCPServerStdio
from crew.models import ParsedQuery
from crew.llm import llm

financial_server = MCPServerStdio(
    command="python",
    args=["server/server.py"],
)

def make_query_parser_agent():
    return Agent(
        role="Query Parsing Specialist",
        goal=(
            "Convert user financial queries into a structured format containing "
            "stock symbols, timeframe, interval, action, and required charts."
        ),
        backstory=(
            "You specialize in understanding financial questions. "
            "You never analyze stocks or call tools. "
            "You only extract structured information."
        ),
        llm=llm,
        verbose=True,
        memory=False,
        allow_delegation=False,
        )


def make_researcher_agent(mcp_tools):
    return Agent(
        role="Senior Financial Researcher",
        goal=(
            "Retrieve accurate financial information using the available MCP tools. "
            "Always use the appropriate analysis tool instead of reasoning from memory."
        ),
        backstory="""
You are a professional financial researcher.

You retrieve stock information by using MCP tools.

Use the provided execution_plan.

Retrieve only the information necessary for the requested analysis.

Never generate charts.

Never write Python code.

Only use get_stock_data() when raw historical data is explicitly required.

Never generate charts.
Never write Python code.
""",
        llm=llm,
        tools=mcp_tools,
        verbose=True,
        max_iter=5,
        max_execution_time=120,
    )


def make_visualization_agent(mcp_tools):
    return Agent(
        role="Financial Visualization Specialist",
       goal=("Generate the charts specified in the ExecutionPlan."),
        backstory="""
You are a Financial Visualization Specialist.

Call generate_chart() once per requested chart.

Your responsibility is to execute the plan.

For every chart in ExecutionPlan.charts:

- call generate_chart()
- use the provided symbols
- use the provided period
- use the provided interval

Never decide which charts should be created.

Never invent new charts.

Never perform financial analysis.

Never write Python code.

Return only the generated chart paths.
""",
        llm=llm,
        tools=mcp_tools,
        verbose=True,
        max_iter=5,
        max_execution_time=120,
)



def make_analyst_agent(mcp_tools):
    return Agent(
        role="Senior Financial Analyst",
        goal=(
            "Interpret financial data, prepare a professional report, "
            "and generate the final PDF report."
        ),
        backstory="""
You are an experienced equity research analyst.

Your responsibilities are:

- Interpret stock analysis
- Explain technical indicators
- Compare companies when needed
- Write a concise professional report
- Generate the final PDF report using the MCP tool

Do not perform calculations yourself.
Always rely on outputs produced by the research tools.
""",
        llm=llm,
        tools=mcp_tools,
        verbose=True,
        max_iter=5,
        max_execution_time=120,
    )
