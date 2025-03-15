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
        self.current_speed = None  # Mevcut hız değerini takip etmek için yeni değişken
        
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
        try:
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
            
            # Her zaman 2 ondalık basamak olacak şekilde formatla
            return f"X{new_x:.2f} Y{new_y:.2f}"
        except ValueError as e:
            raise ValueError(f"Kalibrasyon değerleri uygulanırken hata: {str(e)}")

    def has_calibration_changed(self):
        """Kalibrasyon değerlerinin değişip değişmediğini kontrol et"""
        return (self.calibration_values["x_value"] != self.previous_calibration["x_value"] or 
                self.calibration_values["y_value"] != self.previous_calibration["y_value"])

    def load_file_content(self, content):
        """Dosya içeriğini ilk yükleme sırasında işle - koordinatları kalibre et"""
        if isinstance(content, str):
            lines = content.split('\n')
        else:
            lines = [content]  # Tek satır geldiğinde
        
        calibrated_lines = []
        self.initial_coordinates = []
        
        for line in lines:
            line = line.strip()
            if line:
                if self.is_coordinate_line(line):
                    parts = line.split()
                    if len(parts) >= 2:
                        x_val = float(parts[0][1:])  # X'ten sonraki değer
                        y_val = float(parts[1][1:])  # Y'den sonraki değer
                        
                        # Kalibrasyon değerlerini ekle
                        calibrated_coords = self.apply_calibration(x_val, y_val, True)
                        calibrated_lines.append(calibrated_coords)
                        self.initial_coordinates.append(calibrated_coords)
                else:
                    calibrated_lines.append(line)
        
        # İşlenmiş koordinatları sakla
        self.processed_coordinates = self.initial_coordinates.copy()
        
        # Kalibre edilmiş koordinatları döndür
        return '\n'.join(calibrated_lines) if len(lines) > 1 else calibrated_lines[0]

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
            self.current_speed = None  # Hız ayarları değiştiğinde mevcut hızı sıfırla
            
        except ValueError as e:
            raise ValueError(f"Geçersiz hız değeri: {str(e)}")
    
    def calculate_speed(self, current_index, total_points):
        """Hız değerini hesapla"""
        if total_points <= 1:
            return self.start_speed
            
        # Hız artışı için gereken adım sayısını hesapla
        speed_diff = int(self.max_speed) - int(self.start_speed)
        steps_for_acceleration = speed_diff // int(self.speed_increment)
        
        # Hızlanma ve yavaşlama için kullanılacak nokta sayısı
        acceleration_points = steps_for_acceleration
        deceleration_points = steps_for_acceleration
        
        # Hızlanma bölgesi
        if current_index < acceleration_points:
            new_speed = int(self.start_speed) + (int(self.speed_increment) * current_index)
            new_speed = min(new_speed, int(self.max_speed))
        # Yavaşlama bölgesi - son noktalardan geriye doğru
        elif current_index >= total_points - deceleration_points:
            remaining_steps = total_points - current_index - 1
            new_speed = int(self.start_speed) + (int(self.speed_increment) * remaining_steps)
            new_speed = max(new_speed, int(self.start_speed))
        # Sabit hız bölgesi (maksimum hız)
        else:
            new_speed = int(self.max_speed)
        
        # Eğer hız değişmediyse None döndür, değiştiyse yeni hızı döndür
        if self.current_speed is not None and new_speed == self.current_speed:
            return None
        
        # Mevcut hızı güncelle ve döndür
        self.current_speed = new_speed
        return str(new_speed)

    def apply_punteriz(self, coordinates):
        """Punteriz işlemini uygula"""
        if not coordinates:
            return []
            
        result = []
        start_value = int(self.punteriz_start)
        end_value = int(self.punteriz_end)
        
        # Koordinatları 2 ondalık basamağa yuvarla
        formatted_coordinates = []
        for coord in coordinates:
            parts = coord.split()
            x_val = round(float(parts[0][1:]), 2)  # X değeri
            y_val = round(float(parts[1][1:]), 2)  # Y değeri
            formatted_coordinates.append(f"X{x_val:.2f} Y{y_val:.2f}")
        
        # Hız takibi için değişkeni sıfırla
        self.current_speed = None
        
        # Dikiş Başı Punteriz
        if start_value > 0:
            # İlk indeks rota başlangıcında olduğu için direkt ikinci indeksle başla
            result.extend([
                f"{formatted_coordinates[1]} {self.z_positions['needle_down']}",   # İkinci indeks
                self.z_positions["needle_up"]
            ])
            
            # Punteriz sayısı kadar git-gel yap
            for _ in range(start_value):
                result.extend([
                    f"{formatted_coordinates[0]} {self.z_positions['needle_down']}", # İlk indekse git
                    self.z_positions["needle_up"],
                    f"{formatted_coordinates[1]} {self.z_positions['needle_down']}"  # İkinci indekse dön
                ])
                result.append(self.z_positions["needle_up"])
        
        # Orta kısım - normal ilerleme
        start_idx = 2 if start_value > 0 else 1  # İlk indeks rota başlangıcında olduğu için 1'den başla
        end_idx = len(formatted_coordinates) - 2 if end_value > 0 else len(formatted_coordinates) - 1
        
        # Normal ilerleme için hız kontrolü
        effective_length = end_idx - start_idx + 1  # +1 eklendi çünkü end_idx dahil
        
        # İlk nokta - başlangıç hızı ile
        first_speed = self.calculate_speed(0, effective_length)
        first_coord = f"{formatted_coordinates[start_idx]} {self.z_positions['needle_down']} F{first_speed}"
        result.extend([first_coord, self.z_positions["needle_up"]])
        
        # Diğer noktalar
        for i in range(start_idx + 1, end_idx + 1):  # end_idx dahil
            current_pos = i - start_idx
            speed = self.calculate_speed(current_pos, effective_length)
            coord_line = f"{formatted_coordinates[i]} {self.z_positions['needle_down']}"
            
            # Hız değişmişse F parametresini ekle
            if speed is not None:
                coord_line += f" F{speed}"
            
            # Z30 ekle
            result.extend([coord_line, self.z_positions["needle_up"]])
        
        # Dikiş Sonu Punteriz
        if end_value > 0:
            last_idx = len(formatted_coordinates) - 1
            second_last_idx = last_idx - 1
            
            # Son noktaya git
            result.append(f"{formatted_coordinates[last_idx]} {self.z_positions['needle_down']}")
            
            # Punteriz sayısı (n) kadar git-gel yap
            for i in range(end_value):
                # Sondan bir önceki noktaya git
                result.extend([
                    self.z_positions["needle_up"],
                    f"{formatted_coordinates[second_last_idx]} {self.z_positions['needle_down']}"
                ])
                
                # Son noktaya dön
                result.extend([
                    self.z_positions["needle_up"],
                    f"{formatted_coordinates[last_idx]} {self.z_positions['needle_down']}"
                ])
        
        return result

    def process_gcode(self, content):
        """G-Code içeriğini işle"""
        if not self.processed_coordinates:
            raise ValueError("İşlenecek koordinat bulunamadı")
            
        final_lines = []
        coordinates = self.processed_coordinates
        
        # Hız takibi için değişkeni sıfırla
        self.current_speed = None
        
        # Koordinatları işle
        for i in range(len(coordinates)):
            # Hız hesapla
            speed = self.calculate_speed(i, len(coordinates))
            
            # Koordinat satırını oluştur
            coord_line = coordinates[i]
            
            # Z pozisyonunu ekle
            coord_line += f" {self.z_positions['needle_down']}"
            
            # Hız değerini ekle (ilk koordinat veya hız değiştiğinde)
            if i == 0 or speed is not None:
                coord_line += f" F{speed if speed else self.start_speed}"
            
            # Satırı ekle
            final_lines.append(coord_line)
            
            # Son koordinat değilse Z30 ekle
            if i < len(coordinates) - 1:
                final_lines.append(self.z_positions["needle_up"])
        
        return '\n'.join(final_lines)

    def reset_route_counter(self):
        self.current_route = 1
        self.is_first_process = True
        # Parametrelerin önceki değerlerini sıfırla
        self.previous_route_start_params = []
        # Hız takibi için değişkeni sıfırla
        self.current_speed = None 