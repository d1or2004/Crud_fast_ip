from fastapi import APIRouter, status, Depends, HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from model import Category
from database import SessionLocal
from schemas import CategoryModel
from database import session, Engine
from fastapi.encoders import jsonable_encoder

category = APIRouter(prefix="/category")


@category.put('/{id}')
async def update(id: int, data: CategoryModel, db: Session = Depends(SessionLocal)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday category_id mavjud emas")
    category.name = data.name
    db.commit()
    db.refresh(category)

    return {
        "code": 200,
        "msg": "User update Seccessfully",
        "Category": category
    }

    # if category:
    #     for key, value in data.dict(exclude_unset=True).items():
    #         setattr(category, key, value)
    #     session.commit()
    #     data = {
    #         "code": 200,
    #         "msg": "Update category"
    #     }
    #     return jsonable_encoder(data)
    # return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday id mavjud emas")


@category.delete('/{category_id}', status_code=status.HTTP_200_OK)
async def delete(category_id: int, db: Session = Depends(SessionLocal)):
    db_category = db.query(Category).filter(Category.id == category_id).first()

    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    db.delete(db_category)
    db.commit()

    return {
        "msg": "Category deleted successfully"
    }


@category.get('/{id}')
async def category_id(id: int, db: Session = Depends(SessionLocal)):
    check_category = db.query(Category).filter(Category.id == id).first()
    if check_category:
        return jsonable_encoder(check_category)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday id ga ega category yo'q")
