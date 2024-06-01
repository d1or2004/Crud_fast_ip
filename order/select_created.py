from model import Orders, User, Product
from schemas import OrderModel
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import session, Engine

session = session(bind=Engine)

order_router = APIRouter(prefix="/orders")


@order_router.get('/')
async def select():
    orders = session.query(Orders).all()
    context = [
        {
            "id": order.id,
            "user_id": order.user_id,
            "product_id": order.product_id,
        }
        for order in orders
    ]
    return jsonable_encoder(context)


@order_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(orders: OrderModel):
    check_order = session.query(Orders).filter(Orders.id == orders.id).first()
    check_user_id = session.query(User).filter(User.id == orders.user_id).first()
    check_product_id = session.query(Product).filter(Product.id == orders.product_id).first()

    if check_order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order with this ID already exists")

    if not check_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id does not exist")

    if not check_product_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product_id does not exist")

    new_order = Orders(
        id=orders.id,
        user_id=orders.user_id,
        product_id=orders.product_id
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    data = {
        "code": 201,
        "msg": "Success",
        "order": new_order
    }
    return jsonable_encoder(data)