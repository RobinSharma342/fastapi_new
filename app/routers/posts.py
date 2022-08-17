
from fastapi import APIRouter, status, HTTPException, Depends, Query
from .. import models, schema
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(tags=['Posts'])

##GET ALL POSTS
@router.get("/posts", response_model=List[schema.PostVoteOut])
async def get_posts(db: Session = Depends(get_db), limit: int | None = 5,search: str | None = "", token_data: schema.TokenData = Depends(get_current_user)):

  #  db_post = db.query(models.Post).filter(models.Post.title.contains(search)).all()

    query_result = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).filter(models.Post.title.contains(search)).group_by(models.Post.id).all()

    
    return query_result
    

##GET SINGLE POST
@router.get("/posts/{id}",response_model=schema.PostVoteOut)
#@router.get("/posts/{id}",response_model=schema.GetOut)
#@router.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db), token_data: schema.TokenData = Depends(get_current_user)):
    
    
    query_result = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()

    
    if query_result is not None:
        return query_result
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No post found with {id}")
            
#CREATE A POST

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.CreatePostOut)
async def create_post(post: schema.CreatePostIn, db: Session = Depends(get_db), token_data: schema.TokenData = Depends(get_current_user)):
    user_result: models.User = db.query(models.User).filter(models.User.email == token_data.email).first()
    
    #temp_post = {**post.dict()}
    #temp_post.update({'user_id':'test'})
    #print(temp_post)
    db_post = models.Post(user_id = user_result.id, **post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    
    return db_post

#DELETE A POST
@router.delete("/posts/{id}")
async def   delete_post(id: int, db: Session = Depends(get_db),
            token_data: schema.TokenData = Depends     (get_current_user)):

    user_result: models.User = db.query(models.User).filter(models.User.email == token_data.email).first()
    
    user_id = user_result.id
    
    post:models.Post = db.query(models.Post).filter(models.Post.id == id).first()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post is None:
        return HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "not exist")

    if post and post.user_id != user_id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "not authorized")
    
    post_query.delete()
    db.commit()
    return {"data": post}


        





#UPDATE A POST
@router.put("/posts/{id}", status_code = status.HTTP_200_OK, response_model=schema.UpdatePostOut)
async def update_post(id: int, post: schema.UpdatePostIn, db: Session = Depends(get_db),token_data: schema.TokenData = Depends(get_current_user)):

    #db_post = db.query(models.Post).filter(models.Post.id == id).update(post.dict())
    #db.commit()


    user_result: models.User = db.query(models.User).filter(models.User.email == token_data.email).first()
    
    user_id = user_result.id
    
    post_first:models.Post = db.query(models.Post).filter(models.Post.id == id).first()

    if post_first is None:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "not exist")

    if post_first and post_first.user_id != user_id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "not authorized")
    
    

    db.query(models.Post).filter(models.Post.id == id).update(post.dict())
    db.commit()
    return post



