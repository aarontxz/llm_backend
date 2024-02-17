from fastapi import FastAPI, HTTPException, Depends
from typing import List
from models import Conversation, Prompt, Response, ConversationUpdate
from motor.motor_asyncio import AsyncIOMotorClient
from crud import create_conversation, read_conversation, update_conversation, delete_conversation
from beanie import init_beanie
import openai
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Set OpenAI API Key
openai.api_key = openai_api_key


# Dependency to initialize Beanie
async def initialize_beanie():
    # MongoDB connection URI
    client = AsyncIOMotorClient("mongodb://aaronxz:aaaron@127.0.0.1:27017/")
    # Initialize Beanie
    await init_beanie(database=client["chat_db"], document_models=[Conversation])

@app.post("/conversations/{conversation_id}", response_model=Conversation)
async def createConversation(conversation_id: str, beanie: None = Depends(initialize_beanie)):
    return await create_conversation(conversation_id)

@app.get("/conversations/{conversation_id}", response_model=Conversation)
async def readConversations(conversation_id: str, beanie: None = Depends(initialize_beanie)):
    return await read_conversation(conversation_id)

@app.put("/conversations", response_model=Conversation)
async def updateConversation(data: ConversationUpdate, 
    beanie: None = Depends(initialize_beanie)
):
    conversation_id = data.conversation_id
    prompt = data.prompt
    # Retrieve the conversation from the database
    conversation = await read_conversation(conversation_id)
    
    if not prompt:
        prompt = "hello what is a bulldog"

    # Append the prompt to the conversation's prompts list
    conversation.prompts.append(Prompt(text = prompt))

    # Generate prompt using the existing prompts and responses
    prompt_text = generate_prompt_text(conversation)

    # Send prompt query to OpenAI
    try:
        response_text = openai.Completion.create(
            engine="davinci-002",  # Specify the OpenAI engine
            prompt=prompt_text,
            max_tokens=100  # Specify maximum tokens for the response
        ).choices[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Store the new response
    conversation.responses.append(Response(text=response_text))

    # Update the conversation in the database
    updated_conversation = await update_conversation(
        conversation_id, conversation.prompts, conversation.responses
    )

    return updated_conversation

@app.delete("/conversations/{conversation_id}", response_model=Conversation)
async def deleteConversation(conversation_id: str, beanie: None = Depends(initialize_beanie)):
    return await delete_conversation(conversation_id)

def generate_prompt_text(conversation: Conversation) -> str:
    # Generate prompt based on conversation history
    prompt_text = ""
    if conversation.prompts and conversation.responses:
        for i in range(len(conversation.prompts)):
            prompt_text += f"User: {conversation.prompts[i]}\n"
            if i==len(conversation.prompts):
                prompt_text += f"AI: "
            else:
                prompt_text += f"AI: {conversation.responses[i]}\n"
    return prompt_text



