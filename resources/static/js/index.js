var maps = [];

window.addEventListener('resize', recargarMapas);

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
        }, 300);
    }
}

$('#unirse-juego').click(function () {
    $("#overlay").addClass("active");
    $("#popup").addClass("active");
});

$('#btn-cerrar-popup').click(function () {
    $("#overlay").removeClass("active");
    $("#popup").removeClass("active");
});