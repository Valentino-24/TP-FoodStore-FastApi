from sqlmodel import Session, select
from app.models.ingrediente import Ingrediente


def create_ingrediente(session: Session, ingrediente: Ingrediente):
    session.add(ingrediente)
    session.commit()
    session.refresh(ingrediente)
    return ingrediente


def get_all_ingredientes(session: Session):
    return session.exec(select(Ingrediente)).all()


def get_ingrediente_by_id(session: Session, ingrediente_id: int):
    return session.get(Ingrediente, ingrediente_id)


def update_ingrediente(session: Session, ingrediente: Ingrediente):
    session.add(ingrediente)
    session.commit()
    session.refresh(ingrediente)
    return ingrediente


def delete_ingrediente(session: Session, ingrediente: Ingrediente):
    session.delete(ingrediente)
    session.commit()