from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import User as UserSchema
from auth.auth import AuthHandler
import uuid


def get_db() -> Session:
    """
    This function complete the full cycle of a db session (open, close).
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


router = APIRouter()
auth_handler = AuthHandler()


@router.get("s/", tags=["USERS"])
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


@router.post("/register", status_code=201, tags=["USERS"])
async def register_user(userschema: UserSchema, db: Session = Depends(get_db)):
    try:
        if (
            db.query(UserModel)
            .filter(UserModel.username == userschema.username)
            .first()
        ):
            raise HTTPException(
                status_code=400, detail="The username is already on use"
            )
        user = UserModel(
            id=str(uuid.uuid4()),
            username=userschema.username,
            password=auth_handler.get_password_hash(userschema.password),
        )
        db.add(user)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    else:
        db.commit()
        return (
            db.query(UserModel)
            .filter(UserModel.username == userschema.username)
            .first()
        )


@router.post("/login", status_code=201, tags=["AUTH"])
async def login_user(userschema: UserSchema, db: Session = Depends(get_db)):
    try:
        user = (
            db.query(UserModel)
            .filter(UserModel.username == userschema.username)
            .first()
        )
        if user and auth_handler.verify_password(userschema.password, user.password):
            token = auth_handler.encode_token(user.username)
            return {"access_token": token}
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/unprotected", status_code=200, tags=["AUTH"])
async def get_unprotected():
    return {"message": "unprotected"}


@router.get("/protected", tags=["AUTH"])
async def get_protected(username=Depends(auth_handler.auth_wrapper)):
    return {"Welcome": username}
