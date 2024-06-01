from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from model import Product, Category
from database import SessionLocal
from schemas import ProductModel

product = APIRouter(prefix='/product')


@product.put('/{product_id}', status_code=status.HTTP_200_OK)
async def update(product_id: int, product: ProductModel, db: Session = Depends(SessionLocal)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    category_id = db.query(Category).filter(Category.id == product.category_id).first()
    if db_product and category_id:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.category_id = product.category_id

        db.commit()
        db.refresh(db_product)

        return {
            "code": 200,
            "msg": "Product update successfully",
            "Product": db_product
        }
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday category_id mavjud emas")


@product.delete('/{product_id}', status_code=status.HTTP_200_OK)
async def delete(product_id: int, db: Session = Depends(SessionLocal)):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(db_product)
    db.commit()

    return {
        "msg": "Product deleted successfully"
    }


@product.get('/{id}')
async def category_id(id: int, db: Session = Depends(SessionLocal)):
    check_product = db.query(Product).filter(Product.id == id).first()
    if check_product:
        return jsonable_encoder(check_product)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday id ga ega product yo'q")
