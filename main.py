#!/usr/bin/env python3
"""
JAMA Abstract MCP Server
JAMA tıp dergisi makalelerinden veri çıkarma MCP servisi
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

@mcp.tool()
async def extract_jama_article(url: str) -> Dict[str, Any]:
    """
    JAMA makale linkinden makale verilerini çıkarır
    
    Args:
        url: JAMA makale URL'si
        
    Returns:
        Çıkarılan makale verileri (başlık, yazarlar, özet, vb.)
    """
    return await _extract_jama_article(url)

async def _extract_jama_article(url: str) -> Dict[str, Any]:
    try:
        logger.info(f"JAMA makale çıkarma başlıyor: {url}")
        
        # URL doğrulama
        if "jamanetwork.com" not in url:
            return {"error": "Geçersiz JAMA URL'si"}
        
        # Scraper ile veri çıkarma
        scraper = JAMAScraper(headless=True, timeout=8)
        html_content = await scraper.scrape_article(url)
        
        if not html_content:
            return {"error": "Makale içeriği alınamadı"}
        
        # Parser ile veri ayrıştırma
        parser = DataParser()
        article_data = parser.parse_article(html_content)
        
        logger.info("Makale verisi başarıyla çıkarıldı")
        return {
            "success": True,
            "data": article_data,
            "source_url": url
        }
        
    except Exception as e:
        logger.error(f"extract_jama_article hatası: {e}")
        return {"error": f"Veri çıkarma hatası: {str(e)}"}

@mcp.tool()
async def get_article_visual(url: str) -> Dict[str, Any]:
    """
    JAMA makale linkinden abstract görselini alır (varsa)
    
    Args:
        url: JAMA makale URL'si
        
    Returns:
        Abstract görsel URL'si ve metadata (varsa)
    """
    return await _get_article_visual(url)

async def _get_article_visual(url: str) -> Dict[str, Any]:
    try:
        logger.info(f"Abstract görsel alma başlıyor: {url}")
        
        # URL doğrulama
        if "jamanetwork.com" not in url:
            return {"error": "Geçersiz JAMA URL'si"}
        
        # Scraper ile veri çıkarma
        scraper = JAMAScraper(headless=True, timeout=8)
        html_content = await scraper.scrape_article(url)
        
        if not html_content:
            return {"error": "Makale içeriği alınamadı"}
        
        # Parser ile görsel URL'sini çıkar
        parser = DataParser()
        article_data = parser.parse_article(html_content)
        
        existing_visual_url = article_data.get("existing_visual_url")
        
        if existing_visual_url:
            logger.info("Abstract görsel bulundu")
            return {
                "success": True,
                "visual_url": existing_visual_url,
                "article_title": article_data.get("title", ""),
                "source_url": url,
                "has_visual": True
            }
        else:
            logger.info("Bu makalede abstract görsel bulunamadı")
            return {
                "success": True,
                "has_visual": False,
                "article_title": article_data.get("title", ""),
                "source_url": url,
                "message": "Bu makalede abstract görsel bulunamadı"
            }
        
    except Exception as e:
        logger.error(f"get_article_visual hatası: {e}")
        return {"error": f"Görsel alma hatası: {str(e)}"}

if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="JAMA Abstract MCP Server")
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