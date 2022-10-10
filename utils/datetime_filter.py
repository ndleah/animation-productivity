import pandas as pd
import streamlit as st
import datetime
import re
import base64

def df_filter(message,df):

        ## Range selector
        format = 'YYYY MMM, DD'  # format output
        start_date = min(df['DATE']).strftime("%Y-%m-%d")
        end_date = max(df['DATE']).strftime("%Y-%m-%d")
        
        slider = st.slider('Select date', min_value=start_date, value=end_date ,max_value=end_date, format=format)
        return slider