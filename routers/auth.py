from fastapi import  APIRouter,status, Depends, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from models import models
from utils import utils
from schema import schema
from oauth2 import oauth2


router = APIRouter(tags = ['Authentication'])

@router.post("/login", response_model = schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm  = Depends(), db: Session = Depends(get_db)):


    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()


    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid credential")

    

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credential")

    

    #create a token 
    #return token


    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

