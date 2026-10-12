from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User, Role
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_token, decode_token
from app.core.config import settings
router=APIRouter(prefix='/auth',tags=['Authentication'])
@router.post('/register',response_model=TokenResponse,status_code=201)
def register(data:RegisterRequest,db:Session=Depends(get_db)):
    if db.scalar(select(User).where(User.email==data.email)): raise HTTPException(409,'Email already registered')
    u=User(email=data.email,full_name=data.full_name,password_hash=hash_password(data.password),role=Role.CUSTOMER); db.add(u); db.commit(); db.refresh(u)
    return TokenResponse(access_token=create_token(str(u.id),'access',timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)),refresh_token=create_token(str(u.id),'refresh',timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)))
@router.post('/login',response_model=TokenResponse)
def login(data:LoginRequest,db:Session=Depends(get_db)):
    u=db.scalar(select(User).where(User.email==data.email))
    if not u or not u.is_active or not verify_password(data.password,u.password_hash): raise HTTPException(401,'Invalid credentials')
    return TokenResponse(access_token=create_token(str(u.id),'access',timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)),refresh_token=create_token(str(u.id),'refresh',timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)))
@router.post('/refresh',response_model=TokenResponse)
def refresh(refresh_token:str,db:Session=Depends(get_db)):
    try: p=decode_token(refresh_token)
    except Exception: raise HTTPException(401,'Invalid refresh token')
    if p.get('type')!='refresh': raise HTTPException(401,'Refresh token required')
    u=db.get(User,int(p['sub']))
    if not u or not u.is_active: raise HTTPException(401,'Inactive user')
    return TokenResponse(access_token=create_token(str(u.id),'access',timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)),refresh_token=create_token(str(u.id),'refresh',timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)))
