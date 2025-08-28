import os
from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Server Configuration
    app_name: str = "IntelliSearch Enterprise"
    version: str = "1.0.0"
    debug: bool = False
    port: int = 8000
    
    # Creator Information
    creator_name: str = "Vaibhav Nagre"
    creator_email: str = "vaibhav@example.com"
    creator_github: str = "https://github.com/vaibhavnagre"
    creator_linkedin: str = "https://linkedin.com/in/vaibhavnagre"
    
    # AWS Configuration
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    aws_bedrock_embedding_model_id: str = "amazon.titan-embed-text-v1"
    
    # Database
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    
    # Search
    opensearch_url: str = "https://localhost:9200"
    opensearch_username: str = "admin"
    opensearch_password: str = "admin"
    
    # Authentication
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google OAuth
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    
    # Data Sources
    saviynt_forums_url: str = "https://forums.saviynt.com"
    saviynt_docs_url: str = "https://docs.saviyntcloud.com"
    freshservice_api_key: str
    freshservice_domain: str
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:3001"
    
    # Feature Flags
    use_aws_bedrock: bool = True
    use_opensearch: bool = True
    allow_debug_prompts: bool = False
    
    # Performance
    max_workers: int = 4
    chunk_size: int = 1000
    chunk_overlap: int = 150
    max_chunks_per_query: int = 20
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
