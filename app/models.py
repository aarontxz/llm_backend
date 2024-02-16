from pydantic import BaseModel
from typing import List
from beanie import Document

class Prompt(BaseModel):
    text: str

class Response(BaseModel):
    text: str

class Conversation(Document):
    id: str
    prompts: List[Prompt]
    responses: List[Response]