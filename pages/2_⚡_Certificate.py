from json import tool
import pandas as pd
import pydeck as pdk
import streamlit as st
from utils import *

st.write("# Become a PowerMatch Ambassador!")

with st.sidebar:
  st.image('assets/tinder.png', width=60)

st.image("assets/badge.png",width =280)
st.download_button("Download your certificate here","assets/green.png")