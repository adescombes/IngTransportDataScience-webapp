from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

import geopandas as gpd
import osmnx as ox
from osmnx._errors import InsufficientResponseError
from pandasql import sqldf
from shapely.geometry import Polygon, box

from scripts.geovelo_sql_queries import queries
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
        # tags = {"highway": True}  # Exemple de tags génériques
        osm_data = ox.features.features_from_polygon(polygon, tags_of_interest)

        # queries geovelo
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

        q = "SELECT * FROM sql_df"
        pysqldf = lambda q: sqldf(q, globals())
        osmid_bike_type = [
            pysqldf("""SELECT osmid FROM sql_df WHERE """ + q).osmid for q in queries
        ]
        line_gpd_clipped = organise_df_with_SQLqueries(osmid_bike_type, line)

        osm_data_gpd = gpd.GeoDataFrame(
            line_gpd_clipped, geometry=line_gpd_clipped.geometry
        ).fillna("NaN")

        osm_data_gpd.set_geometry("geometry")

        # fin des queries geovelo -> couche geojson

        geojson_data = osm_data_gpd.to_crs("EPSG:4326").to_json()
        app.logger.debug("Données GeoJSON générées")

        return jsonify({"geojson": geojson_data})

    except InsufficientResponseError:
        app.logger.error("Aucune donnée trouvée pour la zone sélectionnée")
        return jsonify(
            {"geojson": None, "message": "No data found in the selected area."}
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
