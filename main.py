from fastapi import FastAPI
from models import models
from db.database import engine
from routers import post, users, auth, vote
from config import config   

models.Base.metadata.create_all(bind = engine)
app = FastAPI()


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)









