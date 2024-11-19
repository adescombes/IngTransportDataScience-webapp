# here all the function which are use in main are presented below
# import all the dependencies
import geopandas as gpd
import numpy as np
import os
import osmnx as ox
import pandas as pd
from pandasql import sqldf
from pathlib import Path
from pyproj import Transformer
from geovelo_sql_queries import *


def organise_df_with_SQLqueries(osmid_bike_type, df):
    """
    Input: osmid_bike_type = indexes for the result of each SQL queries
           df = a dataframe will all the segment of road on the subsector based on our query on OSM)
    Output: df with two new columns with the information on the type of bike infrastructure and also a new dataframe (line_gpd_bike) with only the segement where you can bike
    """
    df["info"] = "0"
    df.loc[osmid_bike_type[0], "info"] = "Accotement cyclable"  #  à droite
    df.loc[osmid_bike_type[1], "info"] = "Accotement cyclable"  # à gauche
    df.loc[osmid_bike_type[2], "info"] = "Accotement cyclable"
    df.loc[osmid_bike_type[3], "info"] = "Chemin piéton autorisé aux vélos"
    df.loc[osmid_bike_type[4], "info"] = "Chemin piéton autorisé aux vélos"
    df.loc[osmid_bike_type[5], "info"] = "Bande cyclable"  #  à droite
    df.loc[osmid_bike_type[6], "info"] = "Bande cyclable"  # à gauche
    df.loc[osmid_bike_type[7], "info"] = "Bande cyclable"
    df.loc[osmid_bike_type[8], "info"] = "Bande cyclable"  #  à droite
    df.loc[osmid_bike_type[9], "info"] = "Bande cyclable"  #  à gauche
    df.loc[osmid_bike_type[10], "info"] = "Chaussée partagée"
    df.loc[osmid_bike_type[11], "info"] = "Chaussée partagée"
    df.loc[osmid_bike_type[12], "info"] = "Chaussée partagée"
    df.loc[osmid_bike_type[13], "info"] = "Double-sens cyclable"  #  (sans marquage)
    df.loc[osmid_bike_type[14], "info"] = "Double-sens cyclable"  #  (avec marquage)
    df.loc[osmid_bike_type[15], "info"] = (
        "Double-sens cyclable"  #  (avec marquage à gauche)
    )
    df.loc[osmid_bike_type[16], "info"] = (
        "Double-sens cyclable"  #  (avec marquage à droite)
    )
    df.loc[osmid_bike_type[17], "info"] = (
        "Double-sens cyclable"  #  (avec marquage à gauche)
    )
    df.loc[osmid_bike_type[18], "info"] = "Chemin piéton autorisé aux vélos"
    df.loc[osmid_bike_type[19], "info"] = "Chemin piéton autorisé aux vélos"
    df.loc[osmid_bike_type[20], "info"] = "Limite à 30"
    df.loc[osmid_bike_type[21], "info"] = "Chemin piéton autorisé aux vélos"
    df.loc[osmid_bike_type[22], "info"] = "Piste cyclable"  #  à droite
    df.loc[osmid_bike_type[23], "info"] = "Piste cyclable"  #  à gauche
    df.loc[osmid_bike_type[24], "info"] = "Piste cyclable"
    df.loc[osmid_bike_type[25], "info"] = "Piste cyclable"
    df.loc[osmid_bike_type[26], "info"] = "Piste cyclable"
    df.loc[osmid_bike_type[27], "info"] = "Piste cyclable sur trottoir"
    df.loc[osmid_bike_type[28], "info"] = "Piste cyclable sur trottoir"
    df.loc[osmid_bike_type[29], "info"] = "Piste cyclable sur trottoir"
    df.loc[osmid_bike_type[30], "info"] = "Piste cyclable sur trottoir"
    df.loc[osmid_bike_type[30], "info"] = "Piste cyclable sur trottoir"
    df.loc[osmid_bike_type[31], "info"] = "Chemin de terre"
    df.loc[osmid_bike_type[32], "info"] = "Chemin de terre"
    df.loc[osmid_bike_type[33], "info"] = "Trottoir cyclable"
    df.loc[osmid_bike_type[34], "info"] = "Trottoir cyclable"  #  à droite
    df.loc[osmid_bike_type[35], "info"] = "Trottoir cyclable"  # à gauche
    df.loc[osmid_bike_type[36], "info"] = "Trottoir cyclable"
    df.loc[osmid_bike_type[37], "info"] = "Voie bus autorisée aux vélos"
    df.loc[osmid_bike_type[38], "info"] = "Voie bus autorisée aux vélos"
    df.loc[osmid_bike_type[39], "info"] = "Voie bus autorisée aux vélos"
    df.loc[osmid_bike_type[40], "info"] = "Voie verte"
    df.loc[osmid_bike_type[41], "info"] = "Zone 30"
    df.loc[osmid_bike_type[42], "info"] = "Zone de rencontre"
    df.loc[osmid_bike_type[43], "info"] = "Chaucidou"
    df.loc[osmid_bike_type[44], "info"] = "Escalier avec rampe pour vélos"
    df.loc[osmid_bike_type[45], "info"] = "Chemin piéton autorisé aux vélos"
    df.loc[osmid_bike_type[46], "info"] = "Chemin piéton autorisé aux vélos"
    df.loc[osmid_bike_type[47], "info"] = "Vélorue"
    df.loc[osmid_bike_type[48], "info"] = "Limite à 20 km/h"
    df.loc[osmid_bike_type[49], "info"] = "Limite à 50 km/h"

    # add bike = yes
    other_bike_permissive = df[
        (df["info"] == "0")
        & (
            (df.bicycle == "yes")
            | (df.bicycle == "permissive")
            | (df.bicycle == "destination")
            | (df.bicycle == "use_sidepath")
            | (df.bicycle == "optional_sidepath")
            | (df.bicycle == "designated")
        )
    ].index
    df.loc[other_bike_permissive, "info"] = "Autre route autorisée aux vélos"

    return df[["geometry", "length_line", "info", "highway"]]


def define_way_bike(x):
    if x.__contains__("1"):
        return 1
    if x == "0":
        return 0
    else:
        return 2


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
