import base64

from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from mongo.entity.Juego import Juego
from mongo.entity.Mensaje import Mensaje
from mongo.entity.Tesoro import Tesoro
from mongo.repository.juego_repository import find_juego_by_id, delete_juego_by_id, save_juego
from mongo.repository.mensaje_repository import delete_all_mensajes_by_juego, find_all_mensajes_by_juego, save_mensaje

organizador_bp = Blueprint('CAZATESORO_organizador', __name__, template_folder='templates')


@organizador_bp.route("/eliminarJuego/<id>")
@login_required
def eliminar_juego(id):
    user = current_user
    juego = find_juego_by_id(id)
    if user.id == juego.creador or user.get_admin():
        delete_juego_by_id(id)
        delete_all_mensajes_by_juego(id)
    return redirect(url_for('inicio'))


@organizador_bp.route("/reiniciarJuego/<id>")
@login_required
def reiniciar_juego(id):
    user = current_user
    juego = find_juego_by_id(id)
    if user.id == juego.creador or user.get_admin():
        juego.reset_game()
        save_juego(juego)
        delete_all_mensajes_by_juego(id)
    centro_lon = juego.centro[0]
    centro_lat = juego.centro[1]
    return render_template("visualizar.html", juego=juego, user=user, centro_lon=centro_lon,
                           centro_lat=centro_lat, limite_superior=juego.dimensiones[1],
                           limite_inferior=juego.dimensiones[3])


@organizador_bp.route("/verJuego/<id>")
@login_required
def visualizar_juego_creador(id):
    user = current_user
    mensajes = find_all_mensajes_by_juego(id_juego=id)
    mensajes.sort(key=lambda x: x.fecha, reverse=False)
    juego = find_juego_by_id(id)
    return render_template("visualizar.html", juego=juego, user=user, centro_lon=juego.centro[0], mensajes=mensajes,
                           centro_lat=juego.centro[1], limite_superior=juego.dimensiones[1],
                           limite_inferior=juego.dimensiones[3])


@organizador_bp.route("/nuevoMensajeOrganizador/<id>", methods=['POST'])
@login_required
def nuevo_mensaje_organizador(id):
    user = current_user
    mensaje = request.values.get("nuevoMensaje")
    m = Mensaje(user=user, juego=id, mensaje=mensaje)
    save_mensaje(m)
    return redirect(url_for('visualizar_juego_creador', id=id))


@organizador_bp.route('/nuevoJuego')
@login_required
def nuevo_juego():
    user = current_user
    return render_template("nuevojuego.html", user=user, image=url_for('static', filename='img/mapa.png'))


@organizador_bp.route("/recogerdatos", methods=['POST'])
@login_required
def recoger_datos_creacion():
    # print(request.args)
    """Almacena el todos los tesoros en la variable juego"""
    tesoros = {}
    i = 1
    nombre = request.values.get("nombre")
    desc = request.values.get("descripcion")
    coord = request.values.getlist("punto")
    dimensiones = []
    for elem in coord:
        dimensiones.append((float(elem.split(",")[0]), float(elem.split(",")[1])))
    for coordenada, imagen, texto in zip(request.values.getlist("coordenadas"),
                                         request.files.getlist("pista_imagen"),
                                         request.values.getlist("pista_texto")):
        pista_imagen = base64.b64encode(imagen.read()).decode('utf-8')
        tesoro = Tesoro(i, float(coordenada.split(",")[0]), float(coordenada.split(",")[1]),
                        pista_texto=texto,
                        pista_imagen=pista_imagen)
        tesoros[i] = tesoro
        i += 1
    juego = Juego(diccionario_tesoros=tesoros, creador=current_user, dimensiones=dimensiones, titulo=nombre,
                  descripcion=desc)
    save_juego(juego)
    return redirect(url_for('inicio'))
