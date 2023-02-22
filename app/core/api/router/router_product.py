from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from typing import List
from fastapi.responses import JSONResponse
from core.schemas.sc_Product import Schema_Product, Schema_Update_Producto
from core.schemas.sc_User import Schema_User_APIKey
from core.db.repo_product import (
    create_producto,
    read_product,
    read_products,
    delete_product,
    update_product,
    pagination_products,
)
from core.api.router.router_login import get_current_user_from_token
from fastapi.exceptions import RequestValidationError
from ratelimit import limits

router = APIRouter()


@router.post(
    "/add", description="""
    ### Hello, I'm a endpoint and I can create products but i can only 5 calls per hour
    """
)
@limits(calls=5, period=3600)
def add_product(
    data: Schema_Product,
    current_user: Schema_User_APIKey = Depends(get_current_user_from_token),
) -> Schema_Product:
    try:
        if current_user["is_premium"] or current_user["is_admin"]:
            data = create_producto(jsonable_encoder(data))
            if data:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"msg": "Product not registered, code already registered"},
            )
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg":"You don't have the permissions for this action"})
    except Exception as e:
        raise e


@router.get("/products_free", description="""
    ### Hello, I'm a endpoint and I can get products but i can only 5 calls per minute
    """)
@limits(calls=5, period=70)
def list_products() -> List[Schema_Product]:
    try:
        data = read_products(is_admin=False,is_premium=False)
        if data:
            print(len(data))
            return JSONResponse(status_code=status.HTTP_200_OK, content=data)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=data)
    except Exception as e:
        raise e


@router.get("/products_premium", description="""
    ### Hello, I'm a endpoint and I can get products with premium properties but i can only 5 calls per 30 seconds
    """)
@limits(calls=5, period=30)
def list_products_premium(
    current_user: Schema_User_APIKey = Depends(get_current_user_from_token),
) -> List[Schema_Product]:
    try:
        if current_user["is_admin"]:
            data = read_products(is_admin=current_user["is_admin"], is_premium=current_user["is_premium"])
            if data:
                return JSONResponse(status_code=status.HTTP_200_OK, content=data)
        if current_user["is_premium"]:
            data = read_products(is_admin=current_user["is_admin"],is_premium=current_user["is_premium"])
            if data:
                return JSONResponse(status_code=status.HTTP_200_OK, content=data)
        else:
            data = read_products(is_admin=False,is_premium=False)
            return JSONResponse(status_code=status.HTTP_200_OK, content=data)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=data)
    except Exception as e:
        print(e)


@router.get("/product/{code}", description="""
    ### Hello, I'm a endpoint and I can get product but i can only 5 calls per minute.
    """)
@limits(calls=5, period=60)
def retrive_product(code: str) -> Schema_Product:
    try:
        data = read_product(code)
        if data is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"msg": "product does not exist"},
            )
        if data:
            return JSONResponse(status_code=status.HTTP_200_OK, content=data)
    except Exception as e:
        raise e


@router.delete("/delete/{id}", description="""
    ### Hello, I'm a endpoint and I can delete product but i can only 3 calls per hour.
    """)
@limits(calls=5, period=60)
def remove_product(
    id: str, current_user: Schema_User_APIKey = Depends(get_current_user_from_token)
):
    try:
        if current_user["is_admin"]:
            data = delete_product(id)
            if data:
                return JSONResponse(status_code=status.HTTP_200_OK, content=data)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"msg": "product does not exist"},
            )
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"msg": "You don't have the permissions for this action"},
        )
    except Exception as e:
        raise e


@router.patch("/update/{id}", description="""
    ### Hello, I'm a endpoint and I can update product but i can only 3 calls per hour.
    """)
@limits(calls=3, period=3600)
def patch_product(
    id: str,
    data: Schema_Update_Producto,
    current_user: Schema_User_APIKey = Depends(get_current_user_from_token),
) -> str:
    try:
        if current_user["is_admin"]:
            data = update_product(id, data=data)
            if data:
                return JSONResponse(
                    status_code=status.HTTP_200_OK, content={"msg": "Modified product"}
                )
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"msg": "Producto not found"},
            )
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"msg": "You don't have the permissions for this action"},
        )
    except Exception as e:
        raise e


@router.get("/pagination", description="""
    ### Hello, I'm a endpoint and I can get products.
    """)
def pagination(skip: int = 0, limit: int = 10):
    try:
        data = pagination_products(skip=skip, limit=limit)
        return data
    except Exception as e:
        raise e
