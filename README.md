Project Title
Multimodal Agentic AI Shopping Assistant
Overview

This project is a multimodal agentic AI shopping assistant that enables users to discover products through natural language queries or product images.

The system leverages LangGraph-based agent workflows, custom tool calling, vision-language models, and structured product databases to provide intelligent product recommendations, ratings analysis, and transaction execution.

Key Features
1. Product Search ==> Natural language product discovery , Price-based filtering , Organic product filtering , Semantic product recommendations
2. Image-Based Shopping ==>  Upload product images , Vision-language model extracts product attributes , Automatic product matching from database , Multimodal retrieval workflow
3. Agentic Workflows ==> LangGraph multi-step agent orchestration , Tool calling and decision making , Autonomous workflow execution , Memory-aware conversational interactions
4. Shopping Operations ==> Product recommendation , Customer rating aggregation , Product comparison , Order placement and confirmation

Architecture:

User Query / Product Image
            │
            ▼
      LangGraph Agent
            │
 ┌──────────┼──────────┐
 ▼          ▼          ▼
Search    Ratings    Vision
Tool       Tool       Tool
 │          │          │
 ▼          ▼          ▼
SQLite    SQLite     LLM Vision
Database  Reviews     Model
            │
            ▼
      Recommendation
            │
            ▼
      Order Processing

Tech Stack: 
Generative AI
LangChain
LangGraph
Groq LLM
Llama 4 Scout
Qwen3-32B
Data & Storage
SQLite
Vector Retrieval Concepts
Structured Product Database
Application Layer
Streamlit
Python
Deployment
Docker

Project structure: 

agentic-ai-shopping-assistant/

├── app.py
├── shopping_agent.py
├── reviews.py
├── create_database.py
├── store.db
├── resources/
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md

Environment Variables ==> Create a .env file: GROQ_API_KEY=your_api_key

Run Application ==> streamlit run app.py

Docker Deployment

1. Build Docker Image ==> docker build -t shopping-agent .
2. Run Container ==> docker run -p 8501:8501 --env-file .env shopping-agent
3. Open: ==> http://localhost:8501
