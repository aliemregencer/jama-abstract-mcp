#!/usr/bin/env python3
"""
JAMA Abstract MCP Test Script
Yerel HTTP endpoint'ini test eder
"""

import asyncio
import json
import aiohttp
import base64
import uuid
from typing import Dict, Any

# Yerel MCP endpoint
LOCAL_ENDPOINT = "http://localhost:8000/mcp/"

# Session ID
SESSION_ID = str(uuid.uuid4())

# Headers for MCP requests
MCP_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "X-Session-ID": SESSION_ID
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
    print(f"📋 Session ID: {SESSION_ID}")
    
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
                    "name": "jama-abstract-mcp-test",
                    "version": "1.0.0"
                }
            }
        }
        
        try:
            async with session.post(LOCAL_ENDPOINT, json=initialize_request, headers=MCP_HEADERS) as response:
                if response.status == 200:
                    init_response = await parse_mcp_response(response)
                    if init_response:
                        print("✅ MCP sunucusu başarıyla initialize edildi")
                        return True
                    else:
                        print("❌ Initialize response parse edilemedi")
                        return False
                else:
                    print(f"❌ Initialize hatası: {response.status}")
                    print(f"Response: {await response.text()}")
                    return False
        except Exception as e:
            print(f"❌ Initialize hatası: {e}")
            return False

async def test_mcp_endpoint():
    """MCP endpoint'ini test et"""
    print("🔍 MCP Endpoint Test Başlıyor...")
    
    async with aiohttp.ClientSession() as session:
        # 1. Tools listesini al
        print("\n1️⃣ Tools listesi alınıyor...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        try:
            async with session.post(LOCAL_ENDPOINT, json=tools_request, headers=MCP_HEADERS) as response:
                if response.status == 200:
                    tools_response = await parse_mcp_response(response)
                    if tools_response:
                        print("✅ Tools listesi alındı:")
                        if 'result' in tools_response and 'tools' in tools_response['result']:
                            for tool in tools_response['result']['tools']:
                                print(f"   - {tool['name']}: {tool['description']}")
                        else:
                            print("❌ Tools listesi bulunamadı")
                            print(f"Response: {tools_response}")
                    else:
                        print("❌ Tools response parse edilemedi")
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    print(f"Response: {await response.text()}")
        except Exception as e:
            print(f"❌ Tools listesi hatası: {e}")

async def test_extract_jama_article():
    """extract_jama_article tool'unu test et"""
    print("\n2️⃣ extract_jama_article test ediliyor...")
    
    # Test URL (kullanıcının verdiği JAMA makale)
    test_url = "https://jamanetwork.com/journals/jama/fullarticle/2837046"
    
    extract_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "extract_jama_article",
            "arguments": {
                "url": test_url
            }
        }
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(LOCAL_ENDPOINT, json=extract_request, headers=MCP_HEADERS) as response:
                if response.status == 200:
                    extract_response = await parse_mcp_response(response)
                    if extract_response:
                        print("✅ extract_jama_article yanıt aldı:")
                        
                        if 'result' in extract_response:
                            result = extract_response['result']
                            if result.get('success'):
                                data = result.get('data', {})
                                print(f"   - Başlık: {data.get('title', 'N/A')}")
                                print(f"   - DOI: {data.get('doi', 'N/A')}")
                                print(f"   - Population: {data.get('population', 'N/A')}")
                                print(f"   - Intervention: {data.get('intervention', 'N/A')}")
                                print(f"   - Findings: {data.get('findings', 'N/A')}")
                                print(f"   - Settings: {data.get('settings', 'N/A')}")
                                print(f"   - Primary Outcome: {data.get('primary_outcome', 'N/A')}")
                                return result  # Sonraki test için döndür
                            else:
                                print(f"❌ İşlem başarısız: {result.get('error', 'Bilinmeyen hata')}")
                        else:
                            print(f"❌ Beklenmeyen yanıt: {extract_response}")
                    else:
                        print("❌ Extract response parse edilemedi")
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    print(f"Response: {await response.text()}")
        except Exception as e:
            print(f"❌ extract_jama_article hatası: {e}")
    
    return None

async def test_create_abstract_visual(article_data: Dict[str, Any]):
    """create_abstract_visual tool'unu test et"""
    print("\n3️⃣ create_abstract_visual test ediliyor...")
    
    visual_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "create_abstract_visual",
            "arguments": {
                "article_data": article_data
            }
        }
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(LOCAL_ENDPOINT, json=visual_request, headers=MCP_HEADERS) as response:
                if response.status == 200:
                    visual_response = await parse_mcp_response(response)
                    if visual_response:
                        print("✅ create_abstract_visual yanıt aldı:")
                        
                        if 'result' in visual_response:
                            result = visual_response['result']
                            if result.get('success'):
                                print(f"   - Dosya adı: {result.get('filename', 'N/A')}")
                                print(f"   - Mesaj: {result.get('message', 'N/A')}")
                                
                                # Base64 PPTX'i kontrol et
                                pptx_base64 = result.get('pptx_base64')
                                if pptx_base64:
                                    try:
                                        pptx_bytes = base64.b64decode(pptx_base64)
                                        print(f"   - PPTX boyutu: {len(pptx_bytes)} bytes")
                                        
                                        # Test dosyası olarak kaydet
                                        with open("test_output.pptx", "wb") as f:
                                            f.write(pptx_bytes)
                                        print("   - PPTX dosyası 'test_output.pptx' olarak kaydedildi")
                                    except Exception as e:
                                        print(f"   - PPTX decode hatası: {e}")
                                else:
                                    print("   - PPTX verisi bulunamadı")
                            else:
                                print(f"❌ İşlem başarısız: {result.get('error', 'Bilinmeyen hata')}")
                        else:
                            print(f"❌ Beklenmeyen yanıt: {visual_response}")
                    else:
                        print("❌ Visual response parse edilemedi")
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    print(f"Response: {await response.text()}")
        except Exception as e:
            print(f"❌ create_abstract_visual hatası: {e}")

async def test_with_mock_data():
    """Mock data ile test et"""
    print("\n4️⃣ Mock data ile test ediliyor...")
    
    mock_article_data = {
        "success": True,
        "data": {
            "title": "Test Makale Başlığı",
            "population": "100 hasta (50-75 yaş arası)",
            "intervention": "Yeni ilaç tedavisi vs plasebo",
            "findings": "Anlamlı iyileşme gösterildi (p<0.05)",
            "settings": "Çok merkezli randomize kontrollü çalışma",
            "primary_outcome": "Survival rate ve yaşam kalitesi"
        }
    }
    
    await test_create_abstract_visual(mock_article_data)

async def main():
    """Ana test fonksiyonu"""
    print("🚀 JAMA Abstract MCP Yerel Test Başlıyor...")
    print(f"📍 Endpoint: {LOCAL_ENDPOINT}")
    
    # 0. Initialize MCP
    if not await initialize_mcp():
        print("❌ MCP initialize edilemedi, test durduruluyor...")
        return
    
    # 1. Endpoint test
    await test_mcp_endpoint()
    
    # 2. Extract test
    article_data = await test_extract_jama_article()
    
    # 3. Visual test (gerçek data ile)
    if article_data:
        await test_create_abstract_visual(article_data)
    else:
        print("\n⚠️ Gerçek data alınamadı, mock data ile test ediliyor...")
        await test_with_mock_data()
    
    print("\n✅ Test tamamlandı!")

if __name__ == "__main__":
    asyncio.run(main()) 