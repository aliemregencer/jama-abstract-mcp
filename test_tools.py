#!/usr/bin/env python3
"""
Tool Test Script
JAMA Abstract MCP tool'larını test eder
"""

import asyncio
import json
from main import _extract_jama_article, _create_abstract_visual

async def test_extract_jama_article():
    """extract_jama_article tool'unu test et"""
    print("🔍 Testing extract_jama_article...")
    
    # Test URL (daha iyi bir JAMA makale)
    test_url = "https://jamanetwork.com/journals/jama/fullarticle/2813882"
    
    try:
        result = await _extract_jama_article(test_url)
        print(f"✅ Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def test_create_abstract_visual(article_data):
    """create_abstract_visual tool'unu test et"""
    print("\n🎨 Testing create_abstract_visual...")
    
    if not article_data or "error" in article_data:
        print("❌ No valid article data to test with")
        return None
    
    try:
        result = await _create_abstract_visual(article_data)
        print(f"✅ Result: {json.dumps({k: v for k, v in result.items() if k != 'pptx_base64'}, indent=2, ensure_ascii=False)}")
        if result.get('pptx_base64'):
            print(f"📄 PPTX Base64 length: {len(result['pptx_base64'])} characters")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def main():
    """Ana test fonksiyonu"""
    print("🚀 Starting JAMA Abstract MCP Tool Tests...\n")
    
    # Test extract_jama_article
    article_data = await test_extract_jama_article()
    
    # Test create_abstract_visual
    if article_data:
        await test_create_abstract_visual(article_data)
    
    print("\n✨ Tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 