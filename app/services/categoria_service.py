from sqlmodel import Session, select
from app.models.categoria import Categoria
from app.models.producto_categoria import ProductoCategoria
from app.repositories import categoria_repository


def create_categoria(session: Session, data):
    categoria = Categoria(**data.dict())
    return categoria_repository.create_categoria(session, categoria)


def get_all_categorias(session: Session):
    return categoria_repository.get_all_categorias(session)


def get_categoria(session: Session, categoria_id: int):
    return categoria_repository.get_categoria_by_id(session, categoria_id)


def update_categoria(session: Session, categoria_id: int, data):
    categoria = get_categoria(session, categoria_id)
    if not categoria:
        return None

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(categoria, key, value)

    return categoria_repository.update_categoria(session, categoria)


def delete_categoria(session: Session, categoria_id: int):
    categoria = get_categoria(session, categoria_id)
    if not categoria:
        return None

    productos_asociados = session.exec(
        select(ProductoCategoria).where(ProductoCategoria.categoria_id == categoria_id)
    ).all()

    for prod_cat in productos_asociados:
        session.delete(prod_cat)

    session.commit()

    children = session.exec(
        select(Categoria).where(Categoria.parent_id == categoria_id)
    ).all()

    for child in children:
        child.parent_id = None
        session.add(child)

    session.commit()

    categoria_repository.delete_categoria(session, categoria)
    return True