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
from utils import chart, db,datetime_filter
from streamlit.logger import get_logger
import datetime

LOGGER = get_logger(__name__)
df = db.df

def run():
  st.set_page_config(
  page_title="Hello",
  page_icon="👋",
  initial_sidebar_state="expanded",
  menu_items={
      'Get Help': 'https://www.extremelycoolapp.com/help',
      'Report a bug': "https://www.extremelycoolapp.com/bug",
      'About': "# This is a header. This is an *extremely* cool app!"})

  st.write("# Welcome to Streamlit! 👋")

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

  st.title("Data Settings")

  # Filter by State
  department = st.multiselect("Select departments", df['DEPARTMENT_NAME'].unique(), default=df['DEPARTMENT_NAME'].unique())

  # Filter by Date
  # filtered_df = datetime_filter.df_filter('Move sliders to filter dataframe',df)

  # department = st.multiselect("Select project", df['project'].unique(), default=df['project'].unique())
  
  # There are 6 metrics in the final view: 
  # 1. Overheads per productive hour
  overhead_per_prod = chart.overhead_per_prod(df)

  # 2. average daily artists
  avg_daily_artists = chart.avg_daily_artists(df)

  # 3. filesize productivity (size of files submitted)
  filesize_productivity = chart.filesize_productivity(df)

  # 4. count productivity (number of files submitted including duplicate submissions)
  count_productivity = chart.count_productivity(df)

  # 5. review productivity (their old one)
  review_productivity = chart.review_productivity(df)

  # 6. average wait time
  avg_wait_time = chart.avg_wait_time(df)

  # Display all the metrics
  st.altair_chart(overhead_per_prod, use_container_width=True)
  st.altair_chart(avg_daily_artists, use_container_width=True)
  # st.altair_chart(filesize_productivity, use_container_width=True)
  st.altair_chart(count_productivity, use_container_width=True)
  st.altair_chart(review_productivity, use_container_width=True)
  st.altair_chart(avg_wait_time, use_container_width=True)



if __name__ == "__main__":
  run()