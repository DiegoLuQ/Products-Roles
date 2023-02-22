from typing import List
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from datetime import date

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Schema_User(BaseModel):
    username:str
    password:str
    email:str
    is_active=False
    is_admin=False
    is_premium=False

    class Config():
        schema_extra = {
            "example": {
                "email":"prueba@gmail.com",
                "password":"123456",
                "username":"diego"
            }
        }

class Schema_User_APIKey(Schema_User):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    api_key:str
    start_date : date
    exp_date : date  

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Update_API_Key(BaseModel):
    exp_date: date