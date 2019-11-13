from mongo.entity.Juego import Juego
from mongo.entity.Usuario import User
from mongo.mongo_manager import juegos


def create_juego(juego: Juego):
    juegos.insert_one(juego.juego_to_dict())


def find_juego_by_id(juego_id) -> Juego:
    res = juegos.find_one({"id": juego_id})
    if res is not None:
        return None


def find_juego_by_creador_and_estado(user: User, estado: bool= None) -> list:
    res = juegos.find({"creador": user.id})
    lista_juegos = __generar_lista_juegos(res)
    return lista_juegos


def find_juego_by_participante_and_estado(user: User, estado: bool= None) -> list:
    res = juegos.find({"creador": user.id})
    lista_juegos = __generar_lista_juegos(res)
    return lista_juegos


def replace_juego_by_id(juego_id, new_user: User):
    juegos.replace_one({"id": juego_id}, new_user)


def update_juego_by_id(juego_id, actualizacion_user: dict):
    juegos.update_one({"id": juego_id}, {"$set": actualizacion_user})


def __generar_lista_juegos(res: dict) -> list:
    lista_juegos = []
    for x in res:
        lista_juegos.append(__generar_juego(x))
    return lista_juegos


def __generar_juego(res):
    return Juego(juego_last=res)
