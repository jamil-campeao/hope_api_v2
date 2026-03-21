import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Configurações do Banco de Dados
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/hope_api"
    
    # Configurações do App
    DEBUG: bool = False
    PROJECT_NAME: str = "Hope API - SaaS Agendamentos"
    VERSION: str = "0.1.0"
    
    # Integrações (n8n Webhook Base URL)
    N8N_WEBHOOK_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings: Settings = Settings()
