      let cont = 1;
        const markerSource_pop = new ol.source.Vector();
        const markerSource = new ol.source.Vector();

        let centro = document.getElementById("centro").value;
        let dimensiones = document.getElementById("dimensiones").value;
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

        var map_pop = new ol.Map({
            target: 'map_popup',
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM()
                }),
                new ol.layer.Vector({
                    source: markerSource_pop
                })
            ],
            view: new ol.View({
                extent: [limiteInferiorArray[0] - 500, limiteInferiorArray[1] - 500, limiteSuperiorArray[0] + 1000, limiteSuperiorArray[1] + 1000],
                center: ol.proj.fromLonLat(mapCentro),
                zoom: 0
            })
        });
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
                extent: [limiteInferiorArray[0] - 1000, limiteInferiorArray[1] - 1000, limiteSuperiorArray[0] + 1000, limiteSuperiorArray[1] + 1000],
                center: ol.proj.fromLonLat(mapCentro),
                zoom: 0
            })
        });

        var coordinadas = document.getElementsByClassName("tesoroEncontrado");
        for (let tesoro of coordinadas) {
            let first = tesoro.value.split(",")[1].split("~")[0];
            let second = tesoro.value.split(",")[0];
            let id = tesoro.value.split(",")[1].split("~")[1];
            addMarker(first, second, id, true);
        }

        map_pop.on('click', function (evt) {
            var pos = ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326');
            var x_pop = map_pop.getFeaturesAtPixel(evt.pixel);
            if (x_pop.length > 0) {
                for (var y of x_pop) {
                    markerSource_pop.removeFeature(y);
                }
                let puntosMarcados = document.getElementsByName("puntoMarcado");
                let valor = pos[1] + "," + pos[0];
                for (let pm of puntosMarcados) {
                    let pm_lon = parseFloat(pm.value.split(",")[0]);
                    let pm_lat = parseFloat(pm.value.split(",")[1]);
                    if (Math.abs(pm_lon - pos[0]) <= 0.1 && Math.abs(pm_lat - pos[1]) <= 0.1) {
                        let pm_id = pm.id.split("_")[1];
                        document.getElementById("tesorosID").removeChild(document.getElementById("div_" + pm_id));
                        break;
                    }
                }
            } else {
                addMarker(pos[0], pos[1], cont.toString(), false);
            }
        });

        function addMarker(lon, lat, id, precargando) {
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
            var myStyle;
            if (precargando)
                myStyle = new ol.style.Style({
                    image: new ol.style.Circle({
                        radius: 7,
                        fill: new ol.style.Fill({color: 'yellow'}),
                        stroke: new ol.style.Stroke({
                            color: [255, 204, 0], width: 2
                        })
                    }),
                    text: new ol.style.Text({
                        text: id,
                    })
                });
            else
                myStyle = new ol.style.Style({
                    image: new ol.style.Circle({
                        radius: 7,
                        fill: new ol.style.Fill({color: [51, 204, 255]}),
                        stroke: new ol.style.Stroke({
                            color: [0, 153, 255], width: 2
                        })
                    }),
                    text: new ol.style.Text({
                        text: id,
                    })
                });
            iconFeature.setStyle(myStyle);
            markerSource_pop.addFeature(iconFeature);
            if (precargando)
                markerSource.addFeature(iconFeature);
            else {
                let myDiv = document.createElement("div");
                myDiv.id = "div_" + cont.toString();

                let newInput = document.createElement("input");
                newInput.id = "puntoMarcado_" + cont.toString();
                newInput.setAttribute("name", "puntoMarcado");
                newInput.setAttribute("hidden", "hidden");
                newInput.value = lon + "," + lat;
                myDiv.appendChild(newInput);

                let labelInput2 = document.createElement("LABEL");
                labelInput2.id = "labelMarcado_" + cont.toString();
                labelInput2.setAttribute("for", "tesoroMarcado_" + cont.toString());
                labelInput2.innerHTML = "<b>" + cont.toString() + ". Identificación del tesoro posicionado en dicho punto: </b>&nbsp;";
                myDiv.appendChild(labelInput2);

                let newInput2 = document.createElement("input");
                newInput2.id = "tesoroMarcado_" + cont.toString();
                newInput2.setAttribute("name", "tesoroMarcado");
                newInput2.setAttribute("type", "number");
                newInput2.setAttribute("required", "required");
                newInput2.style.marginRight = "10px";
                myDiv.appendChild(newInput2);

                let newInput3 = document.createElement("input");
                newInput3.id = "imagenMarcado_" + cont.toString();
                newInput3.setAttribute("name", "imagenMarcado");
                newInput3.setAttribute("type", "file");
                newInput3.setAttribute("required", "required");
                newInput3.setAttribute("accept", "image/*");
                myDiv.appendChild(newInput3);

                document.getElementById("tesorosID").appendChild(myDiv);

                cont++;
            }
            setTimeout(function () {
                map.updateSize();
            }, 200);
        }

        $('#insertar-tesoro').submit(function (evt) {
            if (document.getElementsByName("puntoMarcado").length === 0) {
                alert("Debes marcar al menos la posición de un tesoro para poder enviar tus hallazgos.");
                evt.preventDefault();
            }
        });

        $('#encontrar-tesoro').click(function () {
            $("#overlay").addClass("active");
            $("#popup").addClass("active");
        });

        $('#btn-cerrar-popup').click(function () {
            $("#overlay").removeClass("active");
            $("#popup").removeClass("active");
        });