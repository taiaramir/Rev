import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from revenue_calculator import calculate_revenue
from utils import create_styled_dataframe

st.set_page_config(layout="wide", page_title="Startup Revenue Projector")

# Custom CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 18px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        padding: 8px 16px;
    }
    .main-header {
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        margin-top: 16px;
        margin-bottom: 16px;
    }
    .plan-header {
        font-size: 16px;
        font-weight: normal;
        margin-bottom: 10px;
    }
    .sidebar-header {
        font-size: 18px;
        font-weight: bold;
        margin-top: 16px;
        margin-bottom: 8px;
    }
    .sidebar .sidebar-content {
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar

# Navigation in Sidebar
menu_item = st.sidebar.radio("", ["Plans", "Revenue", "Graphs"], label_visibility="collapsed")

st.sidebar.markdown("---")

# Base Pricing in Sidebar
st.sidebar.markdown('<p class="sidebar-header">Base Pricing</p>', unsafe_allow_html=True)
base_price = st.sidebar.number_input("Base Price per Customer (Company)", min_value=0.0, value=100.0)
workspace_cost = st.sidebar.number_input("Workspace Cost per User", min_value=0.0, value=5.0)

st.sidebar.markdown("---")

# Projection Period in Sidebar (renamed to "Period")
st.sidebar.markdown('<p class="sidebar-header">Period</p>', unsafe_allow_html=True)
years = st.sidebar.number_input('Number of Years', min_value=1, value=1)
months = st.sidebar.number_input('Additional Months', min_value=0, max_value=11, value=0)

total_months = years * 12 + months

# Main content
if menu_item == "Plans":
    st.markdown('<p class="main-header">Plans</p>', unsafe_allow_html=True)

    plans = ["Basic", "Pro", "Enterprise"]

    customers = {}
    avg_employees = {}
    user_percentages = {}
    prices_per_user = {}
    growth_rates = {}
    churn_rates = {}
    workspace_percentages = {}

    tabs = st.tabs(plans)

    for i, plan in enumerate(plans):
        with tabs[i]:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f'<p class="plan-header">Customer Information</p>', unsafe_allow_html=True)
                customers[plan] = st.number_input(f"Number of Customers", min_value=0, value=10, key=f"customers_{plan}")
                avg_employees[plan] = st.number_input(f"Avg. Employees per Customer", min_value=0, value=10000, key=f"employees_{plan}")
                user_percentages[plan] = st.number_input(f"Percentage of Employees as Users", min_value=0.0, max_value=100.0, value=10.0, key=f"user_percentage_{plan}") / 100
            
            with col2:
                st.markdown(f'<p class="plan-header">Pricing and Growth</p>', unsafe_allow_html=True)
                prices_per_user[plan] = st.number_input(f"Price per User", min_value=0.0, value=10.0 if plan == "Basic" else 20.0 if plan == "Pro" else 30.0, key=f"price_{plan}")
                growth_rates[plan] = st.number_input(f"Monthly Customer Growth Rate %", min_value=0.0, max_value=100.0, value=5.0, key=f"growth_{plan}") / 100
                churn_rates[plan] = st.number_input(f"Monthly Customer Churn Rate %", min_value=0.0, max_value=100.0, value=1.0, key=f"churn_{plan}") / 100
            
            with col3:
                st.markdown(f'<p class="plan-header">Workspace Details</p>', unsafe_allow_html=True)
                workspace_percentages[plan] = st.number_input(f"Workspace Percentage", min_value=0.0, max_value=100.0, value=50.0, key=f"workspace_{plan}") / 100

    if st.button('Calculate Revenue'):
        st.session_state['calculation_done'] = True
        st.session_state['total_revenue'], st.session_state['yearly_data'] = calculate_revenue(
            customers, avg_employees, user_percentages, growth_rates, churn_rates,
            base_price, prices_per_user, workspace_cost, workspace_percentages, total_months
        )
        st.success("Calculation complete! Go to the Revenue page to see the results.")

elif menu_item == "Revenue":
    st.markdown('<p class="main-header">Revenue Projection</p>', unsafe_allow_html=True)
    if 'calculation_done' in st.session_state and st.session_state['calculation_done']:
        st.success(f"Projected Total Revenue: ${st.session_state['total_revenue']:,.2f}")

        st.markdown('<p class="sub-header">Revenue Breakdown by Plan and Year</p>', unsafe_allow_html=True)
        styled_df = create_styled_dataframe(st.session_state['yearly_data'])
        st.table(styled_df)
    else:
        st.warning("Please calculate the revenue projection first on the Plans page.")

elif menu_item == "Graphs":
    st.markdown('<p class="main-header">Revenue Projection Graphs</p>', unsafe_allow_html=True)
    if 'calculation_done' in st.session_state and st.session_state['calculation_done']:
        yearly_data = st.session_state['yearly_data']
        
        # Prepare data for graphs
        years = [data['Year'] for data in yearly_data]
        plans = ["Basic", "Pro", "Enterprise"]
        
        # Graph 1: Total Revenue by Plan
        total_revenue_by_plan = {plan: [data['Total Revenue'][plan] for data in yearly_data] for plan in plans}
        
        fig1 = go.Figure()
        for plan in plans:
            fig1.add_trace(go.Bar(x=years, y=total_revenue_by_plan[plan], name=plan))
        
        fig1.update_layout(title="Total Revenue by Plan", xaxis_title="Year", yaxis_title="Revenue ($)", barmode='stack')
        st.plotly_chart(fig1, use_container_width=True)
        
        # Graph 2: Customer Growth
        customers_by_plan = {plan: [data['Customers'][plan] for data in yearly_data] for plan in plans}
        
        fig2 = go.Figure()
        for plan in plans:
            fig2.add_trace(go.Scatter(x=years, y=customers_by_plan[plan], mode='lines+markers', name=plan))
        
        fig2.update_layout(title="Customer Growth by Plan", xaxis_title="Year", yaxis_title="Number of Customers")
        st.plotly_chart(fig2, use_container_width=True)
        
        # Graph 3: Revenue per Customer
        revenue_per_customer = {plan: [data['Total Revenue'][plan] / data['Customers'][plan] for data in yearly_data] for plan in plans}
        
        fig3 = go.Figure()
        for plan in plans:
            fig3.add_trace(go.Scatter(x=years, y=revenue_per_customer[plan], mode='lines+markers', name=plan))
        
        fig3.update_layout(title="Revenue per Customer by Plan", xaxis_title="Year", yaxis_title="Revenue per Customer ($)")
        st.plotly_chart(fig3, use_container_width=True)
        
    else:
        st.warning("Please calculate the revenue projection first on the Plans page.")