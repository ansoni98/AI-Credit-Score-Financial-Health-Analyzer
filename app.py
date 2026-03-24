import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="AI Credit Score Analyzer", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
.main {background-color: #0e1117; color: white;}
.stMetric {background-color: #1f2937; padding: 12px; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("💳 AI Credit Score & Financial Health Analyzer")

# ---------- Sidebar Inputs ----------
st.sidebar.header("User Input")
income = st.sidebar.number_input("Monthly Income (₹)", value=50000)
expenses = st.sidebar.number_input("Monthly Expenses (₹)", value=30000)

# Loan inputs (NEW)
st.sidebar.markdown("---")
st.sidebar.subheader("🏦 Loan Details")
loan_amount = st.sidebar.number_input("Loan Amount (₹)", value=500000)
interest_rate = st.sidebar.slider("Interest Rate (%)", 5.0, 20.0, 10.0) / 100
loan_years = st.sidebar.slider("Loan Tenure (Years)", 1, 30, 5)

# ---------- Calculations ----------
savings = income - expenses
savings_rate = savings / income if income > 0 else 0

# Credit score logic
credit_score = int(300 + (savings_rate * 550))
credit_score = max(300, min(850, credit_score))

# Financial health score
health_score = int(savings_rate * 100)

# Risk level
if savings_rate > 0.4:
    risk = "Low"
elif savings_rate > 0.2:
    risk = "Moderate"
else:
    risk = "High"

# ---------- KPIs ----------
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Credit Score", credit_score)
col2.metric("Financial Health", f"{health_score}/100")
col3.metric("Savings Rate", f"{round(savings_rate*100,1)}%")

# ---------- Gauge Chart ----------
st.subheader("📈 Credit Score Gauge")
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=credit_score,
    gauge={'axis': {'range': [300, 850]}}
))
st.plotly_chart(fig, use_container_width=True)

# ---------- Expense Breakdown ----------
st.subheader("💰 Income vs Expenses")
fig2 = go.Figure(data=[go.Pie(labels=["Expenses", "Savings"], values=[expenses, savings])])
st.plotly_chart(fig2, use_container_width=True)

# ---------- Risk Display ----------
st.subheader("⚠️ Risk Level")
st.write(f"Your financial risk level is: **{risk}**")

# ---------- AI Insights ----------
st.subheader("🧠 AI Insights")
if savings_rate < 0.2:
    st.error("You are spending too much compared to your income.")
elif savings_rate < 0.4:
    st.warning("Your savings are moderate. Try improving them.")
else:
    st.success("Excellent savings habit! Keep it up.")

# ---------- Recommendations ----------
st.subheader("💡 Recommendations")
if savings_rate < 0.3:
    st.write("- Reduce unnecessary expenses")
    st.write("- Increase savings by at least 20%")
    st.write("- Avoid high debt")
else:
    st.write("- Maintain current financial discipline")
    st.write("- Consider investing surplus funds")

# ---------- Loan Eligibility (NEW) ----------
st.subheader("🏦 Loan Eligibility Prediction")

dti_ratio = expenses / income if income > 0 else 1

if credit_score > 700 and dti_ratio < 0.4:
    eligibility = "High"
    st.success("✅ High chances of loan approval")
elif credit_score > 600:
    eligibility = "Moderate"
    st.warning("⚠️ Moderate chances of approval")
else:
    eligibility = "Low"
    st.error("❌ Low chances of approval")

st.write(f"📊 Debt-to-Income Ratio: {round(dti_ratio*100,1)}%")

# ---------- EMI Calculator (NEW) ----------
st.subheader("📊 EMI Calculator")

monthly_rate = interest_rate / 12
months = loan_years * 12

if monthly_rate > 0:
    emi = loan_amount * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
else:
    emi = loan_amount / months

st.metric("Monthly EMI", f"₹{int(emi)}")
st.write(f"Total Payment: ₹{int(emi * months)}")
st.write(f"Total Interest: ₹{int((emi * months) - loan_amount)}")

# ---------- Future Projection ----------
st.subheader("🔮 1-Year Savings Projection")
projection = savings * 12
st.write(f"Estimated savings after 1 year: ₹{projection}")

st.markdown("---")
st.caption("AI FinTech Project - Credit Score Analyzer with Loan Prediction & EMI Calculator")
