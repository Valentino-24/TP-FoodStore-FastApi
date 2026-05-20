from fastapi import APIRouter, Depends

from app.schemas.usuario import UsuarioCreate, LoginRequest, Token, UsuarioRead
from app.services import auth_service
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=Token)
def register(data: UsuarioCreate):
    return auth_service.register_user(data)


@router.post("/login", response_model=Token)
def login(data: LoginRequest):
    return auth_service.login_user(data)


@router.get("/me", response_model=UsuarioRead)
def me(usuario: Usuario = Depends(auth_service.get_current_user)):
    return usuario
