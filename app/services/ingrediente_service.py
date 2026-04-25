from sqlmodel import Session
from app.models.ingrediente import Ingrediente
from app.repositories import ingrediente_repository


def create_ingrediente(session: Session, data):
    ingrediente = Ingrediente(**data.dict())
    return ingrediente_repository.create_ingrediente(session, ingrediente)


def get_all_ingredientes(session: Session):
    return ingrediente_repository.get_all_ingredientes(session)


def get_ingrediente(session: Session, ingrediente_id: int):
    return ingrediente_repository.get_ingrediente_by_id(session, ingrediente_id)


def update_ingrediente(session: Session, ingrediente_id: int, data):
    ingrediente = get_ingrediente(session, ingrediente_id)
    if not ingrediente:
        return None

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ingrediente, key, value)

    return ingrediente_repository.update_ingrediente(session, ingrediente)


def delete_ingrediente(session: Session, ingrediente_id: int):
    ingrediente = get_ingrediente(session, ingrediente_id)
    if not ingrediente:
        return None
    ingrediente_repository.delete_ingrediente(session, ingrediente)
    return True
