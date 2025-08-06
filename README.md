# JAMA Abstract MCP

JAMA Network makalelerini scraping yöntemiyle analiz eden MCP (Model Context Protocol) servisi.

## Özellikler

- JAMA Network makale linklerini otomatik olarak analiz eder
- Makale içeriğini scraping yöntemiyle çıkarır
- İstenen alanları JSON formatında döner
- Sadece scraping yapar, içerik üretmez veya yeniden yazmaz

## Çıktı JSON Yapısı

Tool aşağıdaki alanları içeren JSON döner:

```json
{
  "title": "Makalenin başlığı",
  "authors": "Yazar isimleri",
  "population": "Katılımcı bilgileri",
  "intervention": "Müdahale yöntemi",
  "outcome": "Birincil çıktı veya gözlemler",
  "findings": "Sonuçlar",
  "settings": "Yapılan yer veya merkez bilgisi",
  "source_url": "Makalenin URL'si"
}
```

## Kurulum

1. Python 3.8+ gerekli
2. Virtual environment oluşturun:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # veya
   .\venv\Scripts\Activate.ps1  # Windows
   ```

3. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Kullanım

### MCP Server Olarak

```bash
python main.py
```

### HTTP Server Olarak

```bash
python main.py --transport http --host 127.0.0.1 --port 8000
```

## Tool Kullanımı

### extract_jama_article

JAMA Network makale linkinden makale verilerini çıkarır.

**Input:**
- `url`: JAMA Network makale URL'si (string)

**Output:**
- JSON formatında makale özeti

**Örnek:**
```python
result = await extract_jama_article("https://jamanetwork.com/journals/jama/fullarticle/...")
```

**Örnek Çıktı:**
```json
{
  "title": "Effect of Vitamin D Supplementation on Cardiovascular Disease",
  "authors": "John Smith, MD; Jane Doe, PhD",
  "population": "10,000 participants aged 50-75 years",
  "intervention": "Daily vitamin D supplementation (2000 IU)",
  "outcome": "Primary outcome was major cardiovascular events",
  "findings": "No significant difference in cardiovascular events between groups",
  "settings": "Multi-center study across 50 hospitals",
  "source_url": "https://jamanetwork.com/journals/jama/fullarticle/..."
}
```

## Teknik Detaylar

- **Scraper**: Selenium WebDriver kullanarak sayfa içeriğini çıkarır
- **Parser**: BeautifulSoup ile HTML içeriğini analiz eder
- **Pattern Matching**: Regex ile belirli alanları tespit eder
- **Error Handling**: Kapsamlı hata yönetimi

## Gereksinimler

- Chrome/Chromium tarayıcısı (WebDriver otomatik kurulur)
- Python 3.8+
- Internet bağlantısı

## Lisans

MIT License
