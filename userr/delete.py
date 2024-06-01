from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from model import User
from database import SessionLocal
from schemas import UserModel

user_delete = APIRouter(prefix="/user")


@user_delete.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: int, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(db_user)
    db.commit()

    return {"msg": "User deleted successfully"}
