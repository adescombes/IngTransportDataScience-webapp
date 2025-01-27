
// Histogramme interactif (Plotly)
var data = [{
    x: ['Type 1', 'Type 2', 'Type 3', 'Type 4'],
    y: [10, 20, 30, 40],
    type: 'bar'
}];
var layout = {
    title: 'Interactive Histogram',
    xaxis: { title: 'Type' },
    yaxis: { title: 'Value' }
};
Plotly.newPlot('chart', data, layout);

// Téléchargement de l'histogramme en JPEG
document.getElementById('download-barplot').addEventListener('click', function () {
    Plotly.toImage(document.getElementById('chart'), { format: 'jpeg', width: 800, height: 600 })
        .then(function (imageData) {
            var link = document.createElement('a');
            link.href = imageData;
            link.download = 'chart.jpeg';
            link.click();
        });
});