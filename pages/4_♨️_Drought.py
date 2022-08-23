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
    This is an application for Near Real Time Drought Information Hub
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    heng.bauran@gmail.com
    """
)

st.title("Drought: KBDI: Keetch-Byram Drought Index")
st.markdown("Keetch-Byram Drought Index (KBDI) is a continuous reference scale for estimating the dryness of the soil and duff layers. The index increases for each day without rain (the amount of increase depends on the daily high temperature) and decreases when it rains. This system is based primarily on recent rainfall patterns. It is a measure of meteorological drought; it reflects water gain or loss within the soil.The scale ranges from 0 (no moisture deficit) to 800 (extreme drought). The range of the index is determined by assuming that there is 20 cm of moisture in a saturated soil that is readily available to the vegetation (Keetch and Byram, 1968). KBDI is world widely used for drought monitoring for national weather forecast, wildfire prevention and usefully especially in regions with rain-fed crops.")

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
    start = st.date_input("Start Date for Drought Filter: YYYY/MM/DD", datetime.date(2022, 7, 1))
with col5:
    end = st.date_input("End Date for Drought Filter: YYYY/MM/DD", datetime.date(2022, 7, 2))

start_date = start.strftime("%Y-%m-%d")
end_date = end.strftime("%Y-%m-%d")

countries=ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
country = countries.filter(ee.Filter.eq('country_na', 'Cambodia'));

dataset = ee.ImageCollection('UTOKYO/WTLAB/KBDI/v1').select('KBDI').filterBounds(country).sort('dateDist').filterDate(start_date,end_date).mosaic().clip(country)

bandViz = {
  'min': 0,
  'max': 800,
  'palette': ['001a4d', '003cb3', '80aaff', '336600', 'cccc00', 'cc9900', 'cc6600',
    '660033'
  ]
};
colors= bandViz["palette"]
Map.addLayer(country,{}, name ="Cambodia Global Boundary")
Map.addLayer(dataset, bandViz, 'Drought Index', True, 1)

# Map.add_colorbar(colors, 0, 1, caption="Modis")
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
