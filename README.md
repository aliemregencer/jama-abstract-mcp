# JAMA Abstract MCP

JAMA tıp dergisi makalelerinden veri çıkarma MCP servisi.

## 🚀 Özellikler

Bu MCP servisi JAMA makalelerinden veri çıkarma ve abstract görsellerini alma işlemlerini gerçekleştirir.

### ✅ Test Sonuçları

- **Scraping**: ✅ Başarılı
- **Parsing**: ✅ Başarılı  
- **MCP Server**: ✅ Başarılı

### 📋 Available Tools

1. **extract_jama_article** - JAMA makale linkinden makale verilerini çıkarır
2. **get_article_visual** - Varsa makalenin abstract görselini alır

### 🔧 Configuration

```yaml
# mcp.yaml
server:
  command: python
  args: ["main.py", "--transport", "stdio"]
  env:
    PYTHONPATH: "."
    PYTHONUNBUFFERED: "1"
```

### 📊 Performance

- **Scraping**: ~15-30 saniye
- **Parsing**: ~1-2 saniye
- **Total Process**: ~20-35 saniye

## 🎯 Kullanım

JAMA makale URL'leri ile kullanılabilir:

```
https://jamanetwork.com/journals/jama/article-abstract/[article-id]
```

### Tool Kullanımı

#### 1. extract_jama_article
Makale linkinden tüm makale verilerini çıkarır:
- Başlık
- Yazarlar
- Abstract
- Anahtar kelimeler
- Yayın tarihi
- Dergi bilgileri
- DOI

#### 2. get_article_visual
Makale linkinden abstract görselini alır (varsa):
- Görsel URL'si
- Makale başlığı
- Görsel varlık durumu

## 📖 Detaylı Bilgi

Detaylı deployment bilgileri için `DEPLOYMENT.md` dosyasına bakın.

Proje tamamen çalışır durumda! 🎉
