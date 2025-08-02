#!/usr/bin/env python3
"""
JAMA Abstract MCP Streaming Test Script
Streaming desteğini test eder
"""

import asyncio
import json
import aiohttp
import base64
from typing import Dict, Any

# Yerel MCP endpoint
LOCAL_ENDPOINT = "http://localhost:8000/mcp/"

# Headers for MCP requests
MCP_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

async def parse_mcp_response(response):
    """MCP response'unu parse et"""
    try:
        content_type = response.headers.get('content-type', '')
        if 'text/event-stream' in content_type:
            # Event stream format
            text = await response.text()
            lines = text.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    data = line[6:]  # Remove 'data: ' prefix
                    if data.strip():
                        return json.loads(data)
            return None
        else:
            # Regular JSON response
            return await response.json()
    except Exception as e:
        print(f"Response parse hatası: {e}")
        return None

async def initialize_mcp():
    """MCP sunucusunu initialize et"""
    print("🔧 MCP sunucusu initialize ediliyor...")
    
    async with aiohttp.ClientSession() as session:
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "jama-abstract-mcp-streaming-test",
                    "version": "1.0.0"
                }
            }
        }
        
        try:
            async with session.post(LOCAL_ENDPOINT, json=initialize_request, headers=MCP_HEADERS) as response:
                if response.status == 200:
                    # Session ID'yi header'dan al
                    session_id = response.headers.get('mcp-session-id')
                    if session_id:
                        print(f"✅ MCP sunucusu başarıyla initialize edildi")
                        print(f"📋 Session ID: {session_id}")
                        return session_id
                    else:
                        print("❌ Session ID bulunamadı")
                        return None
                else:
                    print(f"❌ Initialize hatası: {response.status}")
                    print(f"Response: {await response.text()}")
                    return None
        except Exception as e:
            print(f"❌ Initialize hatası: {e}")
            return None

async def test_streaming_extract(session_id: str):
    """Streaming extract_jama_article test et"""
    print("\n🚀 Streaming extract_jama_article test ediliyor...")
    
    # Test URL
    test_url = "https://jamanetwork.com/journals/jama/fullarticle/2837046"
    
    extract_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "extract_jama_article",
            "arguments": {
                "url": test_url
            }
        }
    }
    
    # Session ID ile header'ı güncelle
    headers = MCP_HEADERS.copy()
    headers["X-Session-ID"] = session_id
    headers["mcp-session-id"] = session_id
    headers["Session-ID"] = session_id
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(LOCAL_ENDPOINT, json=extract_request, headers=headers) as response:
                if response.status == 200:
                    print("✅ Streaming response alındı:")
                    
                    # Streaming response'u parse et
                    content_type = response.headers.get('content-type', '')
                    if 'text/event-stream' in content_type:
                        # Event stream format
                        text = await response.text()
                        lines = text.strip().split('\n')
                        
                        for line in lines:
                            if line.startswith('data: '):
                                data = line[6:]  # Remove 'data: ' prefix
                                if data.strip():
                                    try:
                                        result = json.loads(data)
                                        if 'status' in result:
                                            print(f"   📊 Status: {result['status']}")
                                            if 'message' in result:
                                                print(f"   💬 Message: {result['message']}")
                                        elif 'success' in result:
                                            print(f"   ✅ Success: {result['success']}")
                                            if result.get('success') and 'data' in result:
                                                data = result['data']
                                                print(f"   📄 Title: {data.get('title', 'N/A')}")
                                                print(f"   🔗 DOI: {data.get('doi', 'N/A')}")
                                                return result
                                        elif 'error' in result:
                                            print(f"   ❌ Error: {result['error']}")
                                            return None
                                    except json.JSONDecodeError:
                                        continue
                    else:
                        # Regular JSON response
                        result = await response.json()
                        print(f"   📊 Regular response: {result}")
                        return result
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    print(f"Response: {await response.text()}")
        except Exception as e:
            print(f"❌ Streaming test hatası: {e}")
    
    return None

async def test_streaming_visual(article_data, session_id: str):
    """Streaming create_abstract_visual test et"""
    print("\n🎨 Streaming create_abstract_visual test ediliyor...")
    
    visual_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "create_abstract_visual",
            "arguments": {
                "article_data": article_data
            }
        }
    }
    
    # Session ID ile header'ı güncelle
    headers = MCP_HEADERS.copy()
    headers["X-Session-ID"] = session_id
    headers["mcp-session-id"] = session_id
    headers["Session-ID"] = session_id
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(LOCAL_ENDPOINT, json=visual_request, headers=headers) as response:
                if response.status == 200:
                    print("✅ Streaming visual response alındı:")
                    
                    # Streaming response'u parse et
                    content_type = response.headers.get('content-type', '')
                    if 'text/event-stream' in content_type:
                        # Event stream format
                        text = await response.text()
                        lines = text.strip().split('\n')
                        
                        for line in lines:
                            if line.startswith('data: '):
                                data = line[6:]  # Remove 'data: ' prefix
                                if data.strip():
                                    try:
                                        result = json.loads(data)
                                        if 'status' in result:
                                            print(f"   📊 Status: {result['status']}")
                                            if 'message' in result:
                                                print(f"   💬 Message: {result['message']}")
                                        elif 'success' in result:
                                            print(f"   ✅ Success: {result['success']}")
                                            if result.get('success'):
                                                print(f"   📁 Filename: {result.get('filename', 'N/A')}")
                                                pptx_base64 = result.get('pptx_base64')
                                                if pptx_base64:
                                                    pptx_bytes = base64.b64decode(pptx_base64)
                                                    with open("streaming_test_output.pptx", "wb") as f:
                                                        f.write(pptx_bytes)
                                                    print(f"   💾 PPTX dosyası 'streaming_test_output.pptx' olarak kaydedildi")
                                                return result
                                        elif 'error' in result:
                                            print(f"   ❌ Error: {result['error']}")
                                            return None
                                    except json.JSONDecodeError:
                                        continue
                    else:
                        # Regular JSON response
                        result = await response.json()
                        print(f"   📊 Regular response: {result}")
                        return result
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    print(f"Response: {await response.text()}")
        except Exception as e:
            print(f"❌ Streaming visual test hatası: {e}")
    
    return None

async def main():
    """Ana test fonksiyonu"""
    print("🚀 JAMA Abstract MCP Streaming Test Başlıyor...")
    print(f"📍 Endpoint: {LOCAL_ENDPOINT}")
    print("⚡ Streaming desteği ile optimize edilmiş test")
    
    # 0. Initialize MCP
    session_id = await initialize_mcp()
    if not session_id:
        print("❌ MCP initialize edilemedi, test durduruluyor...")
        return
    
    # 1. Streaming extract test
    article_data = await test_streaming_extract(session_id)
    
    # 2. Streaming visual test
    if article_data:
        await test_streaming_visual(article_data, session_id)
    else:
        print("❌ Article data alınamadı, visual test atlanıyor...")
    
    print("\n✅ Streaming test tamamlandı!")

if __name__ == "__main__":
    asyncio.run(main()) 