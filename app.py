from crew.finance_crew import run_financial_crew

query ="""Analyze the correlation between Amazon (AMZN), Google (GOOGL), Meta (META) and Microsoft (MSFT) over the last five years.

Generate
- Correlation heatmap

Discuss diversification opportunities.

Generate the report."""
result = run_financial_crew(query)
print(result)