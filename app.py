import streamlit as st

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Income Tax Calculator", page_icon="💰", layout="centered")

# -------------------------------
# Title
# -------------------------------
st.title("💰 Income Tax Calculator (India)")
st.markdown("Calculate your income tax with a clean and simple interface.")

# -------------------------------
# Sidebar - Regime Selection
# -------------------------------
st.sidebar.header("⚙️ Settings")
regime = st.sidebar.radio("Choose Tax Regime", ["New Regime", "Old Regime"])

# -------------------------------
# User Inputs
# -------------------------------
st.subheader("📥 Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Annual Income (₹)", min_value=0.0, step=50000.0)

with col2:
    age = st.selectbox("Age Group", ["Below 60", "60 to 80", "Above 80"])

# Deductions (Only for old regime)
deductions = 0
if regime == "Old Regime":
    st.subheader("📉 Deductions")
    deductions = st.number_input("Total Deductions (₹)", min_value=0.0, step=10000.0)

# -------------------------------
# Tax Calculation Functions
# -------------------------------
def calculate_new_regime_tax(income):
    tax = 0
    if income <= 300000:
        tax = 0
    elif income <= 600000:
        tax = (income - 300000) * 0.05
    elif income <= 900000:
        tax = 15000 + (income - 600000) * 0.10
    elif income <= 1200000:
        tax = 45000 + (income - 900000) * 0.15
    elif income <= 1500000:
        tax = 90000 + (income - 1200000) * 0.20
    else:
        tax = 150000 + (income - 1500000) * 0.30
    return tax

def calculate_old_regime_tax(income, age):
    tax = 0

    if age == "Below 60":
        slabs = [(250000, 0), (500000, 0.05), (1000000, 0.2), (float('inf'), 0.3)]
    elif age == "60 to 80":
        slabs = [(300000, 0), (500000, 0.05), (1000000, 0.2), (float('inf'), 0.3)]
    else:
        slabs = [(500000, 0), (1000000, 0.2), (float('inf'), 0.3)]

    prev_limit = 0
    for limit, rate in slabs:
        if income > limit:
            tax += (limit - prev_limit) * rate
            prev_limit = limit
        else:
            tax += (income - prev_limit) * rate
            break

    return tax

# -------------------------------
# Compute Tax
# -------------------------------
if st.button("🧮 Calculate Tax"):
    if income <= 0:
        st.error("⚠️ Please enter a valid income.")
    else:
        if regime == "New Regime":
            tax = calculate_new_regime_tax(income)
            taxable_income = income
        else:
            taxable_income = max(0, income - deductions)
            tax = calculate_old_regime_tax(taxable_income, age)

        # Add 4% cess
        cess = tax * 0.04
        total_tax = tax + cess

        # -------------------------------
        # Output Section
        # -------------------------------
        st.subheader("📊 Tax Summary")

        st.metric("Taxable Income", f"₹ {taxable_income:,.0f}")
        st.metric("Income Tax", f"₹ {tax:,.0f}")
        st.metric("Health & Education Cess (4%)", f"₹ {cess:,.0f}")
        st.success(f"💸 Total Tax Payable: ₹ {total_tax:,.0f}")

        # Simple Visualization
        st.progress(min(total_tax / income if income > 0 else 0, 1.0))