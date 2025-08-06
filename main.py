#!/usr/bin/env python3
"""
Academic Article MCP Server
Akademik makalelerden ana metin çıkarma MCP servisi
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

# FastMCP import
import fastmcp

from scraper import JAMAScraper
from parser import DataParser

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastMCP server instance
mcp = fastmcp.FastMCP("jama-abstract-mcp")

@mcp.tool(
    name="extract_jama_article",
    description="Akademik makale URL'sinden ana metni çıkarır"
)
async def extract_jama_article(url: str) -> Dict[str, Any]:
    """
    Akademik makale URL'sinden ana metni çıkarır
    
    Args:
        url: Akademik makale URL'si
        
    Returns:
        JSON formatında makale ana metni:
        - plain_text: Makalenin ana metni
        - source_url: Makalenin URL'si
    """
    return await _extract_jama_article(url)

async def _extract_jama_article(url: str) -> Dict[str, Any]:
    try:
        logger.info(f"Akademik makale çıkarma başlıyor: {url}")
        
        # URL doğrulama
        if "jamanetwork.com" not in url:
            return {"error": "Geçersiz JAMA URL'si"}
        
        # Scraper ile veri çıkarma
        scraper = JAMAScraper(headless=True, timeout=8)
        html_content = await scraper.scrape_article(url)
        
        if not html_content:
            return {"error": "Makale içeriği alınamadı"}
        
        # Parser ile akademik makale ana metnini çıkarma
        parser = DataParser()
        article_data = parser.parse_article(html_content)
        
        # İstenen JSON yapısını oluştur
        result = {
            "plain_text": article_data.get("plain_text", ""),
            "source_url": url
        }
        
        logger.info("Akademik makale ana metni başarıyla çıkarıldı")
        return result
        
    except Exception as e:
        logger.error(f"extract_jama_article hatası: {e}")
        return {"error": f"Veri çıkarma hatası: {str(e)}"}

if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Academic Article MCP Server")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio",
                       help="Transport protocol to use")
    parser.add_argument("--host", default="127.0.0.1",
                       help="Host to bind to (for HTTP transport)")
    parser.add_argument("--port", type=int, default=8000,
                       help="Port to bind to (for HTTP transport)")

    args = parser.parse_args()

    # Environment variable kontrolü
    transport = os.getenv("MCP_TRANSPORT", args.transport)
    host = os.getenv("MCP_HOST", args.host)
    port = int(os.getenv("MCP_PORT", args.port))

    if transport == "http":
        logger.info(f"Starting HTTP server on {host}:{port}")
        mcp.run(transport="http", host=host, port=port)
    else:
        logger.info("Starting STDIO server")
        mcp.run()