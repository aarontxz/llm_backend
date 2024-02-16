from typing import List, Optional
from models import Conversation, Prompt, Response  

async def create_conversation(conversation: Conversation) -> Conversation:
    try:
        await conversation.insert_one()
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

async def update_conversation(conversation_id: str, prompts: List[Prompt], responses: List[Response]) -> Optional[Conversation]:
    try:
        conversation = await Conversation.get(conversation_id)
        conversation.prompts = prompts
        conversation.responses = responses
        await conversation.update()
        return conversation
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
