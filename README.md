# llm_backend

This project is a backend component that interacts with a Large Language Model (LLM), specifically OpenAI's GPT-3 Turbo. It allows for CRUD operations on conversations containing a history of queries and responses from the LLM.

## Features

1. CRUD operations on conversations.
2. Sending prompt queries and receiving responses from the LLM.
3. Prompts containing existing conversation history as context.
4. Anonymizing and storing prompts and responses in a database for auditing purposes.

## Tech Stack

- Python >= 3.8
- FastAPI
- Pydantic
- Beanie (Async MongoDB ORM)
- OpenAI Python Client
- MongoDB 
- Docker (optional)

## Setup

### Prerequisites

1. Python 3.8 or higher installed on your system.
2. MongoDB setted up with a database named chat_db
3. have your own OPENAI_API_KEY ready in the .env file in the app folder.

### Normal set up

1. Clone this repository to your local machine:
```bash
git clone https://github.com/aarontxz/llm_backend.git
```

2. Navigate to the project directory:
```bash
cd llm_backend
```

3. Install the requirements
```bash
pip install -r requirements.txt
```

4. Navigate into app 
```bash
cd app
```

5. Running the Application
```bash
uvicorn main:app --reload
```

### Alternatively use DOCKER

1. Build the Docker Image:
```bash
docker-compose build
```

2. 
```bash 
docker-compose up
```