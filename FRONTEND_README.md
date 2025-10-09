# OEE Co-Pilot Frontend

A modern, responsive Angular frontend for the OEE Co-Pilot application that provides a seamless chatbot interface for natural language to SQL query conversion.

## Features

### 🤖 Intelligent Chat Interface
- **Natural Language Processing**: Convert natural language queries to SQL
- **Real-time Responses**: Powered by Gemini 2.0 Flash LLM
- **Vector Search**: Enhanced with Pinecone for faster, more accurate responses
- **Conversation History**: Persistent chat sessions with local storage

### 📊 Advanced Data Visualization
- **Interactive Charts**: ECharts integration for pie charts, bar charts, line charts, and more
- **Responsive Design**: Charts adapt to different screen sizes
- **Real-time Updates**: Dynamic chart generation based on query results

### 🎨 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Loading States**: Enhanced loading indicators for slow LLM/Pinecone operations
- **Query Suggestions**: Pre-built suggestions to help users get started
- **Error Handling**: Comprehensive error handling with user-friendly messages

### 🔧 Technical Features
- **Angular 20**: Latest Angular framework with standalone components
- **TypeScript**: Full type safety and modern JavaScript features
- **SCSS**: Advanced styling with modern CSS features
- **ECharts**: Professional-grade charting library
- **RxJS**: Reactive programming for API calls and state management

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Angular CLI (`npm install -g @angular/cli`)
- Backend server running on `http://localhost:8000`

### Installation

1. **Install Dependencies**
   ```bash
   cd ops-copilot-frontend
   npm install
   ```

2. **Start Development Server**
   ```bash
   # From project root
   ./start_frontend.sh
   
   # Or manually
   cd ops-copilot-frontend
   ng serve
   ```

3. **Access the Application**
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000

## Project Structure

```
ops-copilot-frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── chat/           # Main chat interface
│   │   │   ├── dashboard/      # Dashboard components
│   │   │   └── sidebar/        # Navigation sidebar
│   │   ├── services/
│   │   │   ├── api.ts         # Backend API service
│   │   │   └── chat-history.ts # Chat session management
│   │   ├── app.ts             # Main app component
│   │   └── app.config.ts      # App configuration
│   ├── environments/          # Environment configurations
│   └── styles.scss           # Global styles
├── package.json
└── angular.json
```

## Key Components

### ChatComponent
The main chat interface that handles:
- User input and message display
- SQL query generation and display
- Chart visualization
- Results pagination
- Loading states for slow operations

### ApiService
Handles all backend communication:
- Query processing with enhanced error handling
- Health checks and connection status
- Query suggestions
- Proper timeout handling for LLM operations

### ChatHistoryService
Manages chat sessions:
- Local storage persistence
- Session creation and management
- Message history tracking

## API Integration

The frontend integrates with the backend API endpoints:

- `POST /api/query` - Process natural language queries
- `GET /api/suggestions` - Get query suggestions
- `GET /api/schema` - Get database schema
- `GET /health` - Health check

## Styling and Theming

The application uses a modern design system with:
- **Color Palette**: Purple gradient theme with professional colors
- **Typography**: Inter font family for readability
- **Responsive Grid**: CSS Grid and Flexbox for layouts
- **Animations**: Smooth transitions and loading animations
- **Dark/Light Elements**: Professional contrast ratios

## Performance Optimizations

- **Lazy Loading**: Components loaded on demand
- **OnPush Change Detection**: Optimized change detection strategy
- **Virtual Scrolling**: For large result sets
- **Chart Optimization**: Efficient ECharts rendering
- **Caching**: API response caching where appropriate

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development

### Available Scripts

```bash
# Development server
ng serve

# Build for production
ng build --configuration production

# Run tests
ng test

# Lint code
ng lint
```

### Environment Configuration

Update `src/environments/environment.ts` for different environments:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'  // Backend API URL
};
```

## Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   - Ensure backend is running on port 8000
   - Check CORS configuration
   - Verify API endpoints

2. **Charts Not Rendering**
   - Check ECharts import in main.ts
   - Verify chart data format
   - Check browser console for errors

3. **Slow Response Times**
   - This is normal for LLM operations
   - Loading indicators show progress
   - Consider simplifying complex queries

### Performance Tips

- Use query suggestions for faster results
- Keep queries specific and focused
- Monitor network tab for API response times
- Use pagination for large result sets

## Contributing

1. Follow Angular style guide
2. Use TypeScript strict mode
3. Write unit tests for new features
4. Update documentation for API changes
5. Test on multiple browsers

## License

This project is part of the OEE Co-Pilot system.

