# JAMA Abstract MCP - Smithery Deployment

## Smithery'de Deploy Edilmiş MCP

Bu MCP Smithery'de deploy edilmiş durumda ve şu endpoint üzerinden erişilebilir:
```
https://server.smithery.ai/@aliemregencer/jama-abstract-mcp/mcp?api_key=052c1489-c4b2-41c1-8f17-022474b631ec&profile=agreed-newt-U9p9aj
```

## Tool'lar

### 1. extract_jama_article
JAMA makale linkinden makale verilerini çıkarır.

**Parametreler:**
- `url` (string): JAMA makale URL'si (örn: https://jamanetwork.com/journals/jama/article-abstract/...)

**Dönen Veri:**
- `success` (boolean): İşlem başarılı mı?
- `data` (object): Makale verileri
  - `title`: Makale başlığı
  - `authors`: Yazar listesi
  - `abstract`: Özet bilgileri
  - `population`: Çalışma popülasyonu
  - `intervention`: Müdahale bilgisi
  - `findings`: Bulgular
  - `settings`: Çalışma ortamı
  - `primary_outcome`: Birincil sonuç
- `error` (string): Hata mesajı (varsa)

### 2. create_abstract_visual
Makale verilerine göre abstract görsel oluşturur ve PPTX formatında döndürür.

**Parametreler:**
- `article_data` (object): extract_jama_article tool'undan gelen makale verileri

**Dönen Veri:**
- `success` (boolean): İşlem başarılı mı?
- `pptx_base64` (string): Base64 encoded PPTX dosyası
- `filename` (string): Dosya adı
- `message` (string): Bilgi mesajı
- `error` (string): Hata mesajı (varsa)

## Kullanım Örneği

### Postman ile Test

1. **POST** isteği gönderin:
   ```
   POST https://server.smithery.ai/@aliemregencer/jama-abstract-mcp/mcp?api_key=052c1489-c4b2-41c1-8f17-022474b631ec&profile=agreed-newt-U9p9aj
   ```

2. **Headers:**
   ```
   Content-Type: application/json
   ```

3. **Body (extract_jama_article için):**
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

4. **Body (create_abstract_visual için):**
   ```json
   {
     "jsonrpc": "2.0",
     "id": 2,
     "method": "tools/call",
     "params": {
       "name": "create_abstract_visual",
       "arguments": {
         "article_data": {
           "success": true,
           "data": {
             "title": "Makale Başlığı",
             "population": "100 hasta",
             "intervention": "İlaç tedavisi",
             "findings": "Anlamlı iyileşme",
             "settings": "Çok merkezli çalışma",
             "primary_outcome": "Survival rate"
           }
         }
       }
     }
   }
   ```

## Sorun Giderme

### Tool'lar Görünmüyor
1. MCP'nin yeniden deploy edildiğinden emin olun
2. HTTP transport modunun aktif olduğunu kontrol edin
3. Port 8000'in açık olduğunu doğrulayın

### Postman Bağlantı Hatası
1. API key'in doğru olduğunu kontrol edin
2. URL'nin tam olduğunu doğrulayın
3. Content-Type header'ının `application/json` olduğunu kontrol edin
4. JSON-RPC 2.0 formatını kullandığınızdan emin olun

### Timeout Hataları
1. JAMA URL'sinin geçerli olduğunu kontrol edin
2. İnternet bağlantısını kontrol edin
3. JAMA sitesinin erişilebilir olduğunu doğrulayın

## Teknik Detaylar

- **Transport**: HTTP
- **Host**: 0.0.0.0
- **Port**: 8000
- **Framework**: FastMCP
- **Python Version**: 3.8+

## Güncellemeler

### v1.0.1 (Güncel)
- HTTP transport desteği eklendi
- Tool tanımları düzeltildi
- Smithery optimizasyonları yapıldı
- Timeout süreleri artırıldı
- Hata yönetimi iyileştirildi 