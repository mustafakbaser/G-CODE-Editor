import os
import glob
from gcode_processor import GCodeProcessor

class MultiRouteProcessor:
    def __init__(self):
        self.processor = GCodeProcessor()
        self.routes_folder = "Rotalar"
        self.route_files = []
        
    def load_route_files(self):
        """Rotalar klasöründeki tüm .nc dosyalarını yükle"""
        if not os.path.exists(self.routes_folder):
            raise FileNotFoundError("Rotalar klasörü bulunamadı")
            
        # .nc dosyalarını al ve sırala
        self.route_files = sorted(glob.glob(os.path.join(self.routes_folder, "*.nc")))
        if not self.route_files:
            raise FileNotFoundError("İşlenecek .nc dosyası bulunamadı")
            
        return self.route_files
        
    def process_single_route(self, content, route_number):
        """Tek bir rotayı işle"""
        # Koordinatları ayıkla ve kalibre et
        coordinates = []
        for line in content.strip().split('\n'):
            if line.strip().startswith('X') and ' Y' in line:
                # Koordinatları kalibre et
                calibrated_line = self.processor.load_file_content(line.strip())
                coordinates.append(calibrated_line)
                
        if not coordinates:
            raise ValueError(f"Rota {route_number}: İşlenecek koordinat bulunamadı")
            
        # Rota içeriğini oluştur
        route_content = []
        
        # 1. Rota başlığı
        route_content.append(f"% Rota No {route_number}")
        
        # 2. G01 G90 F10000 veya F10000 (sadece ilk rotada G01 G90)
        if route_number == 1:
            route_content.append("G01 G90 F10000")
        else:
            route_content.append("F10000")
        
        # 3. İlk koordinat
        route_content.append(coordinates[0])
        
        # 4. Rota başlangıç parametreleri
        route_content.extend([
            "M114",
            "G04 P200"
        ])
        
        # 5. Üst İp Sıkma Bobini kontrolü
        if self.processor.bobbin_enabled:
            route_content.append("M118")
            route_content.append(self.processor.z_positions["needle_down"])
            if int(self.processor.bobbin_reset_value) == 1:
                route_content.append("M119")
            route_content.append(self.processor.z_positions["needle_up"])
            if int(self.processor.bobbin_reset_value) == 2:
                route_content.append("M119")
        else:
            route_content.extend([
                self.processor.z_positions["needle_down"],
                self.processor.z_positions["needle_up"]
            ])
        
        # 6. Koordinatları işle
        if self.processor.punteriz_enabled:
            # Punteriz işlemi
            punteriz_lines = self.processor.apply_punteriz(coordinates)
            route_content.extend(punteriz_lines)
        else:
            # Normal işlem - hız kontrolü ile
            for i in range(1, len(coordinates)):  # İlk koordinat zaten eklendi
                # Hız hesapla
                speed = self.processor.calculate_speed(i-1, len(coordinates)-1)
                
                # Koordinat satırı
                coord_line = coordinates[i]
                
                # Z pozisyonu ekle
                coord_line += f" {self.processor.z_positions['needle_down']}"
                
                # Hız değeri ekle
                if i == 1 or speed is not None:
                    coord_line += f" F{speed if speed else self.processor.start_speed}"
                
                # Satırı ekle
                route_content.append(coord_line)
                
                # Son koordinat değilse Z30 ekle
                if i < len(coordinates) - 1:
                    route_content.append(self.processor.z_positions["needle_up"])
        
        # 7. İp kesme parametreleri
        route_content.extend(self.processor.thread_cut_params)
        
        return route_content
        
    def process_routes(self):
        """Tüm rotaları işle ve tek bir G-Code oluştur"""
        if not self.route_files:
            self.load_route_files()
            
        final_gcode = []
        
        # 1. G-Code başlangıç parametreleri (sadece bir kez)
        final_gcode.extend(self.processor.start_params)
        
        # 2. Her rotayı işle
        for index, route_file in enumerate(self.route_files, 1):
            try:
                with open(route_file, 'r') as file:
                    content = file.read()
                    # Rotayı işle
                    route_content = self.process_single_route(content, index)
                    final_gcode.extend(route_content)
            except Exception as e:
                raise Exception(f"Rota {index} işlenirken hata: {str(e)}")
                
        # 3. G-Code sonlandırma parametreleri
        final_gcode.extend(self.processor.end_params)
        
        return '\n'.join(final_gcode) 