from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import json
import geopandas as gpd
import osmnx as ox
from osmnx._errors import InsufficientResponseError
import requests
from shapely.geometry import box
from shapely.wkt import loads

from scripts.geovelo_pandas_filters import geovelo_pandas_filters
from scripts.helpers import *


app = Flask(__name__, static_folder="static", static_url_path="")

filtered_line = None


@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


# Exemple d'une route API pour tester
@app.route("/api/ping")
def ping():
    return jsonify({"message": "Server is running!"})


def has_list(x):
    return any(isinstance(i, list) for i in x)


@app.route("/process-rectangle", methods=["POST"])
def process_rectangle():
    app.logger.debug("Requête reçue : %s", request.json)

    data = request.get_json()
    coordinates = data.get("coordinates", [])
    app.logger.debug("Coordonnées reçues : %s", coordinates)

    if not coordinates or len(coordinates) != 2:
        app.logger.error("Coordonnées invalides")
        return jsonify({"geojson": None, "message": "Invalid coordinates."})

    lon_min, lat_min = coordinates[0]
    lon_max, lat_max = coordinates[1]
    polygon = box(lon_min, lat_min, lon_max, lat_max)
    app.logger.debug("Polygone créé : %s", polygon)

    try:
        osm_data = ox.features.features_from_polygon(polygon, tags_of_interest)

        line = osm_data.loc[["way"]].reset_index()
        line = line[
            line.geometry.geom_type == "LineString"
        ].reset_index()  # only the line geometries
        line.crs = "EPSG:4326"
        line = line.to_crs(2056)

        # REQUETES OSM
        filtered_line = geovelo_pandas_filters(line.copy())

        # EXPLODE MULTILINES -> GET ELEVATION
        rows = []
        for _, row in filtered_line.iterrows():

            geom = row["geometry"]
            c = loads(str(geom)).coords

            for i in range(len(c) - 1):

                coords_start = c[i]
                coords_end = c[i + 1]

                new_row = row.copy()
                new_row["geometry"] = "LINESTRING (%f %f, %f %f)" % (
                    coords_start[0],
                    coords_start[1],
                    coords_end[0],
                    coords_end[1],
                )

                rows.append(new_row)

        filtered_line["length"] = filtered_line.length

        total_length = filtered_line["length"].sum()
        filtered_line["length_prct"] = filtered_line["length"].apply(
            lambda x: 100 * x / total_length
        )

        # enlever les valeurs pour les routes "autres routes"
        # pour ne pas qu'elles apparaissent sur l'histogramme
        filtered_line.loc[
            filtered_line["info_regrouped"] == "autres routes", "length_prct"
        ] = 0

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

    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])

    csv_path = "osm_data.csv"
    gdf.to_csv(csv_path, index=False)

    return send_file(csv_path, as_attachment=True, download_name="osm_data.csv")


def get_elevation_swisstopo(coords):
    url = "https://api3.geo.admin.ch/rest/services/height"
    params = {"easting": coords[0], "northing": coords[1], "sr": "2056"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        height_str = response.json()["height"]
        height = round(float(height_str), 5)
        return height
    else:
        raise Exception(
            f"Erreur API Swisstopo : {response.status_code}, {response.text}"
        )


@app.route("/get-elevation", methods=["POST"])
def get_elevation():
    global filtered_line

    try:
        data = request.json
        geojson_data = data["geojson"]

        # Ajoutez ici le code de transformation et requête Swisstopo
        filtered_line = gpd.GeoDataFrame.from_features(geojson_data["features"])

        if filtered_line.empty or "geometry" not in filtered_line:
            return jsonify({"message": "Invalid GeoJSON data."}), 400

        filtered_line = filtered_line.set_crs(epsg=4326, allow_override=True).to_crs(
            epsg=2056
        )

        filtered_line["delta_z"] = 0

        for _, row in filtered_line.iterrows():
            geom = row["geometry"]
            coords = list(geom.coords)

            if len(coords) < 2:
                continue  # Ignore les segments invalides

            elevation_start = get_elevation_swisstopo(coords[0])
            elevation_end = get_elevation_swisstopo(coords[-1])
            delta_z = elevation_end - elevation_start
            filtered_line.at[_, "delta_z"] = abs(delta_z)

        filtered_line["pente"] = filtered_line.apply(
            lambda x: 100 * x["delta_z"] / x["length"] if x["length"] != 0 else 0,
            axis=1,
        )
        filtered_line = filtered_line.to_crs(epsg=4326)
        csv_path = "osm_data_elevation.csv"
        filtered_line.to_csv(csv_path, index=False)

        return jsonify(
            {"geojson": json.dumps(geojson_data)}
        )  # Assurez-vous que ce retour est bien un JSON valide
    except Exception as e:
        print(f"Erreur serveur : {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/download-elevation-csv", methods=["GET"])
def download_elevation_csv():
    global filtered_line

    if filtered_line is None or filtered_line.empty:
        return jsonify({"error": "Aucune donnée d'élévation disponible"}), 400

    # Définition du chemin temporaire
    csv_file = "osm_data_elevation.csv"
    filtered_line.to_csv(csv_file, index=False)

    return send_file(csv_file, as_attachment=True, mimetype="text/csv")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", debug=True, port=port)
