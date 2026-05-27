import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Region Analysis",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("sales.xls")
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🌍 Region Analysis Dashboard")

st.markdown("""
This dashboard analyzes:

- Region Wise Sales
- Region Wise Profit
- Region Wise Quantity
- Region Wise Orders
- Monthly Region Trends
- Category and Segment Analysis by Region
""")

# ---------------------------------------------------
# DATE PROCESSING
# ---------------------------------------------------
if "Order Date" in df.columns:

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Year"] = df["Order Date"].dt.year

    df["Month"] = df["Order Date"].dt.strftime("%B")

    df["Month Number"] = df["Order Date"].dt.month

    df["Year Month"] = df["Order Date"].dt.to_period("M").astype(str)

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("Filters")

filtered_df = df.copy()

# YEAR FILTER
if "Year" in df.columns:

    year_options = sorted(df["Year"].dropna().unique())

    selected_year = st.sidebar.multiselect(
        "Select Year",
        options=year_options,
        default=year_options
    )

    filtered_df = filtered_df[
        filtered_df["Year"].isin(selected_year)
    ]

# REGION FILTER
if "Region" in df.columns:

    region_options = sorted(df["Region"].dropna().unique())

    selected_region = st.sidebar.multiselect(
        "Select Region",
        options=region_options,
        default=region_options
    )

    filtered_df = filtered_df[
        filtered_df["Region"].isin(selected_region)
    ]

# CATEGORY FILTER
if "Category" in df.columns:

    category_options = sorted(df["Category"].dropna().unique())

    selected_category = st.sidebar.multiselect(
        "Select Category",
        options=category_options,
        default=category_options
    )

    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_category)
    ]

# SEGMENT FILTER
if "Segment" in df.columns:

    segment_options = sorted(df["Segment"].dropna().unique())

    selected_segment = st.sidebar.multiselect(
        "Select Segment",
        options=segment_options,
        default=segment_options
    )

    filtered_df = filtered_df[
        filtered_df["Segment"].isin(selected_segment)
    ]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.subheader("Region Metrics")

k1, k2, k3, k4 = st.columns(4)

# TOTAL SALES
if "Sales" in filtered_df.columns:

    total_sales = filtered_df["Sales"].sum()

    k1.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )

# TOTAL PROFIT
if "Profit" in filtered_df.columns:

    total_profit = filtered_df["Profit"].sum()

    k2.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

# TOTAL QUANTITY
if "Quantity" in filtered_df.columns:

    total_quantity = filtered_df["Quantity"].sum()

    k3.metric(
        "Total Quantity",
        int(total_quantity)
    )

# TOTAL ORDERS
if "Order ID" in filtered_df.columns:

    total_orders = filtered_df["Order ID"].nunique()

    k4.metric(
        "Total Orders",
        total_orders
    )

# ---------------------------------------------------
# REGION WISE SALES
# ---------------------------------------------------
st.subheader("Region Wise Sales")

if (
    "Region" in filtered_df.columns
    and "Sales" in filtered_df.columns
):

    region_sales = (
        filtered_df
        .groupby("Region", as_index=False)["Sales"]
        .sum()
    )

    fig1 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        text_auto=True,
        title="Region Wise Sales"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ---------------------------------------------------
# REGION WISE PROFIT
# ---------------------------------------------------
st.subheader("Region Wise Profit")

if (
    "Region" in filtered_df.columns
    and "Profit" in filtered_df.columns
):

    region_profit = (
        filtered_df
        .groupby("Region", as_index=False)["Profit"]
        .sum()
    )

    fig2 = px.pie(
        region_profit,
        names="Region",
        values="Profit",
        title="Region Wise Profit Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ---------------------------------------------------
# REGION WISE QUANTITY
# ---------------------------------------------------
st.subheader("Region Wise Quantity")

if (
    "Region" in filtered_df.columns
    and "Quantity" in filtered_df.columns
):

    region_quantity = (
        filtered_df
        .groupby("Region", as_index=False)["Quantity"]
        .sum()
    )

    fig3 = px.bar(
        region_quantity,
        x="Region",
        y="Quantity",
        color="Region",
        text_auto=True,
        title="Region Wise Quantity"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ---------------------------------------------------
# REGION WISE ORDERS
# ---------------------------------------------------
st.subheader("Region Wise Orders")

if (
    "Region" in filtered_df.columns
    and "Order ID" in filtered_df.columns
):

    region_orders = (
        filtered_df
        .groupby("Region", as_index=False)["Order ID"]
        .nunique()
    )

    region_orders = region_orders.rename(
        columns={"Order ID": "Total Orders"}
    )

    fig4 = px.bar(
        region_orders,
        x="Region",
        y="Total Orders",
        color="Region",
        text_auto=True,
        title="Region Wise Orders"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ---------------------------------------------------
# MONTHLY REGION SALES TREND
# ---------------------------------------------------
st.subheader("Monthly Region Sales Trend")

if (
    "Year Month" in filtered_df.columns
    and "Region" in filtered_df.columns
    and "Sales" in filtered_df.columns
):

    monthly_region_sales = (
        filtered_df
        .groupby(
            ["Year Month", "Region"],
            as_index=False
        )["Sales"]
        .sum()
    )

    fig5 = px.line(
        monthly_region_sales,
        x="Year Month",
        y="Sales",
        color="Region",
        markers=True,
        title="Monthly Region Sales Trend"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# ---------------------------------------------------
# MONTHLY REGION PROFIT TREND
# ---------------------------------------------------
st.subheader("Monthly Region Profit Trend")

if (
    "Year Month" in filtered_df.columns
    and "Region" in filtered_df.columns
    and "Profit" in filtered_df.columns
):

    monthly_region_profit = (
        filtered_df
        .groupby(
            ["Year Month", "Region"],
            as_index=False
        )["Profit"]
        .sum()
    )

    fig6 = px.line(
        monthly_region_profit,
        x="Year Month",
        y="Profit",
        color="Region",
        markers=True,
        title="Monthly Region Profit Trend"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

# ---------------------------------------------------
# CATEGORY ANALYSIS BY REGION
# ---------------------------------------------------
st.subheader("Category Analysis by Region")

if (
    "Region" in filtered_df.columns
    and "Category" in filtered_df.columns
    and "Sales" in filtered_df.columns
):

    category_region = (
        filtered_df
        .groupby(
            ["Region", "Category"],
            as_index=False
        )["Sales"]
        .sum()
    )

    fig7 = px.bar(
        category_region,
        x="Region",
        y="Sales",
        color="Category",
        barmode="group",
        title="Category Wise Sales by Region"
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

# ---------------------------------------------------
# SEGMENT ANALYSIS BY REGION
# ---------------------------------------------------
st.subheader("Segment Analysis by Region")

if (
    "Region" in filtered_df.columns
    and "Segment" in filtered_df.columns
    and "Profit" in filtered_df.columns
):

    segment_region = (
        filtered_df
        .groupby(
            ["Region", "Segment"],
            as_index=False
        )["Profit"]
        .sum()
    )

    fig8 = px.bar(
        segment_region,
        x="Region",
        y="Profit",
        color="Segment",
        barmode="group",
        title="Segment Wise Profit by Region"
    )

    st.plotly_chart(
        fig8,
        use_container_width=True
    )

# ---------------------------------------------------
# REGION SUMMARY TABLE
# ---------------------------------------------------
st.subheader("Region Summary Table")

summary_table = (
    filtered_df
    .groupby("Region", as_index=False)
    .agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Order ID": "nunique"
    })
)

summary_table = summary_table.rename(
    columns={
        "Order ID": "Total Orders"
    }
)

st.dataframe(
    summary_table,
    use_container_width=True
)

# ---------------------------------------------------
# DOWNLOAD FILTERED DATA
# ---------------------------------------------------
st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Region Analysis Data",
    data=csv,
    file_name="region_analysis_filtered_data.csv",
    mime="text/csv"
)
