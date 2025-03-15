import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QTextEdit, QCheckBox, QFrame, QScrollArea, 
                            QPushButton, QFileDialog, QMessageBox, QGroupBox, QSplitter)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
import qdarkstyle
from gcode_processor import GCodeProcessor
from multi_route_processor import MultiRouteProcessor

class GCodeEditorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.processor = GCodeProcessor()
        self.init_ui()
        self.load_default_parameters()
        
    def init_ui(self):
        # Ana pencere ayarları
        self.setWindowTitle("G-CODE Editor Application")
        self.setWindowIcon(QIcon("../icon.ico"))
        self.setGeometry(100, 100, 1200, 800)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter oluştur (sol ve sağ panel arasında)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Sol panel (parametreler)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        # Sağ panel (G-Code içeriği)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        # Panelleri splitter'a ekle
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 800])  # Sol panel daha dar, sağ panel daha geniş
        
        # Sol panel içeriğini oluştur
        self.create_parameter_inputs(left_layout)
        
        # Sağ panel içeriğini oluştur
        self.create_right_panel(right_layout)
        
        # Alt butonlar için layout
        bottom_layout = QHBoxLayout()
        left_layout.addLayout(bottom_layout)
        
        # Butonları oluştur
        self.create_action_buttons(bottom_layout)
        
        # Stil ayarları
        self.apply_styles()
        
    def apply_styles(self):
        # Buton stilleri
        button_style = """
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """
        
        # GroupBox stilleri
        group_style = """
            QGroupBox {
                font-weight: bold;
                border: 1px solid #76797C;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """
        
        # Stilleri uygula
        for widget in self.findChildren(QPushButton):
            widget.setStyleSheet(button_style)
            widget.setMinimumHeight(40)
            
        for widget in self.findChildren(QGroupBox):
            widget.setStyleSheet(group_style)
    
    def create_parameter_inputs(self, layout):
        # Parametreler için scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        scroll_layout.setSpacing(15)
        
        # G-Code Başlangıç Parametreleri
        start_group = QGroupBox("G-Code Başlangıç Parametreleri")
        start_layout = QVBoxLayout(start_group)
        self.start_params_text = QTextEdit()
        self.start_params_text.setMinimumHeight(80)
        start_layout.addWidget(self.start_params_text)
        scroll_layout.addWidget(start_group)
        
        # Rota Başlangıç Parametreleri
        route_start_group = QGroupBox("Rota Başlangıç Parametreleri")
        route_start_layout = QVBoxLayout(route_start_group)
        self.route_start_params_text = QTextEdit()
        self.route_start_params_text.setMinimumHeight(80)
        route_start_layout.addWidget(self.route_start_params_text)
        scroll_layout.addWidget(route_start_group)
        
        # İp Kesme Parametreleri
        thread_cut_group = QGroupBox("İp Kesme Parametreleri")
        thread_cut_layout = QVBoxLayout(thread_cut_group)
        self.thread_cut_params_text = QTextEdit()
        self.thread_cut_params_text.setMinimumHeight(60)
        thread_cut_layout.addWidget(self.thread_cut_params_text)
        scroll_layout.addWidget(thread_cut_group)
        
        # G-Code Sonu Parametreleri
        end_group = QGroupBox("G-Code Sonu Parametreleri")
        end_layout = QVBoxLayout(end_group)
        self.end_params_text = QTextEdit()
        self.end_params_text.setMinimumHeight(80)
        end_layout.addWidget(self.end_params_text)
        scroll_layout.addWidget(end_group)
        
        # Punteriz
        punteriz_group = QGroupBox("Punteriz")
        punteriz_layout = QVBoxLayout(punteriz_group)
        punteriz_controls = QHBoxLayout()
        
        self.punteriz_enabled = QCheckBox("Aktif")
        self.punteriz_enabled.stateChanged.connect(self.toggle_punteriz_input)
        punteriz_controls.addWidget(self.punteriz_enabled)
        
        punteriz_controls.addWidget(QLabel("Dikiş Başı:"))
        self.punteriz_start = QLineEdit("0")
        self.punteriz_start.setEnabled(False)
        self.punteriz_start.setMaximumWidth(80)
        punteriz_controls.addWidget(self.punteriz_start)
        
        punteriz_controls.addWidget(QLabel("Dikiş Sonu:"))
        self.punteriz_end = QLineEdit("0")
        self.punteriz_end.setEnabled(False)
        self.punteriz_end.setMaximumWidth(80)
        punteriz_controls.addWidget(self.punteriz_end)
        
        punteriz_controls.addStretch()
        punteriz_layout.addLayout(punteriz_controls)
        scroll_layout.addWidget(punteriz_group)
        
        # Ayırıcı çizgi
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        scroll_layout.addWidget(line)
        
        # İğne pozisyonları
        needle_group = QGroupBox("İğne Batma ve Geri Çekilme Pozisyonları")
        needle_layout = QVBoxLayout(needle_group)
        needle_controls = QHBoxLayout()
        
        needle_controls.addWidget(QLabel("Batma:"))
        self.needle_down_pos = QLineEdit()
        self.needle_down_pos.setMaximumWidth(100)
        needle_controls.addWidget(self.needle_down_pos)
        
        needle_controls.addWidget(QLabel("Geri Çekilme:"))
        self.needle_up_pos = QLineEdit()
        self.needle_up_pos.setMaximumWidth(100)
        needle_controls.addWidget(self.needle_up_pos)
        
        needle_controls.addStretch()
        needle_layout.addLayout(needle_controls)
        scroll_layout.addWidget(needle_group)
        
        # Dikiş Hızı Kontrolü
        speed_group = QGroupBox("Dikiş Hızı Kontrolü")
        speed_layout = QVBoxLayout(speed_group)
        
        speed_start_layout = QHBoxLayout()
        speed_start_layout.addWidget(QLabel("Başlangıç Hızı (F):"))
        self.start_speed = QLineEdit("10000")
        self.start_speed.setMaximumWidth(100)
        speed_start_layout.addWidget(self.start_speed)
        speed_start_layout.addStretch()
        speed_layout.addLayout(speed_start_layout)
        
        speed_max_layout = QHBoxLayout()
        speed_max_layout.addWidget(QLabel("Maksimum Hız (F):"))
        self.max_speed = QLineEdit("50000")
        self.max_speed.setMaximumWidth(100)
        speed_max_layout.addWidget(self.max_speed)
        speed_max_layout.addStretch()
        speed_layout.addLayout(speed_max_layout)
        
        speed_inc_layout = QHBoxLayout()
        speed_inc_layout.addWidget(QLabel("Artış Hızı (F):"))
        self.speed_increment = QLineEdit("5000")
        self.speed_increment.setMaximumWidth(100)
        speed_inc_layout.addWidget(self.speed_increment)
        speed_inc_layout.addStretch()
        speed_layout.addLayout(speed_inc_layout)
        
        scroll_layout.addWidget(speed_group)
        
        # Üst İp Sıkma Bobini
        bobbin_group = QGroupBox("Üst İp Sıkma Bobini (M118-M119)")
        bobbin_layout = QVBoxLayout(bobbin_group)
        bobbin_controls = QHBoxLayout()
        
        self.bobbin_enabled = QCheckBox("Aktif")
        self.bobbin_enabled.stateChanged.connect(self.toggle_bobbin_input)
        bobbin_controls.addWidget(self.bobbin_enabled)
        
        bobbin_controls.addWidget(QLabel("Kaç Satır Sonra Resetlensin:"))
        self.bobbin_reset_value = QLineEdit("1")
        self.bobbin_reset_value.setEnabled(False)
        self.bobbin_reset_value.setMaximumWidth(80)
        bobbin_controls.addWidget(self.bobbin_reset_value)
        
        bobbin_controls.addStretch()
        bobbin_layout.addLayout(bobbin_controls)
        scroll_layout.addWidget(bobbin_group)
        
        # Makine Kalibrasyon Değerleri
        calibration_group = QGroupBox("Makine Kalibrasyon Değerleri")
        calibration_layout = QVBoxLayout(calibration_group)
        calibration_controls = QHBoxLayout()
        
        calibration_controls.addWidget(QLabel("X:"))
        self.calibration_x = QLineEdit()
        self.calibration_x.setMaximumWidth(120)
        calibration_controls.addWidget(self.calibration_x)
        
        calibration_controls.addWidget(QLabel("Y:"))
        self.calibration_y = QLineEdit()
        self.calibration_y.setMaximumWidth(120)
        calibration_controls.addWidget(self.calibration_y)
        
        calibration_controls.addStretch()
        calibration_layout.addLayout(calibration_controls)
        scroll_layout.addWidget(calibration_group)
        
        # Scroll area'yı tamamla
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
    
    def create_right_panel(self, layout):
        # G-Code içeriği için grup
        content_group = QGroupBox("G-Code İçeriği")
        content_layout = QVBoxLayout(content_group)
        
        # Text alanı
        self.text_area = QTextEdit()
        self.text_area.setLineWrapMode(QTextEdit.NoWrap)  # Satır kaydırma kapalı
        content_layout.addWidget(self.text_area)
        
        layout.addWidget(content_group)
    
    def create_action_buttons(self, layout):
        # G-Code Oluştur butonu
        generate_btn = QPushButton("G-Code Oluştur")
        generate_btn.setIcon(QIcon.fromTheme("document-new"))
        generate_btn.clicked.connect(self.update_parameters)
        layout.addWidget(generate_btn)
        
        # Parametreleri Sıfırla butonu
        reset_btn = QPushButton("Parametreleri Sıfırla")
        reset_btn.setIcon(QIcon.fromTheme("edit-clear"))
        reset_btn.clicked.connect(self.reset_parameters)
        layout.addWidget(reset_btn)
        
        # Dosya Yükle butonu
        load_btn = QPushButton("Dosya Yükle")
        load_btn.setIcon(QIcon.fromTheme("document-open"))
        load_btn.clicked.connect(self.load_file)
        layout.addWidget(load_btn)
        
        # Dosya Kaydet butonu
        save_btn = QPushButton("Dosya Kaydet")
        save_btn.setIcon(QIcon.fromTheme("document-save"))
        save_btn.clicked.connect(self.save_file)
        layout.addWidget(save_btn)
    
    def load_default_parameters(self):
        try:
            with open('../parameters.json', 'r') as file:
                params = json.load(file)
                
                # G-Code Başlangıç Parametreleri
                start_params = '\n'.join(params.get('start_params', []))
                self.start_params_text.setText(start_params)
                
                # Rota Başlangıç Parametreleri
                route_start_params = '\n'.join(params.get('route_start_params', []))
                self.route_start_params_text.setText(route_start_params)
                
                # İp Kesme Parametreleri
                thread_cut_params = '\n'.join(params.get('thread_cut_params', []))
                self.thread_cut_params_text.setText(thread_cut_params)
                
                # G-Code Sonu Parametreleri
                end_params = '\n'.join(params.get('end_params', []))
                self.end_params_text.setText(end_params)
                
                # Z pozisyonları
                z_positions = params.get('z_positions', {"needle_down": "Z3", "needle_up": "Z30"})
                self.needle_down_pos.setText(z_positions["needle_down"])
                self.needle_up_pos.setText(z_positions["needle_up"])
                
                # Makine Kalibrasyon Değerleri
                machine_calibration = params.get('machine_calibration', {"x_value": "21.57001", "y_value": "388.6"})
                self.calibration_x.setText(machine_calibration["x_value"])
                self.calibration_y.setText(machine_calibration["y_value"])
                
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Parametreler yüklenirken hata oluştu: {str(e)}")
    
    def update_parameters(self):
        try:
            # Kalibrasyon değerlerini al
            calibration_x = self.calibration_x.text().strip()
            calibration_y = self.calibration_y.text().strip()
            
            # Z pozisyonlarını al
            needle_down = self.needle_down_pos.text().strip()
            needle_up = self.needle_up_pos.text().strip()
            
            # Üst İp Sıkma Bobini ayarlarını al
            bobbin_enabled = self.bobbin_enabled.isChecked()
            bobbin_reset_value = self.bobbin_reset_value.text().strip() if bobbin_enabled else "1"
            
            # Punteriz ayarlarını al
            punteriz_enabled = self.punteriz_enabled.isChecked()
            punteriz_start = self.punteriz_start.text().strip() if punteriz_enabled else "0"
            punteriz_end = self.punteriz_end.text().strip() if punteriz_enabled else "0"
            
            # Diğer parametreleri güncelle
            self.processor.start_params = self.start_params_text.toPlainText().strip().split('\n')
            self.processor.route_start_params = self.route_start_params_text.toPlainText().strip().split('\n')
            self.processor.thread_cut_params = self.thread_cut_params_text.toPlainText().strip().split('\n')
            self.processor.end_params = self.end_params_text.toPlainText().strip().split('\n')
            
            # Kalibrasyon, Z değerleri ve Bobini ayarlarını güncelle
            self.processor.update_calibration_values(calibration_x, calibration_y)
            self.processor.update_z_positions(needle_down, needle_up)
            self.processor.update_bobbin_settings(bobbin_enabled, bobbin_reset_value)
            
            # Punteriz ayarlarını güncelle
            self.processor.update_punteriz_settings(punteriz_enabled, punteriz_start, punteriz_end)
            
            # Hız ayarlarını al ve doğrula
            start_speed = self.start_speed.text().strip()
            max_speed = self.max_speed.text().strip()
            speed_increment = self.speed_increment.text().strip()
            
            # Hız ayarlarını güncelle
            self.processor.update_speed_settings(start_speed, max_speed, speed_increment)
            
            # Mevcut içeriği kontrol et
            content = self.text_area.toPlainText().strip()
            if not content:
                QMessageBox.warning(self, "Uyarı", "İşlenecek G-Code içeriği bulunamadı. Lütfen önce bir dosya yükleyin.")
                return
            
            # İçeriği işle
            self.process_file()
            QMessageBox.information(self, "Başarılı", "G-Code oluşturuldu.")
                
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İşlem sırasında hata oluştu: {str(e)}")
    
    def load_file(self):
        try:
            # MultiRouteProcessor'ı başlat
            multi_processor = MultiRouteProcessor()
            
            # Rotaları yükle
            multi_processor.load_route_files()
            
            # Ham koordinatları birleştir
            raw_content = []
            
            # G-Code başlangıç parametreleri
            raw_content.extend(self.processor.start_params)
            
            # Her rotayı işle
            for index, route_file in enumerate(multi_processor.route_files, 1):
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
            
            # İçeriği text alanına yükle
            self.text_area.setText('\n'.join(raw_content))
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya yüklenirken hata oluştu: {str(e)}")
    
    def save_file(self):
        try:
            # Şu anki tarihi al ve formatla
            from datetime import datetime
            current_time = datetime.now()
            filename = current_time.strftime("%y_%m_%d_%H_%M_%S.nc")
            
            # gcode klasörünü kontrol et ve yoksa oluştur
            import os
            gcode_dir = "../gcode"
            if not os.path.exists(gcode_dir):
                os.makedirs(gcode_dir)
            
            # Tam dosya yolunu oluştur
            filepath = os.path.join(gcode_dir, filename)
            
            # İçeriği kaydet
            content = self.text_area.toPlainText()
            with open(filepath, 'w') as file:
                file.write(content)
            QMessageBox.information(self, "Başarılı", f"Dosya başarıyla kaydedildi:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya kaydedilirken hata oluştu: {str(e)}")
    
    def process_file(self):
        try:
            # Text alanındaki içeriği al
            content = self.text_area.toPlainText()
            
            # MultiRouteProcessor'ı başlat
            multi_processor = MultiRouteProcessor()
            
            # Processor'a güncel parametreleri aktar
            multi_processor.processor.start_params = self.processor.start_params
            multi_processor.processor.route_start_params = self.processor.route_start_params
            multi_processor.processor.thread_cut_params = self.processor.thread_cut_params
            multi_processor.processor.end_params = self.processor.end_params
            multi_processor.processor.z_positions = self.processor.z_positions
            multi_processor.processor.calibration_values = self.processor.calibration_values
            multi_processor.processor.bobbin_enabled = self.processor.bobbin_enabled
            multi_processor.processor.bobbin_reset_value = self.processor.bobbin_reset_value
            multi_processor.processor.punteriz_enabled = self.processor.punteriz_enabled
            multi_processor.processor.punteriz_start = self.processor.punteriz_start
            multi_processor.processor.punteriz_end = self.processor.punteriz_end
            multi_processor.processor.start_speed = self.processor.start_speed
            multi_processor.processor.max_speed = self.processor.max_speed
            multi_processor.processor.speed_increment = self.processor.speed_increment
            
            # Rotaları işle
            final_content = multi_processor.process_routes()
            
            # Text alanını temizle ve yeni içeriği ekle
            self.text_area.setText(final_content)
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İşlem sırasında hata oluştu: {str(e)}")
    
    def reset_parameters(self):
        """Tüm parametreleri varsayılan değerlerine sıfırla"""
        try:
            # parameters.json dosyasından varsayılan değerleri yükle
            with open('../parameters.json', 'r') as file:
                params = json.load(file)
                
                # G-Code Başlangıç Parametreleri
                start_params = '\n'.join(params.get('start_params', []))
                self.start_params_text.setText(start_params)
                
                # Rota Başlangıç Parametreleri
                route_start_params = '\n'.join(params.get('route_start_params', []))
                self.route_start_params_text.setText(route_start_params)
                
                # İp Kesme Parametreleri
                thread_cut_params = '\n'.join(params.get('thread_cut_params', []))
                self.thread_cut_params_text.setText(thread_cut_params)
                
                # G-Code Sonu Parametreleri
                end_params = '\n'.join(params.get('end_params', []))
                self.end_params_text.setText(end_params)
                
                # Z pozisyonları
                z_positions = params.get('z_positions', {"needle_down": "Z3", "needle_up": "Z30"})
                self.needle_down_pos.setText(z_positions["needle_down"])
                self.needle_up_pos.setText(z_positions["needle_up"])
                
                # Makine Kalibrasyon Değerleri
                machine_calibration = params.get('machine_calibration', {"x_value": "21.57001", "y_value": "388.6"})
                self.calibration_x.setText(machine_calibration["x_value"])
                self.calibration_y.setText(machine_calibration["y_value"])
                
                # Hız Ayarları
                self.start_speed.setText("10000")
                self.max_speed.setText("50000")
                self.speed_increment.setText("5000")
                
                # Punteriz Ayarları
                self.punteriz_enabled.setChecked(False)
                self.punteriz_start.setEnabled(False)
                self.punteriz_end.setEnabled(False)
                self.punteriz_start.setText("0")
                self.punteriz_end.setText("0")
                
                # Üst İp Sıkma Bobini Ayarları
                self.bobbin_enabled.setChecked(False)
                self.bobbin_reset_value.setEnabled(False)
                self.bobbin_reset_value.setText("1")
                
                QMessageBox.information(self, "Başarılı", "Parametreler varsayılan değerlere sıfırlandı.")
                
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Parametreler sıfırlanırken hata oluştu: {str(e)}")
    
    def toggle_bobbin_input(self):
        """Checkbox durumuna göre input alanını etkinleştir/devre dışı bırak"""
        self.bobbin_reset_value.setEnabled(self.bobbin_enabled.isChecked())
        if self.bobbin_enabled.isChecked() and not self.bobbin_reset_value.text().strip():
            self.bobbin_reset_value.setText("1")
    
    def toggle_punteriz_input(self):
        """Checkbox durumuna göre input alanlarını etkinleştir/devre dışı bırak"""
        self.punteriz_start.setEnabled(self.punteriz_enabled.isChecked())
        self.punteriz_end.setEnabled(self.punteriz_enabled.isChecked())
        
        if self.punteriz_enabled.isChecked():
            if not self.punteriz_start.text().strip():
                self.punteriz_start.setText("1")
            if not self.punteriz_end.text().strip():
                self.punteriz_end.setText("1")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Koyu tema uygula
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    # Uygulama fontunu ayarla
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = GCodeEditorGUI()
    window.show()
    sys.exit(app.exec_()) 