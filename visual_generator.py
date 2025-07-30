"""
Visual Data Generator
Abstract görsel oluşturmak için tasarım verilerini hazırlar
"""

import json
from typing import Dict, List, Any, Optional, Tuple
import random
from datetime import datetime

class VisualDataGenerator:
    def __init__(self):
        """Visual Data Generator initialize"""
        self.medical_color_palettes = self._load_medical_palettes()
        self.layout_templates = self._load_layout_templates()
        self.typography_sets = self._load_typography_sets()
    
    def create_visual_data(self, article_data: Dict[str, Any], style_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Makale verilerinden görsel oluşturma verilerini hazırla
        
        Args:
            article_data: Parser'dan gelen makale verileri
            style_preferences: Mevcut görsel analizinden gelen stil tercihleri
            
        Returns:
            Görsel oluşturma için hazırlanmış veriler
        """
        try:
            # Temel görsel verileri
            visual_data = {
                "metadata": self._create_metadata(article_data),
                "content": self._organize_content(article_data),
                "design": self._create_design_specs(article_data, style_preferences),
                "layout": self._determine_layout(article_data),
                "typography": self._create_typography_specs(article_data, style_preferences),
                "colors": self._create_color_scheme(article_data, style_preferences),
                "elements": self._create_visual_elements(article_data),
                "export_settings": self._create_export_settings()
            }
            
            return visual_data
            
        except Exception as e:
            raise Exception(f"Görsel veri oluşturma hatası: {str(e)}")
    
    def _create_metadata(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Görsel metadata oluştur"""
        return {
            "title": article_data.get("title", "Medical Abstract"),
            "source": "JAMA Network",
            "created_at": datetime.now().isoformat(),
            "version": "1.0",
            "article_type": article_data.get("article_type", "research"),
            "doi": article_data.get("doi"),
            "authors_count": len(article_data.get("authors", [])),
            "has_structured_abstract": bool(article_data.get("abstract", {}).get("objective"))
        }
    
    def _organize_content(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """İçerik hiyerarşisi oluştur"""
        abstract = article_data.get("abstract", {})
        
        # Structured abstract varsa öncelikle onu kullan
        content_sections = []
        
        # Ana bölümler
        section_order = [
            ("importance", "Importance"),
            ("objective", "Objective"), 
            ("design", "Design"),
            ("setting", "Setting"),
            ("participants", "Participants"),
            ("intervention", "Intervention"),
            ("main_outcomes", "Main Outcomes"),
            ("results", "Results"),
            ("conclusions", "Conclusions")
        ]
        
        for key, display_name in section_order:
            if abstract.get(key):
                content_sections.append({
                    "type": "structured_section",
                    "label": display_name,
                    "content": abstract[key],
                    "priority": "high" if key in ["objective", "results", "conclusions"] else "medium"
                })
        
        # Structured abstract yoksa full abstract kullan
        if not content_sections and abstract.get("full"):
            content_sections.append({
                "type": "full_abstract",
                "label": "Abstract",
                "content": abstract["full"],
                "priority": "high"
            })
        
        return {
            "primary_title": article_data.get("title", ""),
            "authors": self._format_authors(article_data.get("authors", [])),
            "journal_info": self._format_journal_info(article_data.get("journal_info", {})),
            "sections": content_sections,
            "keywords": article_data.get("keywords", [])[:6],  # Max 6 keyword
            "publication_date": article_data.get("publication_date"),
            "content_length": self._calculate_content_length(content_sections)
        }
    
    def _format_authors(self, authors: List[Dict[str, str]]) -> str:
        """Yazar listesini formatlama"""
        if not authors:
            return ""
        
        if len(authors) == 1:
            author = authors[0]
            name = author.get("name", "")
            degrees = author.get("degrees", "")
            return f"{name} {degrees}".strip()
        
        elif len(authors) <= 3:
            names = [author.get("name", "") for author in authors]
            return ", ".join(names)
        
        else:
            first_author = authors[0].get("name", "")
            return f"{first_author} et al."
    
    def _format_journal_info(self, journal_info: Dict[str, str]) -> str:
        """Dergi bilgilerini formatlama"""
        parts = []
        
        if journal_info.get("name"):
            parts.append(journal_info["name"])
        
        if journal_info.get("volume") and journal_info.get("issue"):
            parts.append(f"Vol {journal_info['volume']}, No {journal_info['issue']}")
        
        return ". ".join(parts)
    
    def _calculate_content_length(self, sections: List[Dict[str, Any]]) -> str:
        """İçerik uzunluğu hesapla"""
        total_chars = sum(len(section.get("content", "")) for section in sections)
        
        if total_chars < 500:
            return "short"
        elif total_chars < 1500:
            return "medium"
        else:
            return "long"
    
    def _create_design_specs(self, article_data: Dict[str, Any], style_preferences: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Tasarım spesifikasyonları"""
        # Varsayılan JAMA stili
        default_style = {
            "theme": "medical_professional",
            "complexity": "clean",
            "visual_hierarchy": "structured",
            "brand_alignment": "jama"
        }
        
        # Mevcut görselden stil çıkarımı
        if style_preferences:
            existing_style = self._extract_style_from_analysis(style_preferences)
            default_style.update(existing_style)
        
        # Makale türüne göre stil ayarı
        article_type = article_data.get("article_type", "research")
        style_adjustments = self._get_style_by_article_type(article_type)
        default_style.update(style_adjustments)
        
        return default_style
    
    def _extract_style_from_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Mevcut görsel analizinden stil çıkar"""
        extracted_style = {}
        
        if "style_characteristics" in analysis:
            style_chars = analysis["style_characteristics"]
            
            # Renk şeması
            if style_chars.get("color_scheme"):
                extracted_style["color_preference"] = style_chars["color_scheme"]
            
            # Tasarım stili
            if style_chars.get("design_style"):
                extracted_style["design_approach"] = style_chars["design_style"]
            
            # Mood
            if style_chars.get("mood"):
                extracted_style["mood"] = style_chars["mood"]
        
        # Layout tercihleri
        if "layout_analysis" in analysis:
            layout = analysis["layout_analysis"]
            if layout.get("alignment"):
                extracted_style["alignment_preference"] = layout["alignment"]
        
        return extracted_style
    
    def _get_style_by_article_type(self, article_type: str) -> Dict[str, Any]:
        """Makale türüne göre stil"""
        type_styles = {
            "research": {
                "formality": "formal",
                "color_intensity": "moderate",
                "visual_elements": "scientific"
            },
            "review": {
                "formality": "academic",
                "color_intensity": "subdued", 
                "visual_elements": "analytical"
            },
            "case_report": {
                "formality": "clinical",
                "color_intensity": "focused",
                "visual_elements": "medical"
            },
            "editorial": {
                "formality": "professional",
                "color_intensity": "bold",
                "visual_elements": "commentary"
            }
        }
        
        return type_styles.get(article_type, type_styles["research"])
    
    def _determine_layout(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Layout belirleme"""
        content = self._organize_content(article_data)
        content_length = content["content_length"]
        sections_count = len(content["sections"])
        
        # İçerik uzunluğuna göre layout seçimi
        if content_length == "short" and sections_count <= 3:
            layout_type = "compact_single_column"
        elif content_length == "medium" and sections_count <= 6:
            layout_type = "balanced_two_section"
        else:
            layout_type = "structured_multi_section"
        
        # Layout spesifikasyonları
        layouts = {
            "compact_single_column": {
                "columns": 1,
                "sections_per_column": sections_count,
                "spacing": "compact",
                "header_size": "large",
                "section_separation": "minimal"
            },
            "balanced_two_section": {
                "columns": 2,
                "sections_per_column": sections_count // 2,
                "spacing": "balanced",
                "header_size": "medium",
                "section_separation": "moderate"
            },
            "structured_multi_section": {
                "columns": 2,
                "sections_per_column": "adaptive",
                "spacing": "generous",
                "header_size": "medium",
                "section_separation": "clear"
            }
        }
        
        selected_layout = layouts[layout_type]
        selected_layout["type"] = layout_type
        selected_layout["canvas_size"] = self._determine_canvas_size(content_length, sections_count)
        
        return selected_layout
    
    def _determine_canvas_size(self, content_length: str, sections_count: int) -> Dict[str, int]:
        """Canvas boyutu belirleme"""
        # JAMA standart boyutları (academic poster format)
        base_sizes = {
            "short": {"width": 800, "height": 600},
            "medium": {"width": 1000, "height": 750},
            "long": {"width": 1200, "height": 900}
        }
        
        size = base_sizes[content_length].copy()
        
        # Bölüm sayısına göre yükseklik ayarı
        if sections_count > 6:
            size["height"] = int(size["height"] * 1.2)
        elif sections_count > 8:
            size["height"] = int(size["height"] * 1.4)
        
        # Aspect ratio kontrolü
        if size["height"] / size["width"] > 1.5:
            size["width"] = int(size["width"] * 1.1)
        
        return size
    
    def _create_typography_specs(self, article_data: Dict[str, Any], style_preferences: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Tipografi spesifikasyonları"""
        # Varsayılan JAMA tipografi
        typography = {
            "font_family": {
                "primary": "Source Sans Pro",
                "secondary": "Georgia",
                "fallback": "Arial, sans-serif"
            },
            "font_sizes": {
                "title": 24,
                "section_header": 16,
                "body": 12,
                "caption": 10,
                "metadata": 9
            },
            "font_weights": {
                "title": "bold",
                "section_header": "semibold",
                "body": "regular",
                "emphasis": "medium"
            },
            "line_spacing": {
                "title": 1.2,
                "section_header": 1.3,
                "body": 1.4,
                "tight": 1.1
            },
            "text_alignment": {
                "title": "center",
                "section_header": "left",
                "body": "left",
                "metadata": "center"
            }
        }
        
        # Mevcut analizden tipografi ayarları
        if style_preferences and "typography_analysis" in style_preferences:
            typo_analysis = style_preferences["typography_analysis"]
            
            if typo_analysis.get("estimated_font_size") != "unknown":
                base_size = int(typo_analysis["estimated_font_size"])
                typography["font_sizes"] = self._scale_font_sizes(base_size)
            
            if typo_analysis.get("font_weight"):
                weight = typo_analysis["font_weight"]
                typography["weight_preference"] = weight
        
        return typography
    
    def _scale_font_sizes(self, base_size: int) -> Dict[str, int]:
        """Base font size'a göre diğer boyutları ölçekle"""
        scale_ratios = {
            "title": 2.0,
            "section_header": 1.33,
            "body": 1.0,
            "caption": 0.83,
            "metadata": 0.75
        }
        
        return {key: int(base_size * ratio) for key, ratio in scale_ratios.items()}
    
    def _create_color_scheme(self, article_data: Dict[str, Any], style_preferences: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Renk şeması oluştur"""
        # JAMA marka renkleri
        jama_colors = {
            "primary": "#1f4788",      # JAMA mavi
            "secondary": "#e8f4f8",    # Açık mavi
            "accent": "#d73027",       # Vurgu kırmızısı
            "text_primary": "#2c3e50", # Koyu metin
            "text_secondary": "#7f8c8d", # Açık metin
            "background": "#ffffff",    # Beyaz arkaplan
            "border": "#ecf0f1"        # Açık gri kenar
        }
        
        # Mevcut görselden renk tercihleri
        if style_preferences and "dominant_colors" in style_preferences:
            colors = style_preferences["dominant_colors"]
            
            # Dominant renkleri adapte et
            if colors.get("primary"):
                primary_color = colors["primary"]["hex"]
                # Tıbbi uygunluk kontrolü
                if self._is_medical_appropriate_color(primary_color):
                    jama_colors["primary"] = primary_color
            
            if colors.get("background"):
                bg_color = colors["background"]["hex"]
                if self._is_readable_background(bg_color):
                    jama_colors["background"] = bg_color
        
        # Makale türüne göre renk ayarı
        article_type = article_data.get("article_type", "research")
        type_colors = self._get_colors_by_type(article_type)
        jama_colors.update(type_colors)
        
        return {
            "palette": jama_colors,
            "accessibility": self._ensure_color_accessibility(jama_colors),
            "gradients": self._create_gradients(jama_colors),
            "usage_guide": self._create_color_usage_guide(jama_colors)
        }
    
    def _is_medical_appropriate_color(self, hex_color: str) -> bool:
        """Tıbbi yayın için uygun renk mi kontrol et"""
        # Çok parlak/neon renkler tıbbi yayınlar için uygun değil
        inappropriate_colors = ["#ff00ff", "#00ff00", "#ffff00", "#ff6600"]
        return hex_color.lower() not in inappropriate_colors
    
    def _is_readable_background(self, hex_color: str) -> bool:
        """Okunabilir arkaplan rengi mi kontrol et"""
        # Çok koyu arkaplanlar metin okunabilirliğini azaltır
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        brightness = sum(rgb) / 3
        return brightness > 200  # Yeterince açık
    
    def _get_colors_by_type(self, article_type: str) -> Dict[str, str]:
        """Makale türüne göre renk ayarları"""
        type_color_adjustments = {
            "research": {"accent": "#2ecc71"},      # Yeşil (bilimsel)
            "review": {"accent": "#f39c12"},        # Turuncu (analitik)
            "case_report": {"accent": "#e74c3c"},   # Kırmızı (klinik)
            "editorial": {"accent": "#9b59b6"}      # Mor (editöryal)
        }
        
        return type_color_adjustments.get(article_type, {})
    
    def _ensure_color_accessibility(self, colors: Dict[str, str]) -> Dict[str, Any]:
        """Renk erişilebilirlik kontrolü"""
        return {
            "contrast_ratio": self._calculate_contrast_ratio(colors["text_primary"], colors["background"]),
            "colorblind_friendly": self._check_colorblind_compatibility(colors),
            "print_friendly": self._check_print_compatibility(colors)
        }
    
    def _calculate_contrast_ratio(self, color1: str, color2: str) -> float:
        """İki renk arasındaki kontrast oranı"""
        # Simplified contrast calculation
        rgb1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        rgb2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        
        l1 = sum(rgb1) / 3 / 255
        l2 = sum(rgb2) / 3 / 255
        
        if l1 > l2:
            return (l1 + 0.05) / (l2 + 0.05)
        else:
            return (l2 + 0.05) / (l1 + 0.05)
    
    def _check_colorblind_compatibility(self, colors: Dict[str, str]) -> bool:
        """Renk körlüğü uyumluluğu"""
        # Basit kontrol: kırmızı-yeşil kombinasyonlarından kaçın
        red_green_problematic = False
        primary_rgb = tuple(int(colors["primary"][i:i+2], 16) for i in (1, 3, 5))
        accent_rgb = tuple(int(colors["accent"][i:i+2], 16) for i in (1, 3, 5))
        
        # Kırmızı dominant ve yeşil accent (veya tersi) problematik
        if (primary_rgb[0] > primary_rgb[1] and accent_rgb[1] > accent_rgb[0]) or \
           (primary_rgb[1] > primary_rgb[0] and accent_rgb[0] > accent_rgb[1]):
            red_green_problematic = True
        
        return not red_green_problematic
    
    def _check_print_compatibility(self, colors: Dict[str, str]) -> bool:
        """Baskı uyumluluğu"""
        # Çok açık renkler baskıda kaybolabilir
        for color_name, color_hex in colors.items():
            if color_name != "background":
                rgb = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
                if sum(rgb) / 3 > 240:  # Çok açık
                    return False
        return True
    
    def _create_gradients(self, colors: Dict[str, str]) -> Dict[str, Dict[str, str]]:
        """Gradient tanımları"""
        return {
            "primary_gradient": {
                "start": colors["primary"],
                "end": colors["secondary"],
                "direction": "vertical"
            },
            "accent_gradient": {
                "start": colors["accent"],
                "end": self._lighten_color(colors["accent"], 0.3),
                "direction": "diagonal"
            },
            "background_gradient": {
                "start": colors["background"],
                "end": colors["border"],
                "direction": "radial"
            }
        }
    
    def _lighten_color(self, hex_color: str, factor: float) -> str:
        """Rengi açma"""
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        lighter_rgb = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
        return "#{:02x}{:02x}{:02x}".format(*lighter_rgb)
    
    def _create_color_usage_guide(self, colors: Dict[str, str]) -> Dict[str, List[str]]:
        """Renk kullanım rehberi"""
        return {
            "headers": [colors["primary"], colors["text_primary"]],
            "body_text": [colors["text_primary"], colors["text_secondary"]],
            "highlights": [colors["accent"]],
            "backgrounds": [colors["background"], colors["secondary"]],
            "borders": [colors["border"]]
        }
    
    def _create_visual_elements(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Görsel öğeler"""
        return {
            "icons": self._select_medical_icons(article_data),
            "decorative_elements": self._create_decorative_elements(),
            "data_visualization": self._suggest_data_viz(article_data),
            "branding": self._create_branding_elements(),
            "interactive_elements": self._define_interactive_elements()
        }
    
    def _select_medical_icons(self, article_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Tıbbi ikonlar seçimi"""
        article_type = article_data.get("article_type", "research")
        keywords = article_data.get("keywords", [])
        
        # Keyword'lere göre ikon eşleştirme
        icon_mapping = {
            "cardiology": "heart",
            "neurology": "brain", 
            "oncology": "medical-cross",
            "pediatrics": "baby",
            "surgery": "scalpel",
            "radiology": "x-ray",
            "pharmacy": "pill",
            "research": "microscope",
            "clinical": "stethoscope",
            "patient": "user",
            "treatment": "medical-bag",
            "diagnosis": "search"
        }
        
        selected_icons = []
        for keyword in keywords[:3]:  # Max 3 ikon
            keyword_lower = keyword.lower()
            for key, icon in icon_mapping.items():
                if key in keyword_lower:
                    selected_icons.append({
                        "name": icon,
                        "context": keyword,
                        "usage": "section_header"
                    })
                    break
        
        # Varsayılan ikonlar
        if not selected_icons:
            default_icons = {
                "research": [{"name": "microscope", "context": "research", "usage": "title"}],
                "review": [{"name": "book-open", "context": "literature", "usage": "title"}],
                "case_report": [{"name": "user", "context": "patient", "usage": "title"}],
                "editorial": [{"name": "edit", "context": "commentary", "usage": "title"}]
            }
            selected_icons = default_icons.get(article_type, default_icons["research"])
        
        return selected_icons
    
    def _create_decorative_elements(self) -> Dict[str, Any]:
        """Dekoratif öğeler"""
        return {
            "dividers": {
                "style": "medical_line",
                "thickness": 1,
                "color": "border",
                "pattern": "solid"
            },
            "frames": {
                "style": "subtle_border",
                "corner_radius": 4,
                "shadow": "soft",
                "color": "border"
            },
            "background_patterns": {
                "style": "medical_grid",
                "opacity": 0.05,
                "scale": "fine"
            }
        }
    
    def _suggest_data_viz(self, article_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Veri görselleştirme önerileri"""
        abstract = article_data.get("abstract", {})
        
        # Results bölümünde sayısal veri var mı kontrol et
        results = abstract.get("results", "")
        if not results:
            return None
        
        # Sayısal pattern arama
        import re
        numbers = re.findall(r'\d+\.?\d*%?', results)
        
        if len(numbers) >= 2:
            return {
                "type": "simple_chart",
                "suggested_format": "bar_chart",
                "data_points": len(numbers),
                "integration": "inline_with_results",
                "style": "minimal_medical"
            }
        
        return None
    
    def _create_branding_elements(self) -> Dict[str, Any]:
        """Marka öğeleri"""
        return {
            "logo_placement": {
                "position": "top_right",
                "size": "small",
                "opacity": 0.7
            },
            "jama_attribution": {
                "text": "JAMA Network",
                "position": "bottom_center",
                "font_size": "metadata",
                "color": "text_secondary"
            },
            "doi_display": {
                "format": "compact",
                "position": "bottom_left",
                "font_size": "metadata"
            }
        }
    
    def _define_interactive_elements(self) -> Dict[str, Any]:
        """İnteraktif öğeler (web için)"""
        return {
            "hover_effects": {
                "section_highlight": True,
                "color_transition": "smooth",
                "scale_effect": "subtle"
            },
            "expandable_sections": {
                "long_abstracts": True,
                "methodology_details": True,
                "author_info": True
            },
            "responsive_layout": {
                "mobile_breakpoint": 768,
                "tablet_breakpoint": 1024,
                "desktop_optimized": True
            }
        }
    
    def _create_export_settings(self) -> Dict[str, Any]:
        """Export ayarları"""
        return {
            "formats": {
                "high_res_png": {
                    "dpi": 300,
                    "compression": "lossless",
                    "color_profile": "sRGB"
                },
                "print_pdf": {
                    "format": "A4",
                    "bleed": "3mm",
                    "color_mode": "CMYK"
                },
                "web_jpg": {
                    "quality": 85,
                    "progressive": True,
                    "color_profile": "sRGB"
                },
                "social_media": {
                    "instagram": {"width": 1080, "height": 1080},
                    "twitter": {"width": 1200, "height": 675},
                    "linkedin": {"width": 1200, "height": 627}
                }
            },
            "optimization": {
                "web_performance": True,
                "file_size_limit": "2MB",
                "progressive_loading": True
            }
        }
    
    def _load_medical_palettes(self) -> Dict[str, Dict[str, str]]:
        """Tıbbi renk paletleri"""
        return {
            "classic_medical": {
                "primary": "#1f4788",
                "secondary": "#e8f4f8", 
                "accent": "#d73027"
            },
            "modern_clinical": {
                "primary": "#2c3e50",
                "secondary": "#ecf0f1",
                "accent": "#3498db"
            },
            "research_focused": {
                "primary": "#27ae60",
                "secondary": "#d5f4e6",
                "accent": "#f39c12"
            }
        }
    
    def _load_layout_templates(self) -> Dict[str, Dict[str, Any]]:
        """Layout şablonları"""
        return {
            "structured_academic": {
                "header_height": 0.15,
                "content_height": 0.75,
                "footer_height": 0.1,
                "margins": {"top": 20, "bottom": 20, "left": 30, "right": 30}
            },
            "modern_clean": {
                "header_height": 0.12,
                "content_height": 0.78,
                "footer_height": 0.1,
                "margins": {"top": 25, "bottom": 25, "left": 25, "right": 25}
            }
        }
    
    def _load_typography_sets(self) -> Dict[str, Dict[str, Any]]:
        """Tipografi setleri"""
        return {
            "academic_standard": {
                "primary_font": "Source Sans Pro",
                "secondary_font": "Georgia",
                "base_size": 12,
                "scale": 1.25
            },
            "modern_readable": {
                "primary_font": "Inter",
                "secondary_font": "Source Serif Pro", 
                "base_size": 13,
                "scale": 1.2
            }
        }