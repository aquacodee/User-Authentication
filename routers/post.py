from fastapi import FastAPI, Response,status, HTTPException, Depends,APIRouter
from typing import  List, Optional
from schema import schema
from models import models
from db.database import  get_db
from sqlalchemy.orm import Session
from oauth2 import oauth2


router  = APIRouter(prefix = "/posts", tags = ['Posts'])


@router.get("/", response_model = List[schema.Post])
def root(db: Session =  Depends(get_db), current_user: int =  Depends(oauth2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute(""" SELECT * FROM  posts""")
    #posts = cursor.fetchall()

   
    posts  = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    return  posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schema.Post)
def create_post(post: schema.PostCreate, db: Session =  Depends(get_db), current_user: int =  Depends(oauth2.get_current_user) ):
    #cursor.execute(""" INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING  * """,
    #(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
   
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return  new_post






@router.get("/{id}", response_model = schema.Post)
def get_post(id: int, db: Session =  Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE ID = %s """, (str(id),))
    #post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found.")


    return  post



@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM post WHERE ID = %s returning * """, (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Not authorized for this action')

    post_query.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model = schema.Post)
def updated_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE post SET title = %s, content= %s, published = %s WHERE id = %s RETURNING * """,
    # (post.title, post.content,post.published, str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist.")



    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Not authorized for this action')

    post_query.update(updated_post.dict(), synchronize_session = False)       
    db.commit()

    return  post_query.first()  