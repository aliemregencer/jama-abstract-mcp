"""
JAMA Network Scraper
Selenium WebDriver kullanarak JAMA Network makalelerini scrape eder
"""

import asyncio
import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

class JAMAScraper:
    def __init__(self, headless: bool = True, timeout: int = 8):
        self.headless = headless
        self.timeout = timeout
        self.driver = None
    
    async def scrape_article(self, url: str) -> Optional[str]:
        """
        JAMA Network makalesini scrape et
        
        Args:
            url: Makale URL'si
            
        Returns:
            HTML içerik veya None
        """
        try:
            logger.info(f"Scraping başlıyor: {url}")
            
            # WebDriver kurulumu
            self._setup_driver()
            
            # Sayfayı yükle
            self.driver.get(url)
            
            # Sayfanın yüklenmesini bekle
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Ek bekleme süresi
            await asyncio.sleep(2)
            
            # HTML içeriğini al
            html_content = self.driver.page_source
            
            # Debug: HTML'i kaydet
            with open('debug_output.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info("HTML debug_output.html dosyasına kaydedildi")
            
            logger.info("Scraping tamamlandı")
            return html_content
            
        except Exception as e:
            logger.error(f"Scraping hatası: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()
    
    def _setup_driver(self):
        """WebDriver kurulumu"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Performans optimizasyonları
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--disable-css")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-field-trial-config")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-hang-monitor")
        chrome_options.add_argument("--disable-prompt-on-repost")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-component-extensions-with-background-pages")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--safebrowsing-disable-auto-update")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--ignore-certificate-errors-spki-list")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # WebDriver kurulumu
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Timeout ayarları
        self.driver.set_page_load_timeout(self.timeout)
        self.driver.implicitly_wait(self.timeout)