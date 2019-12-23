$(document).ready(function () {
    const markerSource = new ol.source.Vector();
    new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            }),
            new ol.layer.Vector({
                source: markerSource
            })
        ],
        view: new ol.View({
            extent: limites,
            center: centroMapa,
            zoom: -5
        })
    });

    var coordinadas = document.getElementsByClassName("tesoro");
    for (let tesoro of coordinadas) {
        let lon = tesoro.value.split(",")[0];
        let lat = tesoro.value.split(",")[1].split("~")[0];
        let id = tesoro.value.split(",")[1].split("~")[1];
        var iconFeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([lat, lon], 'EPSG:4326',
                'EPSG:3857')),
            population: 4000,
            rainfall: 500
        });

        var myStyle = new ol.style.Style({
            image: new ol.style.Circle({
                radius: 10,
                fill: new ol.style.Fill({color: 'yellow'}),
                stroke: new ol.style.Stroke({
                    color: [255, 204, 0], width: 2
                })
            }),
            text: new ol.style.Text({
                text: id,
            })
        });
        iconFeature.setStyle(myStyle);
        markerSource.addFeature(iconFeature);
    }
});