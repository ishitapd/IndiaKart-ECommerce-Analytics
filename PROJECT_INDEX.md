# IndiaKart E-Commerce Analytics

## Main cleaned CSV files

The cleaned CSV files are in `Cleaned_Data`:

- `orders_clean.csv`
- `order_items_clean.csv`
- `kpi_monthly.csv`
- `kpi_category.csv`
- `kpi_customer_segment.csv`
- `kpi_payment_method.csv`
- `kpi_state.csv`
- `kpi_channel.csv`
- `kpi_returns.csv`
- `inventory_health.csv`
- `order_reconciliation.csv`
- `data_quality_report.csv`

The same files remain in `analysis_output` for reproducibility.

## How to run

```powershell
python .\indiakart_analysis.py
.\run_dashboard.ps1
```

Dashboard: `http://localhost:8501`

## Power BI

Use the prepared files in `PowerBI_Import` or `Cleaned_Data`.

Read `PowerBI_dashboard_guide.md` for relationships, DAX measures, and dashboard pages.

## Main project files

- `indiakart_analysis.py` - cleaning, validation, and KPI generation
- `app.py` - interactive Streamlit dashboard
- `schema_and_sql final internmo.sql` - database schema and SQL analysis
- `IndiaKart_findings_report.md` - insights and recommendations
- `PROJECT_COMPLETION.md` - completion checklist
- `PowerBI_dashboard_guide.md` - Power BI setup guide
- `run_dashboard.ps1` - dashboard launcher
