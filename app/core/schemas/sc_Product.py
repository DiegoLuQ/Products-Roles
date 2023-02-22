from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import List

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


class Schema_Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    code: str = Field(min_length=5, max_length=50)
    name: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=5, max_length=250)
    sale: int = Field(gt=0)
    cost: int = Field(gt=0)
    stock: int = Field(ge=0)
    brand: str = Field(min_length=0, max_length=50)
    images: List[str]
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "code":"AD5T88",
                "description": "Una genial polera verano 2023",
                "name":"Polera Adidas",
                "sale": 1500,
                "cost": 570,
                "stock": 50,
                "brand": "Adidas",
                "images": ["www.image_1.cl", "www.image_2.cl"]
            }
        }

class Schema_Update_Producto(BaseModel):
    code: str = None
    name: str = None
    description: str = None
    sale: int = None
    cost: int = None
    stock: int = None
    brand: str = None
    images: List[str]= None