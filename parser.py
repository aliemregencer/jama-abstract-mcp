"""
JAMA HTML Parser
HTML içerikten makale verilerini çıkarır
"""

import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from datetime import datetime

class DataParser:
    def __init__(self):
        """Parser initialize"""
        self.soup = None
    
    def parse_article(self, html_content: str) -> Dict[str, Any]:
        """
        HTML içerikten makale verilerini çıkar
        
        Args:
            html_content: HTML içerik
            
        Returns:
            Ayrıştırılmış makale verileri
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        
        article_data = {
            "title": self._extract_title(),
            "authors": self._extract_authors(),
            "abstract": self._extract_abstract(),
            "keywords": self._extract_keywords(),
            "publication_date": self._extract_publication_date(),
            "journal_info": self._extract_journal_info(),
            "doi": self._extract_doi(),
            "article_type": self._extract_article_type(),
            "existing_visual_url": self._extract_existing_visual(),
            "full_text_preview": self._extract_text_preview(),
            "metadata": self._extract_metadata()
        }
        
        return article_data
    
    def _extract_title(self) -> str:
        """Makale başlığını çıkar"""
        selectors = [
            'h1.article-title',
            'h1[data-testid="article-title"]',
            '.article-header h1',
            'h1.title',
            '.article-title-main'
        ]
        
        for selector in selectors:
            element = self.soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        # Meta tag'den dene
        meta_title = self.soup.find('meta', {'property': 'og:title'})
        if meta_title:
            return meta_title.get('content', '')
        
        return "Başlık bulunamadı"
    
    def _extract_authors(self) -> List[Dict[str, str]]:
        """Yazar bilgilerini çıkar"""
        authors = []
        
        # Ana yazar alanı
        author_sections = self.soup.select('.article-authors .author, .byline .author')
        
        for author_element in author_sections:
            author_info = {}
            
            # İsim
            name_elem = author_element.select_one('.author-name, .name')
            if name_elem:
                author_info['name'] = name_elem.get_text(strip=True)
            
            # Derece/Ünvan
            degree_elem = author_element.select_one('.author-degrees, .degrees')
            if degree_elem:
                author_info['degrees'] = degree_elem.get_text(strip=True)
            
            # Kurum
            affiliation_elem = author_element.select_one('.author-affiliation, .affiliation')
            if affiliation_elem:
                author_info['affiliation'] = affiliation_elem.get_text(strip=True)
            
            if author_info:
                authors.append(author_info)
        
        # Alternatif yöntem
        if not authors:
            author_text = self.soup.select_one('.article-authors, .byline')
            if author_text:
                # Basit string parsing
                text = author_text.get_text(strip=True)
                names = re.split(r'[;,]|\sand\s', text)
                for name in names:
                    clean_name = name.strip()
                    if clean_name:
                        authors.append({'name': clean_name})
        
        return authors
    
    def _extract_abstract(self) -> Dict[str, str]:
        """Abstract çıkar"""
        abstract_data = {}
        
        # Ana abstract
        abstract_elem = self.soup.select_one('.article-abstract, .abstract-content, #abstract')
        if abstract_elem:
            abstract_data['full'] = abstract_elem.get_text(strip=True)
        
        # Structured abstract bölümleri
        sections = {
            'importance': ['.abstract-importance', '.importance'],
            'objective': ['.abstract-objective', '.objective'],
            'design': ['.abstract-design', '.design'],
            'setting': ['.abstract-setting', '.setting'],
            'participants': ['.abstract-participants', '.participants'],
            'intervention': ['.abstract-intervention', '.intervention'],
            'main_outcomes': ['.abstract-outcomes', '.outcomes'],
            'results': ['.abstract-results', '.results'],
            'conclusions': ['.abstract-conclusions', '.conclusions']
        }
        
        for section_name, selectors in sections.items():
            for selector in selectors:
                elem = self.soup.select_one(selector)
                if elem:
                    abstract_data[section_name] = elem.get_text(strip=True)
                    break
        
        return abstract_data
    
    def _extract_keywords(self) -> List[str]:
        """Anahtar kelimeleri çıkar"""
        keywords = []
        
        # Keywords section
        keywords_elem = self.soup.select_one('.keywords, .article-keywords')
        if keywords_elem:
            keyword_links = keywords_elem.select('a, .keyword')
            for link in keyword_links:
                keyword = link.get_text(strip=True)
                if keyword:
                    keywords.append(keyword)
        
        # Meta keywords
        if not keywords:
            meta_keywords = self.soup.find('meta', {'name': 'keywords'})
            if meta_keywords:
                content = meta_keywords.get('content', '')
                keywords = [k.strip() for k in content.split(',') if k.strip()]
        
        return keywords
    
    def _extract_publication_date(self) -> Optional[str]:
        """Yayın tarihini çıkar"""
        date_selectors = [
            '.article-date',
            '.publication-date',
            '[data-testid="publication-date"]'
        ]
        
        for selector in date_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        
        # Meta tag'den
        meta_date = self.soup.find('meta', {'name': 'citation_publication_date'})
        if meta_date:
            return meta_date.get('content')
        
        return None
    
    def _extract_journal_info(self) -> Dict[str, str]:
        """Dergi bilgilerini çıkar"""
        journal_info = {}
        
        # Dergi adı
        journal_elem = self.soup.select_one('.journal-title, .publication-title')
        if journal_elem:
            journal_info['name'] = journal_elem.get_text(strip=True)
        
        # Cilt, sayı
        volume_elem = self.soup.select_one('.volume')
        if volume_elem:
            journal_info['volume'] = volume_elem.get_text(strip=True)
        
        issue_elem = self.soup.select_one('.issue')
        if issue_elem:
            journal_info['issue'] = issue_elem.get_text(strip=True)
        
        return journal_info
    
    def _extract_doi(self) -> Optional[str]:
        """DOI çıkar"""
        # DOI link
        doi_elem = self.soup.select_one('a[href*="doi.org"], .doi')
        if doi_elem:
            if 'href' in doi_elem.attrs:
                return doi_elem['href']
            return doi_elem.get_text(strip=True)
        
        # Meta tag'den
        meta_doi = self.soup.find('meta', {'name': 'citation_doi'})
        if meta_doi:
            return meta_doi.get('content')
        
        return None
    
    def _extract_article_type(self) -> Optional[str]:
        """Makale tipini çıkar"""
        type_elem = self.soup.select_one('.article-type, .article-category')
        if type_elem:
            return type_elem.get_text(strip=True)
        
        # Meta tag'den
        meta_type = self.soup.find('meta', {'name': 'citation_article_type'})
        if meta_type:
            return meta_type.get('content')
        
        return None
    
    def _extract_existing_visual(self) -> Optional[str]:
        """Mevcut abstract görselini bul"""
        # Abstract görseli
        visual_selectors = [
            '.article-abstract img',
            '.abstract-visual img',
            '.graphical-abstract img',
            'figure.abstract-figure img'
        ]
        
        for selector in visual_selectors:
            img = self.soup.select_one(selector)
            if img and img.get('src'):
                src = img['src']
                # Relative URL'i absolute yap
                if src.startswith('/'):
                    src = 'https://jamanetwork.com' + src
                return src
        
        return None
    
    def _extract_text_preview(self) -> str:
        """İlk paragrafları önizleme olarak çıkar"""
        content_elem = self.soup.select_one('.article-full-text, .article-content')
        if content_elem:
            paragraphs = content_elem.select('p')[:3]  # İlk 3 paragraf
            preview = ' '.join([p.get_text(strip=True) for p in paragraphs])
            return preview[:500] + '...' if len(preview) > 500 else preview
        
        return ""
    
    def _extract_metadata(self) -> Dict[str, Any]:
        """Ek metadata çıkar"""
        metadata = {}
        
        # Meta tags
        meta_tags = self.soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        # JSON-LD structured data
        json_scripts = self.soup.find_all('script', {'type': 'application/ld+json'})
        if json_scripts:
            metadata['structured_data'] = []
            for script in json_scripts:
                try:
                    import json
                    data = json.loads(script.string)
                    metadata['structured_data'].append(data)
                except:
                    pass
        
        return metadata