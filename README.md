# Academic Article MCP

Akademik makalelerden ana metin çıkarma MCP (Model Context Protocol) servisi.

## Özellikler

- Akademik makale URL'lerini otomatik olarak analiz eder
- Makale içeriğini scraping yöntemiyle çıkarır
- Sadece akademik makalenin ana metnini döner
- Navigasyon, footer, reklamlar gibi gereksiz elementleri filtreler
- Sadece scraping yapar, içerik üretmez veya yeniden yazmaz

## Çıktı JSON Yapısı

Tool aşağıdaki alanları içeren JSON döner:

```json
{
  "plain_text": "Makalenin ana metni burada yer alır",
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

Akademik makale URL'sinden ana metni çıkarır.

**Input:**
- `url`: Akademik makale URL'si (string)

**Output:**
- JSON formatında makale ana metni

**Örnek:**
```python
result = await extract_jama_article("https://jamanetwork.com/journals/jama/fullarticle/...")
```

**Örnek Çıktı:**
```json
{
  "plain_text": "Guided Internet-Based Cognitive Behavior Therapy for Women With Bulimia Nervosa: A Randomized Clinical Trial\n\nAbstract\n\nImportance: Despite the rising prevalence of bulimia nervosa and the associated risks of chronicity and severe physical and psychological morbidity, access to effective treatment remains poor...\n\nObjective: To determine the effectiveness and acceptability of a guided ICBT program to treat women with bulimia nervosa in Japan...\n\nDesign, Setting, and Participants: This randomized clinical trial was conducted at 7 university hospitals in Japan...\n\nInterventions: Both the control and intervention groups received usual care...\n\nMain Outcomes and Measures: Severity of bulimia nervosa, measured by the weekly combined frequency of episodes involving binge eating and compensatory behaviors...\n\nResults: A total of 61 women met the eligibility criteria and were randomized...\n\nConclusions and Relevance: In this randomized clinical trial, the intervention group experienced a significant decrease in bulimia symptoms compared with the control group...",
  "source_url": "https://jamanetwork.com/journals/jamanetworkopen/fullarticle/..."
}
```

## Teknik Detaylar

- **Scraper**: Selenium WebDriver kullanarak sayfa içeriğini çıkarır
- **Parser**: BeautifulSoup ile HTML içeriğini analiz eder ve akademik makale bölümlerini filtreler
- **Academic Content Extraction**: Sadece akademik makale ana metnini çıkarır (başlık, abstract, methods, results, conclusions)
- **Filtering**: Navigasyon, footer, reklamlar, popup'lar gibi gereksiz elementleri kaldırır
- **Error Handling**: Kapsamlı hata yönetimi

## Filtrelenen Elementler

- Navigasyon bar, header, footer, site menüleri
- Reklamlar, banner'lar, popup'lar, modal'lar
- Cookie bildirimleri, privacy notice'lar
- Login, signup, user menu, search
- Social media, share buttons, comments
- Newsletter, subscribe, back-to-top butonları
- Script, style, iframe, embed elementleri
- Gizli elementler (display: none)

## Akademik Makale Bölümleri

Tool aşağıdaki akademik makale bölümlerini çıkarır:

- **Başlık ve Yazar Bilgileri**: Makale başlığı, yazar isimleri
- **Abstract**: Makale özeti
- **Introduction**: Giriş bölümü
- **Methods/Methodology**: Yöntem bölümü
- **Results/Findings**: Sonuçlar bölümü
- **Discussion**: Tartışma bölümü
- **Conclusion**: Sonuç bölümü
- **References**: Kaynaklar

## Gereksinimler

- Chrome/Chromium tarayıcısı (WebDriver otomatik kurulur)
- Python 3.8+
- Internet bağlantısı

## Lisans

MIT License
