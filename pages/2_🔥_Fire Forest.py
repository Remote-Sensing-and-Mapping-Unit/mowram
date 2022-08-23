import datetime
import ee
import streamlit as st
import geemap.foliumap as geemap
import os
import folium
from streamlit_folium import folium_static

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

st.title("FIRMS: Fire Information for Resources Management System")
st.markdown("The Earth Engine version of the Fire Information for Resource Management System (FIRMS) dataset contains the LANCE fire detection product in rasterized form. The near real-time (NRT) active fire locations are processed by LANCE using the standard MODIS MOD14/MYD14 Fire and Thermal Anomalies product. Each active fire location represents the centroid of a 1km pixel that is flagged by the algorithm as containing one or more fires within the pixel. The data are rasterized as follows: for each FIRMS active fire point, a 1km bounding box (BB) is defined; pixels in the MODIS sinusoidal projection that intersect the FIRMS BB are identified; if multiple FIRMS BBs intersect the same pixel, the one with higher confidence is retained; in case of a tie, the brighter one is retained. The data in the near-real-time dataset are not considered to be of science quality.")


Map = geemap.Map(locate_control=True)

col1, col2, col3, col4, col5= st.columns([1, 1, 1, 2, 2])
with col1:
    longitude = st.number_input("Longitude", 102, 110, 105)
with col2:
    latitude = st.number_input("Latitude", 10, 16, 12)
with col3:
    zoom = st.number_input("Zoom", 0, 20, 7)

Map.setCenter(longitude, latitude, zoom)

with col4:
    start = st.date_input("Start Date for Fire Forest: YYYY/MM/DD", datetime.date(2021, 1, 1))
with col5:
    end = st.date_input("End Date for Fire Forest: YYYY/MM/DD", datetime.date(2021, 1, 3))

start_date = start.strftime("%Y-%m-%d")
end_date = end.strftime("%Y-%m-%d")

countries=ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
country = countries.filter(ee.Filter.eq('country_na', 'Cambodia'));
esa = ee.ImageCollection("FIRMS").select('T21').filterBounds(country).filterDate(start_date,end_date).mosaic().clip(country)
esa_vis = {"min": 325,"max": 400,"palette": ['red', 'orange', 'yellow'],}
Map.addLayer(country,{}, name ="Cambodia Global Boundary")
Map.addLayer(esa, esa_vis, 'fire')

labels = ['Fire Detection']
colors = ['#FF0000']
Map.add_legend(
            title="Legend",
            labels=labels,
            colors=colors)

#for download image
# with open("image.jpg", "rb") as file:
#      btn = st.download_button(
#              label="Download image",
#              data=file,
#              file_name="image.jpg",
#              mime="image/png"
#            )
Map.add_child(folium.LatLngPopup())
# folium_static(Map)


Map.to_streamlit(height=550)
