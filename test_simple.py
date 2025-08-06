#!/usr/bin/env python3
"""
Academic Article Test Script
"""

import asyncio
import json
from main import _extract_jama_article

async def test_academic_article():
    """Test the academic article extraction tool"""
    
    print("🔍 Academic Article Test")
    print("=" * 30)
    
    # Test URL - JAMA Network Open makalesi
    test_url = "https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2837260?resultClick=1"
    
    try:
        print(f"📋 Test URL: {test_url}")
        print("🔄 Tool çalıştırılıyor...")
        
        result = await _extract_jama_article(test_url)
        
        print("✅ Tool tamamlandı!")
        print()
        print("📊 Sonuç:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Kontrol
        if "plain_text" in result:
            text = result["plain_text"]
            print(f"\n📏 Ana metin uzunluğu: {len(text)} karakter")
            print(f"📄 İlk 800 karakter:")
            print("-" * 50)
            print(text[:800])
            print("-" * 50)
            
            # İçerik analizi
            lines = text.split('\n')
            print(f"\n📋 Satır sayısı: {len(lines)}")
            print(f"📄 Boş olmayan satır sayısı: {len([l for l in lines if l.strip()])}")
            
            # Akademik bölüm kontrolü
            academic_keywords = ['abstract', 'introduction', 'methods', 'results', 'conclusion', 'discussion']
            found_sections = []
            for keyword in academic_keywords:
                if keyword.lower() in text.lower():
                    found_sections.append(keyword)
            
            print(f"📚 Bulunan akademik bölümler: {', '.join(found_sections)}")
            
        else:
            print("❌ plain_text alanı bulunamadı")
        
        print()
        print("🎉 Test tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_academic_article()) 