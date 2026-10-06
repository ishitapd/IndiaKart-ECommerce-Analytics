# IndiaKart project completion checklist

Project: `PROJ-INDI-260626`

## Deliverables

| Requirement | Delivered artifact | Status |
|---|---|---|
| Data cleaning | `indiakart_analysis.py` with day-first date parsing and derived fields | Complete |
| Exploratory data analysis | KPI exports in `analysis_output` and dashboard views | Complete |
| KPI calculations | Monthly, category, segment, payment, state, channel, returns, and inventory tables | Complete |
| SQL analysis | `schema_and_sql final internmo.sql` with corrected native DATE expressions | Complete |
| Interactive dashboard | `app.py`, available at `http://localhost:8501` | Complete |
| Power BI dashboard design | `PowerBI_dashboard_guide.md` with model, pages, and DAX measures | Ready to build |
| Validation | `data_quality_report.csv` and executable rerun checks | Complete |
| Insights and recommendations | `IndiaKart_findings_report.md` | Complete |
| Reproducible launch | `run_dashboard.ps1` | Complete |

## Verified results

- 8 tables loaded successfully.
- 50,000 orders and 100,000 line items processed.
- All tested foreign-key relationships resolve.
- Delivered revenue: approximately ₹2.054B.
- Cancellation rate: 11.99%.
- Return rate: 7.87%.
- Below-reorder products: 78.
- Payment-to-order amount mismatches: 0.

## Run commands

```powershell
python .\indiakart_analysis.py
.\run_dashboard.ps1
```

Open the dashboard at `http://localhost:8501`.

The workspace contains all analysis outputs and the Power BI model/DAX specification. Creating the proprietary `.pbix` binary requires Power BI Desktop, so the final visual assembly must be performed there using the supplied guide and CSVs.
