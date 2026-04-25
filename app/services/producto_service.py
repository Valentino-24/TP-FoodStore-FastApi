from sqlmodel import Session, select

from app.models.producto import Producto
from app.models.producto_categoria import ProductoCategoria
from app.models.producto_ingrediente import ProductoIngrediente
from app.models.categoria import Categoria
from app.repositories import producto_repository
from app.models.ingrediente import Ingrediente

from fastapi import HTTPException
from sqlmodel import delete
from sqlalchemy import delete


def delete_producto(session: Session, producto_id: int):
    producto = session.get(Producto, producto_id)

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    session.exec(
        delete(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id
        )
    )

    session.exec(
        delete(ProductoIngrediente).where(
            ProductoIngrediente.producto_id == producto_id
        )
    )

    session.delete(producto)

    session.commit()

    return {"ok": True}


def update_producto(session: Session, producto_id: int, data):
    producto = session.get(Producto, producto_id)

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # 🔹 ACTUALIZAR CAMPOS
    if data.nombre is not None:
        producto.nombre = data.nombre

    if data.descripcion is not None:
        producto.descripcion = data.descripcion

    if data.precio_base is not None:
        producto.precio_base = data.precio_base

    if data.stock_cantidad is not None:
        producto.stock_cantidad = data.stock_cantidad

    if data.disponible is not None:
        producto.disponible = data.disponible

    if data.imagenes is not None:
        producto.imagenes = data.imagenes

    session.exec(
        delete(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id
        )
    )

    session.exec(
        delete(ProductoIngrediente).where(
            ProductoIngrediente.producto_id == producto_id
        )
    )

    if not data.categorias:
        raise HTTPException(status_code=400, detail="Debe tener al menos una categoría")

    principales = [c for c in data.categorias if c.es_principal]

    if len(principales) != 1:
        raise HTTPException(
            status_code=400,
            detail="Debe haber una sola categoría principal"
        )

    for cat in data.categorias:
        categoria = session.get(Categoria, cat.id)
        if not categoria:
            raise HTTPException(
                status_code=400,
                detail=f"La categoria con id {cat.id} no existe"
            )

        session.add(ProductoCategoria(
            producto_id=producto.id,
            categoria_id=cat.id,
            es_principal=cat.es_principal
        ))

    for ing_id in data.ingredientes_ids:
        session.add(ProductoIngrediente(
            producto_id=producto.id,
            ingrediente_id=ing_id
        ))

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return build_producto_response(session, producto)

def build_producto_response(session: Session, producto: Producto):
    categorias_rel = session.exec(
        select(ProductoCategoria).where(ProductoCategoria.producto_id == producto.id)
    ).all()

    categorias = []
    for rel in categorias_rel:
        cat = session.get(Categoria, rel.categoria_id)
        if cat:
            categorias.append({
                "id": cat.id,
                "nombre": cat.nombre,
                "es_principal": rel.es_principal
            })

    ingredientes_rel = session.exec(
        select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto.id)
    ).all()

    ingredientes = []
    for rel in ingredientes_rel:
        ing = session.get(Ingrediente, rel.ingrediente_id)
        if ing:
            ingredientes.append({
                "id": ing.id,
                "nombre": ing.nombre
            })

    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio_base": producto.precio_base,
        "imagenes": producto.imagenes,
        "stock_cantidad": producto.stock_cantidad,
        "disponible": producto.disponible,
        "categorias": categorias,
        "ingredientes": ingredientes
    }


def create_producto(session: Session, data):

    for ing_id in data.ingredientes_ids:
        ingrediente = session.get(Ingrediente, ing_id)
        if not ingrediente:
            raise HTTPException(
                status_code=400,
                detail=f"El ingrediente con id {ing_id} no existe"
            )

    if not data.categorias:
        raise HTTPException(status_code=400, detail="Debe tener al menos una categoría")

    principales = [c for c in data.categorias if c.es_principal]

    if len(principales) != 1:
        raise HTTPException(
            status_code=400,
            detail="Debe haber una sola categoría principal"
        )

    producto = Producto(
        nombre=data.nombre,
        descripcion=data.descripcion,
        precio_base=data.precio_base,
        imagenes=data.imagenes,
        stock_cantidad=data.stock_cantidad,
        disponible=data.disponible
    )

    session.add(producto)
    session.commit()
    session.refresh(producto)

    for cat in data.categorias:
        categoria = session.get(Categoria, cat.id)
        if not categoria:
            raise HTTPException(
                status_code=400,
                detail=f"La categoria con id {cat.id} no existe"
            )

        session.add(ProductoCategoria(
            producto_id=producto.id,
            categoria_id=cat.id,
            es_principal=cat.es_principal
        ))

    for ing_id in data.ingredientes_ids:
        session.add(ProductoIngrediente(
            producto_id=producto.id,
            ingrediente_id=ing_id
        ))

    session.commit()

    return build_producto_response(session, producto)


def get_productos(session: Session):
    productos = producto_repository.get_all_productos(session)
    return [build_producto_response(session, p) for p in productos]


def get_producto(session: Session, producto_id: int):
    producto = producto_repository.get_producto_by_id(session, producto_id)
    if not producto:
        return None
    return build_producto_response(session, producto)