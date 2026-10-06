from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "analysis_output"

st.set_page_config(
    page_title="IndiaKart analytics",
    page_icon=":material/analytics:",
    layout="wide",
)


@st.cache_data
def load_data() -> tuple[pd.DataFrame, ...]:
    orders = pd.read_csv(OUTPUT / "orders_clean.csv", parse_dates=["order_date", "delivered_date"])
    monthly = pd.read_csv(OUTPUT / "kpi_monthly.csv")
    category = pd.read_csv(OUTPUT / "kpi_category.csv")
    segment = pd.read_csv(OUTPUT / "kpi_customer_segment.csv")
    payment = pd.read_csv(OUTPUT / "kpi_payment_method.csv")
    state = pd.read_csv(OUTPUT / "kpi_state.csv")
    returns = pd.read_csv(OUTPUT / "kpi_returns.csv")
    inventory = pd.read_csv(OUTPUT / "inventory_health.csv")
    return orders, monthly, category, segment, payment, state, returns, inventory


def format_inr(value: float) -> str:
    if abs(value) >= 1_000_000_000:
        return f"₹{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"₹{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"₹{value / 1_000:.1f}K"
    return f"₹{value:,.0f}"


orders, monthly, category, segment, payment, state, returns, inventory = load_data()

with st.sidebar:
    st.title("IndiaKart")
    st.caption("E-commerce performance workspace")
    min_date = orders["order_date"].min().date()
    max_date = orders["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    statuses = st.multiselect("Order status", sorted(orders["status"].unique()), default=sorted(orders["status"].unique()))
    channels = st.multiselect("Channel", sorted(orders["channel"].unique()), default=sorted(orders["channel"].unique()))
    categories = st.multiselect("Category", sorted(category["category"].unique()), default=sorted(category["category"].unique()))
    st.caption("Source period: 24 Jun 2023 to 23 Jun 2025")

if len(date_range) == 1:
    start_date = end_date = date_range[0]
else:
    start_date, end_date = date_range

filtered = orders[
    orders["order_date"].dt.date.between(start_date, end_date)
    & orders["status"].isin(statuses)
    & orders["channel"].isin(channels)
]

st.title("IndiaKart analytics")
st.caption("A management view of sales, customers, operations, payments, and returns")

revenue = filtered["final_amount"].sum()
order_count = filtered["order_id"].nunique()
delivered_count = filtered["is_completed"].sum()
cancelled_count = filtered["is_cancelled"].sum()
returned_count = filtered["is_returned"].sum()

with st.container(horizontal=True):
    st.metric("Revenue", format_inr(revenue), border=True)
    st.metric("Orders", f"{order_count:,}", border=True)
    st.metric("Average order value", format_inr(revenue / order_count if order_count else 0), border=True)
    st.metric("Delivered", f"{delivered_count:,}", border=True)
    st.metric("Cancellation rate", f"{cancelled_count * 100 / order_count:.2f}%" if order_count else "0.00%", border=True)
    st.metric("Return rate", f"{returned_count * 100 / order_count:.2f}%" if order_count else "0.00%", border=True)

trend = filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str)).groupby("month", as_index=False).agg(
    revenue_inr=("final_amount", "sum"),
    orders=("order_id", "nunique"),
)
trend["month"] = pd.to_datetime(trend["month"])

left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.subheader("Revenue trend")
        st.line_chart(trend.set_index("month")["revenue_inr"], y_label="Revenue (INR)")
with right:
    with st.container(border=True):
        st.subheader("Orders by status")
        status_view = filtered["status"].value_counts().rename_axis("status").reset_index(name="orders")
        st.bar_chart(status_view.set_index("status"), y="orders", horizontal=True)

st.header("Commercial performance")
left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.subheader("Delivered revenue by category")
        category_view = category[category["category"].isin(categories)].sort_values("revenue_inr", ascending=False)
        st.bar_chart(category_view.set_index("category")["revenue_inr"], y_label="Revenue (INR)")
with right:
    with st.container(border=True):
        st.subheader("Customer segment value")
        st.bar_chart(segment.set_index("segment")["segment_revenue_inr"], y_label="Lifetime value (INR)")

st.header("Geography and payments")
left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.subheader("Top states by delivered revenue")
        st.bar_chart(state.head(10).set_index("state")["revenue_inr"], y_label="Revenue (INR)", horizontal=True)
with right:
    with st.container(border=True):
        st.subheader("Payment method reliability")
        payment_view = payment[["payment_method", "transactions", "failure_rate_pct"]].sort_values("transactions", ascending=False)
        st.dataframe(
            payment_view,
            hide_index=True,
            column_config={
                "payment_method": "Payment method",
                "transactions": st.column_config.NumberColumn("Transactions", format="%d"),
                "failure_rate_pct": st.column_config.NumberColumn("Failure rate", format="%.2f%%"),
            },
        )

st.header("Returns and inventory")
left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.subheader("Return reasons")
        st.bar_chart(returns.set_index("reason")["returns"], y_label="Return requests", horizontal=True)
with right:
    with st.container(border=True):
        st.subheader("Reorder watchlist")
        watchlist = inventory[inventory["below_reorder"]].sort_values("total_inventory_value", ascending=False)
        st.dataframe(
            watchlist[["product_name", "category", "warehouse_location", "quantity_available", "reorder_level", "status"]],
            hide_index=True,
            column_config={
                "product_name": "Product",
                "warehouse_location": "Warehouse",
                "quantity_available": "Available",
                "reorder_level": "Reorder level",
                "status": "Status",
            },
        )

with st.expander("Download prepared tables", icon=":material/download:"):
    for file in sorted(OUTPUT.glob("kpi_*.csv")):
        st.download_button(
            file.stem.replace("_", " ").title(),
            data=file.read_bytes(),
            file_name=file.name,
            mime="text/csv",
            key=file.name,
        )

st.caption("Definitions: revenue uses order final amount; delivered category and state views exclude non-delivered orders; return rate counts returned orders divided by all filtered orders.")
