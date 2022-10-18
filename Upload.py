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

import streamlit as st
import os
from streamlit.logger import get_logger
import pandas as pd
from utils import get_utc

try:
  os.remove("bb")
  os.remove("client_load")
except:
  pass

def preview(profile):
  vals = pd.read_csv(f"data/{profile}.csv")
  data = pd.concat([d_utc, vals], axis=1)
  #st.write(data)
  st.line_chart(data=data.sample(frac=0.1), x="date_utc",y=profile)

client_an_load = None
st.set_page_config(
    page_title="PowerMatch",
    page_icon="⚡")


path = os.path.dirname(__file__)

st.write("# Welcome to PowerMatch ⚡")

with st.sidebar:
  st.image('assets/tinder.png', width=60)

prev = st.radio("Enable Preview", ["Yes", "No"], horizontal=True, index=0)
cl_mapping = {"Data Center":"C01", "Chemical Plant":"C04", "Retail":"C07", "other":"Client"}
client = st.radio("Tell Us Who You Are:", ["Data Center", "Chemical Plant", "Retail", "other"],horizontal=True, index=3)
if client != "other":
  with open("bb", "w") as bb:
    bb.write(cl_mapping[client])
  d_utc = get_utc()
  st.sidebar.success(f"{client} Chosen" )
  if prev == "Yes":
    if client == "Data Center":
      preview("C01")
    if client == "Chemical Plant":
      preview("C04")
    else:
        preview("C07")
else:
  st.file_uploader("Upload Load Profile")


with st.form("my_form"):
   input = st.text_input("Enter your total annual load in MW/h")


   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
      with open("client_load", "w") as bb:
        bb.write(input)
      st.success("Load Submitted")  

 
#col1, col2, col3= st.columns(3)

# LOGGER = get_logger(__name__)
# col1, mid, col2 = st.sidebar.columns([1,5,20])
# path = os.path.dirname(__file__)
# with col1:
#   st.image(path+'tinder.png', width=40)
# with col2:
#   st.header('PowerMatch')




