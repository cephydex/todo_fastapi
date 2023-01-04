from fastapi import APIRouter, status, Depends
from app.schemas import UserSchema
import logging
from config.logconf import LOGGER_NAME
from app.auth.sec_handler import sign_jwt
from app.auth.hashing import Hasher
from datetime import datetime
import jwt
from app.auth.auth_bearer import JWTBearer
from config.conf import settings
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

router = APIRouter()
log = logging.getLogger(LOGGER_NAME)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def user_create(user: UserSchema, db: Session = Depends(get_db)):
    success = False
    data = None
    message = 'User could not be created'
    try:
        hash_pwd = Hasher.get_password_hash(user.password)

        new_user = models.User(email=user.email, password=hash_pwd)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        data = new_user

        success = True
        message = "User created successfully!"
    except Exception as ex:
        log.error(str(ex))

    return {"success": success, "message": message, "data": data}


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(user: UserSchema, db: Session = Depends(get_db)):
    success = False
    password_verified = False
    
    _user = (
        db.query(models.User)
            .with_entities(models.User.id, models.User.email, models.User.password)
            .filter_by(email=user.email)
            .first()
    )
    
    if _user:
        # check for hash verification
        password_verified = Hasher.verify_password(user.password, _user.password)
        if password_verified:
            token = sign_jwt(_user.id, _user.email)
            in_time = datetime.now()
            dt_str = in_time.strftime("%Y-%m-%d, %H:%M:%S")
            log.info(f'User {_user.email} logged in successfully at {dt_str}')
            return token
        
        else:
            return {"success": success, "message": "Invalid credentials provided"}


@router.get("/user", status_code=status.HTTP_200_OK)
async def get_current_user(token: str = Depends(JWTBearer())) -> dict:
    JWT_SECRET = settings.jwt_secret
    JWT_ALGORITHM = settings.jwt_algorithm
    
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], verify_signature=False)
    # log.info(payload)
    return {
        "email": payload.get("email"),
        "id": payload.get("user_id")
    }