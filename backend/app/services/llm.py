import boto3
import json
from typing import List, Dict, Any, Optional
from langchain.llms.base import LLM
from langchain.embeddings.base import Embeddings
from pydantic import BaseModel

from app.config import get_settings


class AWSBedrockLLM(LLM):
    """Custom LLM wrapper for AWS Bedrock"""
    
    model_id: str
    region_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
    
    @property
    def _llm_type(self) -> str:
        return "aws_bedrock"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Call AWS Bedrock model"""
        
        # Configure request based on model type
        if "claude" in self.model_id.lower():
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "top_p": 0.9
            }
        else:
            # Default format for other models
            request_body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 2000,
                    "temperature": 0.1,
                    "topP": 0.9,
                    "stopSequences": stop or []
                }
            }
        
        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body),
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            
            # Parse response based on model type
            if "claude" in self.model_id.lower():
                return response_body.get('content', [{}])[0].get('text', '')
            else:
                return response_body.get('results', [{}])[0].get('outputText', '')
                
        except Exception as e:
            raise Exception(f"Error calling AWS Bedrock: {str(e)}")


class AWSBedrockEmbeddings(Embeddings):
    """Custom embeddings wrapper for AWS Bedrock"""
    
    model_id: str
    region_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents"""
        embeddings = []
        for text in texts:
            embedding = self.embed_query(text)
            embeddings.append(embedding)
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        request_body = {
            "inputText": text
        }
        
        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body),
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            return response_body.get('embedding', [])
            
        except Exception as e:
            raise Exception(f"Error getting embeddings from AWS Bedrock: {str(e)}")


def get_llm() -> AWSBedrockLLM:
    """Get configured AWS Bedrock LLM instance"""
    settings = get_settings()
    
    return AWSBedrockLLM(
        model_id=settings.aws_bedrock_model_id,
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    )


def get_embeddings() -> AWSBedrockEmbeddings:
    """Get configured AWS Bedrock embeddings instance"""
    settings = get_settings()
    
    return AWSBedrockEmbeddings(
        model_id=settings.aws_bedrock_embedding_model_id,
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    )
