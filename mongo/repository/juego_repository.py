from mongo.entity.Juego import Juego
from mongo.entity.Usuario import User
from mongo.mongo_manager import juegos
from bson.objectid import ObjectId


def save_juego(juego: Juego):
    juegos.insert_one(juego.juego_to_dict())


def find_juego_by_id(juego_id) -> Juego:
    res = juegos.find_one({"id": juego_id})
    if res is not None:
        return __generar_juego(res)


def find_juego_by_creador_and_estado(user: User, estado: bool= None) -> list:
    diccionario_busqueda = {"creador": user.id}
    if estado is not None:
        diccionario_busqueda['estado'] = estado 
    res = juegos.find(diccionario_busqueda)
    lista_juegos = __generar_lista_juegos(res)
    return lista_juegos


def find_juego_by_participante_and_estado(user: User, estado: bool= None) -> list:
    diccionario_busqueda = {"participantes."+user.id_mongo: {"$exists": True}}
    if estado is not None:
        diccionario_busqueda['estado'] = estado 
    res = juegos.find(diccionario_busqueda)
    lista_juegos = __generar_lista_juegos(res)
    return lista_juegos


def replace_juego_by_id(juego_id, new_juego: Juego):
    juegos.replace_one({"_id": ObjectId(juego_id)}, new_juego)


def update_juego_by_id(juego_id, actualizacion_juego: dict):
    juegos.update_one({"_id": ObjectId(juego_id)}, {"$set": actualizacion_juego})


def __generar_lista_juegos(res: dict) -> list:
    lista_juegos = []
    for x in res:
        lista_juegos.append(__generar_juego(x))
    return lista_juegos


def __generar_juego(res):
    return Juego(juego_last=res)
