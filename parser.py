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
            "metadata": self._extract_metadata(),
            # Abstract görsel için yeni alanlar
            "population": self._extract_population(),
            "intervention": self._extract_intervention(),
            "findings": self._extract_findings(),
            "settings": self._extract_settings(),
            "primary_outcome": self._extract_primary_outcome()
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
            '.article-title',
            'h1.article-title-main',
            '.article-header .title',
            '.content h1',
            'article h1',
            '.main-content h1'
        ]
        
        for selector in selectors:
            element = self.soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                if title and len(title) > 5:  # Minimum başlık uzunluğu
                    return title
        
        # Meta tag'den dene
        meta_selectors = [
            'meta[property="og:title"]',
            'meta[name="citation_title"]',
            'meta[name="title"]',
            'meta[property="twitter:title"]'
        ]
        
        for selector in meta_selectors:
            meta_title = self.soup.select_one(selector)
            if meta_title:
                title = meta_title.get('content', '')
                if title and len(title) > 5:
                    return title
        
        # JSON-LD structured data'dan dene
        json_scripts = self.soup.find_all('script', {'type': 'application/ld+json'})
        for script in json_scripts:
            try:
                import json
                data = json.loads(script.string)
                if isinstance(data, dict) and 'headline' in data:
                    title = data['headline']
                    if title and len(title) > 5:
                        return title
                elif isinstance(data, dict) and 'name' in data:
                    title = data['name']
                    if title and len(title) > 5:
                        return title
            except:
                continue
        
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
        
        # Ana abstract - daha fazla selector dene
        abstract_selectors = [
            '.article-abstract',
            '.abstract-content', 
            '#abstract',
            '.abstract',
            '.article-abstract-content',
            '.abstract-text',
            '.abstract-body',
            '.article-abstract-body',
            '.abstract-section',
            '.article-abstract-section',
            '.abstract-main',
            '.article-abstract-main',
            '.abstract-full',
            '.article-abstract-full',
            '.abstract-content-text',
            '.article-abstract-content-text',
            '.abstract-paragraph',
            '.article-abstract-paragraph',
            '.abstract-summary',
            '.article-abstract-summary',
            '.abstract-description',
            '.article-abstract-description',
            '.abstract-details',
            '.article-abstract-details',
            '.abstract-info',
            '.article-abstract-info',
            '.abstract-main-content',
            '.article-abstract-main-content',
            '.abstract-main-text',
            '.article-abstract-main-text',
            '.abstract-main-body',
            '.article-abstract-main-body',
            '.abstract-main-section',
            '.article-abstract-main-section',
            '.abstract-main-paragraph',
            '.article-abstract-main-paragraph',
            '.abstract-main-summary',
            '.article-abstract-main-summary',
            '.abstract-main-description',
            '.article-abstract-main-description',
            '.abstract-main-details',
            '.article-abstract-main-details',
            '.abstract-main-info',
            '.article-abstract-main-info'
        ]
        
        for selector in abstract_selectors:
            abstract_elem = self.soup.select_one(selector)
            if abstract_elem:
                abstract_data['full'] = abstract_elem.get_text(strip=True)
                break
        
        # Eğer hala bulunamadıysa, daha genel arama yap
        if 'full' not in abstract_data:
            # Tüm metin içinde "abstract" kelimesini ara
            text_content = self.soup.get_text()
            abstract_patterns = [
                r'Abstract[:\s]*([^.]*?\.)',
                r'ABSTRACT[:\s]*([^.]*?\.)',
                r'Summary[:\s]*([^.]*?\.)',
                r'SUMMARY[:\s]*([^.]*?\.)'
            ]
            
            for pattern in abstract_patterns:
                match = re.search(pattern, text_content, re.IGNORECASE | re.DOTALL)
                if match:
                    abstract_data['full'] = match.group(1).strip()
                    break
        
        # Structured abstract bölümleri
        sections = {
            'importance': ['.abstract-importance', '.importance', '.abstract-importance-text'],
            'objective': ['.abstract-objective', '.objective', '.abstract-objective-text'],
            'design': ['.abstract-design', '.design', '.abstract-design-text'],
            'setting': ['.abstract-setting', '.setting', '.abstract-setting-text'],
            'participants': ['.abstract-participants', '.participants', '.abstract-participants-text'],
            'intervention': ['.abstract-intervention', '.intervention', '.abstract-intervention-text'],
            'main_outcomes': ['.abstract-outcomes', '.outcomes', '.abstract-outcomes-text'],
            'results': ['.abstract-results', '.results', '.abstract-results-text'],
            'conclusions': ['.abstract-conclusions', '.conclusions', '.abstract-conclusions-text']
        }
        
        for section_name, selectors in sections.items():
            for selector in selectors:
                elem = self.soup.select_one(selector)
                if elem:
                    abstract_data[section_name] = elem.get_text(strip=True)
                    break
        
        return abstract_data
    
    def _extract_population(self) -> str:
        """Population bilgisini çıkar"""
        # Abstract'ten population bilgisini çıkar
        abstract = self._extract_abstract()
        
        # Önce participants bölümünden dene
        if 'participants' in abstract:
            return abstract['participants']
        
        # Full abstract'ten population bilgisini çıkar
        if 'full' in abstract:
            full_text = abstract['full']
            # Population pattern'leri ara
            population_patterns = [
                r'(\d+)\s+(?:patients|participants|subjects|individuals)',
                r'(?:enrolled|included|recruited)\s+(\d+)\s+(?:patients|participants|subjects)',
                r'(?:total of|total)\s+(\d+)\s+(?:patients|participants|subjects)',
                r'(\d+)\s+(?:men|women|males|females)',
                r'aged\s+(\d+)\s+to\s+(\d+)\s+years',
                r'(\d+)\s+(?:adults|older adults|elderly)',
                r'(?:randomized|assigned)\s+(\d+)\s+(?:participants|subjects)',
                r'(\d+)\s+(?:community-dwelling|community)',
                r'(?:sample size|sample)\s+of\s+(\d+)',
                r'(\d+)\s+(?:volunteers|individuals)'
            ]
            
            for pattern in population_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    return f"Population: {match.group(0)}"
        
        # Alternatif: HTML'den doğrudan ara
        population_selectors = [
            '.abstract-participants',
            '.participants',
            '.study-population',
            '.population',
            '[data-testid="participants"]',
            '.abstract .participants',
            '.article-abstract .participants'
        ]
        
        for selector in population_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                if text and len(text) > 10:
                    return f"Population: {text}"
        
        return "Population bilgisi bulunamadı"
    
    def _extract_intervention(self) -> str:
        """Intervention bilgisini çıkar"""
        abstract = self._extract_abstract()
        
        # Önce intervention bölümünden dene
        if 'intervention' in abstract:
            return abstract['intervention']
        
        # Full abstract'ten intervention bilgisini çıkar
        if 'full' in abstract:
            full_text = abstract['full']
            # Intervention pattern'leri ara
            intervention_patterns = [
                r'(?:treated with|received|administered)\s+([^.]*?)(?:\.|;)',
                r'(?:intervention|treatment)\s+([^.]*?)(?:\.|;)',
                r'(?:randomized to|assigned to)\s+([^.]*?)(?:\.|;)',
                r'(?:intervention group|treatment group)\s+([^.]*?)(?:\.|;)',
                r'(?:lifestyle intervention|behavioral intervention)\s+([^.]*?)(?:\.|;)',
                r'(?:multidomain intervention|multicomponent intervention)\s+([^.]*?)(?:\.|;)',
                r'(?:self-guided|guided)\s+([^.]*?)(?:\.|;)',
                r'(?:structured|standardized)\s+([^.]*?)(?:\.|;)'
            ]
            
            for pattern in intervention_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    return f"Intervention: {match.group(1).strip()}"
        
        # Alternatif: HTML'den doğrudan ara
        intervention_selectors = [
            '.abstract-intervention',
            '.intervention',
            '.treatment',
            '[data-testid="intervention"]',
            '.abstract .intervention',
            '.article-abstract .intervention'
        ]
        
        for selector in intervention_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                if text and len(text) > 10:
                    return f"Intervention: {text}"
        
        return "Intervention bilgisi bulunamadı"
    
    def _extract_findings(self) -> str:
        """Findings bilgisini çıkar"""
        abstract = self._extract_abstract()
        
        # Önce results bölümünden dene
        if 'results' in abstract:
            return abstract['results']
        
        # Full abstract'ten findings bilgisini çıkar
        if 'full' in abstract:
            full_text = abstract['full']
            # Findings pattern'leri ara
            findings_patterns = [
                r'(?:results|findings|outcomes)\s*:?\s*([^.]*?)(?:\.|;)',
                r'(?:showed|demonstrated|found)\s+([^.]*?)(?:\.|;)',
                r'(?:significant|significant difference)\s+([^.]*?)(?:\.|;)',
                r'(?:improved|increased|decreased)\s+([^.]*?)(?:\.|;)',
                r'(?:no difference|no significant difference)\s+([^.]*?)(?:\.|;)',
                r'(?:cognitive function|memory|attention)\s+([^.]*?)(?:\.|;)',
                r'(?:primary outcome|secondary outcome)\s+([^.]*?)(?:\.|;)'
            ]
            
            for pattern in findings_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    return f"Findings: {match.group(1).strip()}"
        
        # Alternatif: HTML'den doğrudan ara
        findings_selectors = [
            '.abstract-results',
            '.results',
            '.findings',
            '[data-testid="results"]',
            '.abstract .results',
            '.article-abstract .results'
        ]
        
        for selector in findings_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                if text and len(text) > 10:
                    return f"Findings: {text}"
        
        return "Findings bilgisi bulunamadı"
    
    def _extract_settings(self) -> str:
        """Settings bilgisini çıkar"""
        abstract = self._extract_abstract()
        
        # Önce setting bölümünden dene
        if 'setting' in abstract:
            return abstract['setting']
        
        # Full abstract'ten settings bilgisini çıkar
        if 'full' in abstract:
            full_text = abstract['full']
            # Settings pattern'leri ara
            settings_patterns = [
                r'(?:conducted at|performed at|study at)\s+([^.]*?)(?:\.|;)',
                r'(?:hospital|clinic|center|facility)\s+([^.]*?)(?:\.|;)',
                r'(?:multicenter|single-center)\s+([^.]*?)(?:\.|;)',
                r'(?:community|academic|research)\s+([^.]*?)(?:\.|;)',
                r'(?:US|United States|international)\s+([^.]*?)(?:\.|;)',
                r'(?:randomized clinical trial|RCT)\s+([^.]*?)(?:\.|;)',
                r'(?:prospective|retrospective)\s+([^.]*?)(?:\.|;)'
            ]
            
            for pattern in settings_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    return f"Settings: {match.group(1).strip()}"
        
        # Alternatif: HTML'den doğrudan ara
        settings_selectors = [
            '.abstract-setting',
            '.setting',
            '.study-setting',
            '[data-testid="setting"]',
            '.abstract .setting',
            '.article-abstract .setting'
        ]
        
        for selector in settings_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                if text and len(text) > 10:
                    return f"Settings: {text}"
        
        return "Settings bilgisi bulunamadı"
    
    def _extract_primary_outcome(self) -> str:
        """Primary outcome bilgisini çıkar"""
        abstract = self._extract_abstract()
        
        # Önce main_outcomes bölümünden dene
        if 'main_outcomes' in abstract:
            return abstract['main_outcomes']
        
        # Full abstract'ten primary outcome bilgisini çıkar
        if 'full' in abstract:
            full_text = abstract['full']
            # Primary outcome pattern'leri ara
            outcome_patterns = [
                r'(?:primary outcome|primary endpoint|primary end point)\s*:?\s*([^.]*?)(?:\.|;)',
                r'(?:measured|assessed|evaluated)\s+([^.]*?)(?:\.|;)',
                r'(?:outcome|endpoint)\s+([^.]*?)(?:\.|;)',
                r'(?:cognitive function|memory|attention)\s+([^.]*?)(?:\.|;)',
                r'(?:global cognitive|overall cognitive)\s+([^.]*?)(?:\.|;)',
                r'(?:primary measure|primary assessment)\s+([^.]*?)(?:\.|;)',
                r'(?:change in|improvement in)\s+([^.]*?)(?:\.|;)'
            ]
            
            for pattern in outcome_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    return f"Primary Outcome: {match.group(1).strip()}"
        
        # Alternatif: HTML'den doğrudan ara
        outcome_selectors = [
            '.abstract-outcomes',
            '.outcomes',
            '.primary-outcome',
            '[data-testid="outcomes"]',
            '.abstract .outcomes',
            '.article-abstract .outcomes'
        ]
        
        for selector in outcome_selectors:
            elem = self.soup.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                if text and len(text) > 10:
                    return f"Primary Outcome: {text}"
        
        return "Primary outcome bilgisi bulunamadı"
    
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