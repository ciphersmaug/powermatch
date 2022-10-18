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
import inspect
import textwrap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))

def transform_yearly_load(load_profile, yearly_client):
    
    """ Based on the yearly consumption of the client (yearly_client) 
    the chosen load profile (load_profile) is scaled up."""
    
    profile_sum = load_profile.values.sum()
    proportion = yearly_client/profile_sum
    return load_profile.values * proportion *100

def profile_similarity(client, community, feature = "value"):
    
    """ Computes correlation between client and community profile based on the chosen feature column."""
    
    client = client.rename(columns={feature:f"{feature}_1"})
    community = community.rename(columns={feature:f"{feature}_2"})
    df = pd.concat([client[f"{feature}_1"], community[f"{feature}_2"]], axis = 1, ignore_index = True)
    #print(df)
    corr = df.corr(method="spearman")
    return corr.iloc[0][1]

def get_assets(community):
    
    """ Returns proportion of community members that have trading assets."""
    
    assets = community.assets[0]
    return assets

def get_average_for_community(client, community, client_load = "C01", feature ="value"):
    #TODO: Test new np.mean()
    
    """ Returns average electricity price / CO2 emissions (depending on chosen feature)
    for a load profile within a specific community."""
    
    all_prices = client[client_load] * community[feature]
    return np.mean(all_prices)

def get_n_correlated(corr:pd.DataFrame, column:str, n:int = 1,most_correlated:bool=True):
    return list(corr[column].sort_values (ascending=not(most_correlated))[1:1+n].index)
def visualize_n_correlated(df,column,n,most_correlated=True):
    corr = df.corr(method="spearman")
    df[[column]+get_n_correlated(corr,column,n,most_correlated)].plot(figsize=(20,10))

@st.cache
def get_utc():
    df = pd.read_csv("data/aggregation_af.csv")
    return df["date_utc"]

def ampel(value, feature, threshold1, threshold2, inv=False):
 
    col1, col2,col3 = st.columns(3)
    if inv:

        with col1:
            if np.abs(value) >= threshold1:
                st.image("assets/red.png", width=20)      
            elif np.abs(value) >= threshold2:
                st.image("assets/yellow.png", width=20)
            else:
                st.image("assets/green.png", width=20)   
                
        with col2:
            st.write(value)
        with col3:
            st.write(feature)
    else:

        with col1:
            if np.abs(value) >= threshold1:
                st.image("assets/green.png", width=20)   
            elif np.abs(value) >= threshold2:
                st.image("assets/yellow.png", width=20)
            else:
                st.image("assets/red.png", width=20)
        with col2:
            st.write(value)
        with col3:
            st.write(feature)



    


