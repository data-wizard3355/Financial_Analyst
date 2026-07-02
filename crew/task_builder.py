from crew.tasks import (
    make_research_task,
    make_visualization_task,
    make_analysis_task,
)


def build_tasks(
    execution_plan,
    researcher,
    visualization_agent,
    analyst,
):
    tasks = []

    research_task = make_research_task(
        researcher,
        execution_plan,
    )

    tasks.append(research_task)

    if execution_plan.charts:

        visualization_task = make_visualization_task(
            visualization_agent,
            execution_plan,
            research_task,
        )

        tasks.append(visualization_task)

    analysis_task = make_analysis_task(
        analyst,
        execution_plan,
        research_task,
        visualization_task if execution_plan.charts else None,
    )

    tasks.append(analysis_task)

    return tasks


