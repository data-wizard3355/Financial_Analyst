from pydantic import BaseModel, Field,field_validator
from typing import Literal

ActionType = Literal[
    "analysis",
    "technical_analysis",
    "comparison",
    "correlation",
    "volume_analysis",
]

# -------------------------
# Allowed Chart Types
# -------------------------

ChartType = Literal[
    "price",
    "comparison",
    "volume",
    "moving_average",
    "candlestick",
    "rsi",
    "macd",
    "heatmap",
    "returns",
    "volatility",
    "drawdown",
]

# -------------------------
# Allowed Metrics
# -------------------------

MetricType = Literal[
    "summary",
    "technical_indicators",
    "correlation",
    "volatility",
    "returns",
]

# -------------------------
# Chart Request
# -------------------------
class ChartRequest(BaseModel):
    """
    Represents one chart that should be generated.
    """

    chart_type: ChartType = Field(
        description="Type of chart to generate."
    )
    symbols: list[str] = Field(
        description="Stock symbols for this chart."
    )

# -------------------------
# Metric Request
# -------------------------
class MetricRequest(BaseModel):
    """
    Represents one financial computation requested.
    """

    metric: MetricType = Field(
        description="Metric that should be computed."
    )
    symbols: list[str] = Field(
        description="Stocks involved."
    )

# -------------------------
#  Execution Plan 
# -------------------------
class ExecutionPlan(BaseModel):
    """
    Final deterministic execution plan.
    """

    symbols: list[str]
    period: str
    interval: str
    action: ActionType
    charts: list[ChartRequest] = Field(default_factory=list)
    metrics: list[MetricRequest] = Field(default_factory=list)
    comparison: bool = False
    recommendation_requested: bool = False
    recommendation_horizon: str | None = None
    generate_pdf: bool = True



# -------------------------
# Generated Chart
# -------------------------
class GeneratedChart(BaseModel):
    """
    Metadata returned by the visualization agent after creating a chart.
    """
    chart_type: ChartType
    symbols: list[str]
    path: str
    title: str

# -------------------------
# Parsed Query
# -------------------------

class ParsedQuery(BaseModel):
    """
    Structured representation of the user's financial request.

    Produced by the Query Parser Agent and consumed by
    the Research, Visualization and Analyst agents.
    """

    symbols: list[str] = Field(
        description="Stock ticker symbols."
    )

    period: str = Field(
        default="1y",
        description="Historical period."
    )

    interval: str = Field(
        default="1d",
        description="Historical interval."
    )

    action: ActionType = Field(
        description="Primary user intent."
    )

    chart_requests: list[ChartRequest] = Field(
        default_factory=list,
        description="Charts that need to be generated."
    )

    metric_requests: list[MetricRequest] = Field(
        default_factory=list,
        description="Financial metrics to compute."
    )

    comparison: bool = Field(
        default=False,
        description="Whether this is a comparison query."
    )

    pdf_required: bool = Field(
        default=True,
        description="Whether a PDF report should be generated."
    )

    @field_validator("comparison", mode="after")
    @classmethod
    def infer_comparison(cls, value, info):
        symbols = info.data.get("symbols", [])
        return value or len(symbols) >= 2