# Import required libraries
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd


st.set_page_config(
     page_title="AnimalLogic Productivity dashboard",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This is an *extremely* cool app powered by Snowpark for Python, Streamlit, and Snowflake Data Marketplace"
     }
)

# Create Session object
def create_session_object():
   connection_parameters = {
      "account": "YX47125.australia-east.azure",
      "user": "NDLEAH",
      "password": "Anhmeu@123",
      "role": "ACCOUNTADMIN",
      "warehouse": "COMPUTE_WH",
      "database": "ANIMAL_LOGIC",
      "schema": "PUBLIC"
   }
   session = Session.builder.configs(connection_parameters).create()
   print(session.sql('select current_warehouse(), current_database(), current_schema()').collect())
   return session

   # Create Snowpark DataFrames that loads data from Knoema: Environmental Data Atlas
def load_data(session):
    productivity_df = session.table("PUBLIC.FINAL_PRODUCTIVITY_TABLE")
    
    # Convert Snowpark DataFrames to Pandas DataFrames for Streamlit
    productivity_df  = productivity_df.to_pandas()
    
    # Add header and a subheader
    st.header("Knoema: Environment Data Atlas")
    st.subheader("Powered by Snowpark for Python and Snowflake Data Marketplace | Made with Streamlit")
    
 # Display an interactive chart to visualize CO2 Emissions by Top N Countries
    with st.container():
        st.subheader('CO2 Emissions by Top N Countries')
        with st.expander(""):
            st.bar_chart(data=productivity_df.set_index('dept'), width=850, height=500, use_container_width=True)


if __name__ == "__main__":
    session = create_session_object()
    load_data(session)