from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schema, util
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(tags=['Users'])

##GET ALL USERS
@router.get("/users", response_model=List[schema.UserOut], response_model_exclude=["password"])
async def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()

    return users

##GET SINGLE USER
@router.get("/users/{id}", response_model=schema.UserOut, response_model_exclude=["password"])
async def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

 
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No user found with {id}")
    else:
        return user
        
            


#CREATE A USER

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.CreateUserOut, response_model_exclude=["password"])
async def create_user(user: schema.CreateUserIn, db: Session = Depends(get_db)):

    new_user = models.User(**user.dict())
    new_user.password = util.get_password_hash(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



