from typing import List, Optional
from models import Conversation, Prompt, Response, ConversationUpdate
import uuid

async def create_conversation() -> Conversation:
    try:
        conversation = Conversation(id=str(uuid.uuid4()), prompts=[], responses=[])
        await conversation.insert()
        return conversation
    except Exception as e:
        # Handle insertion error
        raise e

async def read_conversation(conversation_id: str) -> Optional[Conversation]:
    try:
        return await Conversation.get(conversation_id)
    except Exception as e:
        # Handle read error
        raise e
    
async def read_all_conversations() -> List[Conversation]:
    try:
        return await Conversation.find_all().to_list()
    except Exception as e:
        raise e

async def update_conversation(conversation_id: str, prompts: List[Prompt], responses: List[Response]) -> Optional[Conversation]:
    try:
        conversation = await Conversation.get(conversation_id)
        conversation.prompts = prompts
        conversation.responses = responses
        return await conversation.save()
    except Exception as e:
        # Handle update error
        raise e

async def delete_conversation(conversation_id: str) -> Optional[Conversation]:
    try:
        conversation = await Conversation.get(conversation_id)
        await conversation.delete()
        return conversation
    except Exception as e:
        # Handle delete error
        raise e
