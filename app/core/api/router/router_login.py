from fastapi import APIRouter, Depends, Response, HTTPException, status, Request, Cookie
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, date
from core.api.utils import OAuth2PasswordBearerWithCookie
from core.db.repo_login import retrive_username, register_user
from core.helpers.hashing_password import Hasher
from core.config.config import settings
from core.helpers.security import create_access_token
from core.schemas.sc_User import Schema_User, Schema_User_APIKey
from core.helpers.generate_apikey import generate_api_key
from jose import jwt, JWTError
from ratelimit import limits
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/login/token")



def authenticate_user(username: str, password: str) -> dict:
    try:
        user = retrive_username(username)
        if not user:
            return False
        pass_hash = user["password"]
        if not Hasher.verify_password(password, pass_hash):
            return False
        return user
    except Exception as e:
        raise e


def credential_exception(msg: str, headers={}):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=msg, headers=headers
    )

def get_current_user_from_token(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise credential_exception("Could not validate credentials")
        
    except JWTError:
        raise credential_exception("Could not validate credentials")
    
    user = retrive_username(username)
    if user is None:
        raise credential_exception("Could not validate credentials")
    return user    

@router.post("/token", description=settings.DESCRIPTION_ROUTE)
def login_for_access(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise credential_exception(
            msg="Incorrect usernamer or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = create_access_token(
        data={
            "sub": user["username"],
            "is_admin": user["is_admin"],
            "exp_date": user["exp_date"],
            "api_key": user["api_key"],
            "is_premium":user["is_premium"]},
        expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register/")
@limits(calls=1, period=15)
def add_new_user(response:Response,model: Schema_User):
    try:
        data_apikey = generate_api_key()
        model.password = Hasher.get_pass_hash(model.password)
        data_user = jsonable_encoder(model)
        data = Schema_User_APIKey(**data_apikey, **data_user)
        new_user = register_user(jsonable_encoder(data))
        if new_user["status"] == 403:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg":new_user["msg"]})
        if new_user["status"] == 201:
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_user)
    except Exception as e:
        raise e
