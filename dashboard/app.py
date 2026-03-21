import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Payroll Dashboard",
    page_icon="💼",
    layout="wide"
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    db_path = os.path.join(os.path.dirname(__file__), "..", "payroll.db")
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "clean_payroll.csv")

    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT * FROM payroll", conn)
        conn.close()
    else:
        df = pd.read_csv(csv_path)

    # Fix floating point precision
    for col in ["gross_pay", "tax_deduction", "net_pay"]:
        df[col] = df[col].round(2)

    return df

df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("Filters")
departments = ["All"] + sorted(df["department"].unique().tolist())
selected_dept = st.sidebar.selectbox("Department", departments)

emp_types = ["All"] + sorted(df["employment_type"].unique().tolist())
selected_type = st.sidebar.selectbox("Employment Type", emp_types)

pay_range = st.sidebar.slider(
    "Gross Pay Range ($)",
    min_value=int(df["gross_pay"].min()),
    max_value=int(df["gross_pay"].max()),
    value=(int(df["gross_pay"].min()), int(df["gross_pay"].max()))
)

# Apply filters
filtered = df.copy()
if selected_dept != "All":
    filtered = filtered[filtered["department"] == selected_dept]
if selected_type != "All":
    filtered = filtered[filtered["employment_type"] == selected_type]
filtered = filtered[
    (filtered["gross_pay"] >= pay_range[0]) &
    (filtered["gross_pay"] <= pay_range[1])
]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("💼 LA City Payroll Dashboard")
st.caption(f"Showing {len(filtered):,} of {len(df):,} employees")
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", f"{len(filtered):,}")
col2.metric("Total Gross Payroll", f"${filtered['gross_pay'].sum():,.0f}")
col3.metric("Avg Net Pay", f"${filtered['net_pay'].mean():,.0f}")
col4.metric("Avg Tax Deduction", f"${filtered['tax_deduction'].mean():,.0f}")

st.divider()

# ── Charts row 1 ──────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 Departments by Avg Gross Pay")
    top_depts = (
        filtered.groupby("department")["gross_pay"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_depts.columns = ["Department", "Avg Gross Pay"]
    fig1 = px.bar(
        top_depts,
        x="Avg Gross Pay",
        y="Department",
        orientation="h",
        color="Avg Gross Pay",
        color_continuous_scale="Blues",
        text_auto="$.0f"
    )
    fig1.update_layout(showlegend=False, coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Employment Type Breakdown")
    emp_counts = filtered["employment_type"].value_counts().reset_index()
    emp_counts.columns = ["Type", "Count"]
    fig2 = px.pie(
        emp_counts,
        names="Type",
        values="Count",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig2, use_container_width=True)

# ── Charts row 2 ──────────────────────────────────────────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Gross Pay Distribution")
    fig3 = px.histogram(
        filtered,
        x="gross_pay",
        nbins=40,
        color_discrete_sequence=["#1f77b4"],
        labels={"gross_pay": "Gross Pay ($)"}
    )
    fig3.update_layout(bargap=0.05)
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.subheader("Gross vs Net Pay by Department")
    dept_pay = (
        filtered.groupby("department")[["gross_pay", "net_pay"]]
        .mean()
        .sort_values("gross_pay", ascending=False)
        .head(10)
        .reset_index()
    )
    fig4 = px.bar(
        dept_pay.melt(id_vars="department", value_vars=["gross_pay", "net_pay"]),
        x="department",
        y="value",
        color="variable",
        barmode="group",
        labels={"value": "Amount ($)", "department": "Department", "variable": "Type"},
        color_discrete_map={"gross_pay": "#1f77b4", "net_pay": "#2ca02c"}
    )
    fig4.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig4, use_container_width=True)

# ── Top Earners Table ─────────────────────────────────────────────────────────
st.divider()
st.subheader("Top 20 Earners")
top_earners = (
    filtered.sort_values("gross_pay", ascending=False)
    .head(20)
    .reset_index(drop=True)
)
top_earners.index += 1
st.dataframe(
    top_earners.style.format({
        "gross_pay": "${:,.2f}",
        "tax_deduction": "${:,.2f}",
        "net_pay": "${:,.2f}"
    }),
    use_container_width=True
)

# ── Raw Data ──────────────────────────────────────────────────────────────────
with st.expander("View Raw Data"):
    st.dataframe(filtered, use_container_width=True)
    csv = filtered.to_csv(index=False)
    st.download_button("Download CSV", csv, "filtered_payroll.csv", "text/csv")
