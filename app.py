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

# Loan inputs
st.sidebar.markdown("---")
st.sidebar.subheader("🏦 Loan Details")
loan_amount = st.sidebar.number_input("Loan Amount (₹)", value=500000)
interest_rate = st.sidebar.slider("Interest Rate (%)", 5.0, 20.0, 10.0) / 100
loan_years = st.sidebar.slider("Loan Tenure (Years)", 1, 30, 5)

# ---------- Calculations ----------
savings = income - expenses
savings_rate = savings / income if income > 0 else 0

credit_score = int(300 + (savings_rate * 550))
credit_score = max(300, min(850, credit_score))

health_score = int(savings_rate * 100)

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

# ---------- Gauge ----------
st.subheader("📈 Credit Score Gauge")
fig = go.Figure(go.Indicator(mode="gauge+number", value=credit_score,
    gauge={'axis': {'range': [300, 850]}}))
st.plotly_chart(fig, use_container_width=True)

# ---------- Pie ----------
st.subheader("💰 Income vs Expenses")
fig2 = go.Figure(data=[go.Pie(labels=["Expenses", "Savings"], values=[expenses, savings])])
st.plotly_chart(fig2, use_container_width=True)

# ---------- Loan Eligibility ----------
st.subheader("🏦 Loan Eligibility Prediction")
dti_ratio = expenses / income if income > 0 else 1

# Probability logic
probability = min(100, max(0, int((credit_score/850)*100 - dti_ratio*50)))

if probability > 70:
    st.success(f"✅ High Approval Probability: {probability}%")
elif probability > 40:
    st.warning(f"⚠️ Moderate Approval Probability: {probability}%")
else:
    st.error(f"❌ Low Approval Probability: {probability}%")

st.write(f"📊 Debt-to-Income Ratio: {round(dti_ratio*100,1)}%")

# ---------- EMI Calculator ----------
st.subheader("📊 EMI Calculator")
monthly_rate = interest_rate / 12
months = loan_years * 12

if monthly_rate > 0:
    emi = loan_amount * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
else:
    emi = loan_amount / months

st.metric("Monthly EMI", f"₹{int(emi)}")

# EMI Graph
balance = loan_amount
balances = []
for i in range(months):
    interest = balance * monthly_rate
    principal = emi - interest
    balance -= principal
    balances.append(balance if balance > 0 else 0)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(y=balances, mode='lines', name='Remaining Loan'))
st.plotly_chart(fig3, use_container_width=True)

# ---------- Chatbot ----------
st.subheader("🤖 Finance AI Assistant")
user_q = st.text_input("Ask a financial question:")

if user_q:
    if "save" in user_q.lower():
        st.write("💡 Try to save at least 20% of your income.")
    elif "loan" in user_q.lower():
        st.write("💡 Maintain a good credit score and low DTI for loan approval.")
    elif "invest" in user_q.lower():
        st.write("💡 Diversify investments across stocks, bonds, and gold.")
    else:
        st.write("💡 Focus on budgeting, saving, and smart investing.")

# ---------- Projection ----------
st.subheader("🔮 1-Year Savings Projection")
projection = savings * 12
st.write(f"Estimated savings after 1 year: ₹{projection}")

st.markdown("---")
st.caption("AI FinTech Project - Advanced Credit Analyzer")
