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
        self.start_speed = "10000"
        self.max_speed = "50000"
        self.speed_increment = "5000"
        
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

    def update_speed_settings(self, start_speed, max_speed, speed_increment):
        """Hız ayarlarını güncelle ve doğrula"""
        try:
            # Değerleri doğrula
            start = int(start_speed)
            max_val = int(max_speed)
            increment = int(speed_increment)
            
            if start <= 0 or max_val <= 0 or increment <= 0:
                raise ValueError("Hız değerleri pozitif olmalıdır")
            
            if start > max_val:
                raise ValueError("Başlangıç hızı maksimum hızdan büyük olamaz")
            
            # Değerleri güncelle
            self.start_speed = str(start)
            self.max_speed = str(max_val)
            self.speed_increment = str(increment)
            
        except ValueError as e:
            raise ValueError(f"Geçersiz hız değeri: {str(e)}")
    
    def calculate_speed(self, current_idx, total_points):
        """Belirli bir indeks için hız değerini hesapla"""
        start = int(self.start_speed)
        max_val = int(self.max_speed)
        increment = int(self.speed_increment)
        
        # Son 8 nokta için hız düşüşü başlat
        deceleration_points = 8
        effective_total = total_points - deceleration_points
        
        if current_idx == 0:
            return start  # İlk nokta için başlangıç hızı
        
        # Hız artışı
        current_speed = start + (current_idx * increment)
        
        # Maksimum hıza ulaşıldıysa
        if current_speed >= max_val:
            if current_idx < effective_total:
                # İlk kez maksimum hıza ulaşıldığında max_val döndür
                prev_speed = start + ((current_idx - 1) * increment)
                if prev_speed < max_val:
                    return max_val
                return None  # Sonraki noktalarda None döndür
            else:
                # Düşüş başladıysa
                remaining_steps = total_points - current_idx
                current_speed = max_val - ((deceleration_points - remaining_steps + 1) * increment)
                return max(start, current_speed)
        
        # Normal artış durumu
        return current_speed

    def apply_punteriz(self, coordinates):
        """Punteriz işlemini uygula"""
        if not coordinates:
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
            result.append(self.z_positions["needle_up"])
            
            # Punteriz sayısı kadar git-gel yap
            for _ in range(start_value):
                result.extend([
                    f"{coordinates[0]} {self.z_positions['needle_down']}",
                    self.z_positions["needle_up"],
                    f"{coordinates[1]} {self.z_positions['needle_down']}"
                ])
                result.append(self.z_positions["needle_up"])
        
        # Orta kısım - normal ilerleme
        start_idx = 2 if start_value > 0 else 0
        end_idx = len(coordinates) - 2 if end_value > 0 else len(coordinates) - 1
        
        # Normal ilerleme için hız kontrolü
        prev_speed = None
        effective_length = end_idx - start_idx
        
        for i in range(start_idx, end_idx):
            current_pos = i - start_idx
            speed = self.calculate_speed(current_pos, effective_length)
            coord_line = f"{coordinates[i]} {self.z_positions['needle_down']}"
            
            # İlk nokta veya hız değişmişse F parametresini ekle
            if speed is not None and (prev_speed is None or speed != prev_speed):
                coord_line += f" F{speed}"
                prev_speed = speed
            
            result.extend([coord_line, self.z_positions["needle_up"]])
        
        # Dikiş Sonu Punteriz
        if end_value > 0:
            last_idx = len(coordinates) - 1
            second_last_idx = last_idx - 1
            
            # Son hız değerini ekle
            speed = self.calculate_speed(effective_length - 1, effective_length)
            if speed is not None and speed != prev_speed:
                result.extend([
                    f"{coordinates[second_last_idx]} {self.z_positions['needle_down']} F{speed}",
                    self.z_positions["needle_up"],
                    f"{coordinates[last_idx]} {self.z_positions['needle_down']}"
                ])
            else:
                result.extend([
                    f"{coordinates[second_last_idx]} {self.z_positions['needle_down']}",
                    self.z_positions["needle_up"],
                    f"{coordinates[last_idx]} {self.z_positions['needle_down']}"
                ])
            result.append(self.z_positions["needle_up"])
            
            for _ in range(end_value):
                result.extend([
                    f"{coordinates[second_last_idx]} {self.z_positions['needle_down']}",
                    self.z_positions["needle_up"],
                    f"{coordinates[last_idx]} {self.z_positions['needle_down']}"
                ])
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
        
        # Punteriz işlemi veya normal ilerleme
        if self.punteriz_enabled:
            # Punteriz işlemini uygula
            punteriz_lines = self.apply_punteriz(coordinates)
            final_lines.extend(punteriz_lines)
        else:
            # Normal ilerleme - hız kontrolü ile
            # İlk koordinat için başlangıç hızını ekle
            if coordinates:
                final_lines.append(f"{coordinates[0]} {self.z_positions['needle_down']} F{self.start_speed}")
                final_lines.append(self.z_positions["needle_up"])
                
                # Diğer koordinatlar için hız artışı/azalışı uygula
                for i in range(1, len(coordinates)):
                    speed = self.calculate_speed(i, len(coordinates))
                    coord_line = f"{coordinates[i]} {self.z_positions['needle_down']}"
                    if speed is not None:
                        coord_line += f" F{speed}"
                    final_lines.extend([coord_line, self.z_positions["needle_up"]])
        
        # İp kesme parametrelerini ekle
        final_lines.extend(self.thread_cut_params)
        
        # Rota numarasını artır
        self.current_route += 1
        
        return '\n'.join(final_lines)

    def reset_route_counter(self):
        self.current_route = 1
        self.is_first_process = True
        # Parametrelerin önceki değerlerini sıfırla
        self.previous_route_start_params = []