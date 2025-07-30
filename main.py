#!/usr/bin/env python3
"""
JAMA Abstract MCP Server
JAMA tıp dergisi makalelerinden veri çıkarma ve görsel analizi
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

# FastMCP import - MCP Protocol yerine
import fastmcp

from scraper import JAMAScraper
from parser import DataParser
from image_analyzer import ImageAnalyzer
from visual_generator import VisualDataGenerator

# WebDriver setup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

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
    try:
        logger.info(f"JAMA makale çıkarma başlıyor: {url}")
        
        # URL doğrulama
        if "jamanetwork.com" not in url:
            return {"error": "Geçersiz JAMA URL'si"}
        
        # Scraper ile veri çıkarma (Smithery için optimize edildi)
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
async def analyze_existing_visual(image_url: str) -> Dict[str, Any]:
    """
    Mevcut abstract görselini analiz eder
    
    Args:
        image_url: Analiz edilecek görsel URL'si
        
    Returns:
        Görsel analiz sonuçları (renkler, layout, tipografi)
    """
    try:
        logger.info(f"Görsel analiz başlıyor: {image_url}")
        
        analyzer = ImageAnalyzer()
        analysis_result = await analyzer.analyze_image(image_url)
        
        logger.info("Görsel analizi tamamlandı")
        return {
            "success": True,
            "analysis": analysis_result
        }
        
    except Exception as e:
        logger.error(f"analyze_existing_visual hatası: {e}")
        return {"error": f"Görsel analiz hatası: {str(e)}"}

@mcp.tool()
async def generate_visual_data(article_data: Dict[str, Any], style_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Yeni görsel oluşturmak için tasarım verilerini hazırlar
    
    Args:
        article_data: Makale verileri
        style_preferences: Stil tercihleri (opsiyonel)
        
    Returns:
        Görsel oluşturma için hazırlanmış tasarım verileri
    """
    try:
        logger.info("Görsel tasarım verileri oluşturuluyor")
        
        generator = VisualDataGenerator()
        visual_data = generator.create_visual_data(article_data, style_preferences)
        
        logger.info("Görsel tasarım verileri hazırlandı")
        return {
            "success": True,
            "visual_data": visual_data
        }
        
    except Exception as e:
        logger.error(f"generate_visual_data hatası: {e}")
        return {"error": f"Görsel veri oluşturma hatası: {str(e)}"}

@mcp.tool()
async def full_pipeline(url: str, analyze_existing: bool = True) -> Dict[str, Any]:
    """
    Tam pipeline: Makale çıkarma + analiz + görsel veri oluşturma
    
    Args:
        url: JAMA makale URL'si
        analyze_existing: Mevcut görseli analiz et mi?
        
    Returns:
        Tüm işlem sonuçları
    """
    try:
        logger.info(f"Full pipeline başlıyor: {url}")
        
        # 1. Makale verilerini çıkar
        article_result = await extract_jama_article(url)
        if not article_result.get("success"):
            return article_result
        
        article_data = article_result["data"]
        result = {"article_data": article_data}
        
        # 2. Mevcut görseli analiz et (varsa)
        if analyze_existing and article_data.get("existing_visual_url"):
            logger.info("Mevcut görsel analiz ediliyor")
            visual_analysis = await analyze_existing_visual(article_data["existing_visual_url"])
            result["visual_analysis"] = visual_analysis
        
        # 3. Yeni görsel verileri oluştur
        style_prefs = result.get("visual_analysis", {}).get("analysis")
        visual_data = await generate_visual_data(article_data, style_prefs)
        result["visual_data"] = visual_data
        
        logger.info("Full pipeline tamamlandı")
        return {
            "success": True,
            "pipeline_result": result,
            "source_url": url
        }
        
    except Exception as e:
        logger.error(f"full_pipeline hatası: {e}")
        return {"error": f"Pipeline hatası: {str(e)}"}

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

    # Smithery için environment variable kontrolü
    transport = os.getenv("MCP_TRANSPORT", args.transport)
    host = os.getenv("MCP_HOST", args.host)
    port = int(os.getenv("MCP_PORT", args.port))

    if transport == "http":
        logger.info(f"Starting HTTP server on {host}:{port}")
        mcp.run(transport="http", host=host, port=port)
    else:
        logger.info("Starting STDIO server")
        mcp.run()