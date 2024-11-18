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
import streamlit as st
from streamlit_keplergl import keplergl_static
import keplergl as kp
from unidecode import unidecode

from geovelo_sql_queries import *
from helpers import *

st.set_page_config(layout="wide")

path_data = "./data"

communes = gpd.read_file(
    os.path.join(path_data, "CH_communes_et_codes_postaux_agreg_centroides_4326.gpkg")
)
communes.set_geometry("geometry")

# FORM -> permet d'attendre un user input pour exécuter l'analyse

with st.form("user_input"):

    st.write("Sélectionner une commune :")

    location = st.selectbox(label="Commune", options=communes["NAME"])

    submitter = st.form_submit_button("zé parti")

    col1, col2 = st.columns(2)

    if submitter:

        commune_infos = communes[communes["NAME"] == location].reset_index()

        coords = (commune_infos["ycoord"], commune_infos["xcoord"])

        geometry = commune_infos["geometry"][0]

        queries_sql = queries

        # définition des grands groupes composant le réseau routier
        road = [
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",
            "unclassified",
            "residential",
        ]
        road_link = [
            "motorway_link",
            "trunk_link",
            "primary_link",
            "secondary_link",
            "tertiary_link",
        ]
        network_n = road + road_link
        highway = (
            road
            + road_link
            + [
                "living_street",
                "busway",
                "cycleway",
                "service",
                "pedestrian",
                "track",
                "path",
                "footway",
                "steps",
            ]
        )

        # définition des tags
        tags_of_interest = {
            "aerialway": ["bicycle"],
            "bicycle": ["conditional", "parking", "convenience", "road", "clothes"],
            "capacity": ["bicycle", "cargo_bike"],
            "cycleway": [
                "left",
                "right",
                "both",
                "lane",
                "share_busway",
                "track",
                "opposite_track",
                "shared_lane",
                "right:oneway",
                "left:oneway",
            ],
            "highway": highway,
            "junction": ["roundabout", "circular"],
            "maxspeed": ["20", "30", "50", "80", "100"],
            "network": ["icn", "lcn", "ncn"],
            "distance": ["*"],
            "route": ["bicycle", "mtb"],
        }

        osm_data = ox.features.features_from_polygon(geometry, tags_of_interest)

        line = osm_data.loc[["way"]].reset_index()
        line = line[
            line.geometry.geom_type == "LineString"
        ].reset_index()  # only the line geometry
        # set the crs for both dataset
        line.crs = "EPSG:4326"  # defini un crs à notre jeu de donnée correspondant à ce quon voit au dessus
        line = line.to_crs(2056)  # change le crs pour correspondre à la suisse
        line["length_line"] = line.length  # calcul la longueur
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

        # COLONNE GAUCHE -> MAP
        with col1:

            kepler_map.add_data(data=commune_infos, name="commune")

            keplergl_static(kepler_map, center_map=True)

        # COLONNE DROITE -> BARPLOT
        with col2:

            total_length = osm_data_gpd["length_line"].sum()

            # on compte les longueurs x2 lorsque les aménagements
            # # sont présents des 2 côtés de la route
            osm_data_gpd["infra_prct"] = osm_data_gpd[
                "length_line_onewaycounted_wholenetwork"
            ].apply(lambda x: np.round(100 * x / total_length, 1))

            df_groupped = (
                osm_data_gpd[["info_regrouped", "infra_prct"]]
                .groupby("info_regrouped")
                .sum()
            ).reset_index()

            df_groupped = df_groupped.sort_values(by="infra_prct")
            df_groupped = df_groupped[df_groupped["info_regrouped"] != "NaN"]

            st.bar_chart(
                data=df_groupped,
                x="info_regrouped",
                y="infra_prct",
                x_label="%"
                + " linéaire (total = %.1f km de voies)" % (total_length / 1000),
                y_label="type d'infrastructure",
                horizontal=True,
                height=300,
            )
