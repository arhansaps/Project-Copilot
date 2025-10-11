# OEE Co-Pilot - Mining Operations Assistant
Made for Manipal Hackathon 2025.
A full-stack application that provides intelligent analysis of mining operations data using natural language queries and AI-powered insights.

## Project Structure

```
ops_copilot/
├── backend/                 # Backend API and services
│   ├── main.py             # FastAPI application
│   ├── langchain_agent.py  # AI agent for natural language processing
│   ├── database.py         # Database operations
│   ├── config_loader.py    # Configuration management
│   ├── config.json         # API keys and database credentials
│   ├── test_credentials.py # Credential testing script
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Docker configuration
│   ├── docker-compose.yml  # Docker Compose setup
│   └── Cleaned Datasets/   # Sample data files
├── frontend/               # Frontend applications
│   ├── ops-copilot-frontend/  # Angular application
│   └── simple_frontend.html   # Simple HTML frontend
└── venv/                   # Python virtual environment
```

## Quick Start
Create a file called backend.json in the backend folder.
In the file, paste:
```
{
  "google_api_key": "Enter your Gemini API Key here",
  "pinecone_api_key": "",
  "database": {
    "host": "database-ishaanmaheshwari2906-85b8.l.aivencloud.com",
    "user": "avnadmin",
    "password": "AVNS_SlDzxmKFpE7g0pMq71l",
    "database": "MiningAndFactoryData",
    "port": 14333
  }
}
```
Enter your actual Gemini API Key.
Save the file.

### 1. Backend Setup
```bash
cd backend
python3 test_credentials.py  # Test configuration
./start_with_new_credentials.sh  # Start API server
```

### 2. Frontend Setup
```bash
cd frontend/ops-copilot-frontend
npm install
ng serve --port 4200
```

### 3. Access Application
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

## Features

- 🤖 **Natural Language Queries**: Ask questions about mining operations in plain English
- 📊 **Data Visualization**: Automatic chart generation for data insights
- 🗄️ **Database Integration**: Connect to Aiven MySQL database
- 🔧 **CSV Upload**: Upload and process mining data files
- 🐳 **Docker Support**: Containerized deployment
- 🌐 **REST API**: Full REST API for frontend integration

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **LangChain**: AI/LLM integration
- **Google Gemini 2.0 Flash**: AI language model
- **MySQL**: Database (hosted on Aiven)
- **Pinecone**: Vector database for semantic search

### Frontend
- **Angular**: Modern web framework

## Documentation

- [Backend Setup Guide](backend/CREDENTIALS_SETUP.md)
- [API Documentation](http://localhost:8000/docs) (when running)
