import json
import re

class GCodeProcessor:
    def __init__(self):
        self.start_params = []
        self.route_start_params = []
        self.end_params = []
        self.thread_cut_params = []
        self.current_route = 1
        self.is_first_process = True
        self.z_positions = {"needle_down": "Z3", "needle_up": "Z30"}
        self.calibration_values = {"x_value": "21.57001", "y_value": "388.6"}
        self.previous_calibration = {"x_value": "21.57001", "y_value": "388.6"}
        self.initial_coordinates = []
        self.processed_coordinates = []
        self.previous_route_start_params = []
        self.bobbin_enabled = False
        self.bobbin_reset_value = "1"
        self.punteriz_enabled = False
        self.punteriz_start = "0"
        self.punteriz_end = "0"
        
    def load_parameters(self, filename):
        with open(filename, 'r') as file:
            params = json.load(file)
            self.start_params = params.get('start_params', [])
            self.route_start_params = params.get('route_start_params', [])
            self.thread_cut_params = params.get('thread_cut_params', [])
            self.end_params = params.get('end_params', [])
            self.z_positions = params.get('z_positions', {"needle_down": "Z3", "needle_up": "Z30"})

    def update_z_positions(self, needle_down, needle_up):
        """Z pozisyonlarını güncelle"""
        self.z_positions["needle_down"] = needle_down
        self.z_positions["needle_up"] = needle_up

    def is_coordinate_line(self, line):
        # X ve Y koordinatlarını içeren satırları kontrol et (Z değeri opsiyonel)
        pattern = r'^X\d+\.?\d*\s+Y\d+\.?\d*(?:\s+Z\d+\.?\d*)?$'
        return bool(re.match(pattern, line.strip()))

    def update_calibration_values(self, x_value, y_value):
        # Önceki değerleri kaydet
        self.previous_calibration = self.calibration_values.copy()
        # Yeni değerleri yuvarla ve güncelle
        self.calibration_values["x_value"] = f"{round(float(x_value), 2):.2f}"
        self.calibration_values["y_value"] = f"{round(float(y_value), 2):.2f}"

    def apply_calibration(self, x, y, is_first_time=False):
        """Koordinatlara kalibrasyon değerlerini uygula"""
        if is_first_time:
            # İlk kez uygulama - doğrudan ekle
            new_x = round(float(x) + float(self.calibration_values["x_value"]), 2)
            new_y = round(float(y) + float(self.calibration_values["y_value"]), 2)
        else:
            # Güncelleme - farkı uygula
            x_diff = round(float(self.calibration_values["x_value"]) - float(self.previous_calibration["x_value"]), 2)
            y_diff = round(float(self.calibration_values["y_value"]) - float(self.previous_calibration["y_value"]), 2)
            new_x = round(float(x) + x_diff, 2)
            new_y = round(float(y) + y_diff, 2)
        
        return f"X{new_x:.2f} Y{new_y:.2f}"

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

    def has_parameters_changed(self):
        """Herhangi bir parametrenin değişip değişmediğini kontrol et"""
        calibration_changed = self.has_calibration_changed()
        route_params_changed = self.route_start_params != self.previous_route_start_params
        return calibration_changed or route_params_changed

    def update_bobbin_settings(self, enabled, reset_value):
        """Üst İp Sıkma Bobini ayarlarını güncelle"""
        self.bobbin_enabled = enabled
        self.bobbin_reset_value = reset_value

    def update_punteriz_settings(self, enabled, start_value, end_value):
        """Punteriz ayarlarını güncelle"""
        self.punteriz_enabled = enabled
        self.punteriz_start = start_value
        self.punteriz_end = end_value

    def apply_punteriz(self, coordinates):
        """Punteriz işlemini uygula"""
        if not coordinates or not self.punteriz_enabled:
            return []
            
        result = []
        start_value = int(self.punteriz_start)
        end_value = int(self.punteriz_end)
        
        # Dikiş Başı Punteriz
        if start_value > 0:
            # İlk iki koordinatı ekle
            result.extend([
                f"{coordinates[0]} {self.z_positions['needle_down']}",  # İlk indeks
                self.z_positions["needle_up"],
                f"{coordinates[1]} {self.z_positions['needle_down']}"   # İkinci indeks
            ])
            result.append(self.z_positions["needle_up"])  # Z30 ekle
            
            # Punteriz sayısı kadar git-gel yap
            for _ in range(start_value):
                result.extend([
                    f"{coordinates[0]} {self.z_positions['needle_down']}",  # İlk indekse git
                    self.z_positions["needle_up"],
                    f"{coordinates[1]} {self.z_positions['needle_down']}"   # İkinci indekse dön
                ])
                result.append(self.z_positions["needle_up"])  # Z30 ekle
        
        # Orta kısım - normal ilerleme
        start_idx = 2 if start_value > 0 else 0  # Başlangıç punteriz varsa 2. indeksten başla
        end_idx = len(coordinates) - 2 if end_value > 0 else len(coordinates) - 1
        
        for i in range(start_idx, end_idx):
            result.extend([
                f"{coordinates[i]} {self.z_positions['needle_down']}",
                self.z_positions["needle_up"]
            ])
        
        # Dikiş Sonu Punteriz
        if end_value > 0:
            last_idx = len(coordinates) - 1
            second_last_idx = last_idx - 1
            
            # Son iki koordinatı ekle
            result.extend([
                f"{coordinates[second_last_idx]} {self.z_positions['needle_down']}",  # Sondan bir önceki
                self.z_positions["needle_up"],
                f"{coordinates[last_idx]} {self.z_positions['needle_down']}"         # Son indeks
            ])
            result.append(self.z_positions["needle_up"])  # Z30 ekle
            
            # Punteriz sayısı kadar git-gel yap
            for _ in range(end_value):
                result.extend([
                    f"{coordinates[second_last_idx]} {self.z_positions['needle_down']}",  # Sondan bir öncekine git
                    self.z_positions["needle_up"],
                    f"{coordinates[last_idx]} {self.z_positions['needle_down']}"         # Son indekse dön
                ])
                # Son punterizin son adımı hariç Z30 ekle
                if _ < end_value - 1:
                    result.append(self.z_positions["needle_up"])
        
        return result

    def process_gcode(self, content):
        """G-Code oluştur butonuna basıldığında tam G-Code içeriğini oluştur"""
        # Her zaman yeni içerik oluştur
        coordinates = []
        if self.has_calibration_changed():
            # Kalibrasyon değiştiyse koordinatları güncelle
            for coord in self.initial_coordinates:
                parts = coord.split()
                if len(parts) >= 2:
                    x_val = parts[0][1:]
                    y_val = parts[1][1:]
                    calibrated_coords = self.apply_calibration(x_val, y_val, is_first_time=False)
                    coordinates.append(calibrated_coords)
            self.processed_coordinates = coordinates
        else:
            # Kalibrasyon değişmediyse mevcut koordinatları kullan
            coordinates = self.processed_coordinates
            
        # Tam G-Code içeriğini oluştur
        final_lines = []
        
        # Başlangıç parametreleri
        if self.is_first_process:
            final_lines.extend(self.start_params)
            self.is_first_process = False
        
        # Rota numarası
        final_lines.append(f"% Rota No {self.current_route}")
        
        # Temel parametreleri ekle
        base_params = ["G01 G90 F10000", "M114", "G04 P200"]
        final_lines.extend(base_params)
        
        # M118-M119 mantığını uygula
        if self.bobbin_enabled:
            # M119'un konumunu belirle
            m119_position = int(self.bobbin_reset_value)
            final_lines.append("M118")
            
            if m119_position == 1:
                final_lines.extend([self.z_positions["needle_down"], "M119", self.z_positions["needle_up"]])
            elif m119_position == 2:
                final_lines.extend([self.z_positions["needle_down"], self.z_positions["needle_up"], "M119"])
            else:
                final_lines.extend([self.z_positions["needle_down"], self.z_positions["needle_up"]])
        else:
            # Checkbox pasifse sadece Z değerlerini ekle
            final_lines.extend([self.z_positions["needle_down"], self.z_positions["needle_up"]])
        
        # Rota başlangıç parametrelerinden gelen diğer değerleri ekle
        if self.route_start_params:
            additional_params = [param for param in self.route_start_params 
                               if param not in base_params and 
                               param not in ["M118", "M119"] and
                               not param.startswith("Z")]
            final_lines.extend(additional_params)
        
        # Önceki parametreleri güncelle
        self.previous_route_start_params = self.route_start_params.copy()
        
        # Koordinatlar ve Z30 değerleri
        if coordinates:
            if self.punteriz_enabled:
                # Punteriz işlemini uygula
                punteriz_lines = self.apply_punteriz(coordinates)
                final_lines.extend(punteriz_lines)
            else:
                # Normal dikiş işlemi
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
        # Parametrelerin önceki değerlerini sıfırla
        self.previous_route_start_params = []