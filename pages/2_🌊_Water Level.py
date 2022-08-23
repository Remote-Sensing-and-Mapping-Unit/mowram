import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data
from gsheetsdb import connect
import itertools

import streamlit as st
from vega_datasets import data
import pandas as pd
import numpy as np

st.set_page_config(initial_sidebar_state="collapsed",layout="wide")

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
# @st.cache(ttl=600)
st.experimental_memo(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

#sample plot
# df =  pd.DataFrame(rows)
# line = alt.Chart(rows).mark_line().encode(
#     x = 'date',
#     y = 'Pakse22'
# ).properties(width = 650, height = 500, title = "Line Plot").interactive()
# st.altair_chart(line)



source = pd.DataFrame(rows)

# Define the base time-series chart.
def get_chart(source):
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(source, title="Water Level (m) for Pakse Station")
        .mark_line()
        .encode(
            x=alt.X("Date:O", title="Date in DD/MM "),
            y=alt.Y("WL", title= "Water Level in meter"),
            color="Year",
            # strokeDash="Year",
        )
    )

    bar = alt.Chart(source).mark_bar().encode(y="Pakse22")
    # band = alt.Chart(source).mark_errorband(extent='ci').encode(
    # x='Date',
    # y=alt.Y('WL', title='Water Level'),
    # )

#     # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

#     # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(source)
        .mark_rule()
        .encode(
            x="Date",
            y="WL",
            opacity=alt.condition(hover, alt.value(0.9), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("WL", title="Water Level"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips ).interactive()

chart = get_chart(source)


# # Add annotations
# ANNOTATIONS = [
#     ("Mar 01, 2008", "Pretty good day for GOOG"),
#     ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"),
#     ("Nov 01, 2008", "Market starts again thanks to..."),
#     ("Dec 01, 2009", "Small crash for GOOG after..."),
# ]
# annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
# annotations_df.date = pd.to_datetime(annotations_df.date)
# annotations_df["y"] = 10
# annotation_layer = (
#     alt.Chart(annotations_df)
#     .mark_text(size=20, text="⬇", dx=-8, dy=-10, align="left")
#     .encode(
#         x="date:T",
#         y=alt.Y("y:Q"),
#         tooltip=["event"],
#     )
#     .interactive()
# )
st.altair_chart(
    (chart ).interactive(),
    use_container_width=True
)