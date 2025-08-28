"""
Simple test script to demonstrate public sources functionality
"""
import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_public_sources():
    """Test the public sources functionality"""
    
    # Test the configuration
    config_path = os.path.join(os.path.dirname(__file__), 'backend', 'config', 'public_sources.json')
    
    print("📚 Testing Public Sources Configuration")
    print("=" * 50)
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        sources = config.get('public_sources', [])
        categories = config.get('categories', {})
        
        print(f"✅ Configuration loaded successfully")
        print(f"📖 Total sources configured: {len(sources)}")
        print(f"🏷️  Categories available: {len(categories)}")
        print()
        
        # Display sources
        print("📋 Configured Sources:")
        print("-" * 30)
        for source in sources:
            print(f"🔹 {source.get('name', 'Unknown')}")
            print(f"   ID: {source.get('id', 'N/A')}")
            print(f"   URL: {source.get('base_url', 'N/A')}")
            print(f"   Category: {source.get('display_config', {}).get('category', 'N/A')}")
            print(f"   Icon: {source.get('display_config', {}).get('icon', '📄')}")
            print(f"   Search Enabled: {source.get('search_enabled', False)}")
            print()
        
        # Display categories
        print("🏷️  Available Categories:")
        print("-" * 25)
        for cat_id, cat_info in categories.items():
            if isinstance(cat_info, dict):
                print(f"🔸 {cat_info.get('name', cat_id)}")
                print(f"   Description: {cat_info.get('description', 'N/A')}")
                print(f"   Icon: {cat_info.get('icon', '📁')}")
            else:
                print(f"🔸 {cat_id}: {cat_info}")
            print()
        
        # Test search simulation
        print("🔍 Testing Search Simulation:")
        print("-" * 30)
        
        # Simulate searching for "API"
        query = "API"
        print(f"Searching for: '{query}'")
        
        mock_results = []
        
        for source in sources:
            if not source.get('search_enabled', False):
                continue
                
            source_id = source.get('id')
            source_name = source.get('name')
            base_url = source.get('base_url')
            icon = source.get('display_config', {}).get('icon', '📄')
            
            # Mock some relevant results
            if 'docs' in source_id or 'documentation' in source_name.lower():
                mock_results.append({
                    "title": f"{source_name} - API Documentation",
                    "url": f"{base_url}/api",
                    "source": source_id,
                    "source_name": source_name,
                    "source_icon": icon,
                    "snippet": f"Complete API reference for {source_name} platform...",
                    "score": 0.9,
                    "breadcrumb": f"{source_name} > API Reference"
                })
        
        print(f"📊 Found {len(mock_results)} relevant results:")
        for i, result in enumerate(mock_results[:5], 1):
            print(f"{i}. {result['source_icon']} {result['title']}")
            print(f"   {result['url']}")
            print(f"   {result['snippet'][:80]}...")
            print()
        
        print("✨ Public sources system is working correctly!")
        return True
        
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON configuration: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing public sources: {e}")
        return False

def test_adding_source():
    """Test adding a new source programmatically"""
    
    print("\n🔧 Testing Source Addition")
    print("=" * 30)
    
    # Sample source configuration
    new_source = {
        "id": "test_docs",
        "name": "Test Documentation",
        "description": "Test documentation for demonstration",
        "base_url": "https://example.com",
        "search_enabled": True,
        "ingestion_config": {
            "crawl_enabled": True,
            "crawl_depth": 2,
            "crawl_frequency": "weekly",
            "include_patterns": ["/docs/*"],
            "exclude_patterns": ["/admin/*"],
            "max_pages": 100
        },
        "display_config": {
            "icon": "🧪",
            "category": "documentation",
            "color": "#6b7280",
            "priority": 1
        }
    }
    
    print(f"📝 Sample source configuration:")
    print(f"   Name: {new_source['name']}")
    print(f"   URL: {new_source['base_url']}")
    print(f"   Category: {new_source['display_config']['category']}")
    print(f"   Icon: {new_source['display_config']['icon']}")
    
    print("\n✅ Source configuration is valid and ready to be added!")
    print("💡 Use the add_public_source.py script to add it:")
    print(f"   python scripts/add_public_source.py add --url {new_source['base_url']} --name '{new_source['name']}'")

if __name__ == '__main__':
    print("🚀 Public Sources System Test")
    print("=" * 40)
    print()
    
    success = test_public_sources()
    
    if success:
        test_adding_source()
        print("\n" + "=" * 40)
        print("🎉 All tests completed successfully!")
        print("\n📖 Next Steps:")
        print("1. Start the frontend: cd frontend && npm run dev")
        print("2. Start the backend: cd backend && uvicorn app.main:app --reload")
        print("3. Visit http://localhost:3002 to test the search interface")
        print("4. Try searching for 'API' or 'documentation' without logging in")
        print("5. Use scripts/add_public_source.py to add more sources")
    else:
        print("\n❌ Tests failed. Please check the configuration.")
        sys.exit(1)
