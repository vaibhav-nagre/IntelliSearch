# Saviynt Enterprise Search

A modern, Google-like enterprise search application with AI-powered RAG capabilities using AWS Bedrock. Search across forums, documentation, and Freshservice tickets with intelligent summarization and chat features.

## ✨ Features

- **Google-like UI**: Clean, intuitive search interface with instant suggestions
- **AI-Powered Search**: RAG capabilities using AWS Bedrock (Claude-3 Sonnet)
- **Multi-Source Search**: Forums, Documentation, and Freshservice tickets
- **Smart Chat**: "AI Deeper" tab with conversational search
- **SSO Authentication**: Google OAuth integration
- **Real-time Suggestions**: Intelligent query completions
- **Citation Support**: All AI responses include source citations
- **Responsive Design**: Works on desktop and mobile
- **Enterprise Security**: Role-based access control

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AWS Bedrock   │
│   (Next.js)     │───▶│   (FastAPI)     │───▶│   (Claude-3)    │
│   GitHub Pages  │    │   Cloud Run     │    │   (Embeddings)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                               ▼
                    ┌─────────────────┐
                    │   Data Layer    │
                    │   PostgreSQL    │
                    │   + pgvector    │
                    │   + OpenSearch  │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **AWS Account** with Bedrock access
- **Google Cloud** account for OAuth

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Saviynt
```

### 2. Configure AWS Credentials

```bash
# Copy environment template
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your AWS credentials:

```env
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
PORT=8000
NODE_ENV=development

# AWS Bedrock Models
AWS_BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
AWS_BEDROCK_EMBEDDING_MODEL_ID=amazon.titan-embed-text-v1
```

### 3. Enable AWS Bedrock Models

Go to AWS Console → Bedrock → Model Access and enable:
- **Claude-3 Sonnet** (for chat and summarization)
- **Titan Embeddings** (for vector search)

### 4. Start the Application

```bash
# Start both frontend and backend
./start.sh

# Or start individually:
./start.sh backend   # Backend only (port 8000)
./start.sh frontend  # Frontend only (port 3000)
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
Saviynt/
├── frontend/                 # Next.js static site
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # React components
│   │   │   └── search/      # Search-specific components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── lib/             # Utilities
│   │   └── types/           # TypeScript definitions
│   ├── package.json
│   └── next.config.js
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── services/        # Business logic
│   │   │   ├── llm.py      # AWS Bedrock integration
│   │   │   ├── rag.py      # RAG pipeline
│   │   │   ├── search.py   # Search service
│   │   │   └── auth.py     # Authentication
│   │   ├── models/          # Data models
│   │   ├── main.py          # FastAPI app
│   │   └── config.py        # Configuration
│   ├── requirements.txt
│   └── Dockerfile
├── ingestion/               # Data crawling scripts
├── infra/                   # Infrastructure as code
└── README.md
```

## 🔧 Configuration

### AWS Bedrock Setup

1. **Enable Model Access**: In AWS Console → Bedrock → Model Access
2. **Request Access**: For Claude-3 and Titan models if needed
3. **Set Regions**: Use `us-east-1` or `us-west-2` for best model availability

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8000/auth/callback`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AWS_REGION` | AWS region for Bedrock | ✅ |
| `AWS_ACCESS_KEY_ID` | AWS access key | ✅ |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | ✅ |
| `PORT` | Backend server port | ✅ |
| `NODE_ENV` | Environment (development/production) | ✅ |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | ⚠️ |
| `SECRET_KEY` | JWT signing secret | ⚠️ |

## 🔌 API Endpoints

### Search
- `POST /search` - Main search with AI summary
- `GET /suggest?q={query}` - Query suggestions

### Chat
- `POST /chat` - AI chat with context

### Admin
- `POST /ingest/run` - Trigger data ingestion
- `GET /admin/stats` - Get system statistics

### Authentication
- `GET /auth/callback` - Google OAuth callback
- `GET /healthz` - Health check

## 🎨 UI Components

### Search Interface
- **Search Input**: Auto-suggestions, voice input
- **Results List**: Titles, snippets, breadcrumbs
- **Quick Answer**: AI-generated summary with citations
- **Filters**: Source, date, content type

### AI Chat
- **Chat Interface**: Message bubbles, streaming responses
- **Source Citations**: Clickable links to original content
- **Suggestions**: Follow-up question recommendations

## 🔒 Security Features

- **OAuth 2.0**: Google SSO integration
- **RBAC**: Role-based access control
- **Data Isolation**: User permissions respected in search
- **HTTPS**: All communications encrypted
- **Input Validation**: Pydantic models for API safety

## 📊 Monitoring

### Health Checks
```bash
curl http://localhost:8000/healthz
```

### Metrics
- Search response times
- AI response quality
- User engagement
- Error rates

## 🚢 Deployment

### Frontend (GitHub Pages)
```bash
cd frontend
npm run build
npm run export
# Deploy dist/ folder to GitHub Pages
```

### Backend (Google Cloud Run)
```bash
cd backend
docker build -t saviynt-search .
gcloud run deploy saviynt-search --image=saviynt-search --region=us-central1
```

## 🧪 Testing

### Frontend
```bash
cd frontend
npm test
npm run test:watch
```

### Backend
```bash
cd backend
python -m pytest
python -m pytest --cov=app
```

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm run dev        # Start dev server
npm run lint       # ESLint
npm run type-check # TypeScript check
```

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload  # Auto-reload on changes
python -m pytest              # Run tests
black app/                     # Format code
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: See `/docs` folder
- **Discussions**: GitHub Discussions

---

Built with ❤️ for Saviynt Enterprise Search
