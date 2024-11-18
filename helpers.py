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
    df.loc[osmid_bike_type[0], "info"] = "Accotements_cyclables-1xD"
    df.loc[osmid_bike_type[1], "info"] = "Accotements_cyclables-1xG"
    df.loc[osmid_bike_type[2], "info"] = "Accotements_cyclables-2x"
    df.loc[osmid_bike_type[3], "info"] = "Autres_chemins_piéton_autorisé_aux_vélos-1x"
    df.loc[osmid_bike_type[4], "info"] = "Autres_chemins_piéton_autorisé_aux_vélos-2x"
    df.loc[osmid_bike_type[5], "info"] = "Bandes_cyclables-1xD"
    df.loc[osmid_bike_type[6], "info"] = "Bandes_cyclables-1xG"
    df.loc[osmid_bike_type[7], "info"] = "Bandes_cyclables-2x"
    df.loc[osmid_bike_type[8], "info"] = "Bandes_cyclables-2xD"
    df.loc[osmid_bike_type[9], "info"] = "Bandes_cyclables-2xG"
    df.loc[osmid_bike_type[10], "info"] = "Bandes_cyclables-1xD"
    df.loc[osmid_bike_type[11], "info"] = "Bandes_cyclables-1xG"
    df.loc[osmid_bike_type[12], "info"] = "Bandes_cyclables-2x"
    df.loc[osmid_bike_type[13], "info"] = "Doubles-sens_cyclables_sans_bande"
    df.loc[osmid_bike_type[14], "info"] = "Doubles-sens_cyclables_en_bande-D"
    df.loc[osmid_bike_type[15], "info"] = "Doubles-sens_cyclables_en_bande-G"
    df.loc[osmid_bike_type[16], "info"] = "Doubles-sens_cyclables_piste-D"
    df.loc[osmid_bike_type[17], "info"] = "Doubles-sens_cyclables_piste-G"
    df.loc[osmid_bike_type[18], "info"] = "Chemin_piéton_autorisé_aux_vélos-1x"
    df.loc[osmid_bike_type[19], "info"] = "Chemin_piéton_autorisé_aux_vélos-2x "
    df.loc[osmid_bike_type[20], "info"] = "Limite_a_30-1x"
    df.loc[osmid_bike_type[21], "info"] = "Limite_a_30-2x"
    df.loc[osmid_bike_type[22], "info"] = "Pedestrian_1x"
    df.loc[osmid_bike_type[23], "info"] = "Pedestrian_2x."
    df.loc[osmid_bike_type[24], "info"] = "Pistes_cyclables-1xD."
    df.loc[osmid_bike_type[25], "info"] = "Pistes_cyclables-1xG"
    df.loc[osmid_bike_type[26], "info"] = "Pistes_cyclables-2x"
    df.loc[osmid_bike_type[27], "info"] = "Pistes_cyclables-2xD"
    df.loc[osmid_bike_type[28], "info"] = "Pistes_cyclables-2xG"
    df.loc[osmid_bike_type[29], "info"] = "Pistes_sur_Trottoirs-1x"
    df.loc[osmid_bike_type[30], "info"] = "Pistes_sur_Trottoirs-1xD"
    df.loc[osmid_bike_type[31], "info"] = "Pistes_sur_Trottoirs-1xG"
    df.loc[osmid_bike_type[32], "info"] = "Pistes_sur_Trottoirs-2x"
    df.loc[osmid_bike_type[33], "info"] = "Routes_services_chemins_agricoles-1x"
    df.loc[osmid_bike_type[34], "info"] = "Routes_services_chemins_agricoles-2x"
    df.loc[osmid_bike_type[35], "info"] = "Trottoirs_cyclables-1x"
    df.loc[osmid_bike_type[36], "info"] = "Trottoirs_cyclables-1xD"
    df.loc[osmid_bike_type[37], "info"] = "Trottoirs_cyclables-1xG"
    df.loc[osmid_bike_type[38], "info"] = "Trottoirs_cyclables-2x"
    df.loc[osmid_bike_type[39], "info"] = "Voies_bus-1xD"
    df.loc[osmid_bike_type[40], "info"] = "Voies_bus-1xG"
    df.loc[osmid_bike_type[41], "info"] = "Voies_bus-2x"
    df.loc[osmid_bike_type[42], "info"] = "Voies_vertes-1x"
    df.loc[osmid_bike_type[43], "info"] = "Voies_vertes-2x"
    df.loc[osmid_bike_type[44], "info"] = "Zones_30-1x"
    df.loc[osmid_bike_type[45], "info"] = "Zones_30-2x"
    df.loc[osmid_bike_type[46], "info"] = "Zones_rencontre-1x"
    df.loc[osmid_bike_type[47], "info"] = "Zones_rencontre-2x"
    df.loc[osmid_bike_type[48], "info"] = "Pistes_cyclables"  # anciennement chaudidou
    df.loc[osmid_bike_type[49], "info"] = "escalier-1xD"
    df.loc[osmid_bike_type[50], "info"] = "escalier-1xG"
    df.loc[osmid_bike_type[51], "info"] = "escalier-2x"
    df.loc[osmid_bike_type[52], "info"] = "Chemin_piéton_autorisé_aux_vélos-1x"
    df.loc[osmid_bike_type[53], "info"] = "Chemin_piéton_autorisé_aux_vélos-2x"
    df.loc[osmid_bike_type[54], "info"] = "velorue-1x"
    df.loc[osmid_bike_type[55], "info"] = "velorue-2x"
    df.loc[osmid_bike_type[58], "info"] = "Limite_a_20-1x"
    df.loc[osmid_bike_type[59], "info"] = "Limite_a_20-2x"
    df.loc[osmid_bike_type[60], "info"] = "Limite_a_50-1x"
    df.loc[osmid_bike_type[61], "info"] = "Limite_a_50-2x"

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
    df.loc[other_bike_permissive, "info"] = "other_bike_permissive"

    # More grouped
    df.loc[osmid_bike_type[0], "info_regrouped"] = "Accotements_cyclables"
    df.loc[osmid_bike_type[1], "info_regrouped"] = "Accotements_cyclables"
    df.loc[osmid_bike_type[2], "info_regrouped"] = "Accotements_cyclables"
    df.loc[osmid_bike_type[3], "info_regrouped"] = "Chemin_piéton_autorisé_aux_vélos"
    df.loc[osmid_bike_type[4], "info_regrouped"] = "Chemin_piéton_autorisé_aux_vélos"
    df.loc[osmid_bike_type[5], "info_regrouped"] = "Bandes_cyclables"
    df.loc[osmid_bike_type[6], "info_regrouped"] = "Bandes_cyclables"
    df.loc[osmid_bike_type[7], "info_regrouped"] = "Bandes_cyclables"
    df.loc[osmid_bike_type[8], "info_regrouped"] = "Bandes_cyclables"
    df.loc[osmid_bike_type[9], "info_regrouped"] = "Bandes_cyclables"
    df.loc[osmid_bike_type[10], "info_regrouped"] = "Bandes_cyclables"
    df.loc[osmid_bike_type[11], "info_regrouped"] = "Bandes_cyclables"
    df.loc[osmid_bike_type[13], "info_regrouped"] = "Double-sens_cyclables"
    df.loc[osmid_bike_type[14], "info_regrouped"] = "Double-sens_cyclables"
    df.loc[osmid_bike_type[15], "info_regrouped"] = "Double-sens_cyclables"
    df.loc[osmid_bike_type[16], "info_regrouped"] = "Double-sens_cyclables"
    df.loc[osmid_bike_type[17], "info_regrouped"] = "Double-sens_cyclables"
    df.loc[osmid_bike_type[18], "info_regrouped"] = "Chemin_piéton_autorisé_aux_vélos"
    df.loc[osmid_bike_type[19], "info_regrouped"] = "Chemin_piéton_autorisé_aux_vélos"
    df.loc[osmid_bike_type[20], "info_regrouped"] = "Limite_a_30"
    df.loc[osmid_bike_type[21], "info_regrouped"] = "Limite_a_30"
    df.loc[osmid_bike_type[22], "info_regrouped"] = "Chemin_piéton_autorisé_aux_vélos"
    df.loc[osmid_bike_type[23], "info_regrouped"] = "Chemin_piéton_autorisé_aux_vélos"
    df.loc[osmid_bike_type[24], "info_regrouped"] = "Pistes_cyclables"
    df.loc[osmid_bike_type[25], "info_regrouped"] = "Pistes_cyclables"
    df.loc[osmid_bike_type[26], "info_regrouped"] = "Pistes_cyclables"
    df.loc[osmid_bike_type[27], "info_regrouped"] = "Pistes_cyclables"
    df.loc[osmid_bike_type[28], "info_regrouped"] = "Pistes_cyclables"
    df.loc[osmid_bike_type[29], "info_regrouped"] = "Pistes_sur_Trottoirs"
    df.loc[osmid_bike_type[30], "info_regrouped"] = "Pistes_sur_Trottoirs"
    df.loc[osmid_bike_type[31], "info_regrouped"] = "Pistes_sur_Trottoirs"
    df.loc[osmid_bike_type[32], "info_regrouped"] = "Pistes_sur_Trottoirs"
    df.loc[osmid_bike_type[33], "info_regrouped"] = "Routes_services_chemins_agricoles"
    df.loc[osmid_bike_type[34], "info_regrouped"] = "Routes_services_chemins_agricoles"
    df.loc[osmid_bike_type[35], "info_regrouped"] = "Trottoirs_cyclables"
    df.loc[osmid_bike_type[36], "info_regrouped"] = "Trottoirs_cyclables"
    df.loc[osmid_bike_type[37], "info_regrouped"] = "Trottoirs_cyclables"
    df.loc[osmid_bike_type[38], "info_regrouped"] = "Trottoirs_cyclables"
    df.loc[osmid_bike_type[39], "info_regrouped"] = "Voies_bus"
    df.loc[osmid_bike_type[40], "info_regrouped"] = "Voies_bus"
    df.loc[osmid_bike_type[41], "info_regrouped"] = "Voies_bus"
    df.loc[osmid_bike_type[42], "info_regrouped"] = "Voies_vertes"
    df.loc[osmid_bike_type[43], "info_regrouped"] = "Voies_vertes"
    df.loc[osmid_bike_type[44], "info_regrouped"] = "Zones_30"
    df.loc[osmid_bike_type[45], "info_regrouped"] = "Zones_30"
    df.loc[osmid_bike_type[46], "info_regrouped"] = "Zones_rencontre"
    df.loc[osmid_bike_type[47], "info_regrouped"] = "Zones_rencontre"
    df.loc[osmid_bike_type[48], "info_regrouped"] = (
        "Pistes_cyclables"  # anciennement chaucidou
    )
    df.loc[osmid_bike_type[49], "info_regrouped"] = "escalier"
    df.loc[osmid_bike_type[50], "info_regrouped"] = "escalier"
    df.loc[osmid_bike_type[51], "info_regrouped"] = "escalier"
    df.loc[osmid_bike_type[52], "info_regrouped"] = "Chemin_piéton_autorisé_aux_vélos"
    df.loc[osmid_bike_type[53], "info_regrouped"] = "Chemin_piéton_autorisé_aux_vélos"
    df.loc[osmid_bike_type[54], "info_regrouped"] = "velorue"
    df.loc[osmid_bike_type[55], "info_regrouped"] = "velorue"
    df.loc[osmid_bike_type[58], "info_regrouped"] = "Limite_a_20"
    df.loc[osmid_bike_type[59], "info_regrouped"] = "Limite_a_20"
    df.loc[osmid_bike_type[60], "info_regrouped"] = "Limite_a_50"
    df.loc[osmid_bike_type[61], "info_regrouped"] = "Limite_a_50"

    # add bike = yes
    df.loc[other_bike_permissive, "info_regrouped"] = "other_bike_permissive"

    # traitement des directions et sens uniques
    df.loc[:, "bike_way"] = df["info"].apply(lambda x: define_way_bike(x))
    df.loc[:, "length_line_onewaycounted_bike"] = df["bike_way"] * df["length_line"]
    df["length_line_onewaycounted_wholenetwork"] = df["length_line"]
    df.loc[osmid_bike_type[56], "length_line_onewaycounted_wholenetwork"] = (
        df.loc[osmid_bike_type[56], "length_line_onewaycounted_wholenetwork"] * 2
    )
    df.loc[osmid_bike_type[57], "length_line_onewaycounted_wholenetwork"] = (
        df.loc[osmid_bike_type[57], "length_line_onewaycounted_wholenetwork"] * 1
    )

    return df[
        [
            "geometry",
            "length_line",
            "info",
            "info_regrouped",
            "highway",
            "bike_way",
            "length_line_onewaycounted_wholenetwork",
            "length_line_onewaycounted_bike",
        ]
    ]


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
