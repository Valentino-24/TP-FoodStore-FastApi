from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.producto import ProductoCreate, ProductoRead , ProductoUpdate
from app.services import producto_service

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoRead)
def create_producto(data: ProductoCreate, session: Session = Depends(get_session)):
    return producto_service.create_producto(session, data)


@router.get("/", response_model=list[ProductoRead])
def get_productos(session: Session = Depends(get_session)):
    return producto_service.get_productos(session)


@router.get("/{producto_id}", response_model=ProductoRead)
def get_producto(producto_id: int, session: Session = Depends(get_session)):
    return producto_service.get_producto(session, producto_id)

@router.put("/{producto_id}", response_model=ProductoRead)
def update_producto(producto_id: int, data: ProductoUpdate, session: Session = Depends(get_session)):
    return producto_service.update_producto(session, producto_id, data)


@router.delete("/{producto_id}")
def delete_producto(producto_id: int, session: Session = Depends(get_session)):
    return producto_service.delete_producto(session, producto_id)