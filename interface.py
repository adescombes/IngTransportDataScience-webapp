import geopandas as gpd
import numpy as np
import os
import sys
import osmnx as ox
import pandas as pd
from pandasql import sqldf
from pathlib import Path
from pyproj import Transformer
import re
import shapely
from shapely.geometry import Polygon
from shapely.validation import make_valid
import streamlit as st
from streamlit_keplergl import keplergl_static
import keplergl as kp
from unidecode import unidecode

from geovelo_sql_queries import *
from helpers import *

st.set_page_config(layout="wide")

import folium
from folium.plugins import Draw
from streamlit_folium import st_folium


with st.form("user_input"):

    st.write("Sélectionner une commune :")

    m = folium.Map(location=[46.95, 7.45], zoom_start=9)
    draw = Draw(export=True).add_to(m)

    draw

    c1, c2 = st.columns(2)

    with c1:

        output = st_folium(m, width=700, height=700)
        submitter = st.form_submit_button("zé parti")

    if submitter:

        with c2:

            drawn_geometry = (
                output.get("last_active_drawing").get("geometry").get("coordinates")[0]
            )

            polygon = Polygon(drawn_geometry)

            queries_sql = queries

            osm_data = ox.features.features_from_polygon(polygon, tags_of_interest)

            line = osm_data.loc[["way"]].reset_index()
            line = line[
                line.geometry.geom_type == "LineString"
            ].reset_index()  # only the line geometries

            line.crs = "EPSG:4326"
            line = line.to_crs(2056)
            line["length_line"] = line.length
            line.set_index("osmid", inplace=True)

            sql_df = line.drop("geometry", axis=1)
            try:
                sql_df.drop(columns="FIXME", inplace=True)
            except:
                print("FIXME column not found")

            sql_df_str = sql_df.map(str)
            q = "SELECT * FROM sql_df_str"
            pysqldf = lambda q: sqldf(q, globals())
            osmid_bike_type = [
                pysqldf("""SELECT osmid FROM sql_df_str WHERE """ + q).osmid
                for q in queries_sql
            ]
            line_gpd_clipped = organise_df_with_SQLqueries(osmid_bike_type, line)

            osm_data_gpd = gpd.GeoDataFrame(
                line_gpd_clipped, geometry=line_gpd_clipped.geometry
            ).fillna("NaN")

            osm_data_gpd.to_csv("osm_data_gpd.csv")

            osm_data_gpd.set_geometry("geometry")

            kepler_map = kp.KeplerGl(height=800)

            for info in osm_data_gpd["info"].unique():
                layer = osm_data_gpd[osm_data_gpd["info"] == info]
                kepler_map.add_data(data=layer, name=info)

            keplergl_static(kepler_map, center_map=True)
