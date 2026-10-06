# Power BI dashboard implementation guide

## 1. Load tables

Import the prepared CSV files from `analysis_output`:

- `orders_clean.csv`
- `order_items_clean.csv`
- `kpi_monthly.csv`
- `kpi_category.csv`
- `kpi_customer_segment.csv`
- `kpi_payment_method.csv`
- `kpi_state.csv`
- `kpi_returns.csv`
- `inventory_health.csv`
- `customers DA.csv`
- `products DA.csv`
- `payments DA.csv`
- `returns DA.csv`
- `inventory DA.csv`

Use `order_id`, `customer_id`, and `product_id` as text fields. Use the date columns as dates with day-first parsing when importing the original source CSVs.

## 2. Recommended model

For a clean Power BI model, use `orders_clean` and `order_items_clean` as the core facts:

- `orders_clean[order_id]` 1-to-many `order_items_clean[order_id]`
- Add `customers` as a dimension through `customer_id`.
- Add `products` as a dimension through `product_id`.
- Add a dedicated calendar table related to `orders_clean[order_date]`.
- Keep `payments`, `returns`, and `inventory_health` as supporting fact tables with single-direction relationships.

Avoid creating many-to-many relationships between the prepared KPI summary tables and the core facts. Use the summaries for validation or separate report pages.

## 3. Core DAX measures

```DAX
Total Revenue = SUM(orders_clean[final_amount])

Delivered Revenue =
CALCULATE(
    [Total Revenue],
    orders_clean[status] = "Delivered"
)

Total Orders = DISTINCTCOUNT(orders_clean[order_id])

Delivered Orders =
CALCULATE(
    [Total Orders],
    orders_clean[status] = "Delivered"
)

Cancelled Orders =
CALCULATE(
    [Total Orders],
    orders_clean[status] = "Cancelled"
)

Returned Orders =
CALCULATE(
    [Total Orders],
    orders_clean[status] = "Returned"
)

Average Order Value = DIVIDE([Total Revenue], [Total Orders])

Cancellation Rate = DIVIDE([Cancelled Orders], [Total Orders])

Return Rate = DIVIDE([Returned Orders], [Total Orders])

Units Sold = SUM(order_items_clean[quantity])

Discount Value = SUM(orders_clean[discount_amount])

Shipping Revenue = SUM(orders_clean[shipping_charge])

Below Reorder Products =
CALCULATE(
    DISTINCTCOUNT(inventory_health[product_id]),
    inventory_health[below_reorder] = TRUE()
)

Payment Failure Rate =
DIVIDE(
    CALCULATE(COUNTROWS(payments), payments[status] = "Failed"),
    COUNTROWS(payments)
)
```

## 4. Suggested report pages

### Executive overview

Cards: Delivered Revenue, Total Orders, Average Order Value, Cancellation Rate, Return Rate.

Visuals: monthly revenue line chart, order-status column chart, delivered revenue by category, delivered revenue by state.

### Customer and product performance

Visuals: lifetime revenue by customer segment, top products by delivered revenue, category revenue share, units sold by category.

### Operations and payments

Visuals: cancellation rate by channel, payment failure rate by method, average delivery days, revenue by shipping partner.

### Returns and inventory

Visuals: return count and value by reason, return rate by category, below-reorder product table, inventory value by warehouse.

## 5. Validation targets

The Power BI cards should match these source-level checks:

- Delivered revenue: approximately ₹2.054B.
- Cancellation rate: 11.99% across all orders.
- Return rate: 7.87% across all orders.
- Products below reorder level: 78.
- Missing foreign-key relationships: 0.
- Payment-to-order amount mismatches: 0.
