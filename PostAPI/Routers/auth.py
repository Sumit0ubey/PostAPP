from fastapi.security.oauth2 import OAuth2PasswordRequestForm # type: ignore
from fastapi import APIRouter, status, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore

from ..oauth2 import create_access_token
from ..database import get_db
from ..schema import Token
from ..utils import verify
from ..models import User


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    access_token = create_access_token(data={"user_id":user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout", status_code=status.HTTP_200_OK)
def logout():
    return {"logout": "logout the user"}

