import asyncio
import aiohttp
import trafilatura
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import re
import time
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ScrapedContent:
    title: str
    content: str
    url: str
    snippet: str
    published_date: Optional[str] = None
    breadcrumb: Optional[str] = None

class WebScraper:
    """Service for scraping and searching web content from public sources"""
    
    def __init__(self):
        self.session = None
        self.user_agent = "Mozilla/5.0 (compatible; IntelliSearchBot/1.0)"
        
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={'User-Agent': self.user_agent}
            )
        return self.session
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    def extract_content_with_trafilatura(self, html: str, url: str) -> Optional[ScrapedContent]:
        """Extract main content from HTML using trafilatura"""
        try:
            # Extract main text content
            content = trafilatura.extract(html, include_comments=False, include_tables=True)
            if not content:
                return None
            
            # Extract title and other metadata
            metadata = trafilatura.extract_metadata(html)
            title = metadata.title if metadata and metadata.title else "Untitled"
            
            # Create snippet (first 200 characters)
            snippet = content[:200] + "..." if len(content) > 200 else content
            
            # Clean up content
            content = re.sub(r'\n\s*\n', '\n\n', content)  # Remove excessive newlines
            
            return ScrapedContent(
                title=title,
                content=content,
                url=url,
                snippet=snippet,
                published_date=metadata.date if metadata else None
            )
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return None
    
    def extract_content_with_bs4(self, html: str, url: str) -> Optional[ScrapedContent]:
        """Fallback content extraction using BeautifulSoup"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Try to find title
            title_elem = soup.find('title')
            title = title_elem.get_text().strip() if title_elem else "Untitled"
            
            # Try to find main content areas
            content_selectors = [
                'main', 'article', '.content', '.main-content', 
                '.post-content', '.entry-content', '#content',
                '.documentation', '.docs-content'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = ' '.join([elem.get_text().strip() for elem in elements])
                    break
            
            # If no specific content area found, get body text
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text()
            
            # Clean up content
            content = re.sub(r'\s+', ' ', content).strip()
            snippet = content[:200] + "..." if len(content) > 200 else content
            
            return ScrapedContent(
                title=title,
                content=content,
                url=url,
                snippet=snippet
            )
        except Exception as e:
            print(f"Error extracting content with BS4 from {url}: {e}")
            return None
    
    async def fetch_and_extract(self, url: str) -> Optional[ScrapedContent]:
        """Fetch a URL and extract its content"""
        try:
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Failed to fetch {url}: HTTP {response.status}")
                    return None
                
                html = await response.text()
                
                # Try trafilatura first
                content = self.extract_content_with_trafilatura(html, url)
                
                # Fall back to BeautifulSoup if trafilatura fails
                if not content or len(content.content) < 100:
                    content = self.extract_content_with_bs4(html, url)
                
                return content
                
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def search_content(self, contents: List[ScrapedContent], query: str) -> List[Dict[str, Any]]:
        """Search through scraped content for query matches"""
        results = []
        query_words = query.lower().split()
        
        for content in contents:
            if not content.content:
                continue
                
            # Calculate relevance score
            score = 0.0
            title_lower = content.title.lower()
            content_lower = content.content.lower()
            
            # Title matches (higher weight)
            title_matches = sum(1 for word in query_words if word in title_lower)
            score += title_matches * 2.0
            
            # Content matches
            content_matches = sum(1 for word in query_words if word in content_lower)
            score += content_matches * 0.5
            
            # Exact phrase match bonus
            if query.lower() in title_lower:
                score += 3.0
            elif query.lower() in content_lower:
                score += 1.0
            
            # Only include results with some relevance
            if score > 0:
                results.append({
                    "title": content.title,
                    "url": content.url,
                    "snippet": content.snippet,
                    "score": score,
                    "published_date": content.published_date,
                    "breadcrumb": content.breadcrumb
                })
        
        # Sort by score (descending)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    async def discover_urls_from_sitemap(self, sitemap_url: str, max_urls: int = 50) -> List[str]:
        """Discover URLs from sitemap"""
        try:
            session = await self._get_session()
            async with session.get(sitemap_url) as response:
                if response.status != 200:
                    return []
                
                content = await response.text()
                soup = BeautifulSoup(content, 'xml')
                
                urls = []
                for loc in soup.find_all('loc'):
                    url = loc.get_text().strip()
                    if url and len(urls) < max_urls:
                        urls.append(url)
                
                return urls
                
        except Exception as e:
            print(f"Error fetching sitemap {sitemap_url}: {e}")
            return []
    
    def discover_urls_from_page(self, base_url: str, html: str, max_urls: int = 20) -> List[str]:
        """Discover URLs from a page's links"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            urls = []
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                
                # Basic filtering
                if (full_url.startswith('http') and 
                    len(urls) < max_urls and
                    urlparse(full_url).netloc == urlparse(base_url).netloc):
                    urls.append(full_url)
            
            return list(set(urls))  # Remove duplicates
            
        except Exception as e:
            print(f"Error discovering URLs from page: {e}")
            return []

# Create a global instance
web_scraper = WebScraper()

# Cleanup function for graceful shutdown
async def cleanup_scraper():
    await web_scraper.close()
