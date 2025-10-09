# OEE Co-Pilot - Mining Operations Assistant

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
- **Angular Frontend**: http://localhost:4200
- **Simple Frontend**: http://localhost:3000

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
- **Google Gemini**: AI language model
- **MySQL**: Database (hosted on Aiven)
- **Pinecone**: Vector database for semantic search

### Frontend
- **Angular**: Modern web framework
- **HTML/CSS/JavaScript**: Simple frontend option

## Documentation

- [Backend Setup Guide](backend/CREDENTIALS_SETUP.md)
- [API Documentation](http://localhost:8000/docs) (when running)

## License

This project is part of the Mhash 2025 technical competition.
