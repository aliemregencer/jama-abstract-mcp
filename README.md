# JAMA Abstract MCP

JAMA tıp dergisi makalelerinden otomatik abstract görselleri oluşturmak için MCP (Model Context Protocol) servisi.

## 🎯 Amaç

Bu MCP servisi, JAMA Network'ten makale linklerini alarak:
1. Makale verilerini otomatik çıkarır (başlık, yazarlar, özet, vb.)
2. Mevcut abstract görsellerini analiz eder
3. Yeni görsel oluşturmak için tasarım verilerini hazırlar
4. Mastra.ai gibi agent'lara hazır veri sunar

## 🏗️ Mimari

```
jama-abstract-mcp/
├── mcp.yaml              # MCP konfigürasyonu
├── main.py               # FastMCP server
├── scraper.py            # Selenium scraping
├── parser.py             # HTML parsing & veri çıkarma
├── image_analyzer.py     # Mevcut görsel analizi
├── visual_generator.py   # Abstract görsel oluşturma logic'i
├── requirements.txt      # Python bağımlılıkları
└── README.md            # Bu dosya
```

## 🚀 Kurulum

### 1. Repository'yi klonlayın
```bash
git clone <repository-url>
cd jama-abstract-mcp
```

### 2. Python sanal ortamı oluşturun
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 4. Chrome WebDriver'ı yükleyin
WebDriver otomatik olarak indirilecek, ancak Chrome browser kurulu olmalı.

## 📖 Kullanım

### MCP Server Olarak

```bash
python main.py
```

### Tool Fonksiyonları

#### 1. `extract_jama_article(url: str)`
JAMA makale linkinden tüm verileri çıkarır.

```python
# Örnek kullanım
result = await extract_jama_article("https://jamanetwork.com/journals/jama/article-abstract/2812345")
```

**Çıktı:**
- Makale başlığı, yazarlar, özet
- Yayın tarihi, dergi bilgileri
- DOI, makale türü
- Anahtar kelimeler
- Mevcut görsel URL'si (varsa)

#### 2. `analyze_existing_visual(image_url: str)`
Mevcut abstract görselini analiz eder.

```python
# Örnek kullanım  
result = await analyze_existing_visual("https://example.com/abstract-visual.jpg")
```

**Çıktı:**
- Renk paleti analizi
- Layout ve tipografi
- Tasarım öğeleri
- Stil karakteristikleri

#### 3. `generate_visual_data(article_data: dict, style_preferences: dict)`
Yeni görsel oluşturmak için tasarım verilerini hazırlar.

```python
# Örnek kullanım
visual_data = await generate_visual_data(article_data, style_preferences)
```

**Çıktı:**
- Layout spesifikasyonları
- Renk şeması
- Tipografi ayarları
- Görsel öğeler
- Export ayarları

#### 4. `full_pipeline(url: str, analyze_existing: bool = True)`
Tam pipeline - tüm işlemleri sırayla çalıştırır.

## 🔧 Konfigürasyon

### mcp.yaml
MCP server ayarları ve tool tanımları.

### Selenium Ayarları
`scraper.py` içinde Chrome options'ları özelleştirilebilir:

```python
# Headless mode
scraper = JAMAScraper(headless=True)

# Screenshot için
await scraper.get_page_screenshots(url, "debug.png")
```

### Görsel Analiz Ayarları
`image_analyzer.py` içinde analiz parametreleri:

```python
# Renk paleti boyutu
color_palette = self._extract_color_palette(num_colors=8)

# Karmaşıklık eşikleri
complexity_score = (edge_density * 0.6) + (color_complexity * 0.4)
```

## 📊 Veri Yapısı

### Makale Verileri
```json
{
  "title": "Makale Başlığı",
  "authors": [
    {
      "name": "Dr. John Doe",
      "degrees": "MD, PhD", 
      "affiliation": "Harvard Medical School"
    }
  ],
  "abstract": {
    "full": "Tam özet metni...",
    "objective": "Amaç...",
    "results": "Sonuçlar...",
    "conclusions": "Sonuçlar..."
  },
  "keywords": ["keyword1", "keyword2"],
  "publication_date": "2024-01-15",
  "journal_info": {
    "name": "JAMA",
    "volume": "331",
    "issue": "2"
  },
  "doi": "10.1001/jama.2024.12345",
  "existing_visual_url": "https://...",
  "metadata": {...}
}
```

### Görsel Analiz Sonuçları
```json
{
  "dimensions": {"width": 800, "height": 600},
  "color_palette": [
    {
      "rgb": [31, 71, 136],
      "hex": "#1f4788", 
      "hsl": [220, 0.63, 0.33],
      "percentage": 25.3
    }
  ],
  "layout_analysis": {
    "has_grid": true,
    "text_regions": [...],
    "alignment": "grid"
  },
  "typography_analysis": {
    "text_density": 0.15,
    "estimated_font_size": 12,
    "font_weight": "medium"
  },
  "style_characteristics": {
    "color_scheme": "professional",
    "design_style": "modern_geometric",
    "mood": "professional",
    "era": "contemporary"
  }
}
```

### Görsel Oluşturma Verileri
```json
{
  "metadata": {...},
  "content": {
    "primary_title": "Makale Başlığı",
    "authors": "Dr. John Doe et al.",
    "sections": [
      {
        "type": "structured_section",
        "label": "Objective",
        "content": "...",
        "priority": "high"
      }
    ]
  },
  "design": {
    "theme": "medical_professional",
    "complexity": "clean"
  },
  "layout": {
    "type": "balanced_two_section",
    "columns": 2,
    "canvas_size": {"width": 1000, "height": 750}
  },
  "typography": {
    "font_family": {"primary": "Source Sans Pro"},
    "font_sizes": {"title": 24, "body": 12}
  },
  "colors": {
    "palette": {
      "primary": "#1f4788",
      "background": "#ffffff"
    }
  },
  "elements": {
    "icons": [...],
    "decorative_elements": {...}
  },
  "export_settings": {...}
}
```

## 🎨 Tasarım Özellikleri

### Renk Paletleri
- **Classic Medical**: JAMA mavi (#1f4788) temalı
- **Modern Clinical**: Gri tonları
- **Research Focused**: Yeşil vurgulu

### Layout Tipleri  
- **Compact Single Column**: Kısa içerik için
- **Balanced Two Section**: Orta uzunluk
- **Structured Multi Section**: Uzun/karmaşık içerik

### Tipografi
- **Primary**: Source Sans Pro (okunabilirlik)
- **Secondary**: Georgia (serif vurgu) 
- **Responsive**: İçerik uzunluğuna göre boyut

## 🔍 Debugging

### Log Seviyeleri
```