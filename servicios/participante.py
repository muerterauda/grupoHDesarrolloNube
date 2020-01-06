import base64

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user

from mongo.entity.Mensaje import Mensaje
from mongo.repository.juego_repository import find_juego_by_id, save_juego
from mongo.repository.mensaje_repository import find_all_mensajes_by_juego, save_mensaje

participante_bp = Blueprint('CAZATESORO_participante', __name__, template_folder='templates')


@participante_bp.route("/nuevoMensaje/<id>", methods=['POST'])
@login_required
def nuevo_mensaje(id):
    user = current_user
    mensaje = request.values.get("nuevoMensaje")
    m = Mensaje(user=user, juego=id, mensaje=mensaje)
    save_mensaje(m)
    return redirect(url_for('ver_juego', id=id))


@participante_bp.route("/juego/<id>")
@login_required
def ver_juego(id):
    user = current_user
    mensajes = find_all_mensajes_by_juego(id_juego=id)
    mensajes.sort(key=lambda x: x.fecha, reverse=False)
    juego = find_juego_by_id(id)
    encontrados = {}
    if user.id_mongo in juego.participantes:
        encontrados = juego.get_tesoros(user)
    return render_template("juego.html", juego=juego, user=user, encontrados=encontrados, mensajes=mensajes,
                           centro_lon=juego.centro[0],
                           centro_lat=juego.centro[1], limite_superior=juego.dimensiones[1],
                           limite_inferior=juego.dimensiones[3])


@participante_bp.route("/anadirJuego/<id>", methods=['GET'])
@login_required
def anadir_participante_juego(id):
    user = current_user
    juego = find_juego_by_id(id)
    juego.add_participante(user)
    save_juego(juego)
    if user.id_mongo in juego.participantes:
        jugando = True
    else:
        jugando = False
    return render_template("juego.html", juego=juego, user=user, jugando=jugando, centro_lon=juego.centro[0],
                           centro_lat=juego.centro[1], limite_superior=juego.dimensiones[1],
                           limite_inferior=juego.dimensiones[3])


@participante_bp.route("/abandonarJuego/<id>")
@login_required
def abandonar_juego(id):
    user = current_user
    juego = find_juego_by_id(id)
    juego.remove_participante(user)
    save_juego(juego)
    return redirect(url_for('inicio'))


@participante_bp.route("/verAciertos/<id>", methods=['POST'])
@login_required
def recoger_datos_jugador(id):
    user = current_user
    juego = find_juego_by_id(id)
    puntos_coor = request.values.getlist("puntoMarcado")
    tesoros_id = request.values.getlist("tesoroMarcado")
    imagenes = request.files.getlist("imagenMarcado")
    error = False
    recien_encontrados = []
    mensaje = None
    for p, t, imagen in zip(puntos_coor, tesoros_id, imagenes):
        try:
            imagen_marcado = base64.b64encode(imagen.read()).decode('utf-8')
            encontrado = juego.encontrar_tesoro(identificador_tesoro=int(t), latitud=p.split(",")[0],
                                                longitud=p.split(",")[1],
                                                imagen_tesoro=imagen_marcado, descubridor=user)
            if encontrado is True:
                recien_encontrados.append(t)
        except Exception:
            error = True
    save_juego(juego)
    if juego.ganador == user.id:
        mensaje = "ganador"
    elif error is True or len(recien_encontrados) == 0:
        mensaje = "ninguno"
    elif error is False:
        mensaje = "acierto"
    encontrados = juego.get_tesoros(user)
    mensajes = find_all_mensajes_by_juego(id_juego=id)
    mensajes.sort(key=lambda x: x.fecha, reverse=False)
    return render_template("juego.html", juego=juego, user=user, jugando=True, encontrados=encontrados, mensaje=mensaje,
                           mensajes=mensajes,
                           recienEncontrados=recien_encontrados, centro_lon=juego.centro[0],
                           centro_lat=juego.centro[1], limite_superior=juego.dimensiones[1],
                           limite_inferior=juego.dimensiones[3])
