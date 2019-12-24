var x = 1;
let fase = 1;
let amarillo_relleno = [255, 255, 0];
let amarillo = [255, 204, 0];
let azul_relleno = [0, 204, 255];
let azul = [0, 153, 204];
let area = [];
let centroDefecto = ol.proj.fromLonLat([-4.4785522, 36.7151063]);

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
        center: centroDefecto,
        zoom: 14
    })
});

var styles = {
    'MultiPolygon': new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'blue',
            lineDash: [4],
            width: 3
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0, 0, 255, 0.1)'
        })
    })
};
var styleFunction = function (feature) {
    return styles[feature.getGeometry().getType()];
};

function resetearZona() {
    fase = 1;
    area = [];
    let coords = document.getElementsByName("punto");
    for (let c of coords) {
        c.value = "";
    }
    document.querySelectorAll('.tesoro').forEach(e => e.remove());
    markerSource.clear();
    var view = new ol.View({
        extent: [-1401164.5156785853, 4272654.721278845, 584975.2411983708, 5479536.252219139],
        center: centroDefecto,
        zoom: 14
    });
    map.setView(view);
    setTimeout(function () {
        map.updateSize();
    }, 200);
}

map.on('click', function (evt) {
        var pos = ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326');
        var x = map.getFeaturesAtPixel(evt.pixel);
        if (x.length > 0) {
            alert("Ya existe un punto aquí. Si se trata de un tesoro, elminelo antes de crear otro en sus proximidades.")
        } else {
            if (fase === 1) {
                addMarker(pos[0], pos[1], evt, azul, azul_relleno);
                area.push(pos);
                // console.log(area);
                document.getElementById("punto" + area.length.toString()).value = pos[1].toString() + " , " + pos[0].toString();

                if (area.length === 4) {
                    // console.log("area llena");
                    fase = 2;
                    let x_med = 0;
                    let y_med = 0;
                    for (let c of area) {
                        x_med += c[0];
                        y_med += c[1];
                    }
                    x_med = x_med / 4;
                    y_med = y_med / 4;
                    let goodOldCoordinates = ol.proj.transform([x_med, y_med], 'EPSG:4326', 'EPSG:3857');
                    let limiteInferior = ol.proj.transform(area[3], 'EPSG:4326', 'EPSG:3857');
                    let limiteSuperior = ol.proj.transform(area[1], 'EPSG:4326', 'EPSG:3857');
                    var view = new ol.View({
                        extent: [limiteInferior[0], limiteInferior[1], limiteSuperior[0], limiteSuperior[1]],
                        center: goodOldCoordinates,
                        zoom: 0
                    });
                    map.setView(view);
                    markerSource.clear();
                }
            } else {
                addMarker(pos[0], pos[1], evt, amarillo, amarillo_relleno);
            }
        }
    }
);

function addMarker(lon, lat, evt, color, relleno) {
    var iconFeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.transform([lon, lat], 'EPSG:4326',
            'EPSG:3857')),
        population: 4000,
        rainfall: 500
    });
    var myStyle;
    if (fase === 1)
        myStyle = new ol.style.Style({
            image: new ol.style.Circle({
                radius: 7,
                fill: new ol.style.Fill({color: relleno}),
                stroke: new ol.style.Stroke({
                    color: color, width: 2
                })
            })
        });
    else
        myStyle = new ol.style.Style({
            image: new ol.style.Circle({
                radius: 7,
                fill: new ol.style.Fill({color: relleno}),
                stroke: new ol.style.Stroke({
                    color: color, width: 2
                })
            }),
            text: new ol.style.Text({
                text: x.toString(),
            })
        });
    iconFeature.setStyle(myStyle);
    markerSource.addFeature(iconFeature);
    if (fase !== 1) {
        $('#listas').append('<div class="card bg-light tesoro" id="tesoro' + x + '" style="margin-top: 10px;">\
                            <div class="card-header text-center">\
                                <h5>Tesoro con identificador: ' + x + '</h5>\
                                <input hidden type="text" name="coordenadas" value="' + lon + ', ' + lat + '"/>\
                            </div>\
                            <div class="card-body">\
                                <div class="card-text">\
                                    <div class="input-group mb-3">\
                                        <label class="sr-only" for="pista_texto' + x + '">Pista</label>\
                                        <div class="input-group-prepend">\
                                                <span class="input-group-text"\
                                                      id="pt' + x + '"><b>Pista</b></span>\
                                        </div>\
                                        <input type="text" class="form-control" required id="pista_texto' + x + '"\
                                               name="pista_texto"\
                                               placeholder="Escriba una pista para poder encontrar el tesoro"\
                                               aria-describedby="pt' + x + '">\
                                    </div>\
                                    <div class="input-group mb-3">\
                                        <div class="input-group-prepend">\
                                            <span class="input-group-text" id="inputGroupFileAddon' + x + '"><b>Pista visual</b></span>\
                                        </div>\
                                        <div class="custom-file">\
                                            <input type="file" accept="image/*" class="custom-file-input" id="inputGroupFile' + x + '"\
                                                   aria-describedby="inputGroupFileAddon' + x + '" name="pista_imagen" required placeholder="Escoge una imagen">\
                                            <label class="custom-file-label" for="inputGroupFile' + x + '">Escoge una imagen</label>\
                                        </div>\
                                    </div>\
                                    <div class="text-center">\
                                        <button class="btn btn-danger eliminarTesoro" onclick="eliminarTesoro(this.id)"\
                                            type="button" id="eliminar' + evt.pixel + 'eliminar' + x + '">Eliminar tesoro</button>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                        <script>\
                        $("#inputGroupFile' + x + '").on("change",function(){\
                        var fileName = $(this).val();\
                        $(this).next(".custom-file-label").html(fileName);\
                        })\
                        </script>');
        x++;
        document.getElementById("nTesoros").value = x;
    }
    setTimeout(function () {
        map.updateSize();
    }, 200);
}

function eliminarTesoro(id) {
    let info = id.toString().split('eliminar');
    var pixeles = info[1].split(",");
    var x = map.getFeaturesAtPixel(pixeles);
    if (x.length > 0) {
        for (var y of x) {
            markerSource.removeFeature(y);
        }
    } else {
        alert("Error al borrar tesoro");
    }
    document.getElementById("listas").removeChild(document.getElementById("tesoro" + info[2].toString()))
    setTimeout(function () {
        map.updateSize();
    }, 200);
}


$('#myForm').submit(function (evt) {
    if (document.getElementsByClassName("tesoro").length === 0) {
        alert("Debes crear al menos un tesoro para poder crear un juego");
        evt.preventDefault();
    }
});