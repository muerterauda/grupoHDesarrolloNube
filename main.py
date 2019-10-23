
import pymongo
from flask import Flask, render_template
app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://GrupoH:H6keoAzQKEXBg46j@desarrollonubegrupoh-0rfcm.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client['pruebaNube']['prueba']


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    t = db.find_one()
    return render_template("holamundo.html", prueba=t['nombreAsignatura'])


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
