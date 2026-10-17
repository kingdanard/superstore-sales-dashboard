import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )
    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"], errors="coerce"
    )

    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df = df.dropna(subset=["Order Date", "Sales"])

    return df

df = load_data()

# Dashboard header
st.title("📊 Superstore Sales Dashboard")
st.write(
    "Explore sales performance across products, regions, "
    "customer segments, and time."
)

# Sidebar filters

st.sidebar.header("Dashboard Filters")

regions = sorted(df["Region"].dropna().unique())
categories = sorted(df["Category"].dropna().unique())
segments = sorted(df["Segment"].dropna().unique())
ship_modes = sorted(df["Ship Mode"].dropna().unique())
subcategories = sorted(df["Sub-Category"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)

selected_subcategories = st.sidebar.multiselect(
    "Sub-Category",
    subcategories,
    default=subcategories
)

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    segments,
    default=segments
)

selected_ship_modes = st.sidebar.multiselect(
    "Ship Mode",
    ship_modes,
    default=ship_modes
)

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# Filter data
filtered_df = df[
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
    & df["Sub-Category"].isin(selected_subcategories)
    & df["Segment"].isin(selected_segments)
    & df["Ship Mode"].isin(selected_ship_modes)
].copy()

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_df = filtered_df[
        filtered_df["Order Date"].dt.date.between(start_date, end_date)
    ]

# KPI Cards

total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["Order ID"].nunique()
average_sales = filtered_df["Sales"].mean() if not filtered_df.empty else 0

st.subheader("Key Performance Indicators")

k1, k2, k3 = st.columns(3)
k1.metric("Total Sales", f"${total_sales:,.2f}")
k2.metric("Total Orders", f"{total_orders:,}")
k3.metric("Average Sales per Row", f"${average_sales:,.2f}")

st.caption(f"Showing {len(filtered_df):,} rows after filtering.")

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# Charts
st.divider()

left, right = st.columns(2)

with left:
    category_sales = (
        filtered_df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_category.update_layout(showlegend=False)
    st.plotly_chart(fig_category, use_container_width=True)

with right:
    region_sales = (
        filtered_df.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_region.update_layout(showlegend=False)
    st.plotly_chart(fig_region, use_container_width=True)

left, right = st.columns(2)

with left:
    subcategory_sales = (
        filtered_df.groupby("Sub-Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=True)
    )

    fig_subcategory = px.bar(
        subcategory_sales,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        title="Sales by Sub-Category",
        color="Sales",
        color_continuous_scale="Teal"
    )
    st.plotly_chart(fig_subcategory, use_container_width=True)

with right:
    segment_sales = (
        filtered_df.groupby("Segment", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_segment = px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        title="Sales by Customer Segment",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_segment, use_container_width=True)


# Monthly sales trend
monthly_df = filtered_df.copy()
monthly_df["Month"] = (
    monthly_df["Order Date"].dt.to_period("M").dt.to_timestamp()
)

monthly_sales = (
    monthly_df.groupby("Month", as_index=False)["Sales"]
    .sum()
    .sort_values("Month")
)

fig_monthly = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True
)
fig_monthly.update_traces(line_width=3)
fig_monthly.update_layout(hovermode="x unified")
st.plotly_chart(fig_monthly, use_container_width=True)


# Filtered dataset table
with st.expander("View Filtered Dataset"):
    st.caption(f"{len(filtered_df):,} rows")
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=450
    )

st.caption("Data source: Superstore Sales Forecasting dataset")
