from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from ..models.order import Order


class OrderRepository: 

    def __init__(self, db: Session):
        self.db = db


    def save_order(self, order: Order):
        self.db.add(order)
        self.db.commit()

    def get_order_by_id(self, id: int) -> Order:
        return self.db.query(Order).filter(Order.id == id).first()
    
    def get_orders_query(self, sort_asc: bool = True):
        query = self.db.query(Order)
        if sort_asc:
            query = query.order_by(asc(Order.created_at))
        else:
            query = query.order_by(desc(Order.created_at))
        return query