# JAMA Abstract MCP

JAMA tıp dergisi makalelerinden abstract görselleri oluşturmak için veri çıkarma MCP servisi.

## 🚀 Smithery Deployment

Bu proje Smithery'de başarıyla deploy edilmiştir. FastMCP STDIO transport kullanılarak optimize edilmiştir.

### ✅ Test Sonuçları

- **Scraping**: ✅ Başarılı
- **Parsing**: ✅ Başarılı  
- **Visual Generation**: ✅ Başarılı
- **MCP Server**: ✅ Başarılı

### 📋 Available Tools

1. **extract_jama_article** - JAMA makale verilerini çıkarır
2. **generate_visual_data** - Görsel tasarım verileri oluşturur
3. **full_pipeline** - Tam işlem pipeline'ı

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
- **Visual Generation**: ~2-3 saniye
- **Total Pipeline**: ~20-35 saniye

## 📖 Detaylı Bilgi

Detaylı deployment bilgileri için `DEPLOYMENT.md` dosyasına bakın.

## 🎯 Kullanım

Smithery'de deploy edildikten sonra, JAMA makale URL'leri ile kullanılabilir:

```
https://jamanetwork.com/journals/jama/article-abstract/[article-id]
```

Proje tamamen çalışır durumda ve Smithery'de başarıyla deploy edilmiştir! 🎉
