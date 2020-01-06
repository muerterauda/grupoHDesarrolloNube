const markerSource = new ol.source.Vector();
var map = new ol.Map({
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
        center: ol.proj.fromLonLat([-4.4785522, 36.7151063]),
        zoom: 4
    })
});


map.on('click', function (evt) {
    var pos = ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326');
    addMarker(pos[0], pos[1]);
});

function addMarker(lon, lat) {
    console.log('lon:', lon);
    console.log('lat:', lat);

    var iconFeatures = [];

    var iconFeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.transform([lon, lat], 'EPSG:4326',
            'EPSG:3857')),
        name: 'Null Island',
        population: 4000,
        rainfall: 500
    });

    var iconStyle = new ol.style.Style({
        image: new ol.style.Icon(({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            opacity: 0.75,
            size: 50000000,
            src: "https://kinsta.com/es/wp-content/uploads/sites/8/2017/04/cambiar-wordpress-url-1.png"
        }))
    });
    iconFeature.setStyle(iconStyle);
    markerSource.addFeature(iconFeature);

}
