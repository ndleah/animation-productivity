import sys
import snowflake.connector
import streamlit as st
import os
# from constant import user, password, account, warehouse, database, schema

@st.experimental_singleton
def init_connection():
  return snowflake.connector.connect(
    user = 'NDLEAH',
    password = 'Anhmeu@123',
    account = 'YX47125.australia-east.azure',
    warehouse = 'COMPUTE_WH',
    database = 'ILAB_DATABASE',
    schema = 'DATAMART'
    )
  
conn = init_connection()

# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
  with conn.cursor() as cur:
    cur.execute(query)
    return cur.fetchall()


# Query Snowflake for features and predictions
data = run_query("SELECT * FROM COMBINED_DATA")