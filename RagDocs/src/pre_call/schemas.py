from pydantic import BaseModel


class ConversationCreateReq(BaseModel):
    conversationId: str
    personaId: str
