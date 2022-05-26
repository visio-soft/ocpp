from fastapi import APIRouter, Depends, status, HTTPException
from v16.CPO.Auth import token
from v16.CPO.Schemas import schemas
from resources.database import get_db
from resources import models
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from v16.CPO.Hashing.hashing import Hash


router = APIRouter(tags=["Authentication"])

"""
Authenticates users
"""

@router.post('/auth/login')
async def auth(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials")

    access_token = token.create_access_token(
        data={"sub": user.username}
    )
    new_token = models.Token(username = user.email, password = user.password, token = access_token)
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return {"access_token": access_token, "token_type": "bearer"}


"""
Refresh token
"""
@router.post('/auth/refresh')
async def auth(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials")

    access_token = token.create_access_token(
        data={"sub": user.username}
    )
    new_token = models.Token(username = user.email, password = user.password, token = access_token)
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return {"access_token": access_token, "token_type": "bearer"}


"""
Creates new user
"""
@router.post('/auth/register', status_code=status.HTTP_201_CREATED)
async def user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(username=request.username, email=request.email, mobile=request.mobile, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user