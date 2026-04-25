from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.ingrediente import IngredienteCreate, IngredienteRead, IngredienteUpdate
from app.services import ingrediente_service

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


@router.post("/", response_model=IngredienteRead)
def create_ingrediente(data: IngredienteCreate, session: Session = Depends(get_session)):
    return ingrediente_service.create_ingrediente(session, data)


@router.get("/", response_model=list[IngredienteRead])
def get_ingredientes(session: Session = Depends(get_session)):
    return ingrediente_service.get_all_ingredientes(session)


@router.get("/{ingrediente_id}", response_model=IngredienteRead)
def get_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    ingrediente = ingrediente_service.get_ingrediente(session, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente


@router.put("/{ingrediente_id}", response_model=IngredienteRead)
def update_ingrediente(
    ingrediente_id: int,
    data: IngredienteUpdate,
    session: Session = Depends(get_session),
):
    ingrediente = ingrediente_service.update_ingrediente(session, ingrediente_id, data)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente


@router.delete("/{ingrediente_id}")
def delete_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    result = ingrediente_service.delete_ingrediente(session, ingrediente_id)
    if not result:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return {"ok": True}