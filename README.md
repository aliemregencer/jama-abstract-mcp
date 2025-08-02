# JAMA Abstract MCP

JAMA tıp dergisi makalelerinden veri çıkarma ve abstract görsel oluşturma MCP servisi.

## 🚀 Özellikler

Bu MCP servisi JAMA makalelerinden veri çıkarma ve abstract görsellerini oluşturma işlemlerini gerçekleştirir.

### ✅ Test Sonuçları

- **Scraping**: ✅ Başarılı
- **Parsing**: ✅ Başarılı  
- **MCP Server**: ✅ Başarılı
- **Abstract Visual Creation**: ✅ Başarılı

### 📋 Available Tools

1. **extract_jama_article** - JAMA makale linkinden makale verilerini çıkarır
2. **create_abstract_visual** - Makale verilerine göre abstract görsel oluşturur ve PPTX formatında döndürür

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
- **Visual Creation**: ~3-5 saniye
- **Total Process**: ~20-40 saniye

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
- Population, Intervention, Findings, Settings, Primary Outcome (abstract görsel için)

#### 2. create_abstract_visual
Makale verilerine göre abstract görsel oluşturur:
- **Input**: `extract_jama_article` tool'undan gelen makale verileri
- **Output**: PPTX formatında abstract görsel (base64 encoded)
- **Özellikler**:
  - JAMA stilinde abstract görsel tasarımı
  - Population, Intervention, Findings, Settings, Primary Outcome bölümleri
  - PowerPoint formatında indirilmeye hazır
  - Otomatik dosya adlandırma

### 📋 Gerekli Kütüphaneler

```bash
pip install -r requirements.txt
```

Yeni eklenen kütüphaneler:
- `python-pptx>=0.6.21` - PPTX oluşturma
- `Pillow>=10.0.0` - Görsel işleme
- `matplotlib>=3.7.0` - Grafik oluşturma
- `seaborn>=0.12.0` - İstatistiksel görselleştirme

## 📖 Detaylı Bilgi

Detaylı deployment bilgileri için `DEPLOYMENT.md` dosyasına bakın.

Proje tamamen çalışır durumda! 🎉
