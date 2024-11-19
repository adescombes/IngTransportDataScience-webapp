import geopandas as gpd
import numpy as np
import io
import osmnx as ox
from pandasql import sqldf
from shapely.geometry import Polygon
import streamlit as st
from streamlit_keplergl import keplergl_static
import keplergl as kp
from geovelo_sql_queries import *
from helpers import *
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import contextlib


def save_geojson_with_bytesio(dataframe):
    # Function to return bytesIO of the geojson
    shp = io.BytesIO()
    dataframe.to_file(shp, driver="GeoJSON")
    return shp


st.set_page_config(layout="wide")
path_cache = "~/Downloads/infra_cyclables.json"


st.write("Dessiner une zone :")
m = folium.Map(location=[46.51, 6.63], zoom_start=12)
draw = Draw(export=False).add_to(m)

output = st_folium(m, width=800, height=500)
step = 0

with st.form("user_input"):

    submitter = st.form_submit_button("c'est parti")

    if submitter:

        col1, col2 = st.columns(2)

        with col1:
            # MAP

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

            osm_data_gpd.set_geometry("geometry")
            osm_data_gpd.to_file(path_cache, driver="GeoJSON")

            kepler_map = kp.KeplerGl(height=800)

            for info in osm_data_gpd["info"].unique():
                layer = osm_data_gpd[osm_data_gpd["info"] == info]
                kepler_map.add_data(data=layer, name=info)

            keplergl_static(kepler_map, center_map=True)

        with col2:

            # PLOTS
            total_length = osm_data_gpd["length_line"].sum()

            # on compte les longueurs x2 lorsque les aménagements
            # # sont présents des 2 côtés de la route
            osm_data_gpd["% linéaire"] = osm_data_gpd["length_line"].apply(
                lambda x: np.round(100 * x / total_length, 1)
            )
            osm_data_gpd.rename(columns={"info": "infrastructure"}, inplace=True)
            df_groupped = (
                osm_data_gpd[["infrastructure", "% linéaire"]]
                .groupby("infrastructure")
                .sum()
            ).reset_index()

            df_groupped = df_groupped[
                df_groupped["infrastructure"] != "0"
            ]  # on enlève tous les "autres"
            df_groupped = df_groupped.sort_values(by="% linéaire")
            df_groupped = df_groupped[df_groupped["infrastructure"] != "NaN"]

            st.bar_chart(
                data=df_groupped,
                x="infrastructure",
                y="% linéaire",
                x_label="%"
                + " linéaire (total = %.1f km de voies)" % (total_length / 1000),
                y_label="type d'infrastructure",
                horizontal=True,
                height=600,
            )
            step = 1

try:
    gdf = gpd.read_file(path_cache)

    # download the geodataframe
    st.download_button(
        label="Download data",
        data=save_geojson_with_bytesio(gdf),
        file_name="infra_cyclables.geojson",
        mime="application/geo+json",
    )


except:
    pass

# if cache still exists, delete it
with contextlib.suppress(FileNotFoundError):
    os.remove(path_cache)
