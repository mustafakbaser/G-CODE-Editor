import json
import re

class GCodeProcessor:
    def __init__(self):
        self.start_params = []
        self.route_start_params = []
        self.route_end_params = []
        self.current_route = 1
        
    def load_parameters(self, filename):
        with open(filename, 'r') as file:
            params = json.load(file)
            self.start_params = params.get('start_params', [])
            # route_start_params artık sabit bir template olarak kullanılacak
            self.route_start_params = [
                "F10000",
                "{first_index}",  # Bu placeholder ile değiştirilecek
                "M114",
                "G04 P200",
                "M118",
                "Z3",
                "Z30",
                "M119"
            ]
            self.route_end_params = params.get('route_end_params', [])

    def is_coordinate_line(self, line):
        # X ve Y koordinatlarını içeren satırları kontrol et
        pattern = r'^X\d+\.?\d*\s+Y\d+\.?\d*\s*$'
        return bool(re.match(pattern, line.strip()))

    def process_gcode(self, content):
        lines = content.split('\n')
        processed_lines = []
        coordinates = []
        
        # Koordinatları topla
        for line in lines:
            line = line.strip()
            if self.is_coordinate_line(line):
                coordinates.append(line)
        
        if coordinates:
            # G-CODE başlangıç parametreleri
            processed_lines.extend(self.start_params)
            
            # Rota numarasını ekle
            processed_lines.append(f"% Rota No {self.current_route}")
            
            # Rota başlangıç parametrelerini ekle
            first_index = coordinates[0]  # Rotanın ilk indexi (koordinatı)
            for param in self.route_start_params:
                if param == "{first_index}":
                    processed_lines.append(first_index)
                else:
                    processed_lines.append(param)
            
            # Koordinatları ekle
            processed_lines.extend(coordinates)
            
            # Rota sonu parametreleri
            processed_lines.extend(self.route_end_params)
            
            self.current_route += 1
        
        return '\n'.join(processed_lines)

    def reset_route_counter(self):
        self.current_route = 1