import streamlit as st
import leafmap
import leafmap.foliumap as leafmap
import folium.plugins as plugins
import folium
from gsheetsdb import connect
import geopandas as gpd
import pandas as pd
import os

st.set_page_config(initial_sidebar_state="collapsed",layout="wide")


# Customize page title
st.title("Welcome to Geospatial App")

st.markdown(
    """
    This application is for Earth Observation
    """
)

