import secrets
import sys
import snowflake.connector
import streamlit as st
import os
import pandas as pd
from datetime import date

# from constant import user, password, account, warehouse, database, schema

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
data = run_query("SELECT * FROM V_DATA_EXPORT")

# Create dataframe of features and predictions
df = pd.DataFrame(data, columns=["DATE", "DEPARTMENT_NAME", "PRODUCTIVE_HOURS", "OVERHEAD_HOURS", "TOTAL_HOURS", "OVERHEADS_PER_PRODUCTIVE", "ARTISTS", "FILSESIZE_PRODUCTIVITY", "COUNT_PRODUCTIVITY", "REVIEW_PRODUCTIVITY", "AVG_WAITTIME"])

# using dictionary to convert specific columns
convert_dict = {'DATE':str,
                'DEPARTMENT_NAME': str,
                'PRODUCTIVE_HOURS': int,
                'OVERHEAD_HOURS': float,
                'TOTAL_HOURS': float,
                'OVERHEADS_PER_PRODUCTIVE': float,
                'ARTISTS': float,
                'FILSESIZE_PRODUCTIVITY': float,
                'COUNT_PRODUCTIVITY': float,
                'REVIEW_PRODUCTIVITY': float,
                'AVG_WAITTIME': float
                }

df = df.astype(convert_dict)

# convert the 'Date' column to datetime format
df['DATE']= pd.to_datetime(df['DATE'])

