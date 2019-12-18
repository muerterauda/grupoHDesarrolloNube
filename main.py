import base64
import json
import os

import flask
from flask import Flask, url_for, redirect, \
    render_template, session, request
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from mysqlx import Auth
from requests.exceptions import HTTPError
from requests_oauthlib import OAuth2Session
from mongo.entity.Juego import Juego, JuegoException
from mongo.entity.Tesoro import Tesoro
from mongo.entity.Usuario import User
from mongo.repository.juego_repository import find_juego_by_creador_and_estado, find_juego_by_participante_and_estado, \
    find_juego_by_id, save_juego, delete_juego_by_id, find_juego_by_estado
from mongo.repository.mensaje_repository import find_all_mensajes_by_juego
from mongo.repository.usuario_repository import find_user_by_id, replace_user_by_id, update_user_by_id, save_user

#
# GOOGLE_LOGIN_CLIENT_ID = "433051237268-etqt25o974bg52mmto23hs4lrg141ihq.apps.googleusercontent.com"
# GOOGLE_LOGIN_CLIENT_SECRET = "MuH32nfjnOETmzIaNAP9vPoQ"

basedir = os.path.abspath(os.path.dirname(__file__))

"""App Configuration"""


class Auth:
    """Google Project Credentials"""
    CLIENT_ID = '433051237268-etqt25o974bg52mmto23hs4lrg141ihq.apps.googleusercontent.com'
    CLIENT_SECRET = 'MuH32nfjnOETmzIaNAP9vPoQ'
    # REDIRECT_URI = 'https://nubeprueba.appspot.com/gCallback'
    REDIRECT_URI = 'https://localhost:5000/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']


class Config:
    """Base config"""
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"


config = {
    "dev": Config,
    "default": Config
}

"""APP creation and configuration"""
app = Flask(__name__)
app.config.from_object(config['dev'])
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    if user_id:
        return find_user_by_id(user_id)
    else:
        return None


""" OAuth Session creation """


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth


@app.route('/login')
def login():
    if current_user.is_authenticated:
        next_f = flask.request.args.get('next')
        if not next_f:
            next_f = session.get('next_f')
        return flask.redirect(next_f or flask.url_for('hello'))
    google = get_google_auth()
    next_f = flask.request.args.get('next')
    if next_f:
        auth_url, state = google.authorization_url(
            Auth.AUTH_URI, access_type='offline')
        session['next_f'] = next_f
    else:
        auth_url, state = google.authorization_url(
            Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)


@app.route('/gCallback')
def callback():
    next_f = session.get('next_f')
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for(next_f))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = find_user_by_id(email)
            if user is None:
                dicccionario_usuario = {'id': email, 'name': user_data['name'], 'tokens': json.dumps(token),
                                        'avatar': user_data['picture']}
                user = User(dicccionario_usuario)
                save_user(user)
                user = find_user_by_id(email)
            else:
                cambiado = False
                if user_data['name'] != user.name:
                    user.name = user_data['name']
                    cambiado = True
                if user.avatar != user_data['picture']:
                    user.avatar = user_data['picture']
                    cambiado = True
                user.tokens = json.dumps(token)
                if cambiado:
                    replace_user_by_id(user.id, user)
                else:
                    update_user_by_id(user.id, {"tokens": user.tokens})
            # session.update('user', user)
            login_user(user)
            if next_f:
                return redirect(next_f)
            else:
                return redirect(url_for('hello'))
        return 'No se pudo conseguir su informacion'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def hello():
    """Return a friendly HTTP greeting."""
    # t = db.find_one()
    user = current_user
    mis_juegos_activos = find_juego_by_participante_and_estado(user, True)
    mis_juegos_acabados = find_juego_by_participante_and_estado(user, False)
    juegos_activos = find_juego_by_estado(True)
    if user.get_admin:
        juegos_acabados = find_juego_by_participante_and_estado(user, False)
    else:
        juegos_acabados = None
    juegos_creados = find_juego_by_creador_and_estado(user)
    return render_template("index.html", mis_juegos_activos=mis_juegos_activos, mis_juegos_acabados=mis_juegos_acabados,
                           juegos_activos=juegos_activos, juegos_acabados=juegos_acabados,
                           juegos_creados=juegos_creados, user=user)


@app.route('/nuevoJuego')
@login_required
def nuevo_juego():
    # t = db.find_one()
    user = current_user
    return render_template("nuevojuego.html", user=user)


@app.route("/juego/<id>")
def ver_juego(id):
    user = current_user
    mensajes = find_all_mensajes_by_juego(id_juego=id)
    juego = find_juego_by_id(id)
    encontrados = {}
    if user.id_mongo in juego.participantes:
        encontrados = juego.get_tesoros(user)
    return render_template("juego.html", juego=juego, user=user, encontrados=encontrados, mensajes=mensajes)


@app.route("/anadirJuego/<id>", methods=['GET'])
def anadir_participante_juego(id):
    user = current_user
    juego = find_juego_by_id(id)
    juego.add_participante(user)
    save_juego(juego)
    if user.id_mongo in juego.participantes:
        jugando = True
    else:
        jugando = False
    return render_template("juego.html", juego=juego, user=user, jugando=jugando)


@app.route("/verJuego/<id>")
def visualizar_juego_creador(id):
    user = current_user
    juego = find_juego_by_id(id)
    return render_template("visualizar.html", juego=juego, user=user)


"""Funcion para eliminar un participante del juego"""


@app.route("/abandonarJuego/<id>")
def abandonar_juego(id):
    user = current_user
    juego = find_juego_by_id(id)
    juego.remove_participante(user)
    save_juego(juego)

    return redirect(url_for('hello'))


"""Funcion para reiniciar la partida"""


@app.route("/reiniciarJuego/<id>")
def reiniciar_juego(id):
    user = current_user
    juego = find_juego_by_id(id)
    if user.id == juego.creador or user.get_admin():
        juego.reset_game()
        save_juego(juego)

    return render_template("visualizar.html", juego=juego, user=user)


@app.route("/eliminarJuego/<id>")
def eliminar_juego(id):
    user = current_user
    juego = find_juego_by_id(id)
    if user.id == juego.creador or user.get_admin():
        delete_juego_by_id(id)

    return redirect(url_for('hello'))


@app.route("/verAciertos/<id>", methods=['POST'])
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
        except Exception as e:
            error = True
    save_juego(juego)
    if juego.ganador == user.id:
        mensaje = "ganador"
    elif error is True or len(recien_encontrados) == 0:
        mensaje = "ninguno"
    elif error is False:
        mensaje = "acierto"
    encontrados = juego.get_tesoros(user)
    return render_template("juego.html", juego=juego, user=user, jugando=True, encontrados=encontrados, mensaje=mensaje,
                           recienEncontrados=recien_encontrados)


@app.route("/recogerdatos", methods=['POST'])
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
        dimensiones.append((elem.split(",")[0], elem.split(",")[1]))
    for coordenada, imagen, texto in zip(request.values.getlist("coordenadas"),
                                         request.files.getlist("pista_imagen"),
                                         request.values.getlist("pista_texto")):
        pista_imagen = base64.b64encode(imagen.read()).decode('utf-8')
        tesoro = Tesoro(i, float(coordenada.split(",")[0]), float(coordenada.split(",")[1]),
                        pista_texto=texto,
                        pista_imagen=pista_imagen)
        tesoros[i] = tesoro
        i += 1
    juego = Juego(diccionario_tesoros=tesoros, creador=current_user, dimensiones=dimensiones, nombre=nombre,
                  descripcion=desc)
    save_juego(juego)
    return redirect(url_for('hello'))


@app.route('/editarJuego/<id>')
@login_required
def editar_juego(id):
    user = current_user

    juego = find_juego_by_id(id)

    return render_template("editarjuego.html", juego=juego, user=user)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(ssl_context='adhoc', host='localhost', debug=True)
