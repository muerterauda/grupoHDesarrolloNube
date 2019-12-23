   var maps = [];
        $(document).ready(function () {
            let todosMapas = document.getElementsByClassName("map");
            for (let m of todosMapas) {
                let centro = m.getElementsByClassName("centro")[0].value;
                let dimensiones = m.getElementsByClassName("dimensiones")[0].value;
                const markerSource = new ol.source.Vector();
                let mapCentro = [];
                mapCentro.push(parseFloat(centro.split(",")[1]));
                mapCentro.push(parseFloat(centro.split(",")[0]));
                let limiteInferior = dimensiones.split("~")[0].replace("[", "").replace("]", "");
                let limiteInferiorArray = [];
                limiteInferiorArray.push(parseFloat(limiteInferior.split(",")[1]));
                limiteInferiorArray.push(parseFloat(limiteInferior.split(",")[0]));
                limiteInferiorArray = ol.proj.transform(limiteInferiorArray, 'EPSG:4326', 'EPSG:3857');
                let limiteSuperior = dimensiones.split("~")[1].replace("[", "").replace("]", "");
                let limiteSuperiorArray = [];
                limiteSuperiorArray.push(parseFloat(limiteSuperior.split(",")[1]));
                limiteSuperiorArray.push(parseFloat(limiteSuperior.split(",")[0]));
                limiteSuperiorArray = ol.proj.transform(limiteSuperiorArray, 'EPSG:4326', 'EPSG:3857');
                maps.push(new ol.Map({
                    target: m.id,
                    layers: [
                        new ol.layer.Tile({
                            source: new ol.source.OSM()
                        }),
                        new ol.layer.Vector({
                            source: markerSource
                        })
                    ],
                    view: new ol.View({
                        extent: [limiteInferiorArray[0], limiteInferiorArray[1], limiteSuperiorArray[0], limiteSuperiorArray[1]],
                        center: ol.proj.fromLonLat(mapCentro),
                        zoom: 0
                    })
                }))
            }
        });

        function recargarMapas() {
            for (let m of maps) {
                setTimeout(function () {
                    m.updateSize();
                }, 200);
            }
        }

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

        var puntosPuestos = new Map();

        map.on('click', function (evt) {
            var pos = ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326');
            addMarker(pos[0], pos[1]);
            var x = map.getFeaturesAtPixel(evt.pixel);
            for (var y of x) {
                markerSource.removeFeature(y);
                alert("eliminado" + y.ol_iud)
            }
        });

        function addMarker(lon, lat) {
            console.log('lon:', lon);
            console.log('lat:', lat);
            /* for (var icono of puntosPuestos.values()) {
                 markerSource.removeFeature(icono);
             }*/
            var iconFeature = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.transform([lon, lat], 'EPSG:4326',
                    'EPSG:3857')),
                population: 4000,
                rainfall: 500
            });

            var myStyle = new ol.style.Style({
                image: new ol.style.Circle({
                    radius: 7,
                    fill: new ol.style.Fill({color: 'yellow'}),
                    stroke: new ol.style.Stroke({
                        color: [255, 204, 0], width: 2
                    })
                })
            });
            iconFeature.setStyle(myStyle);
            markerSource.addFeature(iconFeature);
            puntosPuestos.set(lon + lat, iconFeature);
        }


        $('#unirse-juego').click(function () {
            $("#overlay").addClass("active");
            $("#popup").addClass("active");
        });

        $('#btn-cerrar-popup').click(function () {
            $("#overlay").removeClass("active");
            $("#popup").removeClass("active");
        });