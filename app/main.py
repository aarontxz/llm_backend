from fastapi import FastAPI, HTTPException, Depends
from typing import List
from models import Conversation, Prompt, Response, ConversationUpdate
from motor.motor_asyncio import AsyncIOMotorClient
from crud import create_conversation, read_conversation, update_conversation, delete_conversation, read_all_conversations
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

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Dependency to initialize Beanie
async def initialize_beanie():
    # MongoDB connection URI
    client = AsyncIOMotorClient("mongodb://aaronxz:aaaron@127.0.0.1:27017/")
    # Initialize Beanie
    await init_beanie(database=client["chat_db"], document_models=[Conversation])

@app.post("/conversations", response_model=Conversation)
async def createConversation(beanie: None = Depends(initialize_beanie)):
    return await create_conversation()

@app.get("/conversations/{conversation_id}", response_model=Conversation)
async def readConversations(conversation_id: str, beanie: None = Depends(initialize_beanie)):
    return await read_conversation(conversation_id)

@app.get("/conversations", response_model=List[Conversation])
async def readAllConversations(beanie: None = Depends(initialize_beanie)):
    return await read_all_conversations()

@app.put("/conversations", response_model=Conversation)
async def updateConversation(data: ConversationUpdate, 
    beanie: None = Depends(initialize_beanie)
):
    conversation_id = data.conversation_id
    prompt = data.prompt
    # Retrieve the conversation from the database
    conversation = await read_conversation(conversation_id)

    # Append the prompt to the conversation's prompts list
    conversation.prompts.append(Prompt(text = prompt))

    # Generate prompt using the existing prompts and responses
    prompt_text = generate_prompt_text(conversation)

    # Send prompt query to OpenAI
    try:
        response_text = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Specify the OpenAI engine
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
    if conversation.prompts:
        for i in range(len(conversation.prompts)):
            prompt_text += f"User: {conversation.prompts[i].text}\n"
            if i==len(conversation.prompts)-1:
                prompt_text += f"AI: "
            else:
                prompt_text += f"AI: {conversation.responses[i].text}\n"
    print(prompt_text)
    return prompt_text



