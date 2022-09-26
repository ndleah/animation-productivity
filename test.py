# Import required libraries
import streamlit as st
import snowflake.connector
import pandas as pd
import matplotlib.pyplot as plt
import csv

st.set_page_config(page_title="Customer Churn Dashboard",
layout="wide")

@st.experimental_singleton
def init_connection():
  return snowflake.connector.connect(**st.secrets["snowflake"])
  
conn = init_connection()

# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
  with conn.cursor() as cur:
    cur.execute(query)
    return cur.fetchall()


# Query Snowflake for features and predictions
data = run_query("SELECT * FROM FINAL_PRODUCTIVITY_TABLE")

# Create dataframe of features and predictions
df = pd.DataFrame(data, columns=["Date", "Dept", "Productivity", "Project"])

## Settings section
with st.sidebar:

    st.dataframe(df)
    
    st.title("Data Settings")

    # Filter data by the customer's probability of churn 
    threshold = st.slider('Set Churn Probability Threshold', 0.0, 1.0,(0.4, 0.8))

     # Filter by State
    states = st.multiselect("Select departments", df['Dept'].unique(), default=df['Dept'].unique())