from fastapi import FastAPI, Response,status, HTTPException, Depends,APIRouter
from utils import utils
from schema import schema
from models import models
from db.database import engine, get_db
from sqlalchemy.orm import Session



router = APIRouter(prefix ="/users", tags = ['Users'])


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    #hashingn the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    
    
    return  new_user

@router.get("/{id}", response_model = schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == id).first()

    if not users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id {id} does not exist.")
    
    return users