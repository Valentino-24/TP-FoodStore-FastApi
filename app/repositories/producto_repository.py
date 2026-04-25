from sqlmodel import Session
from app.models.producto import Producto


def create_producto(session: Session, producto: Producto):
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def get_all_productos(session: Session):
    return session.query(Producto).all()


def get_producto_by_id(session: Session, producto_id: int):
    return session.get(Producto, producto_id)