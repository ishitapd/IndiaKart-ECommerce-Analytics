# 🛒 IndiaKart E-Commerce Analytics

> **End-to-End Data Analytics Project** — Uncovering sales trends, customer behavior, product performance, and operational insights from 2 years of e-commerce data.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![SQL](https://img.shields.io/badge/SQL-Analytics-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

---

## 📌 Project Overview

**IndiaKart** is a simulated Indian e-commerce marketplace. This project performs a complete business analytics cycle on **50,000 orders**, **100,000 line items**, and **10,000 customers** spanning **24 June 2023 to 23 June 2025** across 8 relational data tables.

### 🎯 Business Objectives

- Identify top-performing product categories and revenue drivers
- Understand customer segmentation and lifetime value
- Analyse operational bottlenecks (cancellations, returns, inventory)
- Build interactive dashboards for business decision-making
- Deliver actionable recommendations backed by data

---

## 📊 Key Business Results

| Metric | Value |
|--------|-------|
| 💰 Delivered Revenue | **₹2.054 Billion** |
| 📦 Total Orders | **50,000** |
| 🛑 Cancellation Rate | **11.99%** |
| 🔁 Return Rate | **7.87%** |
| 🏆 Top Category | **Electronics (57.74% of revenue)** |
| ⚠️ Low Stock Products | **78 Products** |
| ✅ Payment Reconciliation | **0 mismatches** |

---

## 🗂️ Project Structure

```
IndiaKart-ECommerce-Analytics/
│
├── 📁 Cleaned_Data/                    # Processed & validated datasets
│   ├── orders_clean.csv
│   ├── order_items_clean.csv
│   ├── kpi_monthly.csv
│   ├── kpi_category.csv
│   ├── kpi_customer_segment.csv
│   ├── kpi_payment_method.csv
│   ├── kpi_state.csv
│   ├── kpi_channel.csv
│   ├── kpi_returns.csv
│   ├── inventory_health.csv
│   ├── order_reconciliation.csv
│   └── data_quality_report.csv
│
├── 📁 PowerBI_Import/                  # Power BI ready files
│   ├── IndiaKart_orders.pbids          # Auto-connect to Power BI
│   ├── DAX_Measures.txt                # Copy-paste DAX formulas
│   ├── PowerBI_dashboard_guide.md      # Step-by-step Power BI guide
│   └── [KPI CSV files]
│
├── 📄 app.py                           # ⭐ Streamlit interactive dashboard
├── 📄 indiakart_analysis.py            # ⭐ Python data pipeline & KPI engine
├── 📄 schema_and_sql final internmo.sql # ⭐ SQL schema + 12 business queries
│
├── 📄 data_dictionary __ fin.md        # Full schema & ER diagram reference
├── 📄 IndiaKart_findings_report.md     # Business insights & recommendations
├── 📄 PowerBI_dashboard_guide.md       # Power BI model & DAX specification
├── 📄 PROJECT_INDEX.md                 # Navigation guide
├── 📄 PROJECT_COMPLETION.md            # Verification checklist
└── 📄 run_dashboard.ps1                # One-click dashboard launcher
```

---

## 🔄 How This Project Works — End to End

```
Raw CSV Data (8 Tables)
        │
        ▼
┌─────────────────────────┐
│  STEP 1: Data Cleaning  │  ← indiakart_analysis.py
│  • Date parsing         │
│  • FK validation        │
│  • Derived metrics      │
└─────────────┬───────────┘
              │
              ▼
┌─────────────────────────┐
│  STEP 2: KPI Generation │  ← Python / Pandas
│  • Monthly revenue      │
│  • Category analysis    │
│  • Segment analysis     │
│  • Inventory health     │
└─────────────┬───────────┘
              │
              ▼
┌─────────────────────────┐
│  STEP 3: SQL Analysis   │  ← schema_and_sql final internmo.sql
│  • 12 business queries  │
│  • Star-schema design   │
│  • Indexed tables       │
└─────────────┬───────────┘
              │
        ┌─────┴─────┐
        ▼           ▼
┌──────────────┐  ┌──────────────────┐
│  Streamlit   │  │    Power BI      │
│  Web App     │  │    Dashboard     │
│  (app.py)    │  │  (PowerBI_Import)│
└──────────────┘  └──────────────────┘
        │
        ▼
┌─────────────────────────┐
│  STEP 4: Insights &     │  ← IndiaKart_findings_report.md
│  Recommendations        │
└─────────────────────────┘
```

---

## ⚙️ Getting Started

### Prerequisites

```bash
pip install pandas streamlit
```

### Step 1: Run the Data Pipeline

```bash
python indiakart_analysis.py
```

This will:
- Load all 8 raw CSV tables
- Clean & validate dates, foreign keys, and amounts
- Generate 12 KPI output files in `analysis_output/`
- Print a summary of key metrics

### Step 2: Launch the Interactive Dashboard

```bash
python -m streamlit run app.py
```

Then open your browser at: **http://localhost:8501**

Or use the PowerShell launcher:

```powershell
.\run_dashboard.ps1
```

---

## 📁 Data Tables

| Table | Records | Description |
|-------|---------|-------------|
| `orders` | 50,000 | All customer orders with status, amount, and delivery info |
| `order_items` | 100,000 | Line-item breakdown of every order |
| `customers` | 10,000 | Customer profiles with segments and lifetime value |
| `products` | 1,000 | Product catalogue with pricing and GST rates |
| `inventory` | 1,000 | Warehouse stock levels and reorder thresholds |
| `payments` | 50,000 | Payment records with gateway and failure tracking |
| `returns` | 10,000 | Return requests with reasons and refund status |
| `suppliers` | 200 | Supplier profiles, ratings, and payment terms |

---

## 📈 Dashboard Features

### 🌐 Streamlit Web Dashboard (`app.py`)
- **Sidebar Filters**: Date range, order status, channel, product category
- **KPI Cards**: Revenue, Orders, AOV, Delivered count, Cancellation rate, Return rate
- **Revenue Trend**: Monthly line chart (24 months)
- **Orders by Status**: Horizontal bar chart
- **Category Revenue**: Delivered revenue breakdown by category
- **Customer Segments**: Lifetime value by segment
- **State Performance**: Top 10 states by delivered revenue
- **Payment Reliability**: Failure rate by payment method
- **Return Reasons**: Return request breakdown
- **Inventory Watchlist**: 78 products below reorder level

### 📊 Power BI Dashboard (`PowerBI_Import/`)
- 4 report pages: Executive Overview, Customer & Product, Operations & Payments, Returns & Inventory
- Pre-built DAX measures in `DAX_Measures.txt`
- Star-schema model with calendar table support

---

## 🔍 SQL Analysis (`schema_and_sql final internmo.sql`)

12 business SQL queries covering:

1. Monthly Revenue Trend (GMV)
2. Category-wise Sales Performance
3. Customer Segment RFM Analysis
4. Payment Method Distribution & Failure Rates
5. Return Rate by Category
6. Top 10 Products by Revenue
7. State-wise Revenue Map
8. Inventory Health Check by Warehouse
9. Supplier Performance & Rating
10. Customer Cohort Analysis (Registration Month)
11. Channel Performance (App vs Website vs Mobile Web)
12. Festive Season Sales — Diwali Window (Oct–Nov)

---

## 💡 Key Business Findings

### 🏆 Sales & Categories
- **Electronics** dominates at **₹1.076B** (57.74% of delivered revenue)
- **Sports & Fitness** is the #2 category at ~₹319M
- High category concentration = opportunity for cross-sell into Home & Kitchen, Fashion

### 👥 Customers
- **Regular customers** contribute **₹1.457B** lifetime revenue
- **Premium customers** contribute **₹800M** with higher AOV
- **Inactive customers** generate only ₹15.5M — suppress broad discounting

### ⚙️ Operations
- **11.99% cancellation rate** — needs channel-level root-cause breakdown
- **7.87% return rate** — split across transit damage, defects, and sizing issues

### 📦 Inventory
- **78 products** are below reorder level
- Recommended: weekly reorder queue ranked by sales velocity × margin × lead time

---

## 🗺️ ER Diagram

```
SUPPLIERS (1) ────────────── (M) PRODUCTS
                                   │
INVENTORY (1:1) ──────────── PRODUCTS
                                   │
CUSTOMERS (1) ─────────────── (M) ORDERS ──── (M) ORDER_ITEMS (M) ──── (1) PRODUCTS
                │                  │
                │             (1:1)─┤
                │                  │
                └─────────── (M) PAYMENTS
                │
                └─────────── (M) RETURNS ──── (1) ORDERS
```

---

## 📋 Data Quality Validation

| Check | Result |
|-------|--------|
| Orders with unique IDs | ✅ 50,000 / 50,000 |
| Orders without a customer | ✅ 0 |
| Line items without an order | ✅ 0 |
| Payment-to-order amount match | ✅ 0 mismatches |
| Products below reorder level | ⚠️ 78 (flagged for restocking) |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Data processing & automation |
| **Pandas** | Data cleaning, transformation & KPI calculation |
| **Streamlit** | Interactive web dashboard |
| **SQL (MySQL/PostgreSQL)** | Database schema & business queries |
| **Microsoft Power BI** | Enterprise BI dashboard |
| **GitHub** | Version control & project hosting |

---

## 👩‍💻 Author

**Ishita Prasad**
- GitHub: [@ishitapd](https://github.com/ishitapd)
- Email: ishitaprasad1@gmail.com

---

## 📄 License

This project is created for educational and portfolio purposes as part of a Data Analytics internship/course.

---

> *"Data is the new oil — but only when refined into insights."*
