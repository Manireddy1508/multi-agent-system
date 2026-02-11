"""
Servicio para interactuar con Firestore.
"""
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import firebase_admin
from firebase_admin import credentials, firestore as admin_firestore

from config.settings import settings
from models.chat import ChatHistory, ChatMessage


class FirestoreService:
    """Servicio para manejar operaciones con Firestore."""
    
    def __init__(self):
        """Inicializa el servicio de Firestore."""
        self._db = None
        self._initialize_firebase()
        
    def _initialize_firebase(self):
        """Inicializa Firebase Admin SDK."""
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.firebase_credentials_path)
            firebase_admin.initialize_app(cred, {
                'projectId': settings.firestore_project_id,
            })
        
        self._db = admin_firestore.client()
    
    @property
    def db(self):
        """Getter para la instancia de Firestore."""
        return self._db
    
    def save_chat_history(
        self, 
        user_id: str, 
        agent_id: str, 
        messages: List[ChatMessage],
        chat_id: Optional[str] = None
    ) -> str:
        """
        Guarda el historial del chat en Firestore.
        
        Args:
            user_id: ID del usuario
            agent_id: ID del agente
            messages: Lista de mensajes del chat
            chat_id: ID del chat (opcional, se genera automáticamente si no se proporciona)
        
        Returns:
            str: ID del chat guardado
        """
        if not chat_id:
            chat_id = str(uuid.uuid4())
        
        # Convertir mensajes a diccionarios
        messages_dict = [
            {"role": msg.role.value, "content": msg.content} 
            for msg in messages
        ]
        
        chat_data = {
            "user_id": user_id,
            "agent_id": agent_id,
            "messages": messages_dict,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        # Guardar en Firestore
        self.db.collection("chats").document(chat_id).set(chat_data)
        
        return chat_id
    
    # async def get_chat_history(self, chat_id: str) -> Optional[ChatHistory]:
    #     """
    #     Obtiene el historial de un chat específico.
        
    #     Args:
    #         chat_id: ID del chat
        
    #     Returns:
    #         ChatHistory o None si no existe
    #     """
    #     doc_ref = self.db.collection("chats").document(chat_id)
    #     doc = doc_ref.get()
        
    #     if not doc.exists:
    #         return None
        
    #     data = doc.to_dict()
        
    #     # Convertir mensajes de vuelta a objetos ChatMessage
    #     messages = [
    #         ChatMessage(role=msg["role"], content=msg["content"])
    #         for msg in data["messages"]
    #     ]
        
    #     return ChatHistory(
    #         chat_id=chat_id,
    #         user_id=data["user_id"],
    #         agent_id=data["agent_id"],
    #         messages=messages,
    #         created_at=data["created_at"],
    #         updated_at=data["updated_at"]
    #     )
    
    async def get_user_chats(
        self, 
        user_id: str, 
        agent_id: Optional[str] = None,
        limit: int = 50
    ) -> List[ChatHistory]:
        """
        Obtiene los chats de un usuario específico.
        
        Args:
            user_id: ID del usuario
            agent_id: ID del agente (opcional, para filtrar)
            limit: Límite de resultados
        
        Returns:
            Lista de historiales de chat
        """
        query = self.db.collection("chats").where("user_id", "==", user_id)
        
        if agent_id:
            query = query.where("agent_id", "==", agent_id)
        
        query = query.order_by("updated_at", direction=firestore.Query.DESCENDING).limit(limit)
        
        docs = query.stream()
        
        chat_histories = []
        for doc in docs:
            data = doc.to_dict()
            messages = [
                ChatMessage(role=msg["role"], content=msg["content"])
                for msg in data["messages"]
            ]
            
            chat_history = ChatHistory(
                chat_id=doc.id,
                user_id=data["user_id"],
                agent_id=data["agent_id"],
                messages=messages,
                created_at=data["created_at"],
                updated_at=data["updated_at"]
            )
            chat_histories.append(chat_history)
        
        return chat_histories
    
    async def update_chat_history(
        self, 
        chat_id: str, 
        messages: List[ChatMessage]
    ) -> bool:
        """
        Actualiza el historial de un chat existente.
        
        Args:
            chat_id: ID del chat
            messages: Nueva lista de mensajes
        
        Returns:
            bool: True si se actualizó correctamente
        """
        try:
            messages_dict = [
                {"role": msg.role.value, "content": msg.content} 
                for msg in messages
            ]
            
            update_data = {
                "messages": messages_dict,
                "updated_at": datetime.utcnow()
            }
            
            self.db.collection("chats").document(chat_id).update(update_data)
            return True
        except Exception:
            return False


# Instancia global del servicio
firestore_service = FirestoreService()
