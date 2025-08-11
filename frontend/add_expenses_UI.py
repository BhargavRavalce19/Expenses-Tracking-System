import streamlit as st
from datetime import datetime
import requests

API_URL = 'http://127.0.0.1:8000'

def add_expenses():
    expenses_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility='hidden')
    response = requests.get(f"{API_URL}/expenses/{expenses_date}")

    if response.status_code == 200:
        existing_expenses = response.json()
        # st.write(existing_expenses)
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Education", "Entertainment", "Other"]
    no_of_expense = st.number_input(label="No of Expenses:", min_value=1, step=1, value=1)
    expenses = []

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Amount:")
        with col2:
            st.subheader("Category:")
        with col3:
            st.subheader("Notes:")
        for i in range(no_of_expense):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",
                                               label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(category),
                                              key=f"category_{i}", label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
            requests.post(f"{API_URL}/expenses/{expenses_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses Updated Successfully!")
            else:
                st.error("Failed! to Update Expenses.")
