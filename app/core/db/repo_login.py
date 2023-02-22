from core.config.db_con import db_ecom
from core.schemas.sc_User import Schema_User, Schema_User_APIKey


collection_user = db_ecom.users


def register_user(data: Schema_User_APIKey) -> dict:
    try:
        user_exist = collection_user.find_one({"username": data["username"]})
        if user_exist:
            return {"msg":"The user exists", "status": 403}

        email_exist = collection_user.find_one({"email": data["email"]})
        if email_exist:
            return {"msg":"The email exists", "status": 403}

        data = collection_user.insert_one(data)
        if data:
            new_data = collection_user.find_one({"_id": data.inserted_id})
            return {"data": new_data, "status": 201}
    except Exception as e:
        raise e


def retrive_username(username: str) -> dict:
    try:
        data = collection_user.find_one({"username": username}, {"_id": 0})
        return data
    except Exception as e:
        raise e
