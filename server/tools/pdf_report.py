from pathlib import Path
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Image,
)
from reportlab.platypus import Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer
from reportlab.platypus import PageBreak
REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(exist_ok=True)

SECTION_HEADINGS = {
    "Executive Summary",
    "Trend Analysis",
    "Key Highs and Lows",
    "Technical Indicators",
    "Risks and Observations",
    "Final Recommendation",
}
HEADER_NAMES = {
    "returns": "Returns (%)",
    "volatility": "Volatility (%)",
    "correlation": "Correlation",
    "rsi": "RSI",
    "macd": "MACD",
    "sharpe": "Sharpe Ratio",
}

def format_metric(metric_name: str, value):

    if not isinstance(value, (int, float)):
        return "-"

    metric = metric_name.lower()

    if metric == "returns":
        return f"{value:+.2f}%"

    elif metric == "volatility":
        return f"{value:.2f}%"

    elif metric == "correlation":
        return f"{value:.3f}"

    elif metric == "rsi":
        return f"{value:.2f}"

    elif metric == "macd":
        return f"{value:.2f}"

    elif metric == "sharpe":
        return f"{value:.2f}"

    else:
        return f"{value:.2f}"

def generate_pdf(
    title: str,
    report: str,
    charts: list[str],
    metrics: dict[str, dict[str, float]] | None = None,
    filename: str = "financial_report.pdf",
):
    timestamp = datetime.now().strftime("%d %B %Y %H:%M")
    pdf = REPORT_DIR / filename
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Heading1"], fontSize=22, alignment=TA_CENTER, spaceAfter=18))
    styles.add(ParagraphStyle(name="SectionHeading", parent=styles["Heading2"], fontSize=15, spaceBefore=20, spaceAfter=10))
    styles.add(ParagraphStyle(name="ReportBody", parent=styles["BodyText"], fontSize=11, leading=18, spaceAfter=10))
    styles.add(ParagraphStyle(name="ChartTitle", parent=styles["Heading2"], fontSize=14, alignment=TA_CENTER, spaceAfter=12))

    doc = SimpleDocTemplate(str(pdf), leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []

    story.append(Paragraph(title, styles["ReportTitle"]))
    story.append(Paragraph(f"Generated on: {timestamp}", styles["Italic"]))
    story.append(Spacer(1, 24))

    if metrics:
        story.append(Paragraph("Computed Metrics", styles["SectionHeading"]))
        story.append(Spacer(1, 8))
        metric_names = sorted({m for v in metrics.values() for m in v})
        rows = [["Symbol"] + [HEADER_NAMES.get(m, m.title())for m in metric_names]]
        for symbol, values in metrics.items():
            rows.append([symbol] + [
                format_metric(m,values.get(m),)
                for m in metric_names
            ])
        table = Table(rows, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        report = report.strip()

        # Remove duplicate title if the report starts with it
    if report.startswith(title):
        report = report[len(title):].strip()
        
    for line in report.splitlines():
        line = line.strip()
        if not line:
            continue
        if line in SECTION_HEADINGS:
            story.append(Paragraph(line, styles["SectionHeading"]))
        else:
            story.append(Paragraph(line, styles["ReportBody"]))

    story.append(PageBreak())
    story.append(Paragraph("Charts", styles["ReportTitle"]))
    story.append(Spacer(1, 20))

    for chart in charts:
        chart_title = Paragraph(Path(chart).stem.replace("_", " ").title(), styles["ChartTitle"])
        img = Image(chart)
        img.drawWidth = 460
        img.drawHeight = 260
        story.append(KeepTogether([chart_title, img, Spacer(1, 12)]))

    doc.build(story)

    return {"status": "success", "pdf_path": str(pdf), "charts_added": len(charts)}

