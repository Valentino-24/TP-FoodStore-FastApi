from sqlmodel import Session, select
from app.models.categoria import Categoria


def create_categoria(session: Session, categoria: Categoria):
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def get_all_categorias(session: Session):
    return session.exec(select(Categoria)).all()


def get_categoria_by_id(session: Session, categoria_id: int):
    return session.get(Categoria, categoria_id)


def update_categoria(session: Session, categoria: Categoria):
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def delete_categoria(session: Session, categoria: Categoria):
    session.delete(categoria)
    session.commit()