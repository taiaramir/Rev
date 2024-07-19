import streamlit as st
import pandas as pd
from revenue_calculator import calculate_revenue
from utils import create_styled_dataframe

st.title('Startup Revenue Projector')

st.header("Base Pricing")
col1, col2 = st.columns(2)
with col1:
    base_price = st.number_input("Base Price per Customer (Company)", min_value=0.0, value=100.0)
with col2:
    workspace_cost = st.number_input("Workspace Cost per User", min_value=0.0, value=5.0)

st.markdown("---")

plans = ["Basic", "Pro", "Enterprise"]

customers = {}
avg_employees = {}
user_percentages = {}
prices_per_user = {}
growth_rates = {}
churn_rates = {}
workspace_percentages = {}

# Create tabs for each plan
tabs = st.tabs(plans)

for i, plan in enumerate(plans):
    with tabs[i]:
        st.header(f"{plan} Plan Details")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Customer Information")
            customers[plan] = st.number_input(f"Number of Customers", min_value=0, value=10, key=f"customers_{plan}")
            avg_employees[plan] = st.number_input(f"Avg. Employees per Customer", min_value=0, value=10000, key=f"employees_{plan}")
            user_percentages[plan] = st.number_input(f"Percentage of Employees as Users", min_value=0.0, max_value=100.0, value=10.0, key=f"user_percentage_{plan}") / 100
        
        with col2:
            st.subheader("Pricing and Growth")
            prices_per_user[plan] = st.number_input(f"Price per User", min_value=0.0, value=10.0 if plan == "Basic" else 20.0 if plan == "Pro" else 30.0, key=f"price_{plan}")
            growth_rates[plan] = st.number_input(f"Monthly Customer Growth Rate %", min_value=0.0, max_value=100.0, value=5.0, key=f"growth_{plan}") / 100
            churn_rates[plan] = st.number_input(f"Monthly Customer Churn Rate %", min_value=0.0, max_value=100.0, value=1.0, key=f"churn_{plan}") / 100
        
        with col3:
            st.subheader("Workspace Details")
            st.markdown("""
            <style>
            .workspace-box {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 10px;
                background-color: #f1f8e9;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="workspace-box">', unsafe_allow_html=True)
            workspace_percentages[plan] = st.number_input(f"Workspace Percentage", min_value=0.0, max_value=100.0, value=50.0, key=f"workspace_{plan}") / 100
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    years = st.number_input('Number of Years', min_value=1, value=1)
with col2:
    months = st.number_input('Additional Months', min_value=0, max_value=11, value=0)

total_months = years * 12 + months

if st.button('Calculate Revenue'):
    total_revenue, yearly_data = calculate_revenue(
        customers, avg_employees, user_percentages, growth_rates, churn_rates,
        base_price, prices_per_user, workspace_cost, workspace_percentages, total_months
    )
    st.success(f"Projected Total Revenue: ${total_revenue:,.2f}")

    st.subheader("Revenue Breakdown by Plan and Year")
    styled_df = create_styled_dataframe(yearly_data)
    st.table(styled_df)

st.info('Adjust the values for each plan and click "Calculate Revenue" to see the projection.')