#!/usr/bin/env python3
"""
Script to add new public sources to the enterprise search application.

Usage:
    python add_public_source.py --url "https://example.com" --name "Example Docs" --category "documentation"
    python add_public_source.py --config-file new_source.json
"""

import argparse
import json
import sys
import os
from typing import Dict, Any, Optional, List

# Add the backend app to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.public_sources import PublicSourcesManager

def create_source_config(
    url: str,
    name: str,
    description: str = "",
    category: str = "documentation",
    icon: str = "📄",
    color: str = "#2563eb",
    crawl_depth: int = 2,
    max_pages: int = 500,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Create a source configuration dictionary"""
    
    # Generate ID from name
    source_id = name.lower().replace(' ', '_').replace('-', '_')
    
    # Default patterns
    if include_patterns is None:
        include_patterns = ["/docs/*", "/documentation/*", "/guides/*"]
    
    if exclude_patterns is None:
        exclude_patterns = ["/admin/*", "/private/*", "*/draft/*"]
    
    return {
        "id": source_id,
        "name": name,
        "description": description or f"Documentation and guides from {name}",
        "base_url": url,
        "search_enabled": True,
        "ingestion_config": {
            "crawl_enabled": True,
            "crawl_depth": crawl_depth,
            "crawl_frequency": "weekly",
            "include_patterns": include_patterns,
            "exclude_patterns": exclude_patterns,
            "max_pages": max_pages
        },
        "display_config": {
            "icon": icon,
            "category": category,
            "color": color,
            "priority": 5
        }
    }

def add_source_from_args(args):
    """Add a source from command line arguments"""
    
    config = create_source_config(
        url=args.url,
        name=args.name,
        description=args.description,
        category=args.category,
        icon=args.icon,
        color=args.color,
        crawl_depth=args.crawl_depth,
        max_pages=args.max_pages,
        include_patterns=args.include_patterns.split(',') if args.include_patterns else None,
        exclude_patterns=args.exclude_patterns.split(',') if args.exclude_patterns else None
    )
    
    return config

def add_source_from_file(filepath: str):
    """Add a source from a JSON configuration file"""
    
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
        
        # Validate required fields
        required_fields = ["name", "base_url"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
        
        # Set defaults
        if "id" not in config:
            config["id"] = config["name"].lower().replace(' ', '_').replace('-', '_')
        
        config.setdefault("search_enabled", True)
        config.setdefault("description", f"Documentation from {config['name']}")
        
        # Set default ingestion config
        config.setdefault("ingestion_config", {})
        config["ingestion_config"].setdefault("crawl_enabled", True)
        config["ingestion_config"].setdefault("crawl_depth", 2)
        config["ingestion_config"].setdefault("crawl_frequency", "weekly")
        config["ingestion_config"].setdefault("include_patterns", ["/docs/*", "/documentation/*"])
        config["ingestion_config"].setdefault("exclude_patterns", ["/admin/*", "/private/*"])
        config["ingestion_config"].setdefault("max_pages", 500)
        
        # Set default display config
        config.setdefault("display_config", {})
        config["display_config"].setdefault("icon", "📄")
        config["display_config"].setdefault("category", "documentation")
        config["display_config"].setdefault("color", "#2563eb")
        config["display_config"].setdefault("priority", 5)
        
        return config
        
    except FileNotFoundError:
        print(f"Error: Configuration file '{filepath}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        return None
    except Exception as e:
        print(f"Error reading configuration file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Add a new public source to the search application")
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add source command
    add_parser = subparsers.add_parser('add', help='Add a new source')
    add_parser.add_argument('--url', required=True, help='Base URL of the source')
    add_parser.add_argument('--name', required=True, help='Display name of the source')
    add_parser.add_argument('--description', default='', help='Description of the source')
    add_parser.add_argument('--category', default='documentation', 
                          choices=['documentation', 'tools', 'tutorials'],
                          help='Category of the source')
    add_parser.add_argument('--icon', default='📄', help='Icon for the source')
    add_parser.add_argument('--color', default='#2563eb', help='Color for the source')
    add_parser.add_argument('--crawl-depth', type=int, default=2, help='Maximum crawl depth')
    add_parser.add_argument('--max-pages', type=int, default=500, help='Maximum pages to crawl')
    add_parser.add_argument('--include-patterns', help='Comma-separated include patterns')
    add_parser.add_argument('--exclude-patterns', help='Comma-separated exclude patterns')
    
    # Add from file command
    file_parser = subparsers.add_parser('add-from-file', help='Add source from JSON file')
    file_parser.add_argument('config_file', help='Path to JSON configuration file')
    
    # List sources command
    list_parser = subparsers.add_parser('list', help='List all public sources')
    
    # Remove source command
    remove_parser = subparsers.add_parser('remove', help='Remove a source')
    remove_parser.add_argument('source_id', help='ID of the source to remove')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize the public sources manager with correct path
    config_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'config', 'public_sources.json')
    manager = PublicSourcesManager(config_path)
    
    if args.command == 'add':
        config = add_source_from_args(args)
        
        print(f"Adding source: {config['name']}")
        print(f"URL: {config['base_url']}")
        print(f"Category: {config['display_config']['category']}")
        
        success = manager.add_source(config)
        
        if success:
            print(f"✅ Successfully added source '{config['name']}' with ID '{config['id']}'")
        else:
            print(f"❌ Failed to add source '{config['name']}'")
            sys.exit(1)
    
    elif args.command == 'add-from-file':
        config = add_source_from_file(args.config_file)
        
        if config is None:
            sys.exit(1)
        
        print(f"Adding source from file: {args.config_file}")
        print(f"Source: {config['name']}")
        print(f"URL: {config['base_url']}")
        
        success = manager.add_source(config)
        
        if success:
            print(f"✅ Successfully added source '{config['name']}' with ID '{config['id']}'")
        else:
            print(f"❌ Failed to add source '{config['name']}'")
            sys.exit(1)
    
    elif args.command == 'list':
        sources = manager.get_all_sources()
        
        if not sources:
            print("No public sources configured")
            return
        
        print(f"Configured public sources ({len(sources)}):")
        print("-" * 60)
        
        for source in sources:
            print(f"ID: {source['id']}")
            print(f"Name: {source['name']}")
            print(f"URL: {source['base_url']}")
            print(f"Category: {source.get('display_config', {}).get('category', 'N/A')}")
            print(f"Search Enabled: {source.get('search_enabled', False)}")
            print("-" * 60)
    
    elif args.command == 'remove':
        source = manager.get_source_by_id(args.source_id)
        
        if not source:
            print(f"❌ Source with ID '{args.source_id}' not found")
            sys.exit(1)
        
        print(f"Removing source: {source['name']} ({args.source_id})")
        
        # Confirm removal
        confirm = input("Are you sure? (y/N): ")
        if confirm.lower() != 'y':
            print("Cancelled")
            return
        
        success = manager.remove_source(args.source_id)
        
        if success:
            print(f"✅ Successfully removed source '{args.source_id}'")
        else:
            print(f"❌ Failed to remove source '{args.source_id}'")
            sys.exit(1)

if __name__ == '__main__':
    main()
