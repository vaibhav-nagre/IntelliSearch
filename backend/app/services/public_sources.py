import json
import os
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path
from .web_scraper import web_scraper, ScrapedContent

class PublicSourcesManager:
    """Manages configuration and search for public data sources"""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # Look for config in the backend directory, not the app/services directory
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'public_sources.json')
        
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Public sources config not found at {self.config_path}")
            self._config = {"public_sources": [], "categories": {}, "search_config": {}}
        except json.JSONDecodeError as e:
            print(f"Error parsing public sources config: {e}")
            self._config = {"public_sources": [], "categories": {}, "search_config": {}}
    
    def get_all_sources(self) -> List[Dict[str, Any]]:
        """Get all configured public sources"""
        return self._config.get("public_sources", [])
    
    def get_source_by_id(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific source by ID"""
        for source in self.get_all_sources():
            if source.get("id") == source_id:
                return source
        return None
    
    def get_search_enabled_sources(self) -> List[Dict[str, Any]]:
        """Get sources that are enabled for search"""
        return [source for source in self.get_all_sources() 
                if source.get("search_enabled", False)]
    
    def get_sources_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get sources filtered by category"""
        return [source for source in self.get_all_sources()
                if source.get("display_config", {}).get("category") == category]
    
    def get_categories(self) -> Dict[str, Any]:
        """Get all categories"""
        return self._config.get("categories", {})
    
    def get_search_config(self) -> Dict[str, Any]:
        """Get search configuration"""
        return self._config.get("search_config", {})
    
    async def search_public_sources(self, query: str, source_ids: Optional[List[str]] = None, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Search across public sources by actually scraping content
        """
        if source_ids is None:
            sources = self.get_search_enabled_sources()
        else:
            sources = [self.get_source_by_id(sid) for sid in source_ids if self.get_source_by_id(sid)]
        
        all_results = []
        
        for source in sources:
            if not source:
                continue
                
            source_id = source.get("id")
            source_name = source.get("name")
            base_url = source.get("base_url")
            icon = source.get("display_config", {}).get("icon", "📄")
            category = source.get("display_config", {}).get("category", "documentation")
            
            print(f"Searching {source_name} for: {query}")
            
            try:
                # Get URLs to scrape for this source
                urls_to_search = await self._get_urls_for_source(source, query)
                
                if not urls_to_search:
                    print(f"No URLs found for {source_name}")
                    continue
                
                # Scrape content from URLs
                scraped_contents = []
                for url in urls_to_search[:10]:  # Limit to first 10 URLs per source
                    content = await web_scraper.fetch_and_extract(url)
                    if content:
                        scraped_contents.append(content)
                
                if not scraped_contents:
                    print(f"No content scraped from {source_name}")
                    continue
                
                # Search through scraped content
                search_results = web_scraper.search_content(scraped_contents, query)
                
                # Format results for our API
                for result in search_results[:5]:  # Top 5 results per source
                    formatted_result = {
                        "title": result["title"],
                        "url": result["url"],
                        "source": source_id,
                        "source_name": source_name,
                        "source_icon": icon,
                        "snippet": result["snippet"],
                        "updated_at": result.get("published_date") or "2024-01-15T10:30:00Z",
                        "score": result["score"],
                        "breadcrumb": result.get("breadcrumb") or f"{source_name} > Documentation",
                        "category": category
                    }
                    all_results.append(formatted_result)
                    
                print(f"Found {len(search_results)} results from {source_name}")
                
            except Exception as e:
                print(f"Error searching {source_name}: {e}")
                continue
        
        # Sort all results by score
        all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return all_results[:max_results]
    
    async def _get_urls_for_source(self, source: Dict[str, Any], query: str) -> List[str]:
        """Get URLs to search for a specific source"""
        base_url = source.get("base_url")
        crawl_config = source.get("crawl_config", {})
        
        urls = []
        
        # Try sitemap first
        sitemap_url = crawl_config.get("sitemap_url")
        if sitemap_url:
            print(f"Checking sitemap: {sitemap_url}")
            sitemap_urls = await web_scraper.discover_urls_from_sitemap(sitemap_url, max_urls=30)
            urls.extend(sitemap_urls)
        
        # Add additional URLs from config
        additional_urls = crawl_config.get("additional_urls", [])
        urls.extend(additional_urls)
        
        # If no URLs found, try to discover from base URL
        if not urls and base_url:
            print(f"No sitemap found, trying to discover URLs from {base_url}")
            try:
                content = await web_scraper.fetch_and_extract(base_url)
                if content:
                    # For now, just search the main page
                    urls = [base_url]
                    
                    # Could add logic here to discover more URLs from the main page
                    # discovered_urls = web_scraper.discover_urls_from_page(base_url, content.content)
                    # urls.extend(discovered_urls[:10])
            except Exception as e:
                print(f"Error discovering URLs from {base_url}: {e}")
                if base_url:
                    urls = [base_url]  # Fallback to just the base URL
        
        # Filter URLs based on include/exclude patterns if configured
        include_patterns = crawl_config.get("include_patterns", [])
        exclude_patterns = crawl_config.get("exclude_patterns", [])
        
        if include_patterns or exclude_patterns:
            filtered_urls = []
            for url in urls:
                # Check include patterns
                if include_patterns:
                    if not any(pattern in url for pattern in include_patterns):
                        continue
                
                # Check exclude patterns
                if exclude_patterns:
                    if any(pattern in url for pattern in exclude_patterns):
                        continue
                
                filtered_urls.append(url)
            
            urls = filtered_urls
        
        print(f"Found {len(urls)} URLs to search for {source.get('name')}")
        return [url for url in urls if url and isinstance(url, str)]  # Filter out None values
    
    def search_public_sources_sync(self, query: str, source_ids: Optional[List[str]] = None, max_results: int = 20) -> List[Dict[str, Any]]:
        """Synchronous wrapper for async search - but run in a thread to avoid loop conflicts"""
        import concurrent.futures
        import threading
        
        def run_async_search():
            # Create a new event loop for this thread
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                return new_loop.run_until_complete(self.search_public_sources(query, source_ids, max_results))
            finally:
                new_loop.close()
        
        # Run the async search in a separate thread to avoid event loop conflicts
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_async_search)
            try:
                return future.result(timeout=30)  # 30 second timeout
            except concurrent.futures.TimeoutError:
                print(f"Search timeout for query: {query}")
                return []
            except Exception as e:
                print(f"Error in threaded search: {e}")
                return []
    
    def add_source(self, source_config: Dict[str, Any]) -> bool:
        """Add a new public source to the configuration"""
        try:
            # Validate required fields
            required_fields = ["id", "name", "base_url"]
            for field in required_fields:
                if field not in source_config:
                    raise ValueError(f"Missing required field: {field}")
            
            # Check if source already exists
            if self.get_source_by_id(source_config["id"]):
                raise ValueError(f"Source with ID '{source_config['id']}' already exists")
            
            # Add default values
            source_config.setdefault("search_enabled", True)
            source_config.setdefault("description", "")
            source_config.setdefault("display_config", {})
            source_config["display_config"].setdefault("icon", "📄")
            source_config["display_config"].setdefault("category", "documentation")
            
            # Add to config
            self._config["public_sources"].append(source_config)
            
            # Save to file
            with open(self.config_path, 'w') as f:
                json.dump(self._config, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error adding source: {e}")
            return False
    
    def remove_source(self, source_id: str) -> bool:
        """Remove a source from the configuration"""
        try:
            original_length = len(self._config["public_sources"])
            self._config["public_sources"] = [
                source for source in self._config["public_sources"]
                if source.get("id") != source_id
            ]
            
            if len(self._config["public_sources"]) < original_length:
                # Save to file
                with open(self.config_path, 'w') as f:
                    json.dump(self._config, f, indent=2)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error removing source: {e}")
            return False


# Global instance
public_sources_manager = PublicSourcesManager()
