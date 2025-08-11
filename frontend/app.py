import streamlit as st
from add_expenses_UI import add_expenses
from analytics_UI import analytics_tab
from monthly_analytics_UI import get_expenses_by_moths_tab

st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["Add/Updates", "Analytics", "Monthly Analytics"])

with tab1:
    add_expenses()

with tab2:
    analytics_tab()

with tab3:
    get_expenses_by_moths_tab()