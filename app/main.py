from fastapi import FastAPI, HTTPException
from typing import List
from models import Conversation, Prompt, Response
from motor.motor_asyncio import AsyncIOMotorClient
from crud import create_conversation, read_conversation, update_conversation, delete_conversation
from beanie import init_beanie
import openai

app = FastAPI()

# Set OpenAI API Key
openai.api_key = "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"

@app.post("/conversations/", response_model=Conversation)
async def create_conversation_1(conversation: Conversation):
    # MongoDB connection URI
    client = AsyncIOMotorClient("mongodb://aaronxz:aaaron@127.0.0.1:27017/")

    # # Initialize Beanie
    await init_beanie(database=client["chat_db"], document_models=[Conversation])
    
    print("hello")
    # Generate prompt using conversation history
    prompt_text = generate_prompt_text(conversation)
    
    # Send prompt query to OpenAI
    try:
        response_text = openai.Completion.create(
            engine="davinci-002",  # Specify the OpenAI engine
            prompt=prompt_text,
            max_tokens=100  # Specify maximum tokens for the response
        ).choices[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    # Store response in conversation history
    conversation.responses.append(Response(text=response_text))
    print(conversation)
    
    # Save conversation to database
    await create_conversation(conversation)
    
    return conversation

@app.get("/conversations/{conversation_id}", response_model=List[Conversation])
async def read_conversations(conversation_id: str):
    return await read_conversation(conversation_id)

@app.put("/conversations/{conversation_id}", response_model=Conversation)
async def updateconversation(conversation_id: str, prompts: List[Prompt], responses: List[Response]):
    return await update_conversation(conversation_id, prompts, responses)

@app.delete("/conversations/{conversation_id}", response_model=Conversation)
async def deleteconversation(conversation_id: str):
    return await delete_conversation(conversation_id)

def generate_prompt_text(conversation: Conversation) -> str:
    # Generate prompt based on conversation history
    prompt_text = ""
    if conversation.prompts and conversation.responses:
        for i in range(len(conversation.prompts)):
            prompt_text += f"User: {conversation.prompts[i].text}\n"
            prompt_text += f"AI: {conversation.responses[i].text}\n"
    return prompt_text
