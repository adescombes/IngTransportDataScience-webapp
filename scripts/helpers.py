# here all the function which are use in main are presented below
# import all the dependencies
import geopandas as gpd
import pandas as pd
import osmnx as ox
from geopandas.tools import sjoin
import seaborn as sns
import requests
import numpy as np
import keplergl as kp
import matplotlib.pyplot as plt


def get_slope(x, elevation_model, smooth=True):
    """
    get the slope of a LineString
    Input: x: the linestring [Geometry]
           elevation_model : The DEM [tif]
           smooth: if we want the elevation profile to be smooth or not [boolean]

    """

    line_ = x.geometry
    sample_distance = 1
    elevation_profile = elevation_model.elevation_profile(
        line_, distance=sample_distance, interpolated=True
    )
    # adjust the elevation profile where there is high variance (forests / urban areas)
    elevation_profile = elevation_profile.to_terrain_model()
    # smooth the elevation profile
    if smooth:
        elevation_profile = elevation_profile.smooth()

    inclination = np.abs(elevation_profile.inclination(degrees=True))
    # plot the profile
    # plt.figure(figsize=(25,3))
    # elevation_profile.plot()
    # plt.show()
    distances = elevation_profile.distances
    # print(distances)
    elevations = elevation_profile.elevations
    if (
        (x["tunnel"] == "yes")
        | (x["bridge"] == "yes")
        | (
            (
                (str(x["name"]).__contains__("Dam"))
                | (str(x["name"]).__contains__("dam"))
                | (str(x["name"]).__contains__("Barrage"))
                | (str(x["name"]).__contains__("barrage"))
            )
            & ((str(x["surface"]) == "concrete"))
        )
        | (elevations.min() < 50)
    ):
        return 0
    else:
        return inclination.mean()


def get_osm_data(network_centerpoint, commune_nb, subsector):
    """
    Input: network_centerpoint: the center of the circle where OSM data will be queried
           commune_nb: number of the commune of interest
           subsector: subsector of interes (exemple:       subsectors[subsectors.BZNR.isin([1004,1006])] for Fribourg)
           Output: a dataframe will all the segment of road on the subsector based on our query on OSM)
    """

    # import the data
    dist = 15000
    osm_data = ox.geometries.geometries_from_point(
        network_centerpoint, tags_of_interest, dist=dist
    )
    osm_data_save = osm_data.applymap(lambda x: str(x) if isinstance(x, list) else x)
    # keep the line
    line = osm_data_save.loc[["way"]].reset_index()
    line = line[
        line.geometry.geom_type == "LineString"
    ].reset_index()  # only the line geometry
    # set the crs for both dataset
    line.crs = "EPSG:4326"  # defini un crs à notre jeu de donnée correspondant à ce quon voit au dessus
    line = line.to_crs(2056)  # change le crs pour correspondre à la suisse
    line["length_line[m]"] = line.length  # calcul la longueur
    subsector = subsector.to_crs(2056)  # idem pour l'agglo
    line_gpd_clipped = gpd.clip(
        line, subsector
    )  # garde seulement les données à l'intérieur de l'agglo
    line_gpd_clipped_ss = sjoin(
        subsector[["BZNR", "GMDNAME", "GMDNR", "geometry"]],
        line_gpd_clipped,
        how="right",
    )  # construit un seul dataset avec les deux jeu de donnée
    line_gpd_clipped = line_gpd_clipped_ss[
        line_gpd_clipped_ss["GMDNR"] == commune_nb
    ].copy()  # selectionne que le centre de fribourg pour une analyse plus précise
    line_gpd_clipped.geometry = line_gpd_clipped.intersection(
        subsector[subsector["GMDNR"] == commune_nb].iloc[0, -1]
    ).copy()  # cut all the linestring which are not in the polygon

    # supprimer les chemins de fer and highway nan
    line_gpd_clipped = line_gpd_clipped[~line_gpd_clipped.highway.isna()].copy()

    # get ready to use sql queries
    line_gpd_clipped = line_gpd_clipped.set_index("osmid").copy()
    return line_gpd_clipped


def organise_df_with_SQLqueries(osmid_bike_type, line_gpd_clipped):
    """
    Input: osmid_bike_type = indexes for the result of each SQL queries
           line_gpd_clipped = a dataframe will all the segment of road on the subsector based on our query on OSM)
    Output: line_gpd_clipped with two new columns with the information on the type of bike infrastructure and also a new dataframe (line_gpd_bike) with only the segement where you can bike
    """
    line_gpd_clipped["info"] = "0"
    line_gpd_clipped.loc[osmid_bike_type[0], "info"] = "Accotements_cyclables-1xD"
    line_gpd_clipped.loc[osmid_bike_type[1], "info"] = "Accotements_cyclables-1xG"
    line_gpd_clipped.loc[osmid_bike_type[2], "info"] = "Accotements_cyclables-2x"
    line_gpd_clipped.loc[osmid_bike_type[3], "info"] = (
        "Autres_chemins_piéton_autorisé_aux_vélos-1x"
    )
    line_gpd_clipped.loc[osmid_bike_type[4], "info"] = (
        "Autres_chemins_piéton_autorisé_aux_vélos-2x"
    )
    line_gpd_clipped.loc[osmid_bike_type[5], "info"] = "Bandes_cyclables-1xD"
    line_gpd_clipped.loc[osmid_bike_type[6], "info"] = "Bandes_cyclables-1xG"
    line_gpd_clipped.loc[osmid_bike_type[7], "info"] = "Bandes_cyclables-2x"
    line_gpd_clipped.loc[osmid_bike_type[8], "info"] = "Bandes_cyclables-2xD"
    line_gpd_clipped.loc[osmid_bike_type[9], "info"] = "Bandes_cyclables-2xG"
    line_gpd_clipped.loc[osmid_bike_type[10], "info"] = "Cheminements_cyclables-1xD"
    line_gpd_clipped.loc[osmid_bike_type[11], "info"] = "Cheminements_cyclables-1xG"
    line_gpd_clipped.loc[osmid_bike_type[12], "info"] = "Cheminements_cyclables-2x"
    line_gpd_clipped.loc[osmid_bike_type[13], "info"] = (
        "Doubles-sens_cyclables_sans_bande"
    )
    line_gpd_clipped.loc[osmid_bike_type[14], "info"] = (
        "Doubles-sens_cyclables_en_bande-D"
    )
    line_gpd_clipped.loc[osmid_bike_type[15], "info"] = (
        "Doubles-sens_cyclables_en_bande-G"
    )
    line_gpd_clipped.loc[osmid_bike_type[16], "info"] = "Doubles-sens_cyclables_piste-D"
    line_gpd_clipped.loc[osmid_bike_type[17], "info"] = "Doubles-sens_cyclables_piste-G"
    line_gpd_clipped.loc[osmid_bike_type[18], "info"] = "Footway_path_designated-1x"
    line_gpd_clipped.loc[osmid_bike_type[19], "info"] = "Footway_path_designated-2x "
    line_gpd_clipped.loc[osmid_bike_type[20], "info"] = "Limite_a_30-1x"
    line_gpd_clipped.loc[osmid_bike_type[21], "info"] = "Limite_a_30-2x"
    line_gpd_clipped.loc[osmid_bike_type[22], "info"] = "Pedestrian_1x"
    line_gpd_clipped.loc[osmid_bike_type[23], "info"] = "Pedestrian_2x."
    line_gpd_clipped.loc[osmid_bike_type[24], "info"] = "Pistes_cyclables-1xD."
    line_gpd_clipped.loc[osmid_bike_type[25], "info"] = "Pistes_cyclables-1xG"
    line_gpd_clipped.loc[osmid_bike_type[26], "info"] = "Pistes_cyclables-2x"
    line_gpd_clipped.loc[osmid_bike_type[27], "info"] = "Pistes_cyclables-2xD"
    line_gpd_clipped.loc[osmid_bike_type[28], "info"] = "Pistes_cyclables-2xG"
    line_gpd_clipped.loc[osmid_bike_type[29], "info"] = "Pistes_sur_Trottoirs-1x"
    line_gpd_clipped.loc[osmid_bike_type[30], "info"] = "Pistes_sur_Trottoirs-1xD"
    line_gpd_clipped.loc[osmid_bike_type[31], "info"] = "Pistes_sur_Trottoirs-1xG"
    line_gpd_clipped.loc[osmid_bike_type[32], "info"] = "Pistes_sur_Trottoirs-2x"
    line_gpd_clipped.loc[osmid_bike_type[33], "info"] = (
        "Routes_services_chemins_agricoles-1x"
    )
    line_gpd_clipped.loc[osmid_bike_type[34], "info"] = (
        "Routes_services_chemins_agricoles-2x"
    )
    line_gpd_clipped.loc[osmid_bike_type[35], "info"] = "Trottoirs_cyclables-1x"
    line_gpd_clipped.loc[osmid_bike_type[36], "info"] = "Trottoirs_cyclables-1xD"
    line_gpd_clipped.loc[osmid_bike_type[37], "info"] = "Trottoirs_cyclables-1xG"
    line_gpd_clipped.loc[osmid_bike_type[38], "info"] = "Trottoirs_cyclables-2x"
    line_gpd_clipped.loc[osmid_bike_type[39], "info"] = "Voies_bus-1xD"
    line_gpd_clipped.loc[osmid_bike_type[40], "info"] = "Voies_bus-1xG"
    line_gpd_clipped.loc[osmid_bike_type[41], "info"] = "Voies_bus-2x"
    line_gpd_clipped.loc[osmid_bike_type[42], "info"] = "Voies_vertes-1x"
    line_gpd_clipped.loc[osmid_bike_type[43], "info"] = "Voies_vertes-2x"
    line_gpd_clipped.loc[osmid_bike_type[44], "info"] = "Zones_30-1x"
    line_gpd_clipped.loc[osmid_bike_type[45], "info"] = "Zones_30-2x"
    line_gpd_clipped.loc[osmid_bike_type[46], "info"] = "Zones_rencontre-1x"
    line_gpd_clipped.loc[osmid_bike_type[47], "info"] = "Zones_rencontre-2x"
    line_gpd_clipped.loc[osmid_bike_type[48], "info"] = "chaucidou"
    line_gpd_clipped.loc[osmid_bike_type[49], "info"] = "escalier-1xD"
    line_gpd_clipped.loc[osmid_bike_type[50], "info"] = "escalier-1xG"
    line_gpd_clipped.loc[osmid_bike_type[51], "info"] = "escalier-2x"
    line_gpd_clipped.loc[osmid_bike_type[52], "info"] = "footway_permissive-1x"
    line_gpd_clipped.loc[osmid_bike_type[53], "info"] = "footway_permissive-2x"
    line_gpd_clipped.loc[osmid_bike_type[54], "info"] = "velorue-1x"
    line_gpd_clipped.loc[osmid_bike_type[55], "info"] = "velorue-2x"
    # add bike = yes
    nan_bike_yes = line_gpd_clipped[
        (line_gpd_clipped["info"] == "0")
        & (
            (line_gpd_clipped.bicycle == "yes")
            | (line_gpd_clipped.bicycle == "permissive")
            | (line_gpd_clipped.bicycle == "destination")
            | (line_gpd_clipped.bicycle == "use_sidepath")
            | (line_gpd_clipped.bicycle == "optional_sidepath")
            | (line_gpd_clipped.bicycle == "designated")
        )
    ].index
    line_gpd_clipped.loc[nan_bike_yes, "info"] = "nan_bike_yes"
    # More grouped
    line_gpd_clipped.loc[osmid_bike_type[0], "info_regrouped"] = "Accotements_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[1], "info_regrouped"] = "Accotements_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[2], "info_regrouped"] = "Accotements_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[3], "info_regrouped"] = (
        "Autres_chemins_piéton_autorisé_aux_vélos"
    )
    line_gpd_clipped.loc[osmid_bike_type[4], "info_regrouped"] = (
        "Autres_chemins_piéton_autorisé_aux_vélos"
    )
    line_gpd_clipped.loc[osmid_bike_type[5], "info_regrouped"] = "Bandes_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[6], "info_regrouped"] = "Bandes_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[7], "info_regrouped"] = "Bandes_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[8], "info_regrouped"] = "Bandes_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[9], "info_regrouped"] = "Bandes_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[10], "info_regrouped"] = (
        "Cheminements_cyclables"
    )
    line_gpd_clipped.loc[osmid_bike_type[11], "info_regrouped"] = (
        "Cheminements_cyclables"
    )
    line_gpd_clipped.loc[osmid_bike_type[12], "info_regrouped"] = (
        "Cheminements_cyclables"
    )
    line_gpd_clipped.loc[osmid_bike_type[13], "info_regrouped"] = (
        "Double-sens_cyclables"
    )
    line_gpd_clipped.loc[osmid_bike_type[14], "info_regrouped"] = (
        "Double-sens_cyclables"
    )
    line_gpd_clipped.loc[osmid_bike_type[15], "info_regrouped"] = (
        "Double-sens_cyclables"
    )
    line_gpd_clipped.loc[osmid_bike_type[16], "info_regrouped"] = (
        "Double-sens_cyclables"
    )
    line_gpd_clipped.loc[osmid_bike_type[17], "info_regrouped"] = (
        "Double-sens_cyclables"
    )
    line_gpd_clipped.loc[osmid_bike_type[18], "info_regrouped"] = (
        "Footway_path_designated"
    )
    line_gpd_clipped.loc[osmid_bike_type[19], "info_regrouped"] = (
        "Footway_path_designated"
    )
    line_gpd_clipped.loc[osmid_bike_type[20], "info_regrouped"] = "Limite_a_30"
    line_gpd_clipped.loc[osmid_bike_type[21], "info_regrouped"] = "Limite_a_30"
    line_gpd_clipped.loc[osmid_bike_type[22], "info_regrouped"] = "Pedestrian"
    line_gpd_clipped.loc[osmid_bike_type[23], "info_regrouped"] = "Pedestrian"
    line_gpd_clipped.loc[osmid_bike_type[24], "info_regrouped"] = "Pistes_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[25], "info_regrouped"] = "Pistes_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[26], "info_regrouped"] = "Pistes_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[27], "info_regrouped"] = "Pistes_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[28], "info_regrouped"] = "Pistes_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[29], "info_regrouped"] = "Pistes_sur_Trottoirs"
    line_gpd_clipped.loc[osmid_bike_type[30], "info_regrouped"] = "Pistes_sur_Trottoirs"
    line_gpd_clipped.loc[osmid_bike_type[31], "info_regrouped"] = "Pistes_sur_Trottoirs"
    line_gpd_clipped.loc[osmid_bike_type[32], "info_regrouped"] = "Pistes_sur_Trottoirs"
    line_gpd_clipped.loc[osmid_bike_type[33], "info_regrouped"] = (
        "Routes_services_chemins_agricoles"
    )
    line_gpd_clipped.loc[osmid_bike_type[34], "info_regrouped"] = (
        "Routes_services_chemins_agricoles"
    )
    line_gpd_clipped.loc[osmid_bike_type[35], "info_regrouped"] = "Trottoirs_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[36], "info_regrouped"] = "Trottoirs_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[37], "info_regrouped"] = "Trottoirs_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[38], "info_regrouped"] = "Trottoirs_cyclables"
    line_gpd_clipped.loc[osmid_bike_type[39], "info_regrouped"] = "Voies_bus"
    line_gpd_clipped.loc[osmid_bike_type[40], "info_regrouped"] = "Voies_bus"
    line_gpd_clipped.loc[osmid_bike_type[41], "info_regrouped"] = "Voies_bus"
    line_gpd_clipped.loc[osmid_bike_type[42], "info_regrouped"] = "Voies_vertes"
    line_gpd_clipped.loc[osmid_bike_type[43], "info_regrouped"] = "Voies_vertes"
    line_gpd_clipped.loc[osmid_bike_type[44], "info_regrouped"] = "Zones_30"
    line_gpd_clipped.loc[osmid_bike_type[45], "info_regrouped"] = "Zones_30"
    line_gpd_clipped.loc[osmid_bike_type[46], "info_regrouped"] = "Zones_rencontre"
    line_gpd_clipped.loc[osmid_bike_type[47], "info_regrouped"] = "Zones_rencontre"
    line_gpd_clipped.loc[osmid_bike_type[48], "info_regrouped"] = "chaucidou"
    line_gpd_clipped.loc[osmid_bike_type[49], "info_regrouped"] = "escalier"
    line_gpd_clipped.loc[osmid_bike_type[50], "info_regrouped"] = "escalier"
    line_gpd_clipped.loc[osmid_bike_type[51], "info_regrouped"] = "escalier"
    line_gpd_clipped.loc[osmid_bike_type[52], "info_regrouped"] = "footway_permissive"
    line_gpd_clipped.loc[osmid_bike_type[53], "info_regrouped"] = "footway_permissive"
    line_gpd_clipped.loc[osmid_bike_type[54], "info_regrouped"] = "velorue"
    line_gpd_clipped.loc[osmid_bike_type[55], "info_regrouped"] = "velorue"
    # add bike = yes
    line_gpd_clipped.loc[nan_bike_yes, "info_regrouped"] = "NaN_bike_yes"
    # keep only the bike
    line_gpd_bike = line_gpd_clipped[line_gpd_clipped["info"] != "0"].copy()
    # treat the ways
    line_gpd_bike.loc[:, "bike_way"] = line_gpd_bike["info"].apply(
        lambda x: define_way_bike(x)
    )
    line_gpd_bike.loc[:, "length_line_onewaycounted_bike[m]"] = (
        line_gpd_bike["bike_way"] * line_gpd_bike["length_line[m]"]
    )
    line_gpd_clipped["length_line_onewaycounted_wholenetwork[m]"] = line_gpd_clipped[
        "length_line[m]"
    ]
    # double sens
    line_gpd_clipped.loc[
        osmid_bike_type[56], "length_line_onewaycounted_wholenetwork[m]"
    ] = (
        line_gpd_clipped.loc[
            osmid_bike_type[56], "length_line_onewaycounted_wholenetwork[m]"
        ]
        * 2
    )
    # sens unique
    line_gpd_clipped.loc[
        osmid_bike_type[57], "length_line_onewaycounted_wholenetwork[m]"
    ] = (
        line_gpd_clipped.loc[
            osmid_bike_type[57], "length_line_onewaycounted_wholenetwork[m]"
        ]
        * 1
    )

    return line_gpd_clipped, line_gpd_bike


def define_way_bike(x):
    if x.__contains__("1"):
        return 1
    if x == "0":
        return 0
    else:
        return 2


def analysis_osm_bike_network(
    osm_data_gpd, osm_data_bike_gpd, elevation_model, slope_mask=False
):
    """
    Perform the analysis on the network
    Input: osm_data_gpd: df of the whole network
           osm_data_bike_gpd: df of the bikeable network
           elevation_model: DEM of Interest
           slope_mask: if we want to calculate the slope or not
    Output: kepler_map1: map of the different speed of the network
            kepler_map2: map of the different slope of the network
    """
    # set theme plot
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.set_theme(
        style="ticks", font_scale=1.5, palette=["lightgrey", "green"], rc=custom_params
    )

    # Total of the bike network in [m]
    bike_network_len = osm_data_bike_gpd["length_line_onewaycounted_bike[m]"].sum()
    # Total of the network in [m]
    network_len = osm_data_gpd["length_line_onewaycounted_wholenetwork[m]"].sum()
    # ratio of bikeable network
    ratio_bike = bike_network_len / network_len
    print("Pourcentage de piste cyclable: ", ratio_bike * 100, "%")

    road_network = osm_data_gpd[
        ~osm_data_gpd.highway.isin(
            ["path", "footway", "cycleway", "pedestrian", "track", "steps"]
        )
    ]
    # nombre de NaN attention rapport des segments pas de km
    print(
        "le ratio de NaN ( rapport des segments pas des m ) est ",
        road_network.maxspeed.isna().sum() / road_network.maxspeed.shape[0],
    )
    # map par vitesse
    config_road = np.load("npy/road_network_analysis.npy", allow_pickle="TRUE").item()
    road_network_gpd = gpd.GeoDataFrame(
        road_network, geometry=road_network.geometry
    ).fillna("NaN")
    kepler_map1 = kp.KeplerGl(height=800)
    kepler_map1.add_data(data=road_network_gpd, name="osm_data__gpd")
    kepler_map1.config = config_road
    road_network_withNaN = road_network[
        ["highway", "maxspeed", "length_line_onewaycounted_wholenetwork[m]"]
    ]
    road_network_withNaN_barplot = (
        road_network_withNaN.groupby(["maxspeed"]).sum()
        / road_network_withNaN["length_line_onewaycounted_wholenetwork[m]"].sum()
        * 100
    )
    # Montrer tout les pourcentages de NaN:
    display(road_network_withNaN.groupby(["highway", "maxspeed"]).sum())

    print("bike--------------------")
    # reduit la part du réseau NaN en enlevant les zones ou il y a pas de limite de vitesse
    road_network_bike = osm_data_bike_gpd[
        ~osm_data_bike_gpd.highway.isin(
            ["path", "footway", "cycleway", "pedestrian", "track", "steps"]
        )
    ]
    print(
        "le ratio de NaN est ",
        road_network_bike.maxspeed.isna().sum() / road_network_bike.maxspeed.shape[0],
    )
    # constituation du réseau pour le ROI en pourcentage de m dans le réseau
    road_network_bike_withNaN = road_network_bike[
        ["highway", "maxspeed", "length_line_onewaycounted_bike[m]"]
    ]
    road_network_bike_withNaN = road_network_bike_withNaN.fillna("NaN")
    road_network_withNaN_barplot_bike = (
        road_network_bike_withNaN.groupby(["maxspeed"]).sum()
        / road_network_bike_withNaN["length_line_onewaycounted_bike[m]"].sum()
        * 100
    )

    # analyse commune

    sum_by_speed = road_network_withNaN.groupby(["maxspeed"]).sum()
    sum_by_speed_bike = road_network_bike_withNaN.groupby(["maxspeed"]).sum()
    sum_by_speed = sum_by_speed.rename(
        {"length_line_onewaycounted_wholenetwork[m]": "network distance"}, axis=1
    ).reset_index()
    sum_by_speed_bike = sum_by_speed_bike.rename(
        {"length_line_onewaycounted_bike[m]": "cycling distance"}, axis=1
    ).reset_index()
    repartition = sum_by_speed.merge(sum_by_speed_bike, on="maxspeed").set_index(
        "maxspeed"
    )
    NaN_net = repartition.loc[["NaN"]]
    repartition = repartition.drop(["NaN"], axis=0)
    # graph
    plt.figure(figsize=(15, 7))
    repartition.plot(kind="bar")
    plt.ylabel("distance [m]")
    plt.title("Repartion of the network")
    plt.show()
    plt.figure(figsize=(15, 7))
    NaN_net.plot(kind="bar")
    plt.legend(loc=(0.6, 0.7))
    plt.ylabel("distance [m]")
    plt.title("Repartion of the network")
    plt.show()
    # pie
    # celui la est plus juste car il represente quesqui est cyclable dans le réseau où on a les vitesses
    plt.pie(
        (
            repartition.sum()["network distance"]
            - repartition.sum()["cycling distance"],
            repartition.sum()["cycling distance"],
        ),
        labels=["Network", "Bike"],
        autopct="%.0f%%",
    )
    plt.title(
        "Network vs bikeable network (sur lequel on a des vitesse possible)",
        fontweight="bold",
    )
    plt.show()
    # full

    plt.pie(
        (
            osm_data_gpd["length_line[m]"].sum()
            - osm_data_bike_gpd["length_line[m]"].sum(),
            osm_data_bike_gpd["length_line[m]"].sum(),
        ),
        labels=["Network", "Bike"],
        autopct="%.0f%%",
    )
    plt.title("Network vs bikeable network ", fontweight="bold")
    plt.show()

    # regroupement de toutes les installations
    plt.figure(figsize=(10, 7))
    splot = (
        osm_data_bike_gpd.groupby(["info_regrouped"])
        .sum()["length_line_onewaycounted_bike[m]"]
        .plot(kind="barh")
    )
    plt.ylabel("")
    plt.xlabel("distance [m]")
    plt.title(" Bikeable network type ", fontweight="bold")
    for g in splot.patches:
        splot.annotate(
            format(g.get_width(), ".1f"),
            (g.get_width(), g.get_y()),
            ha="left",
            va="center",
            xytext=(20, 9),
            textcoords="offset points",
        )
    plt.show()

    plt.figure(figsize=(10, 7))
    splot2 = (
        osm_data_bike_gpd.groupby(["info"])
        .sum()["length_line_onewaycounted_bike[m]"]
        .plot(kind="barh")
    )
    plt.ylabel("")
    plt.xlabel("distance [m]")
    plt.title(" Bikeable network type more precise ", fontweight="bold")
    for g in splot2.patches:
        splot2.annotate(
            format(g.get_width(), ".1f"),
            (g.get_width(), g.get_y()),
            ha="left",
            va="top",
            fontsize=12,
            xytext=(20, 9),
            textcoords="offset points",
        )
    plt.show()
    kepler_map2 = "not calculated"
    if slope_mask:
        # slope
        line_without_multiline = line_gpd_clipped[
            line_gpd_clipped.geometry.geom_type == "LineString"
        ]
        line_without_multiline["slope"] = (
            line_without_multiline.apply(
                lambda x: get_slope(x, elevation_model), axis=1
            )
            * 100
        )
        config_slope = np.load("slope.npy", allow_pickle="TRUE").item()
        osm_line_gpd_clipped = gpd.GeoDataFrame(
            line_without_multiline, geometry=osm_data_gpd.geometry
        )
        kepler_map2 = kp.KeplerGl(height=800)
        kepler_map2.add_data(data=osm_line_gpd_clipped, name="osm_line_gpd_clipped ")
        kepler_map2.config = config_slope
    return kepler_map1, kepler_map2


# initialisation osm
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
