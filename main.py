import datetime
import json
import os

import flask
from flask import Flask, url_for, redirect, \
    render_template, session, request, Config
from flask_login import LoginManager, login_required, current_user, logout_user, login_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from mysqlx import Auth
from requests.exceptions import HTTPError
from requests_oauthlib import OAuth2Session

#
# GOOGLE_LOGIN_CLIENT_ID = "433051237268-etqt25o974bg52mmto23hs4lrg141ihq.apps.googleusercontent.com"
# GOOGLE_LOGIN_CLIENT_SECRET = "MuH32nfjnOETmzIaNAP9vPoQ"
basedir = os.path.abspath(os.path.dirname(__file__))

"""App Configuration"""


class Auth:
    """Google Project Credentials"""
    CLIENT_ID = '433051237268-etqt25o974bg52mmto23hs4lrg141ihq.apps.googleusercontent.com'
    CLIENT_SECRET = 'MuH32nfjnOETmzIaNAP9vPoQ'
    REDIRECT_URI = 'https://localhost:5000/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']


class Config:
    """Base config"""
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"


class DevConfig(Config):
    """Dev config"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """Production config"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}

"""APP creation and configuration"""
app = Flask(__name__)
app.config.from_object(config['dev'])
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


@login_manager.user_loader
def load_user(user_id):
    if user_id:
        return User.query.get(int(user_id))
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
        return redirect(url_for('index'))
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
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            if next_f:
                return redirect(next_f)
            else:
                return redirect(url_for('login'))
        return 'Could not fetch your information.'


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
    return render_template("holamundo.html")

@app.route('/f')
@login_required
def f():
    """Return a friendly HTTP greeting."""
    # t = db.find_one()
    return render_template("f.html")


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(ssl_context='adhoc', host='localhost')
