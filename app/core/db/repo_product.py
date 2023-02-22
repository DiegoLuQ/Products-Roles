from core.config.db_con import db_ecom
from core.schemas.sc_Product import Schema_Product, Schema_Update_Producto

db_ecom.products.create_index("code")

def exist_product(code: str, brand: str) -> bool:
    try:
        product = db_ecom.products.find_one({"code": code, "brand": brand})
        if product:
            return True

        return False

    except Exception as e:
        raise e


def create_producto(data: dict) -> dict:
    try:
        exist = exist_product(data["code"], data["brand"])
        if exist:
            return False

        product = db_ecom.products.insert_one(data)
        if product:
            return {"msg": "Registered Product"}

        return {"msg": "Unregistered Product"}

    except Exception as e:
        raise e


def read_product(code: str) -> dict:
    try:
        product = db_ecom.products.find_one({"code": code})
        if product is None:
            return None
        return product
    except Exception as e:
        raise e

def read_product_id(id: str) -> dict:
    try:
        product = db_ecom.products.find_one({"_id": id})
        if product is None:
            return None
        return product
    except Exception as e:
        raise e

def read_products(is_admin:bool, is_premium:bool) -> list:
    try:
        if is_admin:
            products = [x for x in db_ecom.products.find()]
            if products:
                if len(products) == 0:
                    return []
                return products     
        if is_premium:
            products = [x for x in db_ecom.products.find({}, {"cost":0})]
            if products:
                if len(products) == 0:
                    return []
                return products
        products = [x for x in db_ecom.products.find({}, {"cost":0, "stock":0})]
        if products:
            if len(products) == 0:
                return []
            return products
        
    except Exception as e:
        raise e


def delete_product(id: str) -> dict:
    try:
        product = db_ecom.products.find_one_and_delete({"_id":id})
        if not product:
            return False

        return {"msg": "Product Removed"}
    except Exception as e:
        raise e

def update_product(id:str, data:Schema_Update_Producto) -> bool:
    try:
        product = read_product_id(id)
        if not product:
            return False
        
        object_product = dict(Schema_Update_Producto(**product))
        object_product.update(data.dict(exclude_unset = True))
        update_object_product = db_ecom.products.update_one({"_id":id}, {"$set":object_product})
        if update_object_product:
            return True
        else:
            return False
    except Exception as e:
        raise e
    
def pagination_products(skip:int = 0, limit:int=10):
    try:
        products = list(db_ecom.products.find().skip(skip).limit(limit))
        return products
    except Exception as e:
        raise e