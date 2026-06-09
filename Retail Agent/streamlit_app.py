import requests
import streamlit as st
import pandas as pd
import plotly.express as px

from synthetic_data import generate_sales_data, load_sales_data

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Retail AI Analyst",
    page_icon="🛒",
    layout="wide"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("⚙️ Controls")

if st.sidebar.button("🔄 Regenerate Synthetic Data"):
    generate_sales_data()
    st.sidebar.success("New dataset generated!")

# load dataset
df = load_sales_data()

st.sidebar.markdown("### Dataset Filters")

category_filter = st.sidebar.multiselect(
    "Category",
    df["category"].unique()
)

region_filter = st.sidebar.multiselect(
    "Region",
    df["store_region"].unique()
)

# apply filters
filtered_df = df.copy()

if category_filter:
    filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]

if region_filter:
    filtered_df = filtered_df[filtered_df["store_region"].isin(region_filter)]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🛒 AI Retail Sales Intelligence Agent")
st.caption("Ask natural language questions about trends, anomalies, and promotions.")

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${filtered_df['revenue'].sum():,.0f}")
col2.metric("Units Sold", f"{filtered_df['units_sold'].sum():,}")
col3.metric("Avg Price", f"${filtered_df['price'].mean():.2f}")
col4.metric("Stores", filtered_df["store_id"].nunique())

st.divider()

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Sales Trend")

    trend = filtered_df.groupby("date")["units_sold"].sum().reset_index()

    fig = px.line(
        trend,
        x="date",
        y="units_sold",
        title="Daily Units Sold"
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:

    st.subheader("🏆 Category Performance")

    cat = filtered_df.groupby("category")["units_sold"].sum().reset_index()

    fig = px.bar(
        cat,
        x="category",
        y="units_sold",
        title="Units Sold by Category"
    )

    st.plotly_chart(fig, use_container_width=True)


st.divider()

# ---------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------

with st.expander("📄 View Dataset"):

    st.dataframe(filtered_df.head(200))


# ---------------------------------------------------
# AI CHAT AGENT
# ---------------------------------------------------

st.subheader("🤖 Ask the AI Retail Analyst")

example_cols = st.columns(3)

if example_cols[0].button("Compare regions"):
    st.session_state.prompt = "Compare sales across regions"

if example_cols[1].button("Find anomalies in beverages"):
    st.session_state.prompt = "Show anomalies in the Beverages category"

if example_cols[2].button("Promo simulation"):
    st.session_state.prompt = "What if we run a 20% discount on Snacks?"

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


prompt = st.chat_input(
    "Ask something like: 'Which categories sell best during holidays?'",
    key="chat_input"
)

# use example prompt if selected
if "prompt" in st.session_state:
    prompt = st.session_state.prompt
    del st.session_state.prompt

# ---------------------------------------------------
# AI RESPONSE
# ---------------------------------------------------

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing retail data..."):
            api_url = "http://localhost:8000/chat"
            try:
                response = requests.post(
                    api_url,
                    json={"messages": [{"role": "user", "content": prompt}]},
                    timeout=30,
                )
                response.raise_for_status()
                payload = response.json()
                response = payload.get("assistant_message", {}).get("content", "No response from API")
            except requests.RequestException as exc:
                response = f"API request failed: {exc}"

            st.write(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })