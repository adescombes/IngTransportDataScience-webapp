from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

import geopandas as gpd
import osmnx as ox
from osmnx._errors import InsufficientResponseError
from pandasql import sqldf
import pandas as pd
import os
from shapely.geometry import Polygon, box

from scripts.geovelo_pandas_filters import geovelo_pandas_filters
from scripts.helpers import *


app = Flask(__name__, static_folder="static", static_url_path="")

CORS(
    app, origins=["http://127.0.0.1:5500", "http://127.0.0.1:5000"]
)  # Activer CORS pour toutes les routes


def has_list(x):
    return any(isinstance(i, list) for i in x)


@app.route("/process-rectangle", methods=["POST"])
def process_rectangle():
    app.logger.debug("Requête reçue : %s", request.json)

    data = request.get_json()
    coordinates = data.get("coordinates", [])
    app.logger.debug("Coordonnées reçues : %s", coordinates)

    # Vérifier les coordonnées
    if not coordinates or len(coordinates) != 2:
        app.logger.error("Coordonnées invalides")
        return jsonify({"geojson": None, "message": "Invalid coordinates."})

    # Créer un polygone à partir des coordonnées
    lon_min, lat_min = coordinates[0]
    lon_max, lat_max = coordinates[1]
    polygon = box(lon_min, lat_min, lon_max, lat_max)
    app.logger.debug("Polygone créé : %s", polygon)

    # Extraire les données OSM
    try:
        osm_data = ox.features.features_from_polygon(polygon, tags_of_interest)

        line = osm_data.loc[["way"]].reset_index()
        line = line[
            line.geometry.geom_type == "LineString"
        ].reset_index()  # only the line geometries
        line.crs = "EPSG:4326"
        line = line.to_crs(2056)
        line["length"] = line.length

        filtered_line = geovelo_pandas_filters(line.copy())

        # fin des queries geovelo -> couche geojson
        geojson_data = filtered_line.to_crs(4326).to_json()
        app.logger.debug("Données GeoJSON générées")

        return jsonify({"geojson": geojson_data})

    except InsufficientResponseError:
        app.logger.error("Aucune donnée trouvée pour la zone sélectionnée")
        return jsonify(
            {"geojson": None, "message": "No data found in the selected area."}
        )


@app.route("/download-csv", methods=["POST"])
def download_csv():
    data = request.get_json()
    geojson_data = data.get("geojson")

    if not geojson_data:
        return jsonify({"message": "No GeoJSON data provided."}), 400

    # Convertir le GeoJSON en GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])

    # Créer un fichier CSV temporaire
    csv_path = "osm_data.csv"
    gdf.to_csv(csv_path, index=False)

    # Envoyer le fichier CSV
    return send_file(csv_path, as_attachment=True, download_name="osm_data.csv")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
