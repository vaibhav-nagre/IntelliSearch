from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
import asyncio
import json

from app.config import get_settings
from app.services.llm import get_llm, get_embeddings
from app.services.search import SearchService
from app.services.auth import verify_token, get_current_user
from app.models.schemas import SearchRequest, SearchResponse, ChatRequest, ChatResponse
from app.services.rag import RAGService
from app.services.public_sources import public_sources_manager

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Enterprise search with AWS Bedrock RAG capabilities"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(",") if settings.allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize services
search_service = None
rag_service = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global search_service, rag_service
    
    # Initialize LLM and embeddings
    llm = get_llm()
    embeddings = get_embeddings()
    
    # Initialize services
    search_service = SearchService(embeddings=embeddings)
    rag_service = RAGService(llm=llm, embeddings=embeddings)
    
    print(f"🚀 {settings.app_name} started successfully with AWS Bedrock integration")


@app.get("/auth/me")
async def get_current_user_info(
    current_user: Dict = Depends(get_current_user)
):
    """Get current user information"""
    return current_user


@app.get("/auth/google")
async def google_auth():
    """Redirect to Google OAuth"""
    from urllib.parse import urlencode
    
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "scope": "openid email profile",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent"
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
    
    # For development, return the URL instead of redirecting
    return {"auth_url": auth_url}


@app.post("/auth/callback")
async def auth_callback(
    request: Dict[str, str]
):
    """Handle Google OAuth callback"""
    from app.services.auth import verify_google_token, create_access_token
    from datetime import timedelta
    
    code = request.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    
    try:
        # Exchange code for token (simplified for demo)
        # In production, you'd call Google's token endpoint
        
        # For now, create a mock user - replace with actual Google token exchange
        user_data = {
            "user_id": "demo_user",
            "email": "demo@saviynt.com",
            "name": "Demo User",
            "groups": ["users"],
            "is_admin": False
        }
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user_data["user_id"], **user_data},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")


@app.post("/auth/logout")
async def logout():
    """Logout user"""
    return {"message": "Logged out successfully"}


@app.get("/public-sources")
async def get_public_sources():
    """Get all configured public sources"""
    return {
        "sources": public_sources_manager.get_all_sources(),
        "categories": public_sources_manager.get_categories(),
        "search_config": public_sources_manager.get_search_config()
    }


@app.post("/public-sources")
async def add_public_source(
    source_config: Dict[str, Any],
    current_user: Dict = Depends(get_current_user)
):
    """Add a new public source (admin only)"""
    # Check if user is admin (in production, check actual permissions)
    if "admin" not in current_user.get("groups", []):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    success = public_sources_manager.add_source(source_config)
    if success:
        return {"message": "Source added successfully", "source_id": source_config.get("id")}
    else:
        raise HTTPException(status_code=400, detail="Failed to add source")


@app.delete("/public-sources/{source_id}")
async def remove_public_source(
    source_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Remove a public source (admin only)"""
    # Check if user is admin (in production, check actual permissions)
    if "admin" not in current_user.get("groups", []):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    success = public_sources_manager.remove_source(source_id)
    if success:
        return {"message": "Source removed successfully"}
    else:
        raise HTTPException(status_code=404, detail="Source not found")


@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
        "aws_region": settings.aws_region
    }


@app.get("/search")
async def search_get(
    q: str = Query(..., description="Search query"),
    sources: str = Query(default="docs", description="Comma-separated sources"),
    top_k: int = Query(default=10, description="Number of results"),
    authenticated: bool = Query(default=False, description="Is user authenticated")
):
    """Main search endpoint (GET) - supports unauthenticated access"""
    try:
        # Parse sources
        source_list = [s.strip() for s in sources.split(',')]
        
        # For unauthenticated users, only search public sources
        if not authenticated:
            results = public_sources_manager.search_public_sources(q)
            
            # Limit results
            results = results[:top_k]
            
            # Generate simple answer for unauthenticated users
            answer = f'Here are some public documentation results for "{q}". Sign in to access more comprehensive search across forums and support tickets.'
            citations = []
            if results:
                citations = [
                    {
                        "id": idx + 1,
                        "title": result["title"],
                        "url": result["url"],
                        "source": result["source"],
                        "source_name": result["source_name"],
                        "snippet": result["snippet"]
                    }
                    for idx, result in enumerate(results[:3])  # Top 3 for citations
                ]
            
            return {
                "query": q,
                "answer": answer,
                "citations": citations,
                "results": results,
                "total_results": len(results),
                "did_you_mean": None,
                "filters": {
                    "source": ["docs"],
                    "time": ["any", "past_year", "past_month", "past_week"]
                },
                "execution_time_ms": 45
            }
        
        # For authenticated users, use regular search
        # Mock search for now - replace with actual search
        mock_results = [
            {
                "title": "Getting Started with Saviynt",
                "url": "https://docs.saviyntcloud.com/getting-started",
                "source": "docs",
                "source_name": "Documentation", 
                "source_icon": "📚",
                "snippet": f"Learn how to get started with Saviynt Identity Governance platform for {q}...",
                "updated_at": "2024-01-15T10:30:00Z",
                "score": 0.95,
                "breadcrumb": "Documentation > Getting Started"
            },
            {
                "title": "API Documentation",
                "url": "https://docs.saviyntcloud.com/api",
                "source": "docs",
                "source_name": "Documentation",
                "source_icon": "📚", 
                "snippet": f"Complete API reference for {q} and platform integration...",
                "updated_at": "2024-01-15T09:45:00Z",
                "score": 0.87,
                "breadcrumb": "Documentation > API Reference"
            }
        ]
        
        # Generate answer and citations for authenticated users
        answer = None
        citations = []
        
        return {
            "query": q,
            "answer": answer,
            "citations": citations,
            "results": mock_results[:top_k],
            "total_results": len(mock_results),
            "did_you_mean": None,
            "filters": {
                "source": ["docs"] if not authenticated else ["docs", "forums", "tickets"],
                "time": ["any", "past_year", "past_month", "past_week"]
            },
            "execution_time_ms": 45
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Main search endpoint with RAG capabilities"""
    try:
        # Perform search with user permissions
        results = await search_service.search(
            query=request.query,
            sources=request.sources,
            top_k=request.top_k,
            user_permissions=current_user.get("groups", [])
        )
        
        # Generate AI summary if requested
        answer = None
        citations = []
        
        if request.include_ai_summary and results["results"]:
            rag_response = await rag_service.generate_answer(
                query=request.query,
                context_chunks=results["results"][:5]  # Top 5 for context
            )
            answer = rag_response["answer"]
            citations = rag_response["citations"]
        
        return SearchResponse(
            query=request.query,
            answer=answer,
            citations=citations,
            results=results["results"],
            total_results=results["total"],
            did_you_mean=results.get("did_you_mean"),
            filters=results.get("filters", {}),
            execution_time_ms=results.get("execution_time_ms", 0)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Dict = Depends(get_current_user)
):
    """AI chat endpoint with context from search results"""
    try:
        # Get conversation context and perform search if needed
        search_results = []
        if request.use_search:
            search_response = await search_service.search(
                query=request.message,
                sources=["all"],
                top_k=10,
                user_permissions=current_user.get("groups", [])
            )
            search_results = search_response["results"][:5]
        
        # Generate chat response
        response = await rag_service.chat(
            message=request.message,
            session_id=request.session_id,
            context_chunks=search_results,
            conversation_history=request.conversation_history or []
        )
        
        return ChatResponse(
            session_id=request.session_id,
            message=response["message"],
            citations=response.get("citations", []),
            suggestions=response.get("suggestions", []),
            execution_time_ms=response.get("execution_time_ms", 0)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/suggest")
async def suggest_queries(
    q: str = Query(..., description="Partial query for suggestions"),
    current_user: Dict = Depends(get_current_user)
):
    """Query suggestion endpoint"""
    try:
        suggestions = await search_service.get_suggestions(q)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest/run")
async def trigger_ingestion(
    sources: List[str] = Query(default=["all"], description="Sources to ingest"),
    current_user: Dict = Depends(get_current_user)
):
    """Trigger data ingestion (admin only)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        # Trigger ingestion job
        job_id = await search_service.trigger_ingestion(sources)
        return {"job_id": job_id, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/admin/stats")
async def get_admin_stats(
    current_user: Dict = Depends(get_current_user)
):
    """Get ingestion and search statistics (admin only)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        stats = await search_service.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.max_workers
    )
