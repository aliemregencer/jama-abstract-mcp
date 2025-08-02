#!/usr/bin/env python3
"""
Basit MCP Test
"""

import asyncio
import aiohttp
import json

async def test_simple():
    """Basit test"""
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
                "name": "simple-test",
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
                print(f"Headers: {dict(response.headers)}")
                text = await response.text()
                print(f"Response: {text}")
                
                if response.status == 200:
                    # Tools list
                    tools_request = {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/list",
                        "params": {}
                    }
                    
                    print("\n🔧 Tools listesi alınıyor...")
                    async with session.post(endpoint, json=tools_request, headers=headers) as response2:
                        print(f"Status: {response2.status}")
                        text2 = await response2.text()
                        print(f"Response: {text2}")
                        
        except Exception as e:
            print(f"❌ Hata: {e}")

if __name__ == "__main__":
    asyncio.run(test_simple()) 