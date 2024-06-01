from fastapi import APIRouter, status
from schemas import RegisterModel, LoginModel
from database import Engine, session
from model import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder

session = session(bind=Engine)
model_auth = APIRouter(prefix="/auth")


@model_auth.get("/")
async def auth():
    return {
        "massage": "Auth page"
    }


@model_auth.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: RegisterModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu emaildan oldin ro'yxatdan o'tkazilgan")
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu username mavjud")

    new_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active

    )
    session.add(new_user)
    session.commit()
    return user


@model_auth.get('/register')
async def list():
    user = session.query(User).all()
    return jsonable_encoder(user)


@model_auth.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginModel):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Noto'g'ri email yoki parol")

    if not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Noto'g'ri email yoki parol")

    return {"message": "Tizimga muvaffaqiyatli kirdingiz", "user": db_user}


@model_auth.get("/log_out")
async def lot_out():
    return {
        "massage": "This is log out page"
    }


@model_auth.get('/login')
async def list():
    user = session.query(User).all()
    return jsonable_encoder(user)
