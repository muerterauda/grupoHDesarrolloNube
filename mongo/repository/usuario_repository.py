from mongo.entity.Usuario import User
from mongo.mongo_manager import usuarios


def save_user(user: User):
    usuarios.insert_one(user.user_to_dict())


def find_user_by_id(user_id) -> User:
    res = usuarios.find_one({"id": user_id})
    if res is not None:
        return User(res)


def replace_user_by_id(user_id, new_user: User):
    usuarios.replace_one({"id": user_id}, new_user)


def update_user_by_id(user_id, actualizacion_user: dict):
    usuarios.update_one({"id": user_id}, {"$set": actualizacion_user})
