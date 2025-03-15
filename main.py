import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from models.gcode_model import GCodeModel
from views.main_view import MainView
from controllers.main_controller import MainController
from utils.styles import StyleManager

def main():
    """Ana uygulama fonksiyonu."""
    # QApplication oluştur
    app = QApplication(sys.argv)
    
    # Stil yöneticisini kullanarak tüm stilleri uygula
    app = StyleManager.apply_application_style(app)
    
    # Uygulama fontunu ayarla
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Gerekli klasörlerin varlığını kontrol et
    check_required_directories()
    
    # MVC bileşenlerini oluştur
    model = GCodeModel()
    view = MainView()
    controller = MainController(model, view)
    
    # Uygulamayı tam ekran göster
    view.showMaximized()
    
    # Uygulama döngüsünü başlat
    sys.exit(app.exec_())

def check_required_directories():
    """Gerekli klasörlerin varlığını kontrol eder ve yoksa oluşturur."""
    # Rotalar klasörü
    routes_dir = "routes"
    if not os.path.exists(routes_dir):
        os.makedirs(routes_dir)
        print(f"'{routes_dir}' klasörü oluşturuldu.")
    
    # G-Code çıktı klasörü
    gcode_output_dir = "gcode_output"
    if not os.path.exists(gcode_output_dir):
        os.makedirs(gcode_output_dir)
        print(f"'{gcode_output_dir}' klasörü oluşturuldu.")

if __name__ == "__main__":
    main() 