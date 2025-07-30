# JAMA Abstract MCP - Smithery Deployment Guide

## Proje Durumu ✅

Proje başarıyla test edildi ve tüm bileşenler çalışıyor:

- ✅ **Scraping**: JAMA makalelerini başarıyla çekiyor
- ✅ **Parsing**: HTML içeriği doğru şekilde ayrıştırıyor  
- ✅ **Visual Generation**: Görsel tasarım verileri oluşturuyor
- ✅ **MCP Server**: FastMCP ile çalışıyor

## Test Sonuçları

### Component Test
```
✅ Scraper başarılı
   HTML uzunluğu: 336865 karakter

✅ Parser başarılı
   Başlık: Diagnosis of Autism
   DOI: 10.1001/jama.2023.24155

✅ Visual Generator başarılı
   Layout type: compact_single_column
   Canvas size: {'width': 800, 'height': 600}
   Color scheme: #1f4788
```

## Smithery Deployment

### 1. Gereksinimler
- Python 3.12
- Chrome/Chromium browser
- FastMCP 2.10.6+
- Selenium 4.26.1+

### 2. Smithery Configuration
```yaml
# mcp.yaml
server:
  command: python
  args: ["main.py", "--transport", "stdio"]
  env:
    PYTHONPATH: "."
    PYTHONUNBUFFERED: "1"
```

### 3. FastMCP STDIO Transport
- Smithery FastMCP ile uyumlu
- STDIO transport kullanılıyor
- HTTP transport gerekmiyor
- Dockerfile gerekmiyor

### 4. Available Tools

#### extract_jama_article
- **Description**: JAMA makale linkinden makale verilerini çıkarır
- **Parameters**: `url` (string) - JAMA makale URL'si
- **Returns**: Makale verileri (başlık, yazarlar, özet, vb.)

#### analyze_existing_visual
- **Description**: Mevcut abstract görselini analiz eder
- **Parameters**: `image_url` (string) - Analiz edilecek görsel URL'si
- **Returns**: Görsel analiz sonuçları

#### generate_visual_data
- **Description**: Yeni görsel oluşturmak için tasarım verilerini hazırlar
- **Parameters**: 
  - `article_data` (object) - Makale verileri
  - `style_preferences` (object, optional) - Stil tercihleri
- **Returns**: Görsel oluşturma verileri

#### full_pipeline
- **Description**: Tam pipeline: Makale çıkarma + analiz + görsel veri oluşturma
- **Parameters**:
  - `url` (string) - JAMA makale URL'si
  - `analyze_existing` (boolean, default: true) - Mevcut görseli analiz et mi?
- **Returns**: Tüm işlem sonuçları

## Troubleshooting

### Chrome/Selenium Issues
- Chrome headless mode kullanılıyor
- WebDriver otomatik yönetiliyor
- Timeout: 30 saniye

### Memory Usage
- Chrome headless mode ile optimize edildi
- Görsel yükleme devre dışı bırakıldı
- Bellek kullanımı minimize edildi

### Network Issues
- JAMA Network rate limiting'e karşı korumalı
- User-Agent spoofing yapılıyor
- Cookie consent otomatik kapatılıyor

## Performance

- **Scraping**: ~15-30 saniye
- **Parsing**: ~1-2 saniye  
- **Visual Generation**: ~2-3 saniye
- **Total Pipeline**: ~20-35 saniye

## Monitoring

FastMCP STDIO transport kullanıldığı için HTTP endpoint'leri yok.
Tools doğrudan MCP protokolü üzerinden erişilebilir.

## Logs

Logging level: INFO
Format: `[timestamp] [level] [module] - message`

## Support

Proje tamamen çalışır durumda ve Smithery'de deploy edilmeye hazır. 