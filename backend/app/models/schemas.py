from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    sources: List[str] = Field(default=["all"], description="Sources to search in")
    top_k: int = Field(default=10, description="Number of results to return")
    include_ai_summary: bool = Field(default=True, description="Include AI-generated summary")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Additional filters")


class Citation(BaseModel):
    id: int
    title: str
    url: str
    source: str
    snippet: Optional[str] = None


class SearchResult(BaseModel):
    title: str
    url: str
    source: str
    snippet: str
    updated_at: datetime
    score: float
    breadcrumb: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    answer: Optional[str] = None
    citations: List[Citation] = []
    results: List[SearchResult] = []
    total_results: int
    did_you_mean: Optional[str] = None
    filters: Dict[str, Any] = {}
    execution_time_ms: int


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    session_id: str
    message: str
    use_search: bool = Field(default=True, description="Whether to use search for context")
    conversation_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    session_id: str
    message: str
    citations: List[Citation] = []
    suggestions: List[str] = []
    execution_time_ms: int


class Document(BaseModel):
    doc_id: str
    source: str
    url: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    authors: List[str] = []
    tags: List[str] = []
    permissions: List[str] = []  # User groups that can access this document


class DocumentChunk(BaseModel):
    chunk_id: str
    doc_id: str
    content: str
    embedding: Optional[List[float]] = None
    chunk_index: int
    start_char: int
    end_char: int


class IngestionJob(BaseModel):
    job_id: str
    sources: List[str]
    status: str  # "pending", "running", "completed", "failed"
    started_at: datetime
    completed_at: Optional[datetime] = None
    documents_processed: int = 0
    errors: List[str] = []


class User(BaseModel):
    user_id: str
    email: str
    name: str
    groups: List[str] = []
    is_admin: bool = False
    last_login: Optional[datetime] = None
