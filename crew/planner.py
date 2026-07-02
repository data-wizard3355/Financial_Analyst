from crew.models import (
    ParsedQuery,
    ExecutionPlan,
    ChartRequest,
)


DEFAULT_CHARTS = {
    "analysis": ["price"],
    "technical_analysis": ["moving_average"],
    "comparison": ["comparison"],
    "correlation": ["heatmap"],
    "volume_analysis": ["volume"],
}


def build_execution_plan(parsed: ParsedQuery):

    chart_plan = []

    # User explicitly requested charts
    if parsed.chart_requests:

        for chart_request in parsed.chart_requests:

            chart_type = chart_request.chart_type

            if chart_type in ("comparison", "heatmap"):
                chart_plan.append(
                    ChartRequest(
                        chart_type=chart_type,
                        symbols=parsed.symbols,
                    )
                )

            else:
                # honor the symbols already attached to this chart request
                # instead of assuming every symbol needs this chart
                symbols = chart_request.symbols or parsed.symbols

                for symbol in symbols:
                    chart_plan.append(
                        ChartRequest(
                            chart_type=chart_type,
                            symbols=[symbol],
                        )
                    )

    else:

        defaults = DEFAULT_CHARTS.get(parsed.action, [])

        for chart in defaults:

            if chart in ("comparison", "heatmap"):
                chart_plan.append(
                    ChartRequest(
                        chart_type=chart,
                        symbols=parsed.symbols,
                    )
                )

            else:
                for symbol in parsed.symbols:
                    chart_plan.append(
                        ChartRequest(
                            chart_type=chart,
                            symbols=[symbol],
                        )
                    )

    return ExecutionPlan(
        symbols=parsed.symbols,
        period=parsed.period,
        interval=parsed.interval,
        action=parsed.action,
        charts=chart_plan,
        generate_pdf=parsed.pdf_required,
    )