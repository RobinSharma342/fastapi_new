from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    

    email: EmailStr
    password: str
    
   
class UserOut(User):
    created_at: datetime


    class Config:
        orm_mode = True



class CreateUserIn(User):
    pass
    
    

class CreateUserOut(User):
    created_at: datetime

    
    class Config:
        orm_mode = True


class Login(BaseModel):

    email: EmailStr
    password: str
    

class Token(BaseModel):
    

    access_token: str
    token_type: str

class TokenData(BaseModel):
    email:str

class Post(BaseModel):
    
    title: str
    content: str
    published: bool
    created_at: datetime
    

class GetOut(Post):
    user_id: int
    
    
    
    class Config:
        orm_mode = True


class PostVoteOut(BaseModel):
    Post: GetOut
    vote: int
    
    class Config:
        orm_mode = True
               

class CreatePostIn(BaseModel):

    title: str
    content: str
    published: bool = True
    


class CreatePostOut(CreatePostIn):

    title: str
    content: str
    published: bool
    created_at: datetime

    
    class Config:
        orm_mode = True

class UpdatePostIn(BaseModel):

    title: str
    content: str
    published: bool

class UpdatePostOut(BaseModel):

    title: str
    class Config:
        orm_mode = True

class VoteIn(BaseModel):

    postid: int
    direction: bool
    
class VoteOut(BaseModel):

    postid: int
    # userid: int
    
    class Config:
        orm_mode = True
    
