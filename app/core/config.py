from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:admin@localhost:5432/FoodStoreApi"
    JWT_SECRET: str = "supersecretkeyquecambiarenproduccion"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440


settings = Settings()