"""
Image Analyzer
Mevcut abstract görsellerini analiz eder
"""

import cv2
import numpy as np
import requests
from typing import Dict, List, Tuple, Any
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import colorsys

class ImageAnalyzer:
    def __init__(self):
        """Image Analyzer initialize"""
        self.image = None
        self.image_cv = None
    
    async def analyze_image(self, image_url: str) -> Dict[str, Any]:
        """
        Görsel URL'sinden görsel analizi yap
        
        Args:
            image_url: Analiz edilecek görsel URL'si
            
        Returns:
            Analiz sonuçları
        """
        try:
            # Görseli indir
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # PIL ile yükle
            self.image = Image.open(BytesIO(response.content))
            
            # OpenCV formatına çevir
            self.image_cv = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            
            # Analiz sonuçları
            analysis = {
                "dimensions": self._get_dimensions(),
                "color_palette": self._extract_color_palette(),
                "dominant_colors": self._get_dominant_colors(),
                "layout_analysis": self._analyze_layout(),
                "typography_analysis": self._analyze_typography(),
                "design_elements": self._analyze_design_elements(),
                "style_characteristics": self._analyze_style()
            }
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Görsel analiz hatası: {str(e)}")
    
    def _get_dimensions(self) -> Dict[str, int]:
        """Görsel boyutlarını al"""
        return {
            "width": self.image.width,
            "height": self.image.height,
            "aspect_ratio": round(self.image.width / self.image.height, 2)
        }
    
    def _extract_color_palette(self, num_colors: int = 8) -> List[Dict[str, Any]]:
        """Ana renk paletini çıkar"""
        # Görseli küçült (hız için)
        small_image = self.image.resize((150, 150))
        pixels = np.array(small_image).reshape(-1, 3)
        
        # K-means clustering ile dominant renkleri bul
        from sklearn.cluster import KMeans
        
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        colors = []
        for i, color in enumerate(kmeans.cluster_centers_):
            color_rgb = tuple(map(int, color))
            
            colors.append({
                "rgb": color_rgb,
                "hex": "#{:02x}{:02x}{:02x}".format(*color_rgb),
                "hsl": self._rgb_to_hsl(color_rgb),
                "percentage": round(np.sum(kmeans.labels_ == i) / len(pixels) * 100, 2)
            })
        
        # Yüzdeye göre sırala
        colors.sort(key=lambda x: x["percentage"], reverse=True)
        return colors
    
    def _get_dominant_colors(self) -> Dict[str, Any]:
        """En dominant renkleri bul"""
        palette = self._extract_color_palette(5)
        
        return {
            "primary": palette[0] if palette else None,
            "secondary": palette[1] if len(palette) > 1 else None,
            "accent": palette[2] if len(palette) > 2 else None,
            "background": self._detect_background_color(),
            "text_color": self._detect_text_color()
        }
    
    def _detect_background_color(self) -> Dict[str, Any]:
        """Arkaplan rengini tespit et"""
        # Köşelerden örnek al
        corners = [
            self.image.getpixel((0, 0)),
            self.image.getpixel((self.image.width-1, 0)),
            self.image.getpixel((0, self.image.height-1)),
            self.image.getpixel((self.image.width-1, self.image.height-1))
        ]
        
        # En yaygın köşe rengini bul
        from collections import Counter
        most_common = Counter(corners).most_common(1)[0][0]
        
        return {
            "rgb": most_common,
            "hex": "#{:02x}{:02x}{:02x}".format(*most_common),
            "hsl": self._rgb_to_hsl(most_common)
        }
    
    def _detect_text_color(self) -> Dict[str, Any]:
        """Metin rengini tespit et"""
        # Gri tonlamalı görsel oluştur
        gray = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2GRAY)
        
        # Metin bölgelerini tespit et (basit eşikleme)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Siyah/beyaz piksel sayısını karşılaştır
        black_pixels = np.sum(thresh == 0)
        white_pixels = np.sum(thresh == 255)
        
        if black_pixels > white_pixels:
            text_color = (0, 0, 0)  # Siyah
        else:
            text_color = (255, 255, 255)  # Beyaz
        
        return {
            "rgb": text_color,
            "hex": "#{:02x}{:02x}{:02x}".format(*text_color),
            "hsl": self._rgb_to_hsl(text_color)
        }
    
    def _analyze_layout(self) -> Dict[str, Any]:
        """Layout analizi"""
        # Kenar tespiti
        gray = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Çizgiler tespit et
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)
        
        layout_info = {
            "has_grid": self._detect_grid_structure(lines),
            "text_regions": self._detect_text_regions(gray),
            "image_regions": self._detect_image_regions(),
            "whitespace_analysis": self._analyze_whitespace(gray),
            "alignment": self._detect_alignment(lines)
        }
        
        return layout_info
    
    def _detect_grid_structure(self, lines) -> bool:
        """Grid yapısı var mı tespit et"""
        if lines is None:
            return False
        
        horizontal_lines = []
        vertical_lines = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            
            if abs(angle) < 10 or abs(angle) > 170:  # Yatay çizgiler
                horizontal_lines.append(line)
            elif abs(angle - 90) < 10 or abs(angle + 90) < 10:  # Dikey çizgiler
                vertical_lines.append(line)
        
        return len(horizontal_lines) >= 2 and len(vertical_lines) >= 2
    
    def _detect_text_regions(self, gray_image) -> List[Dict[str, int]]:
        """Metin bölgelerini tespit et"""
        # MSER (Maximally Stable Extremal Regions) ile metin alanları
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(gray_image)
        
        text_regions = []
        for region in regions:
            if len(region) > 10:  # Küçük alanları filtrele
                x, y, w, h = cv2.boundingRect(region)
                text_regions.append({
                    "x": int(x), "y": int(y), 
                    "width": int(w), "height": int(h)
                })
        
        return text_regions[:10]  # İlk 10 bölge
    
    def _detect_image_regions(self) -> List[Dict[str, int]]:
        """Görsel/grafik bölgelerini tespit et"""
        # Renk varyasyonu yüksek alanları bul
        hsv = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2HSV)
        
        # Contour tespiti
        gray = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        image_regions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Minimum alan
                x, y, w, h = cv2.boundingRect(contour)
                image_regions.append({
                    "x": int(x), "y": int(y),
                    "width": int(w), "height": int(h),
                    "area": int(area)
                })
        
        return sorted(image_regions, key=lambda x: x["area"], reverse=True)[:5]
    
    def _analyze_whitespace(self, gray_image) -> Dict[str, float]:
        """Beyaz alan analizi"""
        # Beyaz/açık renkli alanları tespit et
        _, binary = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
        white_pixels = np.sum(binary == 255)
        total_pixels = binary.shape[0] * binary.shape[1]
        
        whitespace_ratio = white_pixels / total_pixels
        
        return {
            "whitespace_ratio": round(whitespace_ratio, 3),
            "density": round(1 - whitespace_ratio, 3),
            "balance": "minimal" if whitespace_ratio < 0.3 else "balanced" if whitespace_ratio < 0.6 else "spacious"
        }
    
    def _detect_alignment(self, lines) -> str:
        """Hizalama tespit et"""
        if lines is None:
            return "free_form"
        
        # Çizgilerin pozisyonlarını analiz et
        horizontal_positions = []
        vertical_positions = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            
            if abs(angle) < 10:  # Yatay
                horizontal_positions.append((y1 + y2) / 2)
            elif abs(angle - 90) < 10:  # Dikey
                vertical_positions.append((x1 + x2) / 2)
        
        # Düzenli aralıklar var mı kontrol et
        h_regular = self._check_regular_spacing(horizontal_positions)
        v_regular = self._check_regular_spacing(vertical_positions)
        
        if h_regular and v_regular:
            return "grid"
        elif h_regular:
            return "horizontal_aligned"
        elif v_regular:
            return "vertical_aligned"
        else:
            return "free_form"
    
    def _check_regular_spacing(self, positions) -> bool:
        """Düzenli aralık var mı kontrol et"""
        if len(positions) < 3:
            return False
        
        positions = sorted(positions)
        gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
        
        if not gaps:
            return False
        
        avg_gap = np.mean(gaps)
        variance = np.var(gaps)
        
        return variance < (avg_gap * 0.2) ** 2  # Düşük varyans = düzenli
    
    def _analyze_typography(self) -> Dict[str, Any]:
        """Tipografi analizi"""
        gray = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2GRAY)
        
        # Metin yoğunluğu
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text_pixels = np.sum(binary == 0)  # Siyah pikseller (metin)
        total_pixels = binary.shape[0] * binary.shape[1]
        
        # Karakter boyutu tahmini (contour analizi)
        contours, _ = cv2.findContours(255 - binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        char_heights = []
        for contour in contours:
            _, _, _, h = cv2.boundingRect(contour)
            if 5 < h < 100:  # Makul karakter yüksekliği
                char_heights.append(h)
        
        avg_char_height = np.mean(char_heights) if char_heights else 0
        
        return {
            "text_density": round(text_pixels / total_pixels, 3),
            "estimated_font_size": int(avg_char_height) if avg_char_height > 0 else "unknown",
            "text_distribution": self._analyze_text_distribution(binary),
            "font_weight": self._estimate_font_weight(binary)
        }
    
    def _analyze_text_distribution(self, binary_image) -> str:
        """Metin dağılımı analizi"""
        h, w = binary_image.shape
        
        # Görseli bölgelere ayır
        top_half = binary_image[:h//2, :]
        bottom_half = binary_image[h//2:, :]
        left_half = binary_image[:, :w//2]
        right_half = binary_image[:, w//2:]
        
        # Her bölgedeki metin yoğunluğu
        top_density = np.sum(top_half == 0) / (top_half.shape[0] * top_half.shape[1])
        bottom_density = np.sum(bottom_half == 0) / (bottom_half.shape[0] * bottom_half.shape[1])
        left_density = np.sum(left_half == 0) / (left_half.shape[0] * left_half.shape[1])
        right_density = np.sum(right_half == 0) / (right_half.shape[0] * right_half.shape[1])
        
        # En yoğun bölgeyi bul
        densities = {
            "top": top_density,
            "bottom": bottom_density,
            "left": left_density,
            "right": right_density
        }
        
        max_region = max(densities, key=densities.get)
        
        if densities[max_region] > 0.1:
            return f"{max_region}_heavy"
        else:
            return "evenly_distributed"
    
    def _estimate_font_weight(self, binary_image) -> str:
        """Font kalınlığı tahmini"""
        # Morfolojik işlemlerle font kalınlığını tahmin et
        kernel = np.ones((2,2), np.uint8)
        eroded = cv2.erode(255 - binary_image, kernel, iterations=1)
        
        # Erozyon sonrası kalan piksel oranı
        remaining_ratio = np.sum(eroded > 0) / np.sum(binary_image == 0)
        
        if remaining_ratio > 0.7:
            return "bold"
        elif remaining_ratio > 0.4:
            return "medium"
        else:
            return "light"
    
    def _analyze_design_elements(self) -> Dict[str, Any]:
        """Tasarım öğeleri analizi"""
        return {
            "has_borders": self._detect_borders(),
            "has_shadows": self._detect_shadows(),
            "has_gradients": self._detect_gradients(),
            "geometric_shapes": self._detect_shapes(),
            "visual_complexity": self._calculate_complexity()
        }
    
    def _detect_borders(self) -> bool:
        """Kenar çerçevesi tespit et"""
        gray = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Kenar piksellerini kontrol et
        h, w = edges.shape
        border_pixels = (
            np.sum(edges[0, :]) + np.sum(edges[-1, :]) +  # Üst-alt
            np.sum(edges[:, 0]) + np.sum(edges[:, -1])    # Sol-sağ
        )
        
        return border_pixels > (2 * (h + w) * 0.3)  # %30'dan fazla kenar pikseli
    
    def _detect_shadows(self) -> bool:
        """Gölge efekti tespit et"""
        hsv = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2HSV)
        v_channel = hsv[:, :, 2]  # Value kanalı
        
        # Gradual değişimler (gölge belirtisi)
        grad_x = cv2.Sobel(v_channel, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(v_channel, cv2.CV_64F, 0, 1, ksize=3)
        
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        smooth_gradients = np.sum(gradient_magnitude < 50)  # Yumuşak geçişler
        
        return smooth_gradients > (gradient_magnitude.shape[0] * gradient_magnitude.shape[1] * 0.6)
    
    def _detect_gradients(self) -> bool:
        """Gradient tespit et"""
        hsv = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2HSV)
        
        # Her kanal için linear gradient tespiti
        channels = cv2.split(hsv)
        gradient_found = False
        
        for channel in channels:
            # Yatay ve dikey gradientler
            h_mean = np.mean(channel, axis=0)
            v_mean = np.mean(channel, axis=1)
            
            # Linear trend kontrolü
            h_trend = np.polyfit(range(len(h_mean)), h_mean, 1)[0]
            v_trend = np.polyfit(range(len(v_mean)), v_mean, 1)[0]
            
            if abs(h_trend) > 0.5 or abs(v_trend) > 0.5:
                gradient_found = True
                break
        
        return gradient_found
    
    def _detect_shapes(self) -> List[str]:
        """Geometrik şekiller tespit et"""
        gray = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        shapes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Minimum alan
                # Şekil yaklaşımı
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                vertices = len(approx)
                if vertices == 3:
                    shapes.append("triangle")
                elif vertices == 4:
                    shapes.append("rectangle")
                elif vertices > 8:
                    shapes.append("circle")
                else:
                    shapes.append("polygon")
        
        return list(set(shapes))  # Unique shapes
    
    def _calculate_complexity(self) -> str:
        """Görsel karmaşıklık hesapla"""
        gray = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2GRAY)
        
        # Kenar yoğunluğu
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Renk çeşitliliği
        unique_colors = len(np.unique(self.image_cv.reshape(-1, self.image_cv.shape[2]), axis=0))
        color_complexity = unique_colors / (self.image.width * self.image.height)
        
        # Genel karmaşıklık skoru
        complexity_score = (edge_density * 0.6) + (color_complexity * 0.4)
        
        if complexity_score < 0.1:
            return "simple"
        elif complexity_score < 0.3:
            return "moderate"
        else:
            return "complex"
    
    def _analyze_style(self) -> Dict[str, Any]:
        """Stil karakteristikleri"""
        return {
            "color_scheme": self._determine_color_scheme(),
            "design_style": self._determine_design_style(),
            "mood": self._determine_mood(),
            "era": self._determine_era()
        }
    
    def _determine_color_scheme(self) -> str:
        """Renk şeması belirleme"""
        palette = self._extract_color_palette(5)
        
        if not palette:
            return "unknown"
        
        # Saturation analizi
        saturations = [color["hsl"][1] for color in palette]
        avg_saturation = np.mean(saturations)
        
        # Lightness analizi
        lightnesses = [color["hsl"][2] for color in palette]
        avg_lightness = np.mean(lightnesses)
        
        if avg_saturation < 0.2:
            return "monochromatic"
        elif avg_lightness > 0.8:
            return "light"
        elif avg_lightness < 0.3:
            return "dark"
        elif avg_saturation > 0.7:
            return "vibrant"
        else:
            return "balanced"
    
    def _determine_design_style(self) -> str:
        """Tasarım stili belirleme"""
        elements = self._analyze_design_elements()
        layout = self._analyze_layout()
        
        if elements["geometric_shapes"] and layout["has_grid"]:
            return "modern_geometric"
        elif elements["has_gradients"] and elements["has_shadows"]:
            return "gradient_modern"
        elif elements["visual_complexity"] == "simple":
            return "minimalist"
        elif elements["has_borders"] and not elements["has_shadows"]:
            return "classic"
        else:
            return "contemporary"
    
    def _determine_mood(self) -> str:
        """Görsel atmosfer belirleme"""
        dominant_colors = self._get_dominant_colors()
        
        if not dominant_colors["primary"]:
            return "neutral"
        
        primary_hsl = dominant_colors["primary"]["hsl"]
        hue, saturation, lightness = primary_hsl
        
        # Hue tabanlı mood
        if 0 <= hue <= 60 or 300 <= hue <= 360:  # Kırmızı-sarı
            if saturation > 0.6:
                return "energetic"
            else:
                return "warm"
        elif 60 <= hue <= 180:  # Sarı-yeşil-cyan
            return "fresh"
        elif 180 <= hue <= 300:  # Mavi-mor
            if lightness > 0.7:
                return "calm"
            else:
                return "professional"
        else:
            return "neutral"
    
    def _determine_era(self) -> str:
        """Tasarım dönemi tahmini"""
        elements = self._analyze_design_elements()
        colors = self._determine_color_scheme()
        
        if elements["has_gradients"] and colors == "vibrant":
            return "2010s_modern"
        elif elements["visual_complexity"] == "simple" and colors in ["monochromatic", "light"]:
            return "2020s_minimal"
        elif elements["has_borders"] and not elements["has_gradients"]:
            return "classic_print"
        else:
            return "contemporary"
    
    def _rgb_to_hsl(self, rgb: Tuple[int, int, int]) -> Tuple[int, float, float]:
        """RGB'yi HSL'ye çevir"""
        r, g, b = rgb
        r, g, b = r/255.0, g/255.0, b/255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (int(h * 360), round(s, 3), round(l, 3))