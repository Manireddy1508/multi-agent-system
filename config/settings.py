"""
Configuración del proyecto usando variables de entorno.
"""
import os
import json
from typing import Optional, Any, Dict
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Configuración de la aplicación."""
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "ROKECT_NC") 
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL")
    
    # Firebase Configuration
    firebase_credentials_path: str = os.getenv("FIREBASE_CREDENTIALS_PATH")
    firestore_project_id: str = os.getenv("FIRESTORE_PROJECT_ID")
    
    # API Configuration
    api_title: str = os.getenv("API_TITLE")
    api_version: str = os.getenv("API_VERSION")
    api_description: str = os.getenv("API_DESCRIPTION")
    
    # CORS Configuration
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra='ignore' 


# Instancia global de configuración
settings = Settings()
