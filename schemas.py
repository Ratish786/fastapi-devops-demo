from pydantic import BaseModel

class TaskSchema(BaseModel):
    name: str
    email: str
    phone: str
    password: str

class ResponseSchema(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    
    class Config:
        from_attributes = True    


class LoginSchema(BaseModel):
    email: str
    password: str 

class RefreshSchema(BaseModel):
    refresh_token: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str 

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str              