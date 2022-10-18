from json import tool
import pandas as pd
import pydeck as pdk
import streamlit as st
from utils import *
### https://pydeck.gl/gallery/path_layer.html
### order of nodes must be lon lat

# read nodes from csv
nodes = pd.read_csv('grid_layout/nodes.csv')
# specify german nodes -> Umspannwerke
DE_nodes = ['Altenfeld', 'Bentwisch', 'Dresden-Sued', 'Hamburg-Sued', 'Reuter', 'Wolkramshausen']

# calculate the starting view of the map, picture is focused on this point
# is the middle of all german nodes

starting_view_de = nodes.loc[nodes['name'].isin(DE_nodes)]
starting_view_de_coord = starting_view_de[['lat', 'lon']].mean()

initial_view_state = pdk.ViewState(
    latitude=starting_view_de_coord.lat,
    longitude=starting_view_de_coord.lon,
    zoom=3,
    pitch=20)

# filter nodes to only keep neighboring countries
neighboring_nodes = nodes.loc[~nodes['name'].isin(DE_nodes)]

# read interconnectors from json (json is recommended, csv files will add quotation marks)
interconnectors = pd.read_json('grid_layout/interconnectors.json')

# read de grid paths from json
de_grid = pd.read_json('grid_layout/de_grid.json')

# create layer for map with interconnectors
interconnectors_paths = pdk.Layer(
    type="PathLayer",
    data=interconnectors,
    pickable=True,
    get_color=[255, 100, 100, 100],
    width_scale=20,
    width_min_pixels=10,
    get_path='path',
    get_width=5,
)

# layer for the german grid
de_grid_path = pdk.Layer(
    type="PathLayer",
    data=de_grid,
    pickable=True,
    get_color=[255, 100, 100, 100],
    width_scale=20,
    width_min_pixels=10,
    get_path='path',
    get_width=5,
)

# substations on the plot
nodes_de = pdk.Layer(
    "ScatterplotLayer",
    starting_view_de,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=10,
    radius_max_pixels=15,
    line_width_min_pixels=1,
    get_position=['lon', 'lat'],
    get_fill_color=[255, 0, 0],
    get_line_color=[0, 0, 0],
)

nodes_neighbors = pdk.Layer("ScatterplotLayer",
          neighboring_nodes,
          pickable=True,
          opacity=0.8,
          stroked=True,
          filled=True,
          radius_scale=6,
          radius_min_pixels=15,
          radius_max_pixels=15,
          line_width_min_pixels=1,
          get_position=['lon', 'lat'],
          get_fill_color=[0, 255, 0],
          get_line_color=[0, 0, 0],
)
def show_map():
    st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=starting_view_de_coord.lat,
        longitude=starting_view_de_coord.lon,
        zoom=4,
        pitch=20,
        
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data = starting_view_de,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=10,
            radius_max_pixels=15,
            line_width_min_pixels=1,
            get_position=['lon', 'lat'],
            get_fill_color=[255, 0, 0],
            get_line_color=[0, 0, 0]),
        pdk.Layer(
            "ScatterplotLayer",
            neighboring_nodes,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=15,
            radius_max_pixels=15,
            line_width_min_pixels=1,
            get_position=['lon', 'lat'],
            get_fill_color=[0, 255, 0],
            get_line_color=[0, 0, 0]),
        pdk.Layer(
            type="PathLayer",
            data=de_grid,
            pickable=True,
            get_color=[255, 100, 100, 100],
            width_scale=20,
            width_min_pixels=10,
            get_path='path',
            get_width=5),
        pdk.Layer(
            type="PathLayer",
            data=interconnectors,
            pickable=True,
            get_color=[255, 100, 100, 100],
            width_scale=20,
            width_min_pixels=10,
            get_path='path',
            get_width=5),
        pdk.Layer(
            type='TextLayer',
            id='text-layer',
            data=starting_view_de,
            pickable=True,
            opacity=1,
            get_position=['lon', 'lat'],
            get_text='name',
            get_color=[0,0,0,255],
            billboard=False,
            get_size=18,
            get_angle=0,
            # Note that string constants in pydeck are explicitly passed as strings
            # This distinguishes them from columns in a data set
            get_text_anchor='"middle"',
            get_alignment_baseline='"center"'
        )
        
    ],
#     tooltip={
#    "html": "<b>Select Substation in Dropdown</b>",
#    "style": {
#         "backgroundColor": "steelblue",
#         "color": "white"
#    }
# }
    ))

abbr = {'Altenfeld': 'af', 'Bentwisch':'bt', 'Dresden-Sued':'dr', 'Hamburg-Sued':'hh', 'Reuter':'rt', 'Wolkramshausen':'wk'}
st.set_page_config(page_title="Power Grid", page_icon="🌍")
st.markdown("# Power Grid")
st.sidebar.header("Power Grid")
node = st.sidebar.selectbox('Select Substation', DE_nodes, index =1)

with st.sidebar:
    prios = st.multiselect("Select Criteria of Interest", ["Price","Trading Opportunities" ,"Flexibility", "Security", "CO2 Emissions"])
    if "Price" in prios:
        st.warning("Prices are approximations obtained through data driven methods")


try:
    with open("bb","r") as bb:
        client = bb.read()
    with open("client_load","r") as cl:
        cal = cl.read()
    client_load= pd.read_csv(f"data/{client}.csv")
    cal =  int(cal)
    client_load[client] = transform_yearly_load(client_load,cal)
    loaded = True
except:
    loaded = False



#st.write(client_load)
show_map()

data = pd.read_csv(f"data/aggregation_{abbr[node]}.csv")
tab1, tab2, tab3, tab4 = st.tabs(["Load Profile", "Criteria", "Price Curve", "CO2 Curve"])

with tab1:
   st.header("Load Profile")
   if loaded:
    df_plt = pd.concat([data, client_load], axis=1)
    st.line_chart(data=df_plt.sample(frac=0.1),x="date_utc", y=["value", client], width=0, height=0, use_container_width=True)
   else:
    st.warning("No profile uploaded!")
    st.line_chart(data=data.sample(frac=0.1),x="date_utc", y=["value"], width=0, height=0, use_container_width=True)

with tab2:
    st.header("Indicator Scores")
    prio_dict = {}
    th1 = 0.8
    th2 = 0.4
    df = pd.read_csv(f"data/aggregation_{abbr[node]}.csv")
    if len(prios) == 0:
        st.warning("Select a Criterion")
    if "Flexibility" in prios:
            cl = client_load.rename(columns={client:"value"})
            sim = profile_similarity(cl, df, feature = "value")
            th1 = 0.8
            th2 = 0.4
            ampel(sim, "Flexibility", th1, th2)
    if "Trading Opportunities" in prios:
        value = get_assets(df)
        th2 = 0.2
        prio_dict["Trading Opportunities"]= value     
        #CO2
        ampel(value, "Trading Opportunities", th1, th2)
    if "Security" in prios:
        cl = client_load.rename(columns={client:"value"})
        sim = profile_similarity(cl, df, feature = "value")
        th1 = 0.8
        th2 = 0.4
        ampel(sim, "Security", th1, th2)
    if "Price" in prios:
        prices = pd.read_csv("data/prices_per_node_average_last_year.csv")
        max = prices["value"].max()
        min = prices["value"].min()
        relev = prices.loc[prices.name == node].iloc[0]["value"]
        th1 = min + (max-min)*0.5
        th2 = min + (max-min)*0.8
        ampel(relev, "Prices", th1, th2, inv = True)
    if "CO2 Emissions" in prios:
        prices = pd.read_csv("data/green_nodes_average_last_year.csv")
        max = prices["value"].max()
        min = prices["value"].min()
        relev = prices.loc[prices.name == node].iloc[0]["value"]
        th1 = min + (max-min)*0.5
        th2 = min + (max-min)*0.8
        ampel(relev, "CO2 Emissions", th1, th2, inv = True)
   
        
   

with tab3:
    st.header("Price Curve")
    prices = pd.read_csv(f"data/prices_{abbr[node]}.csv")["nodal_prices"]
    d_utc = get_utc()
    data = pd.concat([prices, d_utc],axis=1)
    st.line_chart(data=data.sample(frac=0.1),x="date_utc", y="nodal_prices", width=0, height=0, use_container_width=True)

with tab4:
    st.header("CO2 Curve")
    em = pd.read_csv(f"data/emissions_for_{abbr[node]}.csv")["relative_co2_emission_factor"]
    data2 = pd.concat([em, d_utc],axis=1)
    st.line_chart(data=data2.sample(frac=0.1),x="date_utc", y="relative_co2_emission_factor", width=0, height=0, use_container_width=True)