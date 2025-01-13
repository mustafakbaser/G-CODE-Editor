import json
import re

class GCodeProcessor:
    def __init__(self):
        self.start_params = []
        self.route_start_params = []
        self.route_end_params = []
        self.end_params = []
        self.thread_cut_params = []
        self.current_route = 1
        self.is_first_process = True
        self.z_positions = {"needle_down": "Z3", "needle_up": "Z30"}
        self.calibration_values = {"x_value": "21.57001", "y_value": "388.6"}
        self.previous_calibration = {"x_value": "21.57001", "y_value": "388.6"}
        self.initial_coordinates = []  # İlk yüklenen koordinatları saklamak için
        self.processed_coordinates = []  # İşlenmiş koordinatları saklamak için
        
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
            self.thread_cut_params = params.get('thread_cut_params', [])
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

    def update_calibration_values(self, x_value, y_value):
        # Önceki değerleri kaydet
        self.previous_calibration = self.calibration_values.copy()
        # Yeni değerleri güncelle
        self.calibration_values["x_value"] = x_value
        self.calibration_values["y_value"] = y_value

    def apply_calibration(self, x, y, is_first_time=False):
        """Koordinatlara kalibrasyon değerlerini uygula"""
        if is_first_time:
            # İlk kez uygulama - doğrudan ekle
            new_x = float(x) + float(self.calibration_values["x_value"])
            new_y = float(y) + float(self.calibration_values["y_value"])
        else:
            # Güncelleme - farkı uygula
            x_diff = float(self.calibration_values["x_value"]) - float(self.previous_calibration["x_value"])
            y_diff = float(self.calibration_values["y_value"]) - float(self.previous_calibration["y_value"])
            new_x = float(x) + x_diff
            new_y = float(y) + y_diff
        
        return f"X{new_x:.5f} Y{new_y:.5f}"

    def has_calibration_changed(self):
        """Kalibrasyon değerlerinin değişip değişmediğini kontrol et"""
        return (self.calibration_values["x_value"] != self.previous_calibration["x_value"] or 
                self.calibration_values["y_value"] != self.previous_calibration["y_value"])

    def load_file_content(self, content):
        """Dosya içeriğini ilk yükleme sırasında işle - sadece koordinatları kalibre et"""
        lines = content.split('\n')
        calibrated_lines = []
        self.initial_coordinates = []
        
        for line in lines:
            line = line.strip()
            if line:
                if self.is_coordinate_line(line):
                    parts = line.split()
                    if len(parts) >= 2:
                        x_val = parts[0][1:]  # X'ten sonraki değer
                        y_val = parts[1][1:]  # Y'den sonraki değer
                        
                        # Kalibrasyon uygula
                        calibrated_coords = self.apply_calibration(x_val, y_val, is_first_time=True)
                        calibrated_lines.append(calibrated_coords)
                        self.initial_coordinates.append(calibrated_coords)
                else:
                    calibrated_lines.append(line)
        
        # İşlenmiş koordinatları sakla
        self.processed_coordinates = self.initial_coordinates.copy()
        
        # Sadece kalibre edilmiş koordinatları döndür
        return '\n'.join(calibrated_lines)

    def process_gcode(self, content):
        """G-Code oluştur butonuna basıldığında tam G-Code içeriğini oluştur"""
        # Kalibrasyon değişmediyse mevcut koordinatları kullan
        if not self.has_calibration_changed():
            coordinates = self.processed_coordinates
        else:
            # Kalibrasyon değiştiyse koordinatları güncelle
            coordinates = []
            for coord in self.initial_coordinates:
                parts = coord.split()
                if len(parts) >= 2:
                    x_val = parts[0][1:]
                    y_val = parts[1][1:]
                    calibrated_coords = self.apply_calibration(x_val, y_val, is_first_time=False)
                    coordinates.append(calibrated_coords)
            self.processed_coordinates = coordinates
        
        # Tam G-Code içeriğini oluştur
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
            for i, coord in enumerate(coordinates):
                final_lines.append(f"{coord} {self.z_positions['needle_down']}")
                if i < len(coordinates) - 1:
                    final_lines.append(self.z_positions["needle_up"])
        
        # Son koordinattan sonra ip kesme parametrelerini ekle
        if self.thread_cut_params:
            final_lines.extend(self.thread_cut_params)
        
        # G-CODE sonu parametreleri
        if self.end_params:
            final_lines.extend(self.end_params)
        
        self.current_route += 1
        return '\n'.join(final_lines)

    def reset_route_counter(self):
        self.current_route = 1
        self.is_first_process = True