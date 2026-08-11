import datetime

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.config import settings

password_hash=PasswordHash.recommended()


def hash_password(password:str)-> str:
    return password_hash.hash(password)

def verify_password(plain_password:str,hashed_password:str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data:dict)->str:
    payload=data.copy()
    expiration_time=(datetime.datetime.now(datetime.timezone.utc) +
                     datetime.timedelta(minutes=settings.access_token_expire_minutes))

    payload.update({
        "exp":expiration_time
    })
    access_token=jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)
    return access_token

def decode_access_token(token:str)->dict|None:
    try:
        payload=jwt.decode(token,settings.secret_key,algorithm=settings.algorithm)
        return payload
    except InvalidTokenError:
        return None