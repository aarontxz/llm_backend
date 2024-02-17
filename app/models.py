from pydantic import BaseModel
from typing import List
from beanie import Document

class Prompt(BaseModel):
    text: str

class Response(BaseModel):
    text: str
    
class ConversationUpdate(BaseModel):
    conversation_id: str
    prompt: str

class Conversation(Document):
    id: str
    prompts: List[Prompt]
    responses: List[Response]