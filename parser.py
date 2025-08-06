"""
Academic Article HTML Parser
HTML içerikten sadece akademik makalelerin ana metnini çıkarır
"""

import re
from typing import Dict, Any
from bs4 import BeautifulSoup

class DataParser:
    def __init__(self):
        """Parser initialize"""
        self.soup = None
    
    def parse_article(self, html_content: str) -> Dict[str, Any]:
        """
        HTML içerikten sadece akademik makalenin ana metnini çıkar
        
        Args:
            html_content: HTML içerik
            
        Returns:
            Akademik makalenin ana metni
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        
        # Gereksiz elementleri kaldır
        self._remove_unwanted_elements()
        
        # Akademik makale ana metnini çıkar
        plain_text = self._extract_academic_content()
        
        return {
            "plain_text": plain_text
        }
    
    def _remove_unwanted_elements(self):
        """Gereksiz elementleri kaldır"""
        # Kaldırılacak elementler
        unwanted_selectors = [
            # Navigasyon ve header/footer
            'nav', '.navigation', '.navbar', '.header', '.footer', '.site-header', '.site-footer',
            '.breadcrumb', '.breadcrumbs', '.pagination', '.pager',
            
            # Reklamlar ve popup'lar
            '.advertisement', '.ads', '.banner', '.popup', '.modal', '.overlay',
            '.cookie-notice', '.consent', '.privacy-notice', '.gdpr-notice',
            
            # Kullanıcı arayüzü
            '.login', '.signup', '.auth', '.user-menu', '.user-panel',
            '.search', '.filter', '.sort', '.tools', '.sidebar',
            
            # Sosyal medya ve paylaşım
            '.social', '.share', '.social-media', '.sharing',
            '.comments', '.related', '.recommended', '.suggestions',
            
            # Teknik elementler
            'script', 'style', 'noscript', 'iframe', 'embed',
            '.hidden', '.invisible', '[style*="display: none"]',
            '.skip-link', '.sr-only', '.visually-hidden',
            
            # Site özel elementleri
            '.site-menu', '.main-menu', '.top-bar', '.bottom-bar',
            '.newsletter', '.subscribe', '.newsletter-signup',
            '.back-to-top', '.scroll-to-top', '.floating-button',
            
            # Reklam widget'ları
            '.widget-ConfigurableAd', '.SCM-SharedWidgets-AsyncAdLoader',
            '.widget-DynamicWidgetLayout', '.widget-WidgetLoader'
        ]
        
        for selector in unwanted_selectors:
            elements = self.soup.select(selector)
            for element in elements:
                element.decompose()
    
    def _extract_academic_content(self) -> str:
        """Akademik makale ana metnini çıkar"""
        # Sadece body içeriğini al
        body = self.soup.find('body')
        if not body:
            return "İçerik bulunamadı"
        
        # Akademik makale içeriği için özel seçiciler
        academic_content = []
        
        # 1. JAMA Network özel makale container'ı ara
        article_selectors = [
            '.widget-ArticleFulltext',  # JAMA Network ana makale container'ı
            'article', '.article', '.paper', '.manuscript',
            '.article-content', '.paper-content', '.manuscript-content',
            '.full-text', '.article-full-text', '.paper-full-text',
            '.main-content', '.content-main', '.article-body',
            '[role="main"]', '.main', '.content',
            '.article-container', '.paper-container', '.manuscript-container'
        ]
        
        article_container = None
        for selector in article_selectors:
            article_container = self.soup.select_one(selector)
            if article_container:
                break
        
        # Eğer makale container bulunamazsa body'yi kullan
        if not article_container:
            article_container = body
        
        # 2. JAMA Network özel akademik makale bölümlerini çıkar
        academic_sections = [
            # Başlık ve yazar bilgileri
            'h1', 'h2', '.title', '.article-title', '.paper-title',
            '.author', '.authors', '.byline', '.author-info',
            '.meta-authors--limited', '.meta-authors--remaining',
            
            # Abstract ve özet
            '.abstract', '.summary', '.article-abstract', '.paper-abstract',
            '[data-testid="abstract"]', '.abstract-content',
            '#AbstractSection', '.section-type-abstract',
            
            # Ana içerik bölümleri
            '.introduction', '.background', '.methods', '.methodology',
            '.materials', '.materials-and-methods', '.results', '.findings',
            '.discussion', '.conclusion', '.conclusions', '.summary',
            
            # Paragraflar
            'p', '.paragraph', '.text', '.para',
            
            # Alt başlıklar
            'h3', 'h4', 'h5', 'h6',
            
            # Listeler
            'ul', 'ol', 'li',
            
            # Tablolar
            'table', '.table', '.data-table',
            
            # Referanslar
            '.references', '.bibliography', '.citations', '.works-cited'
        ]
        
        # Her bölüm için içerik topla
        for section in academic_sections:
            elements = article_container.select(section)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 5:  # Kısa metinleri filtrele
                    academic_content.append(text)
        
        # 3. Eğer yeterli içerik yoksa, daha geniş arama yap
        if len(academic_content) < 10:
            # Tüm div'leri tara
            all_divs = article_container.find_all('div')
            for div in all_divs:
                text = div.get_text(strip=True)
                if text and len(text) > 20:  # Uzun metinleri al
                    # Gereksiz içerikleri filtrele
                    if not any(skip in text.lower() for skip in [
                        'cookie', 'privacy', 'terms', 'contact', 'about', 'home',
                        'menu', 'search', 'login', 'sign up', 'subscribe', 'newsletter',
                        'follow us', 'share', 'back to top', '©', 'all rights reserved',
                        'advertisement', 'ad', 'sponsored', 'promoted'
                    ]):
                        academic_content.append(text)
        
        # 4. Eğer hala yeterli içerik yoksa, tüm metni al ve temizle
        if len(academic_content) < 5:
            all_text = article_container.get_text()
            # Metni temizle ve bölümlere ayır
            lines = all_text.split('\n')
            clean_lines = []
            for line in lines:
                line = line.strip()
                # Gereksiz satırları filtrele
                if (line and len(line) > 10 and 
                    not line.startswith('©') and 
                    not line.startswith('Privacy') and
                    not line.startswith('Cookie') and
                    not line.startswith('Terms') and
                    not line.startswith('Contact') and
                    not line.startswith('About') and
                    not line.startswith('Home') and
                    not line.startswith('Menu') and
                    not line.startswith('Search') and
                    not line.startswith('Login') and
                    not line.startswith('Sign up') and
                    not line.startswith('Subscribe') and
                    not line.startswith('Newsletter') and
                    not line.startswith('Follow us') and
                    not line.startswith('Share') and
                    not line.startswith('Back to top')):
                    clean_lines.append(line)
            return '\n\n'.join(clean_lines)
        
        # 5. İçeriği birleştir ve temizle
        plain_text = '\n\n'.join(academic_content)
        
        # Fazla boşlukları temizle
        plain_text = re.sub(r'\n\s*\n\s*\n', '\n\n', plain_text)
        plain_text = re.sub(r' +', ' ', plain_text)
        
        return plain_text.strip()