
# Konfigurasi halaman
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('train.csv)

    df['Order Date'] = pd.to_datetime(
        df['Order Date'], format='%d/%m/%Y'
    )
    df['Ship Date'] = pd.to_datetime(
        df['Ship Date'], format='%d/%m/%Y'
    )

    return df

df = load_data()

# Judul dashboard
st.title("📊 Superstore Sales Dashboard")
st.write("Explore sales performance across categories, regions, and customer segments.")

# Sidebar filters
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df['Region'].dropna().unique()),
    default=sorted(df['Region'].dropna().unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df['Category'].dropna().unique()),
    default=sorted(df['Category'].dropna().unique())
)

segments = st.sidebar.multiselect(
    "Select Customer Segment",
    options=sorted(df['Segment'].dropna().unique()),
    default=sorted(df['Segment'].dropna().unique())
)

# Filter data
filtered_df = df[
    df['Region'].isin(regions)
    & df['Category'].isin(categories)
    & df['Segment'].isin(segments)
]

# KPI metrics
total_sales = filtered_df['Sales'].sum()
total_orders = filtered_df['Order ID'].nunique()
average_sales = filtered_df['Sales'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Average Sales per Row", f"${average_sales:,.2f}")

st.divider()

# Sales by category
st.subheader("Sales by Category")

sales_category = (
    filtered_df.groupby('Category')['Sales']
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(sales_category)

# Sales by subcategory
st.subheader("Sales by Subcategory")

sales_subcategory = (
    filtered_df.groupby('Sub-Category')['Sales']
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(sales_subcategory)

# Sales by region
st.subheader("Sales by Region")

sales_region = (
    filtered_df.groupby('Region')['Sales']
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(sales_region)

# Monthly sales trend
st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df.set_index('Order Date')['Sales']
    .resample('MS')
    .sum()
)

st.line_chart(monthly_sales)

# Sales by customer segment
st.subheader("Sales by Customer Segment")

sales_segment = (
    filtered_df.groupby('Segment')['Sales']
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(sales_segment)

# Data preview
with st.expander("View Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

st.caption("Data source: Superstore Sales Forecasting dataset")
