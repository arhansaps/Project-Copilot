# OEE Co-Pilot - Frontend-Backend Integration Guide

This guide explains how to run and integrate the Angular frontend with the Python FastAPI backend for the OEE Co-Pilot application.

## System Overview

The OEE Co-Pilot consists of:

### Backend (Python FastAPI)
- **Location**: Project root directory
- **Port**: 8000
- **Features**: 
  - Gemini 2.0 Flash LLM integration
  - Pinecone vector database
  - MySQL database connectivity
  - Natural language to SQL conversion
  - Chart generation with ECharts JSON specs

### Frontend (Angular)
- **Location**: `ops-copilot-frontend/` directory
- **Port**: 4200
- **Features**:
  - Modern responsive chat interface
  - Real-time chart visualization
  - Query suggestions
  - Enhanced loading states
  - Conversation history

## Quick Start

### 1. Start the Backend

```bash
# From project root directory
python main.py
```

The backend will start on `http://localhost:8000`

### 2. Start the Frontend

```bash
# Option 1: Use the provided script
./start_frontend.sh

# Option 2: Manual start
cd ops-copilot-frontend
npm install  # First time only
ng serve
```

The frontend will start on `http://localhost:4200`

### 3. Access the Application

Open your browser and navigate to: `http://localhost:4200`

## API Integration Details

### Backend Endpoints

The frontend communicates with these backend endpoints:

#### 1. Query Processing
```http
POST /api/query
Content-Type: application/json

{
  "query": "What % of time was the machine ACTIVE vs INACTIVE today?",
  "conversation_history": [
    {"role": "user", "content": "Previous query"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

**Response:**
```json
{
  "query": "What % of time was the machine ACTIVE vs INACTIVE today?",
  "sql_query": "SELECT status, COUNT(*) as count FROM Factory_Equipment_Logs GROUP BY status LIMIT 1000",
  "results": [
    {"status": "Active", "count": 150},
    {"status": "Inactive", "count": 50}
  ],
  "chart_spec": {
    "title": {"text": "Distribution", "left": "center"},
    "series": [{
      "name": "Data",
      "type": "pie",
      "data": [
        {"value": 150, "name": "Active"},
        {"value": 50, "name": "Inactive"}
      ]
    }]
  },
  "natural_language_response": "Based on the data, the machine was Active 75% of the time and Inactive 25% of the time today.",
  "metadata": {
    "result_count": 2,
    "execution_time_ms": 1250,
    "chart_type": "pie"
  }
}
```

#### 2. Health Check
```http
GET /health
```

#### 3. Query Suggestions
```http
GET /api/suggestions
```

#### 4. Database Schema
```http
GET /api/schema
```

### Frontend-Backend Communication

The integration is handled by the `ApiService` in the Angular frontend:

```typescript
// Enhanced error handling for LLM operations
processQuery(request: QueryRequest): Observable<QueryResponse> {
  return this.http.post<QueryResponse>(`${this.baseUrl}/api/query`, request, {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }),
    timeout: 60000 // 60 seconds for LLM/Pinecone operations
  }).pipe(
    retry(2), // Retry for network issues
    catchError(this.handleError.bind(this))
  );
}
```

## Key Integration Features

### 1. Enhanced Loading States

The frontend provides detailed loading feedback for slow LLM operations:

```typescript
// Loading stages for user feedback
loadingStage: string = '';
loadingProgress: number = 0;
estimatedTimeRemaining: number = 0;

// Stages shown to user:
// 1. "Analyzing your natural language query..."
// 2. "Processing with Gemini 2.0 Flash LLM..."
// 3. "Searching Pinecone vector database..."
// 4. "Executing SQL query on database..."
// 5. "Generating charts and visualizations..."
```

### 2. Chart Visualization

The backend generates ECharts JSON specifications that the frontend renders:

```typescript
// Backend generates chart spec
chart_spec: {
  "type": "pie",
  "title": {"text": "Distribution"},
  "series": [{
    "name": "Data",
    "type": "pie",
    "data": [{"value": 150, "name": "Active"}]
  }]
}

// Frontend renders with ECharts
<div echarts 
     [options]="getChartOptions(message.chartSpec)" 
     [initOpts]="chartInitOpts"
     class="chart">
</div>
```

### 3. Error Handling

Comprehensive error handling for different scenarios:

```typescript
private handleError(error: HttpErrorResponse): Observable<never> {
  if (error.status === 0) {
    errorMessage = 'Network connection failed. Please check your internet connection and ensure the backend server is running.';
  } else if (error.status === 500) {
    errorMessage = 'Server error occurred. This might be due to LLM processing issues or Pinecone vector search problems.';
  } else if (error.status === 408 || error.name === 'TimeoutError') {
    errorMessage = 'Request timeout. The LLM or Pinecone operations are taking longer than expected.';
  }
  // ... more error handling
}
```

### 4. Query Suggestions

The frontend loads and displays query suggestions from the backend:

```typescript
// Load suggestions on component init
private loadSuggestions(): void {
  this.apiService.getQuerySuggestions().subscribe({
    next: (suggestions) => {
      this.suggestions = suggestions;
    },
    error: (error) => {
      // Fallback suggestions if API fails
      this.suggestions = [
        "What % of time was the machine ACTIVE vs INACTIVE today?",
        "Show me all INACTIVE episodes less than 60 seconds",
        // ... more suggestions
      ];
    }
  });
}
```

## Performance Considerations

### 1. LLM Response Times

- **Normal Range**: 5-30 seconds for complex queries
- **Factors**: Query complexity, Pinecone vector search, database size
- **Frontend Handling**: Progress indicators, timeout handling, retry logic

### 2. Pinecone Vector Search

- **Purpose**: Semantic similarity search for better context
- **Performance**: Adds 2-5 seconds to response time
- **Benefit**: More accurate and contextual responses

### 3. Database Queries

- **Optimization**: Backend uses connection pooling and query optimization
- **Limits**: Results limited to 1000 rows for performance
- **Pagination**: Frontend handles large result sets with pagination

## Development Workflow

### 1. Backend Development

```bash
# Start backend in development mode
python main.py

# Backend will auto-reload on file changes
# Check logs for API calls and errors
```

### 2. Frontend Development

```bash
# Start frontend development server
cd ops-copilot-frontend
ng serve

# Frontend will auto-reload on file changes
# Hot module replacement for instant updates
```

### 3. Testing Integration

1. **Health Check**: Verify backend is running
2. **Simple Query**: Test with a basic query
3. **Chart Generation**: Verify charts render correctly
4. **Error Handling**: Test with invalid queries
5. **Performance**: Monitor response times

## Troubleshooting

### Common Issues

#### 1. Backend Not Starting
```bash
# Check Python dependencies
pip install -r requirements.txt

# Check environment variables
# Ensure .env file exists with required keys:
# - GOOGLE_API_KEY
# - PINECONE_API_KEY
# - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
```

#### 2. Frontend Build Errors
```bash
# Clear node_modules and reinstall
cd ops-copilot-frontend
rm -rf node_modules package-lock.json
npm install

# Check Angular CLI version
ng version
```

#### 3. CORS Issues
The backend is configured to allow CORS from `http://localhost:4200`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 4. API Timeout Issues
- Increase timeout in frontend API service
- Check backend logs for processing time
- Consider query complexity

### Performance Monitoring

#### Backend Monitoring
```python
# Check execution times in logs
logger.info(f"Query executed in {execution_time_ms}ms")
```

#### Frontend Monitoring
```typescript
// Monitor API response times
console.log('API Response Time:', response.metadata.execution_time_ms);
```

## Production Deployment

### Backend Deployment
1. Use production WSGI server (Gunicorn)
2. Configure reverse proxy (Nginx)
3. Set up SSL certificates
4. Configure environment variables

### Frontend Deployment
1. Build production bundle: `ng build --configuration production`
2. Serve static files with web server
3. Configure API URL for production backend
4. Set up CDN for assets

## Security Considerations

1. **API Keys**: Never expose API keys in frontend code
2. **CORS**: Configure appropriate CORS policies
3. **Input Validation**: Backend validates all inputs
4. **SQL Injection**: Backend uses parameterized queries
5. **Rate Limiting**: Consider implementing rate limiting

## Support

For issues or questions:
1. Check the logs in both frontend and backend
2. Verify all environment variables are set
3. Test with simple queries first
4. Check network connectivity
5. Review the comprehensive error messages in the UI

