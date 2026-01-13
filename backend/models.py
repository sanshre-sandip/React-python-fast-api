from pydantic import BaseModel, EmailStr

# User registration model
class User(BaseModel):
    username: str
    email: EmailStr
    password: str

# User login model
class LoginUser(BaseModel):
    email: EmailStr
    password: str
