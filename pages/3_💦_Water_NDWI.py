import datetime
import ee
import streamlit as st
import geemap.foliumap as geemap
import os
import folium
from streamlit_folium import folium_static
import geemap.foliumap as geemap

st.set_page_config(initial_sidebar_state="collapsed",layout="wide")

st.sidebar.title("About")
st.sidebar.info(
    """
    This is an application for Near Real Time Fire Information Hub
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    heng.bauran@gmail.com
    """
)

st.title("Water: MODIS Terra Daily NDWI")
st.markdown("The Normalized Difference Water Index (NDWI) is sensitive to changes in liquid water content of vegetation canopies. It is derived from the Near-IR band and a second IR band, ≈1.24μm when available and the nearest available IR band otherwise. It ranges in value from -1.0 to 1.0. See Gao (1996) for details. This product is generated from the MODIS/006/MOD09GA surface reflectance composites. Modis Terra of default Color Code with ['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff'] is classified from 0 to 1")

# def app():

#     st.title("Change layer opacity")

#     col1, _, col2, _ = st.columns([1, 0.3, 2, 2])

#     with col1:
#         layer = st.selectbox("Select a layer", ["Cambodia Global Boundary", "water"])

#     with col2:
#         opacity = st.slider(
#             "Opacity", min_value=0.0, max_value=1.0, value=0.8, step=0.05
#         )

Map = geemap.Map(locate_control=True)

col1, col2, col3, col4, col5= st.columns([1, 1, 1, 2, 2])
with col2:
    longitude = st.number_input("Longitude", 102, 110, 105)
with col1:
    latitude = st.number_input("Latitude", 10, 16, 12)
with col3:
    zoom = st.number_input("Zoom", 0, 20, 7)

Map.setCenter(longitude, latitude, zoom)

with col4:
    start = st.date_input("Start Date for Water Filter: YYYY/MM/DD", datetime.date(2022, 7, 1))
with col5:
    end = st.date_input("End Date for Water Filter: YYYY/MM/DD", datetime.date(2022, 7, 2))

start_date = start.strftime("%Y-%m-%d")
end_date = end.strftime("%Y-%m-%d")

countries=ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
country = countries.filter(ee.Filter.eq('country_na', 'Cambodia'));

dataset = ee.ImageCollection("MODIS/MOD09GA_006_NDWI").select('NDWI').filterBounds(country).filterDate(start_date,end_date).mosaic().clip(country)

vis_params = {
    'min': 0,
    'max': 1,
    'palette': ['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff'],
    }
colors= vis_params["palette"]
Map.addLayer(country,{}, name ="Cambodia Global Boundary")
Map.addLayer(dataset, vis_params, 'water', True, 1)

# Map.add_colorbar(colors, caption="Modis")
Map.add_child(folium.LatLngPopup())

#for download image
# with open("image.jpg", "rb") as file:
#      btn = st.download_button(
#              label="Download image",
#              data=file ,
#              file_name="image.jpg",
#              mime="image/png"
#            )

Map.to_streamlit(height=550)
