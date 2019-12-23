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

var centroMapa = ol.proj.fromLonLat(mapCentro);
var limites = [limiteInferiorArray[0] - 500, limiteInferiorArray[1] - 500, limiteSuperiorArray[0] + 500, limiteSuperiorArray[1] + 500];
