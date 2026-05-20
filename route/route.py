from fastapi import APIRouter , Depends , status, Request, Body
from service import service
from db import get_db
from schemas import ResponseSchema,TaskSchema,LoginSchema,RefreshSchema,LoginResponse,RefreshResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/signup",response_model=ResponseSchema)
def register(user: TaskSchema, db: Session = Depends(get_db)):
    return service.register_service(db, user)

@router.post("/login" , status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return service.login_user(body, db)

@router.get("/is_auth", status_code=status.HTTP_200_OK)    
def is_authenticated(request: Request, db: Session = Depends(get_db)):
    return service.is_authenticated(request, db)

@router.post("/refresh", response_model=RefreshResponse)
def refresh(body: RefreshSchema, db: Session = Depends(get_db)):
    return service.refresh_access_token(body.refresh_token, db)



