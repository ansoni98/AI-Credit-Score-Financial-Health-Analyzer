import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="AI Credit Score Analyzer", layout="wide")

# ---------- Premium Glass UI ----------
st.markdown("""
<style>
body {background: linear-gradient(135deg, #0f172a, #020617);} 
.stApp {background: transparent;}
.glass {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

st.title("💳 AI Credit Score & Financial Health Analyzer")

# ---------- Sidebar Inputs ----------
st.sidebar.header("User Input")
income = st.sidebar.number_input("Monthly Income (₹)", value=50000)
expenses = st.sidebar.number_input("Monthly Expenses (₹)", value=30000)

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

dti_ratio = expenses / income if income > 0 else 1
probability = min(100, max(0, int((credit_score/850)*100 - dti_ratio*50)))

# ---------- Dashboard Cards ----------
st.subheader("📊 Financial Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("💳 Credit Score", credit_score)
col2.metric("📈 Health Score", f"{health_score}/100")
col3.metric("💰 Savings Rate", f"{round(savings_rate*100,1)}%")

# ---------- Advanced Analytics ----------
st.subheader("📊 Advanced Analytics")
fig = go.Figure()
fig.add_trace(go.Bar(x=["Income","Expenses","Savings"], y=[income, expenses, savings]))
st.plotly_chart(fig, use_container_width=True)

fig2 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=credit_score,
    gauge={'axis': {'range': [300, 850]}}
))
st.plotly_chart(fig2, use_container_width=True)

# ---------- Loan Probability ----------
st.subheader("🏦 Loan Approval Probability")
if probability > 70:
    st.success(f"✅ {probability}% Approval Chance")
elif probability > 40:
    st.warning(f"⚠️ {probability}% Approval Chance")
else:
    st.error(f"❌ {probability}% Approval Chance")

# ---------- EMI ----------
st.subheader("📊 EMI Calculator")
monthly_rate = interest_rate / 12
months = loan_years * 12

emi = loan_amount * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1) if monthly_rate>0 else loan_amount/months
st.metric("Monthly EMI", f"₹{int(emi)}")

# EMI Trend
balance = loan_amount
balances = []
for i in range(months):
    interest = balance * monthly_rate
    principal = emi - interest
    balance -= principal
    balances.append(balance if balance>0 else 0)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(y=balances, mode='lines', name='Remaining Loan'))
st.plotly_chart(fig3, use_container_width=True)

# ---------- AI Chatbot (Upgraded placeholder) ----------
st.subheader("🤖 AI Financial Assistant")
query = st.text_input("Ask anything about finance:")

if query:
    if "credit" in query.lower():
        st.write("💡 Maintain low expenses and high savings to improve credit score.")
    elif "loan" in query.lower():
        st.write("💡 Lower DTI ratio increases loan approval chances.")
    elif "invest" in query.lower():
        st.write("💡 Diversify investments for better returns.")
    else:
        st.write("💡 Focus on saving, investing, and smart financial planning.")

# ---------- Projection ----------
st.subheader("🔮 Future Projection")
st.write(f"Estimated yearly savings: ₹{savings*12}")

st.markdown("---")
st.caption("🚀 Advanced AI FinTech Dashboard | Premium UI")
