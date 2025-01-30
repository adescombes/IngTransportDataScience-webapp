var baseLayers = {};
var overlays = {};

var map = L.map('map').setView([46.52, 6.63], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

var layerControl = L.control.layers(baseLayers, overlays).addTo(map);


const mapboxUrl = 'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/{z}/{x}/{y}?access_token=sk.eyJ1IjoiYWRlLXRyYW5zaXRlYyIsImEiOiJjbTRiZzFxYWUwNDJ1MmtyNDNia29qYWN3In0.1dSIQ5MuxXILFGhf5aqYkA';
const attr = '&copy; <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> <strong><a href="https://labs.mapbox.com/contribute/" target="_blank">Improve this map</a></strong>contributors';

L.tileLayer(mapboxUrl, {
    attribution: attr
}).addTo(map);

let currentGeoJSON = null; 
let geojsonLayer;
let elevationLayer;

// Ajout des outils de dessin
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var drawControl = new L.Control.Draw({
    draw: {
        rectangle: true, 
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

function showLoadingCursor() {
    document.body.classList.add("loading"); 
    document.querySelector(".leaflet-container").classList.add("loading");
}

function hideLoadingCursor() {
    document.body.classList.remove("loading"); 
    document.querySelector(".leaflet-container").classList.remove("loading"); 

}

document.getElementById('run-button').addEventListener('click', function (event) {

    event.preventDefault(); // Empêche le comportement par défaut

    if (!currentCoordinates) {
        alert("Veuillez dessiner un rectangle avant d'appuyer sur RUN.");
        return;
    }

    showLoadingCursor();

    console.log('Bouton RUN cliqué, envoi des coordonnées au backend...');

    fetch("/process-rectangle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ coordinates: currentCoordinates }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.geojson) {
                currentGeoJSON = JSON.parse(data.geojson);

                const categories = [...new Set(currentGeoJSON.features.map(f => f.properties.info_regrouped))];
                addLegend(categories);
                    
                geojsonLayer = L.geoJSON(currentGeoJSON, {
                    style: feature => ({
                        color: getColor(feature.properties.info_regrouped),
                        weight: 3,
                        opacity: 1
                    })
                }).addTo(map);
                
                layerControl.addOverlay(geojsonLayer, "Infrastructures cyclables");

                map.fitBounds(geojsonLayer.getBounds());
    
                // Afficher les boutons une fois la carte chargée
                document.getElementById("download-osm-data").style.display = "block";
                document.getElementById("elevation-button").style.display = "block";

                plotHistogram(currentGeoJSON);
                
            } else {
                console.error("Aucun GeoJSON retourné.");
                alert("Aucune donnée disponible pour la zone sélectionnée.");
            }
        })
        .catch((error) => console.error("Erreur :", error))
        .finally(() => hideLoadingCursor());
});



document.addEventListener('DOMContentLoaded', function () {
    const downloadButton = document.getElementById("download-osm-data");
    const elevationButton = document.getElementById("elevation-button");
    const downloadElevation = document.getElementById("download-elevation");

    if (downloadButton) {
        downloadButton.style.display = "none";  // Caché au départ
    }
    if (elevationButton) {
        elevationButton.style.display = "none"; // Caché au départ
    }
    if (downloadElevation) {
        downloadElevation.style.display = "none"; // Caché au départ
    }
});

document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('download-osm-data').addEventListener('click', function () {
        if (!currentGeoJSON) {
            alert("Veuillez d'abord dessiner une zone et charger les données.");
            return;
        }

        console.log('Bouton DOWNLOAD cliqué, téléchargement des données en cours...');


        fetch("/download-csv", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ geojson: currentGeoJSON }), 
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
            .catch(error => console.error("Erreur :", error))
            .finally(() => hideLoadingCursor());
    });
});

// légende pour les infras cyclables
function addLegend(infoCategories) {
    var legend = L.control({ position: "bottomright" });

    legend.onAdd = function (map) {
        var div = L.DomUtil.create("div", "info_regrouped legend");
        div.innerHTML = "<h4>Légende</h4>";
        infoCategories.forEach(category => {
            // Ajoute une ligne colorée à côté de chaque catégorie
            div.innerHTML += `
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="
                        width: 30px; 
                        height: 4px; 
                        background-color: ${getColor(category)}; 
                        margin-right: 10px;">
                    </div>
                    ${category}
                </div>`;
        });
        return div;
    };

    legend.addTo(map);
}


// Fonction pour assigner des couleurs par catégorie
function getColor(category) {
    switch (category) {
        case "Accotement cyclable":
            return "#aacf76";
        case "Autre chemin piéton autorisé aux vélos":
            return "#588e0f";
        case "Bande cyclable": 
            return "#0ddbfa";
        case "Cheminement cyclable":
            return "#a713e7";
        case "Double-sens cyclable":
            return "#99ee22";
        case "Chemin piéton":
            return "#9a2328";
        case "Limite à 30":
            return "#0a4d00";
        case "Piste cyclable":
            return "#f05f84";
        case "Piste sur trottoir":
            return "#c0690d";
        case "Route de service / chemin agricole":
            return "#75a5b1";
        case "Trottoir cyclable":
            return "#3214c5";
        case "Voie bus":
            return "#12fed3";
        case "Voie verte":
            return "#c70f0d";
        case "Zone 30":
            return "#f27533";
        case "Zone de rencontre":
            return "#671f52";
        case "chaucidou":
            return "#8c2100";
        case "escalier":
            return "#da1155";
        case "Chemin piéton":
            return "#ea1278";
        case "autres routes":
            return "#000000"
    };
}

/// ELEVATION ......
document.addEventListener('DOMContentLoaded', function () {

    document.getElementById("elevation-button").addEventListener("click", function () {
                
        console.log('bouton élévation cliqué')

        showLoadingCursor();

        fetch("/get-elevation", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ geojson: currentGeoJSON }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.geojson) {
                    currentGeoJSON = JSON.parse(data.geojson);

                    elevationLayer = L.geoJSON(currentGeoJSON, {
                        style: feature => ({
                            color: getElevationColor(feature.properties.pente),
                            weight: 3,
                            opacity: 1
                        })
                    }).addTo(map);

                    layerControl.addOverlay(elevationLayer, "Élévation");
                    addElevationLegend();
                    document.getElementById("download-elevation").style.display = "block";

                } else {
                    alert("Erreur lors du calcul de l'élévation.");
                }
            })
            .finally(() => hideLoadingCursor()); 
    });
});

// légende pour le dénivelé
function addElevationLegend() {
    var legend = L.control({ position: "bottomright" });

    legend.onAdd = function (map) {
        var div = L.DomUtil.create("div", "pente legend");
        div.innerHTML = "<h4>Dénivelé (%)</h4>";

        // Définir les classes d'élévation utilisées dans getElevationColor
        var elevationClasses = [
            { range: "> 15%", color: "#800026" },
            { range: "10 - 15%", color: "#BD0026" },
            { range: "7.5 - 10%", color: "#E31A1C" },
            { range: "5 - 7.5%", color: "#FC4E2A" },
            { range: "2.5 - 5%", color: "#FD8D3C" },
            { range: "0 - 2.5%", color: "#FEB24C" },
        ];

        // Boucle pour générer les éléments de légende
        elevationClasses.forEach(entry => {
            div.innerHTML += `
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="
                        width: 30px; 
                        height: 10px; 
                        background-color: ${entry.color}; 
                        margin-right: 10px;">
                    </div>
                    ${entry.range}
                </div>`;
        });

        return div;
    };

    legend.addTo(map);
}

function getElevationColor(pente) {
    return pente > 15 ? "#800026" :
           pente > 10  ? "#BD0026" :
           pente > 7.5  ? "#E31A1C" :
           pente > 5  ? "#FC4E2A" :
           pente > 2.5   ? "#FD8D3C" :
           pente > -1   ? "#FEB24C" :
           "#FFEDA0";  // Couleur pour valeurs négatives ou inconnues
}


document.addEventListener('DOMContentLoaded', function () {

    document.getElementById("download-elevation").addEventListener("click", function () {
        console.log("Téléchargement du fichier d'élévation...");
    
        fetch("/download-elevation-csv", { method: "GET" })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.style.display = "none";
            a.href = url;
            a.download = "elevation_data.csv";
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            console.log("Fichier CSV téléchargé avec succès.");
        })
        .catch(error => console.error("Erreur :", error))
    });
});



// Histogramme

function plotHistogram(data) {
    // Extraire les catégories et calculer les sommes
    const aggregated = data.features.reduce((acc, feature) => {
        const info_regrouped = feature.properties.info_regrouped;
        const length_prct = feature.properties.length_prct || 0;
        acc[info_regrouped] = (acc[info_regrouped] || 0) + length_prct;
        return acc;
    }, {});

    const categories = Object.keys(aggregated);
    const values = Object.values(aggregated);

    // Générer les couleurs pour chaque catégorie en utilisant `getColor`
    const colors = categories.map(category => getColor(category));

    const plotData = [{
        x: values, // Valeurs sur l'axe X (longueurs)
        y: categories, // Catégories sur l'axe Y
        type: "bar",
        orientation: "h", // Barres horizontales
        marker: {
            color: colors // Couleurs personnalisées
        }
    }];

    const layout = {
        title: "% linéaire des infrastructures cyclables",
        xaxis: { title: "% linéaire" }, // Axe X montre les longueurs
        yaxis: { title: "", automargin: true },
        margin: {
            l: 150,  // Ajuste cette valeur (largeur en pixels pour l'axe Y)
            r: 20,
            t: 50,
            b: 50
        }
    };

    Plotly.newPlot("chart", plotData, layout);
}







