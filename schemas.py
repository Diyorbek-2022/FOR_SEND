from pydantic import BaseModel
from typing import Optional

class SingUpModel(BaseModel):
    # id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "example_11",
                "email": "example@gmail.com",
                "password": "example1234",
                "is_staff": False,
                "is_active": True
            }
        }



class Settings(BaseModel):
    authjwt_secret_key: str = 'fa1637a3690fda3a7cbb494645262913e2330f5efb5e163352eb38f1b201b4b3'


class LoginModel(BaseModel):
    username_or_email: str
    password: str

    # class Config:
    #     orm_mode = True

class OrderModel(BaseModel):
    quantity: int
    order_statuses: Optional[str] = "PENDING"
    user_id: Optional[int] = None
    product_id: Optional[int] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                # "product_id": 1,
                "order_statuses": "PENDING",
            }
        }

class OrderStatusModel(BaseModel):
    order_statuses: Optional[str] = "PENDING"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_statuses": "PENDING",
            }
        }