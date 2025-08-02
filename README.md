# JAMA Abstract MCP

JAMA tıp dergisi makalelerinden veri çıkarma ve abstract görsel oluşturma MCP servisi.

## 🚀 Smithery'de Deploy Edilmiş

Bu MCP Smithery'de deploy edilmiş durumda ve şu endpoint üzerinden erişilebilir:

```
https://server.smithery.ai/@aliemregencer/jama-abstract-mcp/mcp?api_key=052c1489-c4b2-41c1-8f17-022474b631ec&profile=agreed-newt-U9p9aj
```

## 🛠️ Tool'lar

### 1. extract_jama_article
JAMA makale linkinden makale verilerini çıkarır.

**Parametreler:**
- `url` (string): JAMA makale URL'si

**Dönen Veri:**
- Makale başlığı, yazarlar, özet, popülasyon, müdahale, bulgular, ortam ve birincil sonuç

### 2. create_abstract_visual
Makale verilerine göre abstract görsel oluşturur ve PPTX formatında döndürür.

**Parametreler:**
- `article_data` (object): extract_jama_article tool'undan gelen makale verileri

**Dönen Veri:**
- Base64 encoded PPTX dosyası

## 📋 Kullanım Örneği

### Postman ile Test

1. **POST** isteği gönderin:
   ```
   POST https://server.smithery.ai/@aliemregencer/jama-abstract-mcp/mcp?api_key=052c1489-c4b2-41c1-8f17-022474b631ec&profile=agreed-newt-U9p9aj
   ```

2. **Headers:**
   ```
   Content-Type: application/json
   ```

3. **Body (extract_jama_article):**
   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "tools/call",
     "params": {
       "name": "extract_jama_article",
       "arguments": {
         "url": "https://jamanetwork.com/journals/jama/article-abstract/..."
       }
     }
   }
   ```

## 🧪 Test

Test dosyasını çalıştırmak için:

```bash
python test_tools.py
```

Bu script Smithery endpoint'ini test eder ve sonuçları gösterir.

## 🔧 Teknik Detaylar

- **Framework**: FastMCP
- **Transport**: HTTP
- **Host**: 0.0.0.0
- **Port**: 8000
- **Python Version**: 3.8+

## 📦 Bağımlılıklar

- fastmcp>=0.9.0
- selenium>=4.15.0
- beautifulsoup4>=4.12.0
- python-pptx>=0.6.21
- matplotlib>=3.7.0
- seaborn>=0.12.0

## 🚨 Sorun Giderme

### Tool'lar Görünmüyor
1. MCP'nin yeniden deploy edildiğinden emin olun
2. HTTP transport modunun aktif olduğunu kontrol edin
3. Port 8000'in açık olduğunu doğrulayın

### Postman Bağlantı Hatası
1. API key'in doğru olduğunu kontrol edin
2. Content-Type header'ının `application/json` olduğunu kontrol edin
3. JSON-RPC 2.0 formatını kullandığınızdan emin olun

## 📄 Lisans

MIT License

## 👨‍💻 Geliştirici

Ali Emre Gencer
