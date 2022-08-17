from fastapi import APIRouter, status, HTTPException, Depends

from app.oauth2 import get_current_user
from .. import models, schema, util
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(tags=['Votes'])


# CREATE A VOTE

@router.post("/vote", status_code=status.HTTP_201_CREATED)
async def create_vote(vote: schema.VoteIn, db: Session = Depends(get_db), token_data: schema.TokenData = Depends(get_current_user)):

    user_result: models.User = db.query(models.User).filter(models.User.email == token_data.email).first()

    print(f"user id {user_result.id}" )
    print(f"vote id {vote.postid}")

    is_vote_exist: models.Vote = db.query(models.Vote).filter(models.Vote.user_id == user_result.id, models.Vote.post_id == vote.postid).count()
    
    print(is_vote_exist)
    
    if vote.direction:
        if is_vote_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user_result.id} already voted for post {vote.postid}")
        else:
            db_vote = models.Vote(user_id = user_result.id, post_id = vote.postid)
            db.add(db_vote)
            db.commit()
            db.refresh(db_vote)
            return {"message":"vote added"}
    else:
        if is_vote_exist:
            db.query(models.Vote).filter(models.Vote.user_id == user_result.id, models.Vote.post_id == vote.postid).delete()
            db.commit()
            return {"message":"vote deleted"}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"user {user_result.id} already downvoted for post {vote.postid}")

