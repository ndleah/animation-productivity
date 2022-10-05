# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Import required libraries
import streamlit as st
import pandas as pd
import sys
from utils import chart, db
import logging

LOGGER = logging.getLogger(__name__)

def run():
  st.set_page_config(page_title="Customer Churn Dashboard",
  layout="wide")

  st.markdown(
          """
          Streamlit is an open-source app framework built specifically for
          Machine Learning and Data Science projects.
          **👈 Select a demo from the sidebar** to see some examples
          of what Streamlit can do!
          ### Want to learn more?
          - Check out [streamlit.io](https://streamlit.io)
          - Jump into our [documentation](https://docs.streamlit.io)
          - Ask a question in our [community
            forums](https://discuss.streamlit.io)
          ### See more complex demos
          - Use a neural net to [analyze the Udacity Self-driving Car Image
            Dataset](https://github.com/streamlit/demo-self-driving)
          - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
      """
      )



  # Create dataframe of features and predictions
  df = pd.DataFrame(db.data, columns=["WEEK", "DEPARTMENT", "WEIGHTED_OUTPUT", "DAYS_LOGGED", "WEIGHTED_OUTPUT_MOD", "DAYS_LOGGED_MOD", "WEIGHTED_OUTPUT_MOVING_AVERAGE", "DAYS_LOGGED_MOD_MOVING_AVERAGE", "HUMAN_EFFICIENCY"])
  
  # Filter by State
  department = st.multiselect("Select departments", df['DEPARTMENT'].unique(), default=df['DEPARTMENT'].unique())
  # department = st.multiselect("Select project", df['project'].unique(), default=df['project'].unique())
  
  chart_display = chart.get_chart(df)
  st.altair_chart(chart_display, use_container_width=True)

  st.title("Data Settings")

  

if __name__ == "__main__":
    run()