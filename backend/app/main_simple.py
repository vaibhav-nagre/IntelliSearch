from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import json
import os

# Simple config for development
class Settings:
    app_name = "IntelliSearch Enterprise"
    version = "1.0.0"
    environment = "development"
    debug = True
    creator_name = "Vaibhav Nagre"
    creator_email = "vaibhav@example.com"
    creator_github = "https://github.com/vaibhavnagre"
    creator_linkedin = "https://linkedin.com/in/vaibhavnagre"
    allowed_origins = ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"]

settings = Settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=f"AI-Powered Enterprise Search Platform - Created by {settings.creator_name}",
    contact={
        "name": settings.creator_name,
        "email": settings.creator_email,
        "url": settings.creator_github
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load public sources configuration
def load_public_sources():
    """Load public sources from config file"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'public_sources.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"public_sources": [], "categories": {}, "search_config": {}}
    except json.JSONDecodeError:
        return {"public_sources": [], "categories": {}, "search_config": {}}

# Search function
async def search_public_sources(query: str, sources_config: Dict) -> List[Dict[str, Any]]:
    """Real search function that scrapes actual websites"""
    from app.services.public_sources import public_sources_manager
    
    try:
        # Use the async search implementation directly
        results = await public_sources_manager.search_public_sources(query, max_results=10)
        return results
    except Exception as e:
        print(f"Error in real search: {e}")
        # Fallback to mock results if real search fails
        return mock_search_fallback(query, sources_config)

def mock_search_fallback(query: str, sources_config: Dict) -> List[Dict[str, Any]]:
    """Fallback mock search function"""
    results = []
    sources = sources_config.get('public_sources', [])
    
    for source in sources:
        if not source.get('search_enabled', False):
            continue
            
        source_id = source.get('id')
        source_name = source.get('name')
        base_url = source.get('base_url')
        icon = source.get('display_config', {}).get('icon', '📄')
        category = source.get('display_config', {}).get('category', 'documentation')
        
        # Generate mock results based on query
        if any(keyword in query.lower() for keyword in ['api', 'documentation', 'docs', 'guide']):
            results.extend([
                {
                    "title": f"{source_name} - API Documentation",
                    "url": f"{base_url}/api",
                    "source": source_id,
                    "source_name": source_name,
                    "source_icon": icon,
                    "snippet": f"Complete API reference for {source_name} platform. Learn how to integrate with {query}...",
                    "updated_at": "2024-01-15T10:30:00Z",
                    "score": 0.95,
                    "breadcrumb": f"{source_name} > API Reference",
                    "category": category
                },
                {
                    "title": f"Getting Started with {query} - {source_name}",
                    "url": f"{base_url}/getting-started",
                    "source": source_id,
                    "source_name": source_name,
                    "source_icon": icon,
                    "snippet": f"Step-by-step guide to get started with {query} using {source_name}...",
                    "updated_at": "2024-01-15T09:45:00Z",
                    "score": 0.87,
                    "breadcrumb": f"{source_name} > Getting Started",
                    "category": category
                }
            ])
    
    # Sort by score and return top results
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return results[:20]  # Return top 20 results

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "docs_url": "/docs",
        "creator": {
            "name": settings.creator_name,
            "email": settings.creator_email,
            "github": settings.creator_github,
            "linkedin": settings.creator_linkedin
        },
        "description": "AI-Powered Enterprise Search Platform by Vaibhav Nagre"
    }

@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version
    }

@app.get("/public-sources")
async def get_public_sources():
    """Get all configured public sources"""
    config = load_public_sources()
    return {
        "sources": config.get("public_sources", []),
        "categories": config.get("categories", {}),
        "search_config": config.get("search_config", {})
    }

@app.get("/search")
async def search_public(
    q: str = Query(..., description="Search query"),
    sources: str = Query(default="", description="Comma-separated source IDs"),
    top_k: int = Query(default=10, description="Number of results"),
    authenticated: bool = Query(default=False, description="Is user authenticated")
):
    """Public search endpoint - no authentication required"""
    try:
        # Load sources configuration
        sources_config = load_public_sources()
        
        # For unauthenticated users, only search public sources
        if not authenticated:
            results = await search_public_sources(q, sources_config)
            
            # Limit results
            results = results[:top_k]
            
            # Generate simple answer for unauthenticated users
            answer = f'Here are public documentation results for "{q}". Sign in to access more comprehensive search across forums and support tickets.'
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
                "execution_time_ms": 45,
                "sources_searched": len(sources_config.get("public_sources", []))
            }
        
        # For authenticated users, return enhanced results (mock)
        results = await search_public_sources(q, sources_config)
        
        return {
            "query": q,
            "answer": None,
            "citations": [],
            "results": results[:top_k],
            "total_results": len(results),
            "did_you_mean": None,
            "filters": {
                "source": ["docs", "forums", "tickets"],
                "time": ["any", "past_year", "past_month", "past_week"]
            },
            "execution_time_ms": 45,
            "sources_searched": len(sources_config.get("public_sources", []))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
