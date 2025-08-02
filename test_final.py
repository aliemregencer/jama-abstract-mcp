#!/usr/bin/env python3
"""
Final MCP Test
"""

import asyncio
import aiohttp
import json
import base64

async def parse_response(response):
    """Response'u parse et"""
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

async def test_final():
    """Final test"""
    endpoint = "http://localhost:8000/mcp/"
    
    # Initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": "final-test",
                "version": "1.0.0"
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            # Initialize
            print("🔧 Initialize ediliyor...")
            async with session.post(endpoint, json=init_request, headers=headers) as response:
                print(f"Status: {response.status}")
                session_id = response.headers.get('mcp-session-id')
                print(f"Session ID: {session_id}")
                
                if response.status == 200 and session_id:
                    # Session ID ile header'ı güncelle
                    headers["mcp-session-id"] = session_id
                    
                    # Extract test
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
                    
                    print(f"\n🚀 Extract test ediliyor: {test_url}")
                    print(f"Request: {json.dumps(extract_request, indent=2)}")
                    async with session.post(endpoint, json=extract_request, headers=headers) as response2:
                        print(f"Status: {response2.status}")
                        if response2.status == 200:
                            result = await parse_response(response2)
                            if result:
                                print(f"✅ Extract başarılı!")
                                print(f"   - Success: {result.get('success', False)}")
                                
                                if result.get('success') and 'data' in result:
                                    data = result['data']
                                    print(f"   - Title: {data.get('title', 'N/A')}")
                                    print(f"   - DOI: {data.get('doi', 'N/A')}")
                                    
                                    # Visual test
                                    visual_request = {
                                        "jsonrpc": "2.0",
                                        "id": 2,
                                        "method": "tools/call",
                                        "params": {
                                            "name": "create_abstract_visual",
                                            "arguments": {
                                                "article_data": result
                                            }
                                        }
                                    }
                                    
                                    print(f"\n🎨 Visual test ediliyor...")
                                    async with session.post(endpoint, json=visual_request, headers=headers) as response3:
                                        print(f"Status: {response3.status}")
                                        if response3.status == 200:
                                            visual_result = await parse_response(response3)
                                            if visual_result:
                                                print(f"✅ Visual başarılı!")
                                                print(f"   - Success: {visual_result.get('success', False)}")
                                                
                                                if visual_result.get('success'):
                                                    pptx_base64 = visual_result.get('pptx_base64')
                                                    if pptx_base64:
                                                        pptx_bytes = base64.b64decode(pptx_base64)
                                                        with open("final_test_output.pptx", "wb") as f:
                                                            f.write(pptx_bytes)
                                                        print(f"   💾 PPTX dosyası 'final_test_output.pptx' olarak kaydedildi")
                                                else:
                                                    print(f"   ❌ Visual error: {visual_result.get('error', 'Unknown error')}")
                                            else:
                                                print("❌ Visual response parse edilemedi")
                                        else:
                                            print(f"❌ Visual HTTP Error: {response3.status}")
                                else:
                                    print(f"   ❌ Extract error: {result.get('error', 'Unknown error')}")
                            else:
                                print("❌ Extract response parse edilemedi")
                        else:
                            print(f"❌ Extract HTTP Error: {response2.status}")
                            text = await response2.text()
                            print(f"Response: {text}")
                else:
                    print("❌ Initialize başarısız")
                    
        except Exception as e:
            print(f"❌ Hata: {e}")

if __name__ == "__main__":
    asyncio.run(test_final()) 