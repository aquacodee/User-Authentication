from jose import JWTError, jwt
from datetime import datetime, timedelta
from schema import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from db import database
from db.database import get_db
from sqlalchemy.orm import Session
from models import models
from config.config import settings




oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

#SECRET KEY
#Algorithm
#Expiriation

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minute

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentilas_exception

        token_data = schema.TokenData(id = id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code =  status.HTTP_401_UNAUTHORIZED, detail = f"could not validate credentials", 
    headers = {"WWW-Authenticate": "Bearer"})


    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    
    return user 

