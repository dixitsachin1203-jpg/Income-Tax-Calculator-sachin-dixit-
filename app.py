import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Income Tax Calculator",
    page_icon="💰",
    layout="wide"
)

# -----------------------
# Custom Styling
# -----------------------
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: white;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("⚙️ Tax Settings")

income = st.sidebar.number_input("Annual Income (₹)", min_value=0, value=1000000, step=50000)
deductions = st.sidebar.number_input("Deductions (₹)", min_value=0, value=150000, step=10000)

regime = st.sidebar.radio(
    "Choose Tax Regime",
    ["Old Regime", "New Regime"]
)

# -----------------------
# Tax Calculation Functions
# -----------------------
def calculate_old_tax(income, deductions):
    taxable_income = max(0, income - deductions)
    tax = 0
    breakdown = []

    slabs = [
        (250000, 0),
        (500000, 0.05),
        (1000000, 0.20),
        (float("inf"), 0.30)
    ]

    prev_limit = 0
    for limit, rate in slabs:
        if taxable_income > prev_limit:
            taxable = min(limit - prev_limit, taxable_income - prev_limit)
            slab_tax = taxable * rate
            tax += slab_tax
            breakdown.append((f"{prev_limit}-{limit}", slab_tax))
        prev_limit = limit

    return tax, taxable_income, breakdown


def calculate_new_tax(income):
    taxable_income = income
    tax = 0
    breakdown = []

    slabs = [
        (300000, 0),
        (600000, 0.05),
        (900000, 0.10),
        (1200000, 0.15),
        (1500000, 0.20),
        (float("inf"), 0.30)
    ]

    prev_limit = 0
    for limit, rate in slabs:
        if taxable_income > prev_limit:
            taxable = min(limit - prev_limit, taxable_income - prev_limit)
            slab_tax = taxable * rate
            tax += slab_tax
            breakdown.append((f"{prev_limit}-{limit}", slab_tax))
        prev_limit = limit

    return tax, taxable_income, breakdown

# -----------------------
# Main UI
# -----------------------
st.title("💰 Income Tax Calculator")
st.caption("Advanced UI with charts and insights")

col1, col2, col3 = st.columns(3)

# Calculate tax
if regime == "Old Regime":
    tax, taxable_income, breakdown = calculate_old_tax(income, deductions)
else:
    tax, taxable_income, breakdown = calculate_new_tax(income)

# Metrics
col1.metric("💼 Income", f"₹ {income:,.0f}")
col2.metric("📉 Taxable Income", f"₹ {taxable_income:,.0f}")
col3.metric("💸 Tax Payable", f"₹ {tax:,.0f}")

st.divider()

# -----------------------
# Charts
# -----------------------
df = pd.DataFrame(breakdown, columns=["Slab", "Tax Paid"])

col4, col5 = st.columns(2)

with col4:
    st.subheader("📊 Tax Distribution (Pie)")
    fig_pie = px.pie(df, values="Tax Paid", names="Slab", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with col5:
    st.subheader("📈 Tax by Slab (Bar)")
    fig_bar = px.bar(df, x="Slab", y="Tax Paid", color="Tax Paid", text_auto=True)
    st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------
# Detailed Table
# -----------------------
st.subheader("📋 Detailed Breakdown")
st.dataframe(df, use_container_width=True)

# -----------------------
# Insights Section
# -----------------------
st.subheader("🧠 Insights")

if regime == "Old Regime":
    st.info("Old regime benefits people with high deductions.")
else:
    st.info("New regime offers lower tax rates but no deductions.")

if tax == 0:
    st.success("You have no tax liability 🎉")
elif tax < 50000:
    st.warning("Your tax is relatively low.")
else:
    st.error("You have a higher tax liability. Consider planning investments.")
