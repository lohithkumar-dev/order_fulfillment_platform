from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from app.db.session import get_db
from app.db.models.user import User
from app.core.security import decode_token
bearer=HTTPBearer()
def current_user(credentials: HTTPAuthorizationCredentials=Depends(bearer), db:Session=Depends(get_db)):
    try: payload=decode_token(credentials.credentials)
    except JWTError: raise HTTPException(status_code=401,detail='Invalid or expired token')
    if payload.get('type')!='access': raise HTTPException(status_code=401,detail='Access token required')
    user=db.get(User,int(payload['sub']))
    if not user or not user.is_active: raise HTTPException(status_code=401,detail='Inactive or missing user')
    return user
def require_roles(*roles):
    def checker(user=Depends(current_user)):
        if user.role.value not in roles: raise HTTPException(status_code=403,detail='Insufficient permissions')
        return user
    return checker
