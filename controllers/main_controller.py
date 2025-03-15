from models.gcode_model import GCodeModel
from views.main_view import MainView
from utils.language import LanguageManager

class MainController:
    """
    G-CODE Editor uygulamasının ana controller sınıfı.
    Model ve View arasındaki iletişimi sağlar.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # View olaylarını bağla
        self.connect_signals()
        
        # Varsayılan parametreleri yükle
        self.load_default_parameters()
        
    def connect_signals(self):
        """View'daki butonları controller fonksiyonlarına bağlar."""
        self.view.generate_btn.clicked.connect(self.update_parameters)
        self.view.reset_btn.clicked.connect(self.reset_parameters)
        self.view.load_btn.clicked.connect(self.load_file)
        self.view.save_btn.clicked.connect(self.save_file)
        
        # Checkbox olaylarını bağla
        self.view.punteriz_enabled.stateChanged.connect(self.toggle_punteriz_input)
        self.view.bobbin_enabled.stateChanged.connect(self.toggle_bobbin_input)
    
    def load_default_parameters(self):
        """Varsayılan parametreleri yükler."""
        try:
            params = self.model.load_default_parameters()
            self.view.set_parameters(params)
        except Exception as e:
            self.view.show_error(str(e))
    
    def update_parameters(self):
        """Parametreleri günceller ve G-CODE'u işler."""
        try:
            # Arayüzdeki parametreleri al
            params = self.view.get_parameters()
            
            # Model'i güncelle
            self.model.update_processor_parameters(params)
            
            # Mevcut içeriği kontrol et
            content = self.view.get_gcode_content()
            if not content:
                self.view.show_warning(LanguageManager.get_text('msg_no_content', self.view.current_language))
                return
            
            # İçeriği işle
            processed_content = self.model.process_gcode()
            
            # İşlenmiş içeriği görüntüle
            self.view.set_gcode_content(processed_content)
            
            self.view.show_info(LanguageManager.get_text('msg_gcode_generated', self.view.current_language))
                
        except Exception as e:
            self.view.show_error(f"{str(e)}")
    
    def load_file(self):
        """Rota dosyalarını yükler."""
        try:
            # Dosyaları yükle ve işle
            content = self.model.load_route_files()
            
            # İçeriği görüntüle
            self.view.set_gcode_content(content)
            
            self.view.show_info(LanguageManager.get_text('msg_file_loaded', self.view.current_language))
            
        except Exception as e:
            self.view.show_error(f"{str(e)}")
    
    def save_file(self):
        """G-CODE içeriğini dosyaya kaydeder."""
        try:
            # Mevcut içeriği al
            content = self.view.get_gcode_content()
            
            if not content.strip():
                self.view.show_warning(LanguageManager.get_text('msg_no_content_save', self.view.current_language))
                return
            
            # İçeriği kaydet
            filepath = self.model.save_gcode(content)
            
            # Başarı mesajı göster
            self.view.show_info(LanguageManager.get_text('msg_file_saved', self.view.current_language).format(filepath))
            
        except Exception as e:
            self.view.show_error(f"{str(e)}")
    
    def reset_parameters(self):
        """Tüm parametreleri varsayılan değerlerine sıfırlar."""
        try:
            # Varsayılan parametreleri yükle
            self.load_default_parameters()
            
            # Başarı mesajı göster
            self.view.show_info(LanguageManager.get_text('msg_parameters_reset', self.view.current_language))
            
        except Exception as e:
            self.view.show_error(f"{str(e)}")
    
    def toggle_bobbin_input(self):
        """Checkbox durumuna göre input alanını etkinleştir/devre dışı bırak"""
        self.view.bobbin_reset_value.setEnabled(self.view.bobbin_enabled.isChecked())
        if self.view.bobbin_enabled.isChecked() and not self.view.bobbin_reset_value.text().strip():
            self.view.bobbin_reset_value.setText("1")
    
    def toggle_punteriz_input(self):
        """Checkbox durumuna göre input alanlarını etkinleştir/devre dışı bırak"""
        self.view.punteriz_start.setEnabled(self.view.punteriz_enabled.isChecked())
        self.view.punteriz_end.setEnabled(self.view.punteriz_enabled.isChecked())
        
        if self.view.punteriz_enabled.isChecked():
            if not self.view.punteriz_start.text().strip():
                self.view.punteriz_start.setText("1")
            if not self.view.punteriz_end.text().strip():
                self.view.punteriz_end.setText("1") 