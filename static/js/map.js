// Initialisation de la carte Leaflet
var map = L.map('map').setView([46.52, 6.63], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

const mapboxUrl = 'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/{z}/{x}/{y}?access_token=sk.eyJ1IjoiYWRlLXRyYW5zaXRlYyIsImEiOiJjbTRiZzFxYWUwNDJ1MmtyNDNia29qYWN3In0.1dSIQ5MuxXILFGhf5aqYkA';
const attr = '&copy; <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> <strong><a href="https://labs.mapbox.com/contribute/" target="_blank">Improve this map</a></strong>contributors';

L.tileLayer(mapboxUrl, {
    attribution: attr
}).addTo(map);

// Ajout des outils de dessin
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var drawControl = new L.Control.Draw({
    draw: {
        rectangle: true, // Permet uniquement de dessiner des rectangles
        polygon: false,
        polyline: false,
        circle: false,
        marker: false
    },
    edit: {
        featureGroup: drawnItems
    }
});
map.addControl(drawControl);

// Stocker les coordonnées du polygone dessiné
var currentCoordinates = null;

// Gestion de l'événement "dessin terminé"
map.on(L.Draw.Event.CREATED, function (event) {
    var layer = event.layer;
    drawnItems.clearLayers(); // Supprimer les anciens rectangles
    drawnItems.addLayer(layer);

    // Récupérer les coordonnées du rectangle
    var bounds = layer.getBounds();
    currentCoordinates = [
        [bounds.getSouthWest().lng, bounds.getSouthWest().lat], // Bottom-left
        [bounds.getNorthEast().lng, bounds.getNorthEast().lat]  // Top-right
    ];

    console.log('Coordonnées stockées :', currentCoordinates);
});

document.getElementById('run-button').addEventListener('click', function (event) {
    event.preventDefault(); // Empêche le comportement par défaut

    if (!currentCoordinates) {
        alert("Veuillez dessiner un rectangle avant d'appuyer sur RUN.");
        return;
    }

    console.log('Bouton RUN cliqué, envoi des coordonnées au backend...');

    // Envoyer les coordonnées au backend
    fetch("/process-rectangle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ coordinates: currentCoordinates }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            console.log("Réponse du backend :", data);
            if (data.geojson) {
                // Mettre à jour currentGeoJSON avec les données reçues
                currentGeoJSON = JSON.parse(data.geojson);

                // Ajouter la couche GeoJSON à la carte
                var geojsonLayer = L.geoJSON(currentGeoJSON, {
                    style: {
                        color: "blue",
                        weight: 2,
                        opacity: 0.8,
                    },
                }).addTo(map);
                map.fitBounds(geojsonLayer.getBounds());
                console.log('Les données sont affichées sur la carte.');
            } else {
                console.error("Aucun GeoJSON retourné.");
                alert("Aucune donnée disponible pour la zone sélectionnée.");
            }
        })
        .catch((error) => console.error("Erreur :", error));
});


let currentGeoJSON = null; // Variable pour stocker les données GeoJSON


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('download-osm-data').addEventListener('click', function () {
        if (!currentGeoJSON) {
            alert("Veuillez d'abord dessiner une zone et charger les données.");
            return;
        }

        console.log('Bouton DOWNLOAD cliqué, téléchargement des données en cours...');

        // Envoyer une requête pour télécharger le CSV
        fetch("/download-csv", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ geojson: currentGeoJSON }), // Vous devez stocker currentGeoJSON
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.blob();
            })
            .then(blob => {
                // Créer un lien pour télécharger le fichier
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.style.display = "none";
                a.href = url;
                a.download = "osm_data.csv";
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                console.log("Fichier CSV téléchargé avec succès.");
            })
            .catch(error => console.error("Erreur :", error));
    });
});
