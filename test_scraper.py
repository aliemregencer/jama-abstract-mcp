#!/usr/bin/env python3
"""
JAMA Scraper Test Script
Scraper'ı doğrudan test eder
"""

import asyncio
import json
from scraper import JAMAScraper
from parser import DataParser

async def test_scraper():
    """Scraper'ı test et"""
    print("🔍 JAMA Scraper Test Başlıyor...")
    
    # Test URL
    test_url = "https://jamanetwork.com/journals/jama/fullarticle/2837046"
    print(f"📄 Test URL: {test_url}")
    
    try:
        # 1. Scraper ile HTML çek - daha hızlı timeout
        print("\n1️⃣ HTML içerik çekiliyor...")
        scraper = JAMAScraper(headless=True, timeout=6)  # 6 saniye timeout
        html_content = await scraper.scrape_article(test_url)
        
        if html_content:
            print(f"✅ HTML içerik başarıyla çekildi")
            print(f"   - HTML uzunluğu: {len(html_content)} karakter")
            
            # 2. Parser ile veri çıkar
            print("\n2️⃣ Veri ayrıştırılıyor...")
            parser = DataParser()
            article_data = parser.parse_article(html_content)
            
            if article_data:
                print("✅ Veri başarıyla ayrıştırıldı:")
                print(f"   - Başlık: {article_data.get('title', 'N/A')}")
                print(f"   - DOI: {article_data.get('doi', 'N/A')}")
                
                # Abstract bilgilerini detaylı incele
                abstract = article_data.get('abstract', {})
                if abstract:
                    print(f"\n📋 Abstract Bilgileri:")
                    for key, value in abstract.items():
                        if value:
                            print(f"   - {key}: {value[:200]}...")
                
                # Abstract'ın tam metnini göster
                if 'full' in abstract and abstract['full']:
                    print(f"\n📄 Full Abstract:")
                    print(f"{abstract['full'][:500]}...")
                
                # Population, Intervention, Findings, Settings, Primary Outcome
                print(f"\n🔍 Abstract Bileşenleri:")
                print(f"   - Population: {article_data.get('population', 'N/A')}")
                print(f"   - Intervention: {article_data.get('intervention', 'N/A')}")
                print(f"   - Findings: {article_data.get('findings', 'N/A')}")
                print(f"   - Settings: {article_data.get('settings', 'N/A')}")
                print(f"   - Primary Outcome: {article_data.get('primary_outcome', 'N/A')}")
                
                return article_data
            else:
                print("❌ Veri ayrıştırılamadı")
                return None
        else:
            print("❌ HTML içerik çekilemedi")
            return None
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        return None

async def test_visual_creation(article_data):
    """Görsel oluşturmayı test et"""
    print("\n3️⃣ Görsel oluşturma test ediliyor...")
    
    try:
        from main import _generate_abstract_pptx
        
        pptx_base64 = await _generate_abstract_pptx(article_data)
        
        if pptx_base64:
            print("✅ PPTX başarıyla oluşturuldu")
            print(f"   - Base64 uzunluğu: {len(pptx_base64)} karakter")
            
            # Dosyaya kaydet
            import base64
            pptx_bytes = base64.b64decode(pptx_base64)
            with open("test_output.pptx", "wb") as f:
                f.write(pptx_bytes)
            print(f"   - PPTX dosyası 'test_output.pptx' olarak kaydedildi")
            return True
        else:
            print("❌ PPTX oluşturulamadı")
            return False
            
    except Exception as e:
        print(f"❌ Görsel oluşturma hatası: {e}")
        return False

async def main():
    """Ana test fonksiyonu"""
    print("🚀 JAMA Abstract MCP Scraper Test Başlıyor...")
    print("⚡ Optimize edilmiş hızlı test modu")
    
    # 1. Scraper test
    article_data = await test_scraper()
    
    # 2. Görsel oluşturma test
    if article_data:
        await test_visual_creation(article_data)
    
    print("\n✅ Test tamamlandı!")

if __name__ == "__main__":
    asyncio.run(main()) 