# IndiaKart e-commerce analytics report

## Scope

The analysis covers 24 June 2023 to 23 June 2025 across 8 related tables: orders, order items, customers, products, inventory, payments, returns, and suppliers.

## Executive summary

- Delivered revenue is approximately **₹2.054 billion**.
- The overall cancellation rate is **11.99%**.
- The overall returned-order rate is **7.87%**.
- **Electronics** is the primary revenue engine at **57.74%** of delivered line-item revenue.
- **Uttar Pradesh** and **Maharashtra** are the two largest delivered-revenue states.
- **Regular** customers contribute the largest lifetime revenue pool, followed by **Premium** customers.
- **78 products** are below their configured reorder levels.
- Payment records reconcile exactly to order final amounts; all foreign-key checks passed.

## Business findings

### Sales and category mix

Electronics contributes approximately ₹1.076 billion, followed by Sports & Fitness at approximately ₹319 million. This concentration creates a strong growth opportunity but also exposes IndiaKart to category concentration risk.

Recommended action: protect availability and supplier coverage for high-value Electronics products while testing cross-sell bundles in Sports & Fitness, Home & Kitchen, and Fashion.

### Customers

Regular customers contribute approximately ₹1.457 billion in lifetime revenue, while Premium customers contribute approximately ₹800 million. Inactive customers contribute only approximately ₹15.5 million.

Recommended action: use Premium customers for retention and early-access campaigns, and use Regular customers for replenishment, loyalty, and cross-category offers. Suppress broad discounting for inactive customers until reactivation tests show positive incremental value.

### Operations

The 11.99% cancellation rate is material. The dashboard should be used to break cancellations down by channel, payment method, state, and fulfillment partner before changing policy.

Recommended action: prioritize root-cause analysis for high-volume channels and payment methods, then track cancellation rate as a weekly operating KPI.

### Returns

Return requests are distributed across Damaged in Transit, Defective Product, Size Issue, and Changed Mind. No single reason dominates enough to justify one universal intervention.

Recommended action: separate logistics damage from product-quality and sizing issues. Use packaging and carrier audits for transit damage, product QA for defects, and improved size guidance for Fashion.

### Inventory

78 products are below reorder level. Inventory value and reorder quantity should be considered together so that low-stock alerts prioritize both revenue-critical items and products with high customer demand.

Recommended action: create a weekly reorder queue ranked by recent delivered units, margin, current available quantity, and supplier lead time.

## Data quality and metric definitions

- All table primary keys are unique.
- All tested foreign-key relationships resolve successfully.
- Source dates are parsed with the `DD-MM-YYYY` format.
- Order final amount reconciles to payment amount for every order.
- Line-item totals equal order `total_amount` for the core order calculation; shipping is handled separately at the order level.
- A stricter `line items + shipping` reconciliation flags 10,071 orders for review, so the dashboard does not silently treat that difference as product revenue.

## Dashboard

Run the interactive dashboard with:

```powershell
streamlit run app.py
```

The dashboard uses the prepared tables in `analysis_output` and supports date, status, channel, and category filters.
