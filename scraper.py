"""
JAMA Web Scraper
Selenium kullanarak JAMA makalelerini scrape eder (Smithery için optimize edildi)
"""

import asyncio
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

class JAMAScraper:
    def __init__(self, headless: bool = True, timeout: int = 8):
        """
        JAMA Scraper initialize
        
        Args:
            headless: Tarayıcıyı gizli modda çalıştır
            timeout: Sayfa yükleme timeout süresi (Smithery için kısaltıldı)
        """
        self.headless = headless
        self.timeout = timeout
        self.driver = None
    
    def _setup_driver(self) -> webdriver.Chrome:
        """Chrome driver'ı otomatik kurulum ile ayarla"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Smithery için ultra agresif performans optimizasyonları
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--disable-css")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--memory-pressure-off")
        chrome_options.add_argument("--max_old_space_size=2048")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-field-trial-config")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # WebDriver otomatik kurulum
        try:
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"ChromeDriver kurulum hatası: {e}")
            # Fallback: sistem PATH'den dene
            return webdriver.Chrome(options=chrome_options)
    
    async def scrape_article(self, url: str) -> Optional[str]:
        """
        JAMA makale sayfasını scrape et
        
        Args:
            url: JAMA makale URL'si
            
        Returns:
            HTML içerik veya None
        """
        try:
            self.driver = self._setup_driver()
            
            # Sayfayı yükle
            self.driver.get(url)
            
            # Smithery için ultra hızlı yükleme
            wait = WebDriverWait(self.driver, 2)  # Sadece 2 saniye bekle
            
            # Ana içerik alanlarından birinin yüklenmesini bekle
            try:
                wait.until(EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "article-full-text")),
                    EC.presence_of_element_located((By.CLASS_NAME, "article-header")),
                    EC.presence_of_element_located((By.TAG_NAME, "article")),
                    EC.presence_of_element_located((By.CLASS_NAME, "content")),
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                ))
            except TimeoutException:
                print("Ana içerik alanları bulunamadı, devam ediliyor...")
            
            # Cookie/popup'ları kapat (varsa) - ultra hızlı
            await self._handle_popups_ultra_fast()
            
            # Minimum bekleme
            await asyncio.sleep(0.1)
            
            # HTML içeriğini al
            html_content = self.driver.page_source
            
            return html_content
            
        except TimeoutException:
            print(f"Timeout: Sayfa yüklenemedi - {url}")
            return None
        except WebDriverException as e:
            print(f"WebDriver hatası: {e}")
            return None
        except Exception as e:
            print(f"Beklenmeyen hata: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()
    
    async def _handle_popups_ultra_fast(self):
        """Cookie consent ve diğer popup'ları ultra hızlı kapat (Smithery için)"""
        try:
            # Ultra hızlı cookie consent butonu
            cookie_buttons = [
                "//button[contains(text(), 'Accept')]",
                "//button[contains(text(), 'I Accept')]",
                "//button[@id='onetrust-accept-btn-handler']",
                "//button[contains(@class, 'cookie-accept')]",
                "//button[contains(@class, 'consent-accept')]"
            ]
            
            for button_xpath in cookie_buttons:
                try:
                    button = WebDriverWait(self.driver, 0.5).until(  # Sadece 0.5 saniye bekle
                        EC.element_to_be_clickable((By.XPATH, button_xpath))
                    )
                    button.click()
                    await asyncio.sleep(0.1)  # Minimum bekleme
                    break
                except TimeoutException:
                    continue
            
            # Ultra hızlı popup kapatma
            try:
                close_selectors = [
                    "[data-dismiss='modal']",
                    ".modal-close",
                    ".close",
                    ".popup-close",
                    "[aria-label='Close']"
                ]
                
                for selector in close_selectors:
                    try:
                        close_button = WebDriverWait(self.driver, 0.5).until(  # Sadece 0.5 saniye bekle
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        close_button.click()
                        await asyncio.sleep(0.1)  # Minimum bekleme
                        break
                    except TimeoutException:
                        continue
                        
            except Exception:
                pass
                
        except Exception as e:
            print(f"Popup kapatma hatası: {e}")
    
    async def _handle_popups_fast(self):
        """Cookie consent ve diğer popup'ları hızlı kapat (eski versiyon)"""
        await self._handle_popups_ultra_fast()
    
    async def _handle_popups(self):
        """Cookie consent ve diğer popup'ları kapat (eski versiyon)"""
        await self._handle_popups_ultra_fast()
    
    async def get_page_screenshots(self, url: str, save_path: str = "screenshot.png") -> bool:
        """
        Sayfa ekran görüntüsü al (debug için)
        
        Args:
            url: URL
            save_path: Kayıt yolu
            
        Returns:
            Başarılı mı?
        """
        try:
            self.driver = self._setup_driver()
            self.driver.get(url)
            
            await asyncio.sleep(3)
            self.driver.save_screenshot(save_path)
            
            return True
            
        except Exception as e:
            print(f"Screenshot hatası: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def __del__(self):
        """Cleanup"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass