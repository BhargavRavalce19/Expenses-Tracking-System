import streamlit as st
import pandas as pd
import requests



st.title("Total Expenses By Months")

API_URL= "http://127.0.0.1:8000/monthly_expenses"

def get_expenses_by_moths_tab():
    if st.button("Get Monthly"):
        try:
            response = requests.get(API_URL)
            response.raise_for_status()

            data = response.json()
            df = pd.DataFrame(data)
            df= df.rename(columns={"year": "Year",
                                   "month_num": "Month No.",
                                   "month_name": "Month Name",
                                   "total_amount": "Total Amount"})
            df.set_index("Month No.", inplace=True)


            st.subheader("Table View")
            st.dataframe(df)

            st.subheader("Monthly Insights")
            st.bar_chart(df.set_index("Month Name")["Total Amount"])

        except requests.exceptions.RequestException as e:
            st.error(f"Error:{e}")

