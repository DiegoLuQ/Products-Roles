from datetime import datetime, timedelta, date
from typing import Optional
from jose import jwt, JWTError, ExpiredSignatureError
from core.config.config import settings
import pytz
chile_tz = pytz.timezone("America/Santiago")

def create_access_token(data:dict, expires_delta:Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                                algorithm=settings.ALGORITHM)
        return encode_jwt
        
    except Exception as e:
        print(e)


class Token_Methods:
    def __init__(self, data:str, date:int):
        self:data = data
    
    @staticmethod
    def decode_(data:str) -> dict:
        decoded = jwt.decode(token=data, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    @staticmethod
    def convert_int_date(date:int) -> date:
        convert_date = datetime.fromtimestamp(date, chile_tz)
        return convert_date
    
    @staticmethod
    def encode_(data:dict) -> str:
        encode_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encode_jwt
    
    @staticmethod
    def compare_datenow_dateexp(date):
        convert_date = datetime._fromtimestamp(date, chile_tz)
        date_now = datetime.now(chile_tz)
        if date_now < convert_date:
            return True
        return False
    
def refresh_access_token(date, expires_delta:int=None):
    try:
        decode_token = jwt.decode(token=data, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)

        convert_date = Token_Methods.convert_int_date(decode_token["exp"])
        if convert_date < datetime.now(chile_tz):
            return {"msg":"Token Expirado"}

        new_access_token = create_access_token(decode_token)
        return new_access_token

    except ExpiredSignatureError:
        return {"msg": "Token expirado"}
    except JWTError:
        return {"msg": "Token Invalido"}
    except Exception as e:
        raise e
    
