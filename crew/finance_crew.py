import os
from crewai import Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from crew.planner import build_execution_plan
from crew.agents import (
    make_query_parser_agent, make_researcher_agent,
    make_visualization_agent, make_analyst_agent,
)
from crew.task_builder import build_tasks
from crew.tasks import make_query_parsing_task
server_params = StdioServerParameters(
    command="python",
    args=["server/server.py"],
    env={**os.environ},
)


def run_financial_crew(query: str):

    with MCPServerAdapter(server_params, connect_timeout=60) as mcp_tools:

        # ---------- PHASE 1 ----------
        # Parse Query

        query_parser_agent = make_query_parser_agent()

        query_parsing_task = make_query_parsing_task(query_parser_agent)

        parser_crew = Crew(
        agents=[query_parser_agent],
        tasks=[query_parsing_task],
        process=Process.sequential,
        verbose=True,
        )
        parsed_result = parser_crew.kickoff(inputs={"query": query})

        parsed_query = parsed_result.pydantic
        

        # ---------- PHASE 2 ----------
        # Build Plan

        execution_plan = build_execution_plan(parsed_query)

        # ---------- PHASE 3 ----------
        # Execute Plan

        researcher = make_researcher_agent(mcp_tools)
        visualization_agent = make_visualization_agent(mcp_tools)
        analyst = make_analyst_agent(mcp_tools)

        tasks = build_tasks(
        execution_plan,
        researcher,
        visualization_agent,
        analyst,
        )
        execution_crew = Crew(
        agents=[
            researcher,
            visualization_agent,
            analyst,
        ],

        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        )
        return execution_crew.kickoff(
        inputs={
        "execution_plan": execution_plan.model_dump()})