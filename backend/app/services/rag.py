import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from app.services.llm import AWSBedrockLLM, AWSBedrockEmbeddings
from app.models.schemas import SearchResult, Citation, ChatMessage


class RAGService:
    """Retrieval-Augmented Generation service using AWS Bedrock"""
    
    def __init__(self, llm: AWSBedrockLLM, embeddings: AWSBedrockEmbeddings):
        self.llm = llm
        self.embeddings = embeddings
        self.conversation_store = {}  # In production, use Redis or database
    
    async def generate_answer(
        self, 
        query: str, 
        context_chunks: List[SearchResult]
    ) -> Dict[str, Any]:
        """Generate an AI answer from search results with citations"""
        start_time = time.time()
        
        # Prepare context
        context_text = self._prepare_context(context_chunks)
        
        # Create system prompt for search summarization
        system_prompt = """You are an enterprise search summarizer for Saviynt products and services. 
Answer concisely using ONLY the provided context passages. 
Always produce citation footnotes like [1], [2] that map to provided source URLs. 
If unsure or context is insufficient, say so and suggest narrower queries. 
Never fabricate links or information not in the context."""
        
        # Create user prompt
        user_prompt = f"""Context passages:
{context_text}

Question: {query}

Please provide a comprehensive answer based on the context above, including relevant citations."""
        
        # Combine prompts
        full_prompt = f"{system_prompt}\n\nHuman: {user_prompt}\n\nAssistant:"
        
        # Generate response
        response = self.llm._call(full_prompt)
        
        # Extract citations and create citation objects
        citations = self._extract_citations(response, context_chunks)
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            "answer": response,
            "citations": citations,
            "execution_time_ms": execution_time
        }
    
    async def chat(
        self,
        message: str,
        session_id: str,
        context_chunks: List[SearchResult],
        conversation_history: List[ChatMessage]
    ) -> Dict[str, Any]:
        """Handle chat conversation with context"""
        start_time = time.time()
        
        # Get or create conversation
        if session_id not in self.conversation_store:
            self.conversation_store[session_id] = []
        
        # Add current message to history
        current_message = ChatMessage(
            role="user",
            content=message,
            timestamp=datetime.utcnow()
        )
        self.conversation_store[session_id].append(current_message)
        
        # Prepare context from search results
        context_text = self._prepare_context(context_chunks) if context_chunks else ""
        
        # Prepare conversation history
        history_text = self._prepare_conversation_history(
            self.conversation_store[session_id][-6:]  # Last 6 messages
        )
        
        # Create system prompt for chat
        system_prompt = """You are an internal product assistant for Saviynt. 
Use the provided search context to answer questions accurately. 
Respect permissions: never reveal content not returned by the search tool. 
Cite sources for any claim derived from documents or tickets.
Be helpful, concise, and professional."""
        
        # Create user prompt
        user_prompt = f"""Search context:
{context_text}

Conversation history:
{history_text}

Current question: {message}

Please provide a helpful response based on the available context."""
        
        # Combine prompts
        full_prompt = f"{system_prompt}\n\nHuman: {user_prompt}\n\nAssistant:"
        
        # Generate response
        response = self.llm._call(full_prompt)
        
        # Add assistant response to conversation
        assistant_message = ChatMessage(
            role="assistant",
            content=response,
            timestamp=datetime.utcnow()
        )
        self.conversation_store[session_id].append(assistant_message)
        
        # Extract citations
        citations = self._extract_citations(response, context_chunks)
        
        # Generate suggestions for follow-up questions
        suggestions = self._generate_suggestions(message, response)
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            "message": response,
            "citations": citations,
            "suggestions": suggestions,
            "execution_time_ms": execution_time
        }
    
    def _prepare_context(self, search_results: List[SearchResult]) -> str:
        """Prepare context text from search results"""
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(
                f"[{i}] Source: {result.source}\n"
                f"Title: {result.title}\n"
                f"URL: {result.url}\n"
                f"Content: {result.snippet}\n"
                f"Last Updated: {result.updated_at.strftime('%Y-%m-%d')}\n"
            )
        return "\n---\n".join(context_parts)
    
    def _prepare_conversation_history(self, messages: List[ChatMessage]) -> str:
        """Prepare conversation history text"""
        history_parts = []
        for msg in messages[:-1]:  # Exclude current message
            history_parts.append(f"{msg.role.title()}: {msg.content}")
        return "\n".join(history_parts)
    
    def _extract_citations(
        self, 
        response: str, 
        context_chunks: List[SearchResult]
    ) -> List[Citation]:
        """Extract citations from response and map to context chunks"""
        citations = []
        
        # Simple citation extraction - look for [1], [2], etc.
        import re
        citation_pattern = r'\[(\d+)\]'
        found_citations = re.findall(citation_pattern, response)
        
        for cite_num in found_citations:
            cite_idx = int(cite_num) - 1
            if 0 <= cite_idx < len(context_chunks):
                result = context_chunks[cite_idx]
                citation = Citation(
                    id=cite_idx + 1,
                    title=result.title,
                    url=result.url,
                    source=result.source,
                    snippet=result.snippet[:150] + "..." if len(result.snippet) > 150 else result.snippet
                )
                if citation not in citations:
                    citations.append(citation)
        
        return citations
    
    def _generate_suggestions(self, question: str, response: str) -> List[str]:
        """Generate follow-up question suggestions"""
        # Simple suggestion generation - could be enhanced with ML
        suggestions = []
        
        if "how" in question.lower():
            suggestions.append("Can you provide more details about the implementation?")
            suggestions.append("What are the best practices for this?")
        
        if "what" in question.lower():
            suggestions.append("How does this work in practice?")
            suggestions.append("Are there any limitations I should know about?")
        
        if "error" in question.lower() or "issue" in question.lower():
            suggestions.append("What are common solutions for this issue?")
            suggestions.append("How can I prevent this in the future?")
        
        # Default suggestions
        if not suggestions:
            suggestions = [
                "Can you explain this in more detail?",
                "Are there any related topics I should know about?",
                "What's the best way to implement this?"
            ]
        
        return suggestions[:3]  # Return max 3 suggestions
