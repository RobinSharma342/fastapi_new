from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schema, util

from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Login'])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user_data: schema.User = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    
    if not user_data:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect username/password")

    is_valid_password = util.verify_password(form_data.password, user_data.password)
    if not is_valid_password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect username/password")

    access_token = create_access_token({"sub":user_data.email})
    print(access_token)

    return {"access_token":access_token, "token_type": "bearer"}

