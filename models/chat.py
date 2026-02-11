"""
Modelos Pydantic para el sistema de chat.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class MessageRole(str, Enum):
    """Roles disponibles para los mensajes."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Modelo para un mensaje individual del chat."""
    role: MessageRole = Field(..., description="Rol del mensaje")
    content: str = Field(..., min_length=1, description="Contenido del mensaje")


class ChatRequest(BaseModel):
    """Modelo para la request del endpoint /chat."""
    messages: List[ChatMessage] = Field(..., min_items=1, description="Historial de mensajes")
    agent_id: str = Field(..., min_length=1, description="ID del agente a utilizar")


class ChatResponse(BaseModel):
    """Modelo para la response del endpoint /chat."""
    reply: str = Field(..., description="Respuesta generada por el agente")


class ChatHistory(BaseModel):
    """Modelo para el historial guardado en Firestore."""
    chat_id: str = Field(..., description="ID único del chat")
    user_id: str = Field(..., description="ID del usuario")
    agent_id: str = Field(..., description="ID del agente utilizado")
    messages: List[ChatMessage] = Field(..., description="Historial completo de mensajes")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de creación")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de última actualización")


class FirebaseUser(BaseModel):
    """Modelo para el usuario decodificado de Firebase."""
    uid: str = Field(..., description="ID único del usuario")
    email: Optional[str] = Field(None, description="Email del usuario")
    email_verified: Optional[bool] = Field(None, description="Si el email está verificado")
