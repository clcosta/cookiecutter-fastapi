from datetime import timedelta

from core.models import SettingsJWT, User
from core.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    HEADER_TYPE,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)

from core.db import DataBase
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from passlib.context import CryptContext

router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@AuthJWT.load_config
def load_config_from_settings():
    return SettingsJWT(
        authjwt_algorithm=ALGORITHM,
        authjwt_secret_key=SECRET_KEY,
        authjwt_access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        authjwt_refresh_token_expires=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
        authjwt_header_type=HEADER_TYPE,
    )


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )

{% if cookiecutter.database|lower() == 'n' %}
@router.post("/login")
def login(user: User, Authorize: AuthJWT = Depends()):
    db = DataBase()
    if not db.check_exists_user(user.username):
        raise HTTPException(status_code=401, detail="User not found!")
    db_password = db.get_password(user.username)
    if verify_password(user.password, db_password):
        token = Authorize.create_access_token(subject=user.username)
        refresh_token = Authorize.create_refresh_token(subject=user.username)
        return {"access_token": token, "refresh_token": refresh_token}
    raise HTTPException(status_code=401, detail="Wrong password")

@router.post("/signup")
def signup(user: User):
    db = DataBase()
    if db.check_exists_user(user.username):
        raise HTTPException(status_code=401, detail="Already exists an user with that username!")
    if user.username and user.password:
        db.add_user(user.username, hash_password(user.password))
        return {"message":"User created successfully!"}
    raise HTTPException(status_code=400, detail="Username and password is required")
{% else %}
@router.post("/login")
def login(user: User, Authorize: AuthJWT = Depends()):
    with DataBase() as db:
        if not db.exists_user(user.username):
            raise HTTPException(status_code=401, detail="User not found!")
        db_password = db.get_password(user.username)
        if verify_password(user.password, db_password):
            token = Authorize.create_access_token(subject=user.username)
            refresh_token = Authorize.create_refresh_token(subject=user.username)
            return {"access_token": token, "refresh_token": refresh_token}
        raise HTTPException(status_code=401, detail="Wrong password")

@router.post("/signup")
def signup(user: User):
    with DataBase() as db:
        if db.exists_user(user.login):
            raise HTTPException(status_code=401, detail="Usurário já existe")
        if user.login and user.password:
            db.add_user(user.login, hash_password(user.password))
            return {"message":"Usuário criado com sucesso!"}
        raise HTTPException(status_code=400, detail="Login e senha são obrigatórios")
{% endif %}

@router.post("/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    user = Authorize.get_jwt_subject()
    new_token = Authorize.create_access_token(subject=user)
    return {"access_token": new_token}