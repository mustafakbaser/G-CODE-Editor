import json
import re

class GCodeProcessor:
    def __init__(self):
        self.start_params = []
        self.route_start_params = []
        self.route_end_params = []
        self.end_params = []
        self.thread_cut_params = []
        self.safe_route_params = []
        self.current_route = 1
        self.is_first_process = True
        self.z_positions = {"needle_down": "Z3", "needle_up": "Z30"}
        
    def load_parameters(self, filename):
        with open(filename, 'r') as file:
            params = json.load(file)
            self.start_params = params.get('start_params', [])
            self.route_start_params = [
                "F10000",
                "M114",
                "G04 P200",
                "M118",
                self.z_positions["needle_down"],
                self.z_positions["needle_up"],
                "M119"
            ]
            self.route_end_params = params.get('route_end_params', [])
            self.end_params = params.get('end_params', [])
            self.z_positions = params.get('z_positions', {"needle_down": "Z3", "needle_up": "Z30"})

    def update_z_positions(self, needle_down, needle_up):
        self.z_positions["needle_down"] = needle_down
        self.z_positions["needle_up"] = needle_up
        # route_start_params'ı güncelle
        self.route_start_params = [
            "F10000",
            "M114",
            "G04 P200",
            "M118",
            needle_down,
            needle_up,
            "M119"
        ]

    def is_coordinate_line(self, line):
        # X ve Y koordinatlarını içeren satırları kontrol et (Z değeri opsiyonel)
        pattern = r'^X\d+\.?\d*\s+Y\d+\.?\d*(?:\s+Z\d+\.?\d*)?$'
        return bool(re.match(pattern, line.strip()))

    def process_gcode(self, content):
        lines = content.split('\n')
        processed_lines = []
        coordinates = []
        start_coordinates = set()
        
        # Başlangıç koordinatlarını belirle
        if self.is_first_process:
            for line in self.start_params:
                if self.is_coordinate_line(line):
                    start_coordinates.add(line.strip())
        
        # Koordinatları topla
        has_coordinates = False
        for line in lines:
            line = line.strip()
            if line:  # Boş satırları atla
                if self.is_coordinate_line(line):
                    # X Y koordinatlarını al
                    xy_coords = ' '.join(line.split()[:2])  # İlk iki değeri (X Y) al
                    if xy_coords not in start_coordinates:
                        # Her zaman güncel Z değerini kullan
                        coordinates.append(f"{xy_coords} {self.z_positions['needle_down']}")
                        has_coordinates = True
                elif "% Rota No" not in line:  # Rota numarası satırını atlayarak diğer içeriği koru
                    processed_lines.append(line)
        
        # Eğer koordinat varsa veya ilk işlemse
        if has_coordinates or self.is_first_process:
            final_lines = []
            
            # Başlangıç parametreleri
            if self.is_first_process:
                final_lines.extend(self.start_params)
                self.is_first_process = False
            
            # Rota numarası
            final_lines.append(f"% Rota No {self.current_route}")
            
            # Rota başlangıç parametreleri
            final_lines.extend(self.route_start_params)
            
            # Koordinatlar ve Z30 değerleri
            if coordinates:
                # Son koordinat hariç her koordinattan sonra Z30 ekle
                for i, coord in enumerate(coordinates):
                    final_lines.append(coord)  # Koordinatı ekle
                    if i < len(coordinates) - 1:  # Son koordinat değilse
                        final_lines.append(self.z_positions["needle_up"])  # Z30 değerini ekle
            
            # Rota sonu parametreleri
            final_lines.extend(self.route_end_params)
            
            # G-CODE sonu parametreleri
            final_lines.extend(self.end_params)
            
            self.current_route += 1
            return '\n'.join(final_lines)
        
        return content  # Eğer işlenecek koordinat yoksa mevcut içeriği koru

    def reset_route_counter(self):
        self.current_route = 1
        self.is_first_process = True