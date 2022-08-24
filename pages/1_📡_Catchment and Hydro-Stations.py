from ast import With
import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
st.sidebar.title("About")
st.sidebar.info(
    """
    This is an application for Near Real Time Water Resources Information Hub (NEWRIH)
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    heng.bauran@gmail.com
    """
)

#for color of title
new_title = '<p style="font-family:Impact; border-radius:5px;color:white;padding-left:17px; background-image: linear-gradient(to right, green, yellow); font-size: 42px;opacity:0.8;">Catchment & Hydro Stations in Cambodia</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.file_uploader('Upload your file')

col1, col2, col3= st.columns([3, 3, 1])
with col1:
    lat = st.text_input("Latitude", " 12")
with col2:
    lng = st.text_input("Longitude", "105")
with col3:
    zoom = st.text_input("Zoom", "7")

m = leafmap.Map(center=[float(lat), float(lng)],
    zoom=int(zoom),
    locate_control=True)
m.add_basemap("HYBRID")
m.add_basemap("SATTELITE")
m.add_basemap("Esri.NatGeoWorldMap")


hydro = '/data/hydrostation1.csv'
cambodia = '/data/cambodia.geojson'
catchment='https://raw.githubusercontent.com/yputhealy/mowram/main/data/catchment.geojson'

# m.add_geojson(cambodia,layer_name='Cambodia Province')
m.add_geojson(catchment,layer_name='Cambodia Catchment')
m.add_data(
    catchment,
    column='areakm',
    scheme='EqualInterval',
    cmap='Blues',
    legend_title='Area in Square Kilometers',
    layer_name= "Choropleth Map Layer"
)
m.add_points_from_xy(
            hydro,
            x="Latitude",
            y="Longitude",
            # color_column='Name',
            # icon_names=['gear', 'map', 'leaf', 'globe','fa-star', 'fa-star-o',
            # 'fa-star-half','fa-tags','fa-tag', 'fa-tint', 'fa-search',],
            # spin=True,
            #add_legend=True,
            layer_name="Hydro Station"
        )
m.add_labels(
    catchment,
    "Name",
    font_size="4pt",
    font_color="blue",
    font_family="arial",
    font_weight="bold",
    layer_name= "Label"
)

#add color bar
# colors = ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
# vmin = 0
# vmax = 4000
# m.add_colorbar(colors=colors, vmin=vmin, vmax=vmax)

m.to_streamlit(height=700)
