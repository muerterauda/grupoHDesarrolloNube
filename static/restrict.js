function transform(extent) {
  return ol.proj.transformExtent(extent, 'EPSG:4326', 'EPSG:3857');
}

var extents = {
  India: transform([68.17665, 7.96553, 97.40256, 35.49401]),
  Argentina: transform([-73.41544, -55.25, -53.62835, -21.83231]),
  Nigeria: transform([2.6917, 4.24059, 14.57718, 13.86592]),
  Sweden: transform([11.02737, 55.36174, 23.90338, 69.10625])
};


var key = 'pk.eyJ1IjoibWFudXBsLTk3IiwiYSI6ImNrM3Vmd2JvNzBjM3kzZ3Brc253cTl0b3EifQ.06G3hmSOFoDuxGu38AT76w';

var base = new ol.layer.Tile({
  source: new ol.source.TileJSON({
    url: 'https://api.tiles.mapbox.com/v4/mapbox.world-light.json?secure&access_token=' + key,
    crossOrigin: 'anonymous'
  })
});

var overlay = new ol.layer.Tile({
  extent: extents.Argentina,
  source: new ol.source.TileJSON({
    url: 'https://api.tiles.mapbox.com/v4/mapbox.world-black.json?secure&access_token=' + key,
    crossOrigin: 'anonymous'
  })
});

var map = new ol.Map({
  layers: [base, overlay],
  target: 'map',
  view: new ol.View({
    center: [-0.119687322282424, 51.50328025],
    zoom: 4
  })
});


//overlay.setExtent(extents[event.target.id]);
