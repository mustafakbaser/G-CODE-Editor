import json
import os
import shutil
from datetime import datetime
from models.gcode_processor import GCodeProcessor
from models.multi_route_processor import MultiRouteProcessor

class GCodeModel:
    """
    G-CODE verilerini ve işlemlerini yöneten model sınıfı.
    """
    def __init__(self):
        self.processor = GCodeProcessor()
        self.multi_processor = MultiRouteProcessor()
        self.content = ""
        self.parameters_file = self._get_parameters_file_path()
        
        # Parametreler dosyasını kopyala (eğer yoksa)
        self._ensure_parameters_file_exists()
        
    def _get_parameters_file_path(self):
        """parameters.json dosyasının yolunu döndürür."""
        # Mevcut dizinde ara
        local_path = "parameters.json"
        if os.path.exists(local_path):
            return local_path
            
        # Bulunamazsa varsayılan olarak yerel yolu döndür
        return local_path
    
    def _ensure_parameters_file_exists(self):
        """parameters.json dosyasının varlığını kontrol eder ve yoksa kopyalar."""
        if not os.path.exists(self.parameters_file):
            # Varsayılan parametreleri oluştur
            default_params = {
                "start_params": [
                    "% G-Code Starting Parameters",
                    "#MW6789 = 219",
                    "M115",
                    "G04 P200",
                    "X5 Y26",
                    "X50 Y50"
                ],
                "route_start_params": [
                    "G01 G90 F10000",
                    "M114",
                    "G04 P200",
                    "M118",
                    "Z3",
                    "Z30",
                    "M119"
                ],
                "thread_cut_params": [
                    "% Cutting Parameters",
                    "Z28",
                    "G04 P50",
                    "M124",
                    "G04 P50",
                    "M112",
                    "G04 P150",
                    "F2000",
                    "Z1",
                    "F10000",
                    "G04 P50",
                    "M120",
                    "G04 P500",
                    "M121",
                    "G04 P50",
                    "M125",
                    "G04 P50",
                    "M113",
                    "G04 P50",
                    "G91",
                    "G1",
                    "Z-5",
                    "G04 P80",
                    "M126",
                    "G04 P100",
                    "M127",
                    "G04 P200",
                    "G90",
                    "Z0",
                    "M115",
                    "G04 P200"
                ],
                "end_params": [
                    "% G-Code End Parameters",
                    "F10000",
                    "X50 Y50",
                    "X5 Y26",
                    "M111",
                    "M2"
                ],
                "z_positions": {
                    "needle_down": "Z3",
                    "needle_up": "Z30"
                },
                "machine_calibration": {
                    "x_value": "21.57",
                    "y_value": "388.60"
                }
            }
            
            # Varsayılan parametreleri kaydet
            with open(self.parameters_file, 'w') as file:
                json.dump(default_params, file, indent=4)
            print(f"Varsayılan parameters.json dosyası oluşturuldu.")
        
    def load_default_parameters(self):
        """Varsayılan parametreleri parameters.json dosyasından yükler."""
        try:
            with open(self.parameters_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            raise Exception(f"Parametreler yüklenirken hata oluştu: {str(e)}")
    
    def save_parameters(self, params):
        """Parametreleri parameters.json dosyasına kaydeder."""
        try:
            # Mevcut parametreleri yükle
            current_params = self.load_default_parameters()
            
            # Yeni parametreleri güncelle
            current_params['start_params'] = params.get('start_params', current_params.get('start_params', []))
            current_params['route_start_params'] = params.get('route_start_params', current_params.get('route_start_params', []))
            current_params['thread_cut_params'] = params.get('thread_cut_params', current_params.get('thread_cut_params', []))
            current_params['end_params'] = params.get('end_params', current_params.get('end_params', []))
            
            # Z pozisyonları
            if 'z_positions' not in current_params:
                current_params['z_positions'] = {}
            current_params['z_positions']['needle_down'] = params.get('needle_down', current_params['z_positions'].get('needle_down', 'Z3'))
            current_params['z_positions']['needle_up'] = params.get('needle_up', current_params['z_positions'].get('needle_up', 'Z30'))
            
            # Makine kalibrasyonu
            if 'machine_calibration' not in current_params:
                current_params['machine_calibration'] = {}
            current_params['machine_calibration']['x_value'] = params.get('calibration_x', current_params['machine_calibration'].get('x_value', '21.57'))
            current_params['machine_calibration']['y_value'] = params.get('calibration_y', current_params['machine_calibration'].get('y_value', '388.60'))
            
            # Dosyaya kaydet
            with open(self.parameters_file, 'w') as file:
                json.dump(current_params, file, indent=4)
                
            return True
        except Exception as e:
            raise Exception(f"Parametreler kaydedilirken hata oluştu: {str(e)}")
    
    def update_processor_parameters(self, params):
        """Processor parametrelerini günceller."""
        # Kalibrasyon değerleri
        self.processor.update_calibration_values(
            params.get('calibration_x', '0'), 
            params.get('calibration_y', '0')
        )
        
        # Z pozisyonları
        self.processor.update_z_positions(
            params.get('needle_down', 'Z3'), 
            params.get('needle_up', 'Z30')
        )
        
        # Bobbin ayarları
        self.processor.update_bobbin_settings(
            params.get('bobbin_enabled', False), 
            params.get('bobbin_reset_value', '1')
        )
        
        # Punteriz ayarları
        self.processor.update_punteriz_settings(
            params.get('punteriz_enabled', False), 
            params.get('punteriz_start', '0'), 
            params.get('punteriz_end', '0')
        )
        
        # Hız ayarları
        self.processor.update_speed_settings(
            params.get('start_speed', '10000'), 
            params.get('max_speed', '50000'), 
            params.get('speed_increment', '5000')
        )
        
        # Diğer parametreler
        self.processor.start_params = params.get('start_params', [])
        self.processor.route_start_params = params.get('route_start_params', [])
        self.processor.thread_cut_params = params.get('thread_cut_params', [])
        self.processor.end_params = params.get('end_params', [])
        
        # Parametreleri kaydet
        self.save_parameters(params)
    
    def load_route_files(self):
        """Rota dosyalarını yükler ve işler."""
        try:
            # Rotalar klasörünü ayarla
            self.multi_processor.routes_folder = "routes"
            
            # Rotaları yükle
            self.multi_processor.load_route_files()
            
            # Ham koordinatları birleştir
            raw_content = []
            
            # G-Code başlangıç parametreleri
            raw_content.extend(self.processor.start_params)
            
            # Her rotayı işle
            for index, route_file in enumerate(self.multi_processor.route_files, 1):
                with open(route_file, 'r') as file:
                    content = file.read()
                    
                    # Rota başlığını ekle
                    raw_content.append(f"% Rota No {index}")
                    
                    # Koordinatları ayıkla ve ekle
                    for line in content.strip().split('\n'):
                        if line.strip().startswith('X') and ' Y' in line:
                            # Koordinatları kalibre et
                            calibrated_content = self.processor.load_file_content(line)
                            raw_content.append(calibrated_content)
            
            # İçeriği kaydet
            self.content = '\n'.join(raw_content)
            return self.content
            
        except Exception as e:
            raise Exception(f"Dosya yüklenirken hata oluştu: {str(e)}")
    
    def process_gcode(self):
        """G-CODE içeriğini işler."""
        try:
            # MultiRouteProcessor'a güncel parametreleri aktar
            self.multi_processor.processor.start_params = self.processor.start_params
            self.multi_processor.processor.route_start_params = self.processor.route_start_params
            self.multi_processor.processor.thread_cut_params = self.processor.thread_cut_params
            self.multi_processor.processor.end_params = self.processor.end_params
            self.multi_processor.processor.z_positions = self.processor.z_positions
            self.multi_processor.processor.calibration_values = self.processor.calibration_values
            self.multi_processor.processor.bobbin_enabled = self.processor.bobbin_enabled
            self.multi_processor.processor.bobbin_reset_value = self.processor.bobbin_reset_value
            self.multi_processor.processor.punteriz_enabled = self.processor.punteriz_enabled
            self.multi_processor.processor.punteriz_start = self.processor.punteriz_start
            self.multi_processor.processor.punteriz_end = self.processor.punteriz_end
            self.multi_processor.processor.start_speed = self.processor.start_speed
            self.multi_processor.processor.max_speed = self.processor.max_speed
            self.multi_processor.processor.speed_increment = self.processor.speed_increment
            self.multi_processor.processor.current_speed = None  # Hız takibi için değişkeni sıfırla
            
            # Rotaları işle
            final_content = self.multi_processor.process_routes()
            self.content = final_content
            return final_content
            
        except Exception as e:
            raise Exception(f"İşlem sırasında hata oluştu: {str(e)}")
    
    def save_gcode(self, content):
        """G-CODE içeriğini dosyaya kaydeder."""
        try:
            # Şu anki tarihi al ve formatla
            current_time = datetime.now()
            filename = current_time.strftime("%y_%m_%d_%H_%M_%S.nc")
            
            # gcode_output klasörünü kontrol et ve yoksa oluştur
            gcode_dir = "gcode_output"
            if not os.path.exists(gcode_dir):
                os.makedirs(gcode_dir)
            
            # Tam dosya yolunu oluştur
            filepath = os.path.join(gcode_dir, filename)
            
            # İçeriği kaydet
            with open(filepath, 'w') as file:
                file.write(content)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"Dosya kaydedilirken hata oluştu: {str(e)}") 