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

import pickle
from pathlib import Path

import streamlit as st
import pandas as pd
import sys
from utils import chart, db
from streamlit.logger import get_logger
from datetime import datetime
import streamlit_authenticator as stauth  # pip install streamlit-authenticator

LOGGER = get_logger(__name__)


df = db.df
clist = list(df['DEPARTMENT_NAME'].unique())
metric_list= ["OVERHEADS_PER_PRODUCTIVE","ARTISTS","FILESIZE_PRODUCTIVITY","COUNT_PRODUCTIVITY","REVIEW_PRODUCTIVITY","AVG_WAITTIME"]
metric_labels = {
  "OVERHEADS_PER_PRODUCTIVE": "Overheads per Productive Hour", 
  "ARTISTS": "Average Daily Artists", 
  "FILESIZE_PRODUCTIVITY": "Filesize Productivity",
  "COUNT_PRODUCTIVITY": "Count Productivity",
  "REVIEW_PRODUCTIVITY": "Review Productivity",
  "AVG_WAITTIME": "Average Wait Time"}


def run():

  """
    Main function to run the whole program.
    Parameters
    ----------
    None
    Returns
    -------
    The main application contains 4 sections:
        1. Overall Information
        2. Numeric Columns Information
        3. Text Columns Information
        4. Datetime Columns Information
    """
  # --- USER AUTHENTICATION ---
    
  st.set_page_config(
  page_title="Productivity Dashboard!",
  page_icon=":bar_chart:",
  layout="wide")

  st.title("Productivity Dashboard! 📊")

  with st.expander("Metrics Description - Expand to read", expanded=False):

        st.markdown(
            """
            **🚀 Productivity:**
            * **`Total Review Value:`** The weighted value of reviews from submitted work. A Director review has a value of 1, internal review has a value of 0.75, and automated reviews have a vlue of 0.05.
            * **`File Size Change:`** The change in the file size from the last recorded entry. This approximates the magnitude of the work completed.
            * **`Total File Size:`** The total size of the file submitted. This approximates the work completed and the complexity of its context.
            * **`Normalised Productivity:`** This take the *File Size Chnage* and normalises by the peak productivity over the project ( % peak peak productivity). This should only be used after completion of the project.

            **👤 Overheads:**
            * **`Overhead Hours:`** Hours submitted with tasks: `td`,`meeting`,`prod`,`training`, or `supervision`. These indicate human hours with no direct value added to this project.
            * **`Productive Hours:`** Hours submitted that are not *Overhead Hours*
            * **`Overheads per Productive Hour:`** The number of *Overhead ours per Productive Hour*. This may identify inefficiencies where Overheads are high when not justified in business context.
            """
            )

        citation = "**Reference:** Transparent exploration of machine learning for biomarker discovery from proteomics and omics data\nFurkan M. Torun, Sebastian Virreira Winter, Sophia Doll, Felix M. Riese, Artem Vorobyev, Johannes B. Mueller-Reif, Philipp E. Geyer, Maximilian T. Strauss\nbioRxiv 2021.03.05.434053; doi: https://doi.org/10.1101/2021.03.05.434053"

        st.markdown(citation)

  
  # Layout (Sidebar)
  st.sidebar.image("img/Animal_Logic_logo.png", use_column_width=True)
  st.sidebar.markdown("## Data Settings")

  metric = st.sidebar.selectbox(label = "Choose a metric:", options = metric_list)
  
  st.sidebar.markdown('###')
  department_list = st.sidebar.multiselect('Select Departments:', clist,
                                  default=clist)
  st.sidebar.info("You selected: {}".format(", ".join(clist)))
  title = f"{metric_labels[metric]}"

  source = df[df['DEPARTMENT_NAME'].isin(department_list)]

  # Contents
  # There are 6 metrics in the final view: 
  line_chart = chart.build_metric(source, metric, title)

  # Display all the metrics
  st.altair_chart(line_chart, use_container_width=True)



if __name__ == "__main__":
  run()