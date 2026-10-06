from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "analysis_output"
DATE_FORMAT = "%d-%m-%Y"


FILES = {
    "customers": "customers DA.csv",
    "inventory": "inventory DA.csv",
    "orders": "orders DA.csv",
    "order_items": "order_items DA.csv",
    "payments": "payments DA.csv",
    "products": "products DA.csv",
    "returns": "returns DA.csv",
    "suppliers": "suppliers DA.csv",
}


def load_tables() -> dict[str, pd.DataFrame]:
    tables = {name: pd.read_csv(ROOT / filename) for name, filename in FILES.items()}
    for table in tables.values():
        for column in table.columns:
            if column.endswith("_date") or column in {"created_date", "launch_date"}:
                table[column] = pd.to_datetime(table[column], format=DATE_FORMAT, errors="coerce")
    return tables


def export(table: pd.DataFrame, name: str) -> None:
    table.to_csv(OUTPUT / f"{name}.csv", index=False)


def build_outputs(tables: dict[str, pd.DataFrame]) -> dict[str, int | float]:
    orders = tables["orders"].copy()
    items = tables["order_items"].copy()
    customers = tables["customers"].copy()
    payments = tables["payments"].copy()
    products = tables["products"].copy()
    returns = tables["returns"].copy()
    inventory = tables["inventory"].copy()

    orders["month"] = orders["order_date"].dt.to_period("M").astype(str)
    orders["delivery_days"] = (orders["delivered_date"] - orders["order_date"]).dt.days
    orders["is_completed"] = orders["status"].eq("Delivered")
    orders["is_cancelled"] = orders["status"].eq("Cancelled")
    orders["is_returned"] = orders["status"].eq("Returned")

    item_totals = items.groupby("order_id", as_index=False)["total_price"].sum()
    item_totals = item_totals.rename(columns={"total_price": "line_item_total"})
    reconciliation = orders.merge(item_totals, on="order_id", how="left")
    reconciliation["line_item_total"] = reconciliation["line_item_total"].fillna(0)
    reconciliation["expected_final_amount"] = (
        reconciliation["line_item_total"] + reconciliation["shipping_charge"]
    ).round(2)
    reconciliation["reconciliation_difference"] = (
        reconciliation["final_amount"] - reconciliation["expected_final_amount"]
    ).round(2)
    reconciliation["reconciles"] = reconciliation["reconciliation_difference"].eq(0)

    monthly = orders.groupby("month", as_index=False).agg(
        orders=("order_id", "nunique"),
        revenue_inr=("final_amount", "sum"),
        delivered_orders=("is_completed", "sum"),
        cancelled_orders=("is_cancelled", "sum"),
        returned_orders=("is_returned", "sum"),
        average_order_value_inr=("final_amount", "mean"),
        discounts_inr=("discount_amount", "sum"),
        shipping_revenue_inr=("shipping_charge", "sum"),
    )
    monthly["cancel_rate_pct"] = monthly["cancelled_orders"] * 100 / monthly["orders"]
    monthly["return_rate_pct"] = monthly["returned_orders"] * 100 / monthly["orders"]

    delivered_order_ids = orders.loc[orders["is_completed"], "order_id"]
    delivered_items = items[items["order_id"].isin(delivered_order_ids)]
    category = delivered_items.groupby("category", as_index=False).agg(
        units_sold=("quantity", "sum"),
        revenue_inr=("total_price", "sum"),
        orders=("order_id", "nunique"),
        discount_inr=("discount_amount", "sum"),
    )
    category["revenue_share_pct"] = category["revenue_inr"] * 100 / category["revenue_inr"].sum()
    category["gross_margin_inr"] = delivered_items.merge(
        products[["product_id", "cost_price"]], on="product_id", how="left"
    ).assign(cost=lambda frame: frame["quantity"] * frame["cost_price"]).groupby("category")["total_price"].sum().sub(
        delivered_items.merge(products[["product_id", "cost_price"]], on="product_id", how="left").assign(
            cost=lambda frame: frame["quantity"] * frame["cost_price"]
        ).groupby("category")["cost"].sum(),
        fill_value=0,
    ).reindex(category["category"]).to_numpy()

    segment = customers.groupby("segment", as_index=False).agg(
        customers=("customer_id", "nunique"),
        average_orders=("total_orders", "mean"),
        average_lifetime_value_inr=("total_spent", "mean"),
        segment_revenue_inr=("total_spent", "sum"),
        average_age=("age", "mean"),
    )

    payment = payments.groupby("payment_method", as_index=False).agg(
        transactions=("payment_id", "nunique"),
        amount_inr=("amount", "sum"),
        failed_transactions=("status", lambda values: values.eq("Failed").sum()),
    )
    payment["failure_rate_pct"] = payment["failed_transactions"] * 100 / payment["transactions"]

    state = orders[orders["is_completed"]].groupby("state", as_index=False).agg(
        customers=("customer_id", "nunique"),
        orders=("order_id", "nunique"),
        revenue_inr=("final_amount", "sum"),
        average_order_value_inr=("final_amount", "mean"),
    )

    channel = orders.groupby("channel", as_index=False).agg(
        orders=("order_id", "nunique"),
        revenue_inr=("final_amount", "sum"),
        average_order_value_inr=("final_amount", "mean"),
        cancelled_orders=("is_cancelled", "sum"),
    )
    channel["cancel_rate_pct"] = channel["cancelled_orders"] * 100 / channel["orders"]

    returns_by_reason = returns.groupby("reason", as_index=False).agg(
        returns=("return_id", "nunique"),
        return_value_inr=("return_amount", "sum"),
        pending_refunds=("refund_status", lambda values: values.eq("Pending").sum()),
        rejected_returns=("refund_status", lambda values: values.eq("Rejected").sum()),
    )

    inventory_health = inventory.merge(
        products[["product_id", "product_name", "category"]], on="product_id", how="left"
    )
    inventory_health["below_reorder"] = (
        inventory_health["quantity_available"] < inventory_health["reorder_level"]
    )
    inventory_health = inventory_health[
        [
            "product_id",
            "product_name",
            "category",
            "warehouse_location",
            "quantity_available",
            "quantity_reserved",
            "reorder_level",
            "reorder_quantity",
            "total_inventory_value",
            "status",
            "below_reorder",
        ]
    ]

    export(orders, "orders_clean")
    export(items, "order_items_clean")
    export(monthly.round(2), "kpi_monthly")
    export(category.round(2).sort_values("revenue_inr", ascending=False), "kpi_category")
    export(segment.round(2).sort_values("segment_revenue_inr", ascending=False), "kpi_customer_segment")
    export(payment.round(2).sort_values("transactions", ascending=False), "kpi_payment_method")
    export(state.round(2).sort_values("revenue_inr", ascending=False), "kpi_state")
    export(channel.round(2).sort_values("revenue_inr", ascending=False), "kpi_channel")
    export(returns_by_reason.round(2).sort_values("return_value_inr", ascending=False), "kpi_returns")
    export(inventory_health, "inventory_health")
    export(reconciliation, "order_reconciliation")

    quality = pd.DataFrame(
        [
            {"check": "orders", "metric": "row_count", "value": len(orders)},
            {"check": "orders", "metric": "unique_order_ids", "value": orders["order_id"].nunique()},
            {"check": "relationships", "metric": "orders_without_customer", "value": int((~orders["customer_id"].isin(customers["customer_id"])).sum())},
            {"check": "relationships", "metric": "items_without_order", "value": int((~items["order_id"].isin(orders["order_id"])).sum())},
            {"check": "reconciliation", "metric": "orders_reconciled_to_items_plus_shipping", "value": int(reconciliation["reconciles"].sum())},
            {"check": "reconciliation", "metric": "orders_not_reconciled", "value": int((~reconciliation["reconciles"]).sum())},
            {"check": "inventory", "metric": "below_reorder_count", "value": int(inventory_health["below_reorder"].sum())},
            {"check": "returns", "metric": "return_count", "value": len(returns)},
        ]
    )
    export(quality, "data_quality_report")

    return {
        "tables_loaded": len(tables),
        "orders": len(orders),
        "delivered_revenue_inr": round(orders.loc[orders["is_completed"], "final_amount"].sum(), 2),
        "cancel_rate_pct": round(orders["is_cancelled"].mean() * 100, 2),
        "return_rate_pct": round(orders["is_returned"].mean() * 100, 2),
        "reconciliation_failures": int((~reconciliation["reconciles"]).sum()),
    }


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    summary = build_outputs(load_tables())
    print(pd.Series(summary).to_string())
    print(f"\nOutputs written to: {OUTPUT}")


if __name__ == "__main__":
    main()
