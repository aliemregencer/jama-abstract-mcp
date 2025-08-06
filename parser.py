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
            "population": self._extract_population(),
            "intervention": self._extract_intervention(),
            "outcome": self._extract_outcome(),
            "findings": self._extract_findings(),
            "settings": self._extract_settings(),
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
            '.article-title-main',
            'h1',
            '.title',
            '[data-testid="title"]',
            'meta[property="og:title"]',
            'meta[name="citation_title"]'
        ]
        
        for selector in selectors:
            element = self.soup.select_one(selector)
            if element:
                if selector.startswith('meta'):
                    return element.get('content', '')
                else:
                    return element.get_text(strip=True)
        
        return "Başlık bulunamadı"
    
    def _extract_authors(self) -> str:
        """Yazar isimlerini string olarak çıkar"""
        authors = []
        
        # Ana yazar alanı
        author_selectors = [
            '.article-authors .author',
            '.byline .author',
            '.authors',
            '.author-list',
            '[data-testid="authors"]',
            '.contributors',
            '.author'
        ]
        
        for selector in author_selectors:
            author_elements = self.soup.select(selector)
            for author_element in author_elements:
                # İsim
                name_elem = author_element.select_one('.author-name, .name, span')
                if name_elem:
                    authors.append(name_elem.get_text(strip=True))
                else:
                    # Direkt element text'ini al
                    text = author_element.get_text(strip=True)
                    if text and len(text) > 2:
                        authors.append(text)
        
        # Alternatif yöntem - tüm sayfada yazar arama
        if not authors:
            # Meta tag'lerden yazar bilgisi
            meta_authors = self.soup.find('meta', {'name': 'citation_author'})
            if meta_authors:
                authors.append(meta_authors.get('content', ''))
            
            # Text içinde yazar pattern'leri
            page_text = self.soup.get_text()
            author_patterns = [
                r'by\s+([^\.]+)',
                r'authors?[:\s]+([^\.]+)',
                r'written\s+by\s+([^\.]+)'
            ]
            
            for pattern in author_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    authors.extend([m.strip() for m in matches[0].split(',')])
                    break
        
        return ", ".join(authors) if authors else "Yazar bilgisi bulunamadı"
    
    def _extract_population(self) -> str:
        """Katılımcı bilgilerini çıkar"""
        # Structured abstract'tan population bilgisi
        population_selectors = [
            '.abstract-participants',
            '.participants',
            '[data-testid="participants"]',
            '.population',
            '.study-population'
        ]
        
        for selector in population_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        
        # Abstract içinde population arama
        abstract_elem = self.soup.select_one('.article-abstract, .abstract-content, #abstract')
        if abstract_elem:
            abstract_text = abstract_elem.get_text()
            # Population ile ilgili cümleleri bul
            population_patterns = [
                r'participants?[^.]*\.',
                r'patients?[^.]*\.',
                r'subjects?[^.]*\.',
                r'individuals?[^.]*\.',
                r'cohort[^.]*\.'
            ]
            
            for pattern in population_patterns:
                matches = re.findall(pattern, abstract_text, re.IGNORECASE)
                if matches:
                    return matches[0].strip()
        
        return "Katılımcı bilgisi bulunamadı"
    
    def _extract_intervention(self) -> str:
        """Müdahale yöntemini çıkar"""
        # Structured abstract'tan intervention bilgisi
        intervention_selectors = [
            '.abstract-intervention',
            '.intervention',
            '[data-testid="intervention"]',
            '.treatment',
            '.method'
        ]
        
        for selector in intervention_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        
        # Abstract içinde intervention arama
        abstract_elem = self.soup.select_one('.article-abstract, .abstract-content, #abstract')
        if abstract_elem:
            abstract_text = abstract_elem.get_text()
            # Intervention ile ilgili cümleleri bul
            intervention_patterns = [
                r'intervention[^.]*\.',
                r'treatment[^.]*\.',
                r'therapy[^.]*\.',
                r'procedure[^.]*\.',
                r'method[^.]*\.'
            ]
            
            for pattern in intervention_patterns:
                matches = re.findall(pattern, abstract_text, re.IGNORECASE)
                if matches:
                    return matches[0].strip()
        
        return "Müdahale bilgisi bulunamadı"
    
    def _extract_outcome(self) -> str:
        """Birincil çıktı veya gözlemleri çıkar"""
        # Structured abstract'tan outcome bilgisi
        outcome_selectors = [
            '.abstract-outcomes',
            '.outcomes',
            '[data-testid="outcomes"]',
            '.primary-outcome',
            '.endpoint'
        ]
        
        for selector in outcome_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        
        # Abstract içinde outcome arama
        abstract_elem = self.soup.select_one('.article-abstract, .abstract-content, #abstract')
        if abstract_elem:
            abstract_text = abstract_elem.get_text()
            # Outcome ile ilgili cümleleri bul
            outcome_patterns = [
                r'outcome[^.]*\.',
                r'endpoint[^.]*\.',
                r'result[^.]*\.',
                r'measure[^.]*\.',
                r'primary[^.]*\.'
            ]
            
            for pattern in outcome_patterns:
                matches = re.findall(pattern, abstract_text, re.IGNORECASE)
                if matches:
                    return matches[0].strip()
        
        return "Çıktı bilgisi bulunamadı"
    
    def _extract_findings(self) -> str:
        """Sonuçları çıkar"""
        # Structured abstract'tan results bilgisi
        findings_selectors = [
            '.abstract-results',
            '.results',
            '[data-testid="results"]',
            '.findings',
            '.conclusion'
        ]
        
        for selector in findings_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        
        # Abstract içinde findings arama
        abstract_elem = self.soup.select_one('.article-abstract, .abstract-content, #abstract')
        if abstract_elem:
            abstract_text = abstract_elem.get_text()
            # Findings ile ilgili cümleleri bul
            findings_patterns = [
                r'result[^.]*\.',
                r'finding[^.]*\.',
                r'conclusion[^.]*\.',
                r'significant[^.]*\.',
                r'difference[^.]*\.'
            ]
            
            for pattern in findings_patterns:
                matches = re.findall(pattern, abstract_text, re.IGNORECASE)
                if matches:
                    return matches[0].strip()
        
        return "Sonuç bilgisi bulunamadı"
    
    def _extract_settings(self) -> str:
        """Yapılan yer veya merkez bilgisini çıkar"""
        # Structured abstract'tan setting bilgisi
        settings_selectors = [
            '.abstract-setting',
            '.setting',
            '[data-testid="setting"]',
            '.location',
            '.center'
        ]
        
        for selector in settings_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        
        # Abstract içinde setting arama
        abstract_elem = self.soup.select_one('.article-abstract, .abstract-content, #abstract')
        if abstract_elem:
            abstract_text = abstract_elem.get_text()
            # Setting ile ilgili cümleleri bul
            settings_patterns = [
                r'setting[^.]*\.',
                r'center[^.]*\.',
                r'hospital[^.]*\.',
                r'clinic[^.]*\.',
                r'location[^.]*\.'
            ]
            
            for pattern in settings_patterns:
                matches = re.findall(pattern, abstract_text, re.IGNORECASE)
                if matches:
                    return matches[0].strip()
        
        return "Yer bilgisi bulunamadı"
    
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