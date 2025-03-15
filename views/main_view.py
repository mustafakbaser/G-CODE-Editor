import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QTextEdit, QCheckBox, QFrame, QScrollArea, 
                            QPushButton, QFileDialog, QMessageBox, QGroupBox, QSplitter, QGridLayout, QAction, QActionGroup)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from utils.styles import StyleManager
from utils.language import LanguageManager

class MainView(QMainWindow):
    """
    G-CODE Editor uygulamasının ana görünüm sınıfı.
    """
    def __init__(self):
        super().__init__()
        self.current_language = 'tr'  # Varsayılan dil
        self.init_ui()
        
    def init_ui(self):
        """Ana kullanıcı arayüzünü oluşturur."""
        # Ana pencere ayarları
        self.setWindowTitle("G-CODE Editor Application")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setGeometry(100, 100, 1200, 800)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Splitter oluştur (sol ve sağ panel arasında)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Sol panel (parametreler)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(15)
        
        # Başlık etiketi - Sol Panel
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            background-color: white;
            border-bottom: 2px solid #1976D2;
        """)
        title_frame.setMinimumHeight(50)
        title_frame.setMaximumHeight(50)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(15, 5, 15, 5)
        
        self.title_label = QLabel(LanguageManager.get_text('title_parameters', self.current_language))
        self.title_label.setStyleSheet("""
            font-size: 14pt; 
            font-weight: bold; 
            color: #1976D2;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.title_label)
        
        left_layout.addWidget(title_frame)
        
        # Sağ panel (G-Code içeriği)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(15)
        
        # Başlık etiketi - Sağ Panel
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            background-color: white;
            border-bottom: 2px solid #1976D2;
        """)
        content_frame.setMinimumHeight(50)
        content_frame.setMaximumHeight(50)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(15, 5, 15, 5)
        
        self.content_title = QLabel(LanguageManager.get_text('title_output', self.current_language))
        self.content_title.setStyleSheet("""
            font-size: 14pt; 
            font-weight: bold; 
            color: #1976D2;
        """)
        self.content_title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.content_title)
        
        right_layout.addWidget(content_frame)
        
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
        
        # Menü oluştur
        self.create_menu()
        
        # Stil ayarları
        self.apply_styles()
        
    def create_menu(self):
        """Menü çubuğunu oluşturur."""
        menubar = self.menuBar()
        
        # Dosya menüsü
        self.file_menu = menubar.addMenu(LanguageManager.get_text('menu_file', self.current_language))
        
        # Dosya Yükle
        self.load_action = QAction(LanguageManager.get_text('menu_load_file', self.current_language), self)
        self.load_action.setShortcut('Ctrl+O')
        self.load_action.triggered.connect(self.load_btn.click)
        self.file_menu.addAction(self.load_action)
        
        # Dosya Kaydet
        self.save_action = QAction(LanguageManager.get_text('menu_save_file', self.current_language), self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.save_btn.click)
        self.file_menu.addAction(self.save_action)
        
        self.file_menu.addSeparator()
        
        # Çıkış
        self.exit_action = QAction(LanguageManager.get_text('menu_exit', self.current_language), self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)
        
        # Düzen menüsü
        self.edit_menu = menubar.addMenu(LanguageManager.get_text('menu_edit', self.current_language))
        
        # G-Code Oluştur
        self.generate_action = QAction(LanguageManager.get_text('menu_generate_gcode', self.current_language), self)
        self.generate_action.setShortcut('F5')
        self.generate_action.triggered.connect(self.generate_btn.click)
        self.edit_menu.addAction(self.generate_action)
        
        # Parametreleri Sıfırla
        self.reset_action = QAction(LanguageManager.get_text('menu_reset_parameters', self.current_language), self)
        self.reset_action.setShortcut('Ctrl+R')
        self.reset_action.triggered.connect(self.reset_btn.click)
        self.edit_menu.addAction(self.reset_action)
        
        # Dil menüsü
        self.language_menu = menubar.addMenu(LanguageManager.get_text('menu_language', self.current_language))
        
        # Türkçe
        self.tr_action = QAction('Türkçe', self)
        self.tr_action.setCheckable(True)
        self.tr_action.setChecked(self.current_language == 'tr')
        self.tr_action.triggered.connect(lambda: self.change_language('tr'))
        self.language_menu.addAction(self.tr_action)
        
        # İngilizce
        self.en_action = QAction('English', self)
        self.en_action.setCheckable(True)
        self.en_action.setChecked(self.current_language == 'en')
        self.en_action.triggered.connect(lambda: self.change_language('en'))
        self.language_menu.addAction(self.en_action)
        
        # Dil aksiyonlarını bir gruba ekle
        self.language_action_group = QActionGroup(self)
        self.language_action_group.addAction(self.tr_action)
        self.language_action_group.addAction(self.en_action)
        self.language_action_group.setExclusive(True)
        
        # Yardım menüsü
        self.help_menu = menubar.addMenu(LanguageManager.get_text('menu_help', self.current_language))
        
        # Hakkında
        self.about_action = QAction(LanguageManager.get_text('menu_about', self.current_language), self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)
    
    def change_language(self, lang_code):
        """Uygulamanın dilini değiştirir."""
        if self.current_language == lang_code:
            return
            
        self.current_language = lang_code
        
        # Başlıkları güncelle
        self.title_label.setText(LanguageManager.get_text('title_parameters', self.current_language))
        self.content_title.setText(LanguageManager.get_text('title_output', self.current_language))
        
        # Menüleri güncelle
        self.file_menu.setTitle(LanguageManager.get_text('menu_file', self.current_language))
        self.load_action.setText(LanguageManager.get_text('menu_load_file', self.current_language))
        self.save_action.setText(LanguageManager.get_text('menu_save_file', self.current_language))
        self.exit_action.setText(LanguageManager.get_text('menu_exit', self.current_language))
        
        self.edit_menu.setTitle(LanguageManager.get_text('menu_edit', self.current_language))
        self.generate_action.setText(LanguageManager.get_text('menu_generate_gcode', self.current_language))
        self.reset_action.setText(LanguageManager.get_text('menu_reset_parameters', self.current_language))
        
        self.language_menu.setTitle(LanguageManager.get_text('menu_language', self.current_language))
        
        self.help_menu.setTitle(LanguageManager.get_text('menu_help', self.current_language))
        self.about_action.setText(LanguageManager.get_text('menu_about', self.current_language))
        
        # Grup başlıklarını güncelle
        for widget in self.findChildren(QGroupBox):
            if widget.title() == "G-Code Başlangıç Parametreleri" or widget.title() == "G-Code Start Parameters":
                widget.setTitle(LanguageManager.get_text('group_start_params', self.current_language))
            elif widget.title() == "Rota Başlangıç Parametreleri" or widget.title() == "Route Start Parameters":
                widget.setTitle(LanguageManager.get_text('group_route_start_params', self.current_language))
            elif widget.title() == "İp Kesme Parametreleri" or widget.title() == "Thread Cut Parameters":
                widget.setTitle(LanguageManager.get_text('group_thread_cut_params', self.current_language))
            elif widget.title() == "G-Code Sonu Parametreleri" or widget.title() == "G-Code End Parameters":
                widget.setTitle(LanguageManager.get_text('group_end_params', self.current_language))
            elif widget.title() == "Punteriz":
                widget.setTitle(LanguageManager.get_text('group_punteriz', self.current_language))
            elif widget.title() == "İğne Batma ve Geri Çekilme Pozisyonları" or widget.title() == "Needle Down and Up Positions":
                widget.setTitle(LanguageManager.get_text('group_needle_positions', self.current_language))
            elif widget.title() == "Dikiş Hızı Kontrolü" or widget.title() == "Sewing Speed Control":
                widget.setTitle(LanguageManager.get_text('group_speed_control', self.current_language))
            elif widget.title() == "Üst İp Sıkma Bobini (M118-M119)" or widget.title() == "Upper Thread Tightening Bobbin (M118-M119)":
                widget.setTitle(LanguageManager.get_text('group_bobbin', self.current_language))
            elif widget.title() == "Makine Kalibrasyon Değerleri" or widget.title() == "Machine Calibration Values":
                widget.setTitle(LanguageManager.get_text('group_calibration', self.current_language))
            elif widget.title() == "G-Code İçeriği" or widget.title() == "G-Code Content":
                widget.setTitle(LanguageManager.get_text('group_gcode_content', self.current_language))
        
        # Butonları güncelle
        self.generate_btn.setText(LanguageManager.get_text('button_generate', self.current_language))
        self.reset_btn.setText(LanguageManager.get_text('button_reset', self.current_language))
        self.load_btn.setText(LanguageManager.get_text('button_load', self.current_language))
        self.save_btn.setText(LanguageManager.get_text('button_save', self.current_language))
        
        # Etiketleri güncelle
        for widget in self.findChildren(QLabel):
            if widget.text() == "Dikiş Başı:" or widget.text() == "Stitch Start:":
                widget.setText(LanguageManager.get_text('label_stitch_start', self.current_language))
            elif widget.text() == "Dikiş Sonu:" or widget.text() == "Stitch End:":
                widget.setText(LanguageManager.get_text('label_stitch_end', self.current_language))
            elif widget.text() == "Batma:" or widget.text() == "Down:":
                widget.setText(LanguageManager.get_text('label_needle_down', self.current_language))
            elif widget.text() == "Geri Çekilme:" or widget.text() == "Up:":
                widget.setText(LanguageManager.get_text('label_needle_up', self.current_language))
            elif widget.text() == "Başlangıç Hızı (F):" or widget.text() == "Start Speed (F):":
                widget.setText(LanguageManager.get_text('label_start_speed', self.current_language))
            elif widget.text() == "Maksimum Hız (F):" or widget.text() == "Maximum Speed (F):":
                widget.setText(LanguageManager.get_text('label_max_speed', self.current_language))
            elif widget.text() == "Artış Hızı (F):" or widget.text() == "Speed Increment (F):":
                widget.setText(LanguageManager.get_text('label_speed_increment', self.current_language))
            elif widget.text() == "Kaç Satır Sonra Resetlensin:" or widget.text() == "Reset After Lines:":
                widget.setText(LanguageManager.get_text('label_bobbin_reset', self.current_language))
            elif widget.text() == "Hazır" or widget.text() == "Ready":
                widget.setText(LanguageManager.get_text('label_ready', self.current_language))
            elif widget.text() == "Düzenleniyor" or widget.text() == "Editing":
                widget.setText(LanguageManager.get_text('label_editing', self.current_language))
            elif widget.text().startswith("Satır:") or widget.text().startswith("Lines:"):
                widget.setText(f"{LanguageManager.get_text('label_lines', self.current_language)} {self.text_area.document().lineCount()}")
        
        # Checkbox'ları güncelle
        for widget in self.findChildren(QCheckBox):
            if widget.text() == "Aktif" or widget.text() == "Active":
                widget.setText(LanguageManager.get_text('label_active', self.current_language))
        
        # Kullanıcıya bilgi ver
        QMessageBox.information(
            self, 
            LanguageManager.get_text('msg_language_changed', self.current_language),
            LanguageManager.get_text('msg_language_changed_text', self.current_language).format(
                "Türkçe" if lang_code == 'tr' else "English"
            )
        )
    
    def show_about(self):
        """Hakkında dialogunu gösterir."""
        QMessageBox.about(
            self, 
            LanguageManager.get_text('msg_about_title', self.current_language),
            LanguageManager.get_text('msg_about_text', self.current_language)
        )
        
    def apply_styles(self):
        """Arayüz stillerini uygular."""
        # Butonlar için stil
        for widget in self.findChildren(QPushButton):
            widget.setStyleSheet(StyleManager.get_button_style())
            widget.setMinimumHeight(40)
            
        # GroupBox için stil
        for widget in self.findChildren(QGroupBox):
            widget.setStyleSheet(StyleManager.get_group_style())
            
        # QTextEdit için stil
        for widget in self.findChildren(QTextEdit):
            widget.setStyleSheet(StyleManager.get_text_edit_style())
            
        # QLineEdit için stil
        for widget in self.findChildren(QLineEdit):
            widget.setStyleSheet(StyleManager.get_line_edit_style())
            
        # QCheckBox için stil
        for widget in self.findChildren(QCheckBox):
            widget.setStyleSheet(StyleManager.get_checkbox_style())
            
        # QScrollBar için stil
        self.setStyleSheet(StyleManager.get_scroll_bar_style())
            
        # QLabel için stil
        for widget in self.findChildren(QLabel):
            widget.setStyleSheet(StyleManager.get_label_style())
            
        # QSplitter için stil
        for widget in self.findChildren(QSplitter):
            widget.setStyleSheet(StyleManager.get_splitter_style())
    
    def create_parameter_inputs(self, layout):
        """Sol paneldeki parametre giriş alanlarını oluşturur."""
        # Parametreler için scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        scroll_layout.setSpacing(15)
        
        # G-Code Başlangıç Parametreleri
        start_group = QGroupBox(LanguageManager.get_text('group_start_params', self.current_language))
        start_layout = QVBoxLayout(start_group)
        start_layout.setContentsMargins(10, 15, 10, 10)
        self.start_params_text = QTextEdit()
        self.start_params_text.setMinimumHeight(100)
        start_layout.addWidget(self.start_params_text)
        scroll_layout.addWidget(start_group)
        
        # Rota Başlangıç Parametreleri
        route_start_group = QGroupBox(LanguageManager.get_text('group_route_start_params', self.current_language))
        route_start_layout = QVBoxLayout(route_start_group)
        route_start_layout.setContentsMargins(10, 15, 10, 10)
        self.route_start_params_text = QTextEdit()
        self.route_start_params_text.setMinimumHeight(100)
        route_start_layout.addWidget(self.route_start_params_text)
        scroll_layout.addWidget(route_start_group)
        
        # İp Kesme Parametreleri
        thread_cut_group = QGroupBox(LanguageManager.get_text('group_thread_cut_params', self.current_language))
        thread_cut_layout = QVBoxLayout(thread_cut_group)
        thread_cut_layout.setContentsMargins(10, 15, 10, 10)
        self.thread_cut_params_text = QTextEdit()
        self.thread_cut_params_text.setMinimumHeight(100)
        thread_cut_layout.addWidget(self.thread_cut_params_text)
        scroll_layout.addWidget(thread_cut_group)
        
        # G-Code Sonu Parametreleri
        end_group = QGroupBox(LanguageManager.get_text('group_end_params', self.current_language))
        end_layout = QVBoxLayout(end_group)
        end_layout.setContentsMargins(10, 15, 10, 10)
        self.end_params_text = QTextEdit()
        self.end_params_text.setMinimumHeight(100)
        end_layout.addWidget(self.end_params_text)
        scroll_layout.addWidget(end_group)
        
        # Punteriz
        punteriz_group = QGroupBox(LanguageManager.get_text('group_punteriz', self.current_language))
        punteriz_layout = QVBoxLayout(punteriz_group)
        punteriz_layout.setContentsMargins(10, 15, 10, 10)
        punteriz_controls = QGridLayout()
        punteriz_controls.setVerticalSpacing(10)
        punteriz_controls.setHorizontalSpacing(15)
        
        self.punteriz_enabled = QCheckBox(LanguageManager.get_text('label_active', self.current_language))
        punteriz_controls.addWidget(self.punteriz_enabled, 0, 0, 1, 2)
        
        punteriz_controls.addWidget(QLabel(LanguageManager.get_text('label_stitch_start', self.current_language)), 1, 0)
        self.punteriz_start = QLineEdit("0")
        self.punteriz_start.setEnabled(False)
        self.punteriz_start.setFixedWidth(120)
        punteriz_controls.addWidget(self.punteriz_start, 1, 1)
        
        punteriz_controls.addWidget(QLabel(LanguageManager.get_text('label_stitch_end', self.current_language)), 2, 0)
        self.punteriz_end = QLineEdit("0")
        self.punteriz_end.setEnabled(False)
        self.punteriz_end.setFixedWidth(120)
        punteriz_controls.addWidget(self.punteriz_end, 2, 1)
        
        punteriz_layout.addLayout(punteriz_controls)
        scroll_layout.addWidget(punteriz_group)
        
        # İğne pozisyonları
        needle_group = QGroupBox(LanguageManager.get_text('group_needle_positions', self.current_language))
        needle_layout = QVBoxLayout(needle_group)
        needle_layout.setContentsMargins(10, 15, 10, 10)
        needle_controls = QGridLayout()
        needle_controls.setVerticalSpacing(10)
        needle_controls.setHorizontalSpacing(15)
        
        needle_controls.addWidget(QLabel(LanguageManager.get_text('label_needle_down', self.current_language)), 0, 0)
        self.needle_down_pos = QLineEdit()
        self.needle_down_pos.setFixedWidth(120)
        needle_controls.addWidget(self.needle_down_pos, 0, 1)
        
        needle_controls.addWidget(QLabel(LanguageManager.get_text('label_needle_up', self.current_language)), 1, 0)
        self.needle_up_pos = QLineEdit()
        self.needle_up_pos.setFixedWidth(120)
        needle_controls.addWidget(self.needle_up_pos, 1, 1)
        
        needle_layout.addLayout(needle_controls)
        scroll_layout.addWidget(needle_group)
        
        # Dikiş Hızı Kontrolü
        speed_group = QGroupBox(LanguageManager.get_text('group_speed_control', self.current_language))
        speed_layout = QVBoxLayout(speed_group)
        speed_layout.setContentsMargins(10, 15, 10, 10)
        speed_controls = QGridLayout()
        speed_controls.setVerticalSpacing(10)
        speed_controls.setHorizontalSpacing(15)
        
        speed_controls.addWidget(QLabel(LanguageManager.get_text('label_start_speed', self.current_language)), 0, 0)
        self.start_speed = QLineEdit("10000")
        self.start_speed.setFixedWidth(120)
        speed_controls.addWidget(self.start_speed, 0, 1)
        
        speed_controls.addWidget(QLabel(LanguageManager.get_text('label_max_speed', self.current_language)), 1, 0)
        self.max_speed = QLineEdit("50000")
        self.max_speed.setFixedWidth(120)
        speed_controls.addWidget(self.max_speed, 1, 1)
        
        speed_controls.addWidget(QLabel(LanguageManager.get_text('label_speed_increment', self.current_language)), 2, 0)
        self.speed_increment = QLineEdit("5000")
        self.speed_increment.setFixedWidth(120)
        speed_controls.addWidget(self.speed_increment, 2, 1)
        
        speed_layout.addLayout(speed_controls)
        scroll_layout.addWidget(speed_group)
        
        # Üst İp Sıkma Bobini
        bobbin_group = QGroupBox(LanguageManager.get_text('group_bobbin', self.current_language))
        bobbin_layout = QVBoxLayout(bobbin_group)
        bobbin_layout.setContentsMargins(10, 15, 10, 10)
        bobbin_controls = QGridLayout()
        bobbin_controls.setVerticalSpacing(10)
        bobbin_controls.setHorizontalSpacing(15)
        
        self.bobbin_enabled = QCheckBox(LanguageManager.get_text('label_active', self.current_language))
        bobbin_controls.addWidget(self.bobbin_enabled, 0, 0, 1, 2)
        
        bobbin_controls.addWidget(QLabel(LanguageManager.get_text('label_bobbin_reset', self.current_language)), 1, 0)
        self.bobbin_reset_value = QLineEdit("1")
        self.bobbin_reset_value.setEnabled(False)
        self.bobbin_reset_value.setFixedWidth(120)
        bobbin_controls.addWidget(self.bobbin_reset_value, 1, 1)
        
        bobbin_layout.addLayout(bobbin_controls)
        scroll_layout.addWidget(bobbin_group)
        
        # Makine Kalibrasyon Değerleri
        calibration_group = QGroupBox(LanguageManager.get_text('group_calibration', self.current_language))
        calibration_layout = QVBoxLayout(calibration_group)
        calibration_layout.setContentsMargins(10, 15, 10, 10)
        calibration_controls = QGridLayout()
        calibration_controls.setVerticalSpacing(10)
        calibration_controls.setHorizontalSpacing(15)
        
        calibration_controls.addWidget(QLabel(LanguageManager.get_text('label_x', self.current_language)), 0, 0)
        self.calibration_x = QLineEdit()
        self.calibration_x.setFixedWidth(120)
        calibration_controls.addWidget(self.calibration_x, 0, 1)
        
        calibration_controls.addWidget(QLabel(LanguageManager.get_text('label_y', self.current_language)), 1, 0)
        self.calibration_y = QLineEdit()
        self.calibration_y.setFixedWidth(120)
        calibration_controls.addWidget(self.calibration_y, 1, 1)
        
        calibration_layout.addLayout(calibration_controls)
        scroll_layout.addWidget(calibration_group)
        
        # Scroll area'yı tamamla
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
    
    def create_right_panel(self, layout):
        """Sağ paneldeki G-Code içerik alanını oluşturur."""
        # G-Code içeriği için grup
        content_group = QGroupBox(LanguageManager.get_text('group_gcode_content', self.current_language))
        content_layout = QVBoxLayout(content_group)
        content_layout.setContentsMargins(10, 15, 10, 10)
        
        # Text alanı
        self.text_area = QTextEdit()
        self.text_area.setLineWrapMode(QTextEdit.NoWrap)  # Satır kaydırma kapalı
        self.text_area.setMinimumHeight(500)
        
        # Monospace font kullan
        font = QFont("Consolas", 10)
        self.text_area.setFont(font)
        
        # Satır numaralarını göster
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #FAFAFA;
                color: #212121;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                padding: 10px;
                selection-background-color: #2196F3;
                selection-color: white;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QTextEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        
        content_layout.addWidget(self.text_area)
        
        # Durum çubuğu
        status_layout = QHBoxLayout()
        self.status_label = QLabel(LanguageManager.get_text('label_ready', self.current_language))
        self.status_label.setStyleSheet("color: #757575; font-style: italic;")
        status_layout.addWidget(self.status_label)
        
        # Satır ve karakter sayısı
        self.line_count_label = QLabel(f"{LanguageManager.get_text('label_lines', self.current_language)} 0")
        self.line_count_label.setStyleSheet("color: #757575;")
        status_layout.addWidget(self.line_count_label)
        
        # Sağa hizala
        status_layout.addStretch()
        
        content_layout.addLayout(status_layout)
        layout.addWidget(content_group)
        
        # Text değişikliklerini izle
        self.text_area.textChanged.connect(self.update_line_count)
    
    def update_line_count(self):
        """Metin alanındaki satır sayısını günceller."""
        text = self.text_area.toPlainText()
        line_count = text.count('\n') + 1 if text else 0
        self.line_count_label.setText(f"{LanguageManager.get_text('label_lines', self.current_language)} {line_count}")
        
        if text:
            self.status_label.setText(LanguageManager.get_text('label_editing', self.current_language))
        else:
            self.status_label.setText(LanguageManager.get_text('label_ready', self.current_language))
    
    def create_action_buttons(self, layout):
        """Alt kısımdaki aksiyon butonlarını oluşturur."""
        # Buton container
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 15, 0, 0)
        button_layout.setSpacing(15)
        
        # G-Code Oluştur butonu
        self.generate_btn = QPushButton(LanguageManager.get_text('button_generate', self.current_language))
        self.generate_btn.setIcon(QIcon.fromTheme("document-new"))
        self.generate_btn.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(self.generate_btn)
        
        # Parametreleri Sıfırla butonu
        self.reset_btn = QPushButton(LanguageManager.get_text('button_reset', self.current_language))
        self.reset_btn.setIcon(QIcon.fromTheme("edit-clear"))
        self.reset_btn.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(self.reset_btn)
        
        # Dosya Yükle butonu
        self.load_btn = QPushButton(LanguageManager.get_text('button_load', self.current_language))
        self.load_btn.setIcon(QIcon.fromTheme("document-open"))
        self.load_btn.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(self.load_btn)
        
        # Dosya Kaydet butonu
        self.save_btn = QPushButton(LanguageManager.get_text('button_save', self.current_language))
        self.save_btn.setIcon(QIcon.fromTheme("document-save"))
        self.save_btn.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(self.save_btn)
        
        layout.addWidget(button_container)
    
    def get_parameters(self):
        """Kullanıcı arayüzündeki tüm parametreleri alır."""
        params = {
            'start_params': self.start_params_text.toPlainText().strip().split('\n'),
            'route_start_params': self.route_start_params_text.toPlainText().strip().split('\n'),
            'thread_cut_params': self.thread_cut_params_text.toPlainText().strip().split('\n'),
            'end_params': self.end_params_text.toPlainText().strip().split('\n'),
            'calibration_x': self.calibration_x.text().strip(),
            'calibration_y': self.calibration_y.text().strip(),
            'needle_down': self.needle_down_pos.text().strip(),
            'needle_up': self.needle_up_pos.text().strip(),
            'bobbin_enabled': self.bobbin_enabled.isChecked(),
            'bobbin_reset_value': self.bobbin_reset_value.text().strip(),
            'punteriz_enabled': self.punteriz_enabled.isChecked(),
            'punteriz_start': self.punteriz_start.text().strip(),
            'punteriz_end': self.punteriz_end.text().strip(),
            'start_speed': self.start_speed.text().strip(),
            'max_speed': self.max_speed.text().strip(),
            'speed_increment': self.speed_increment.text().strip()
        }
        return params
    
    def set_parameters(self, params):
        """Parametreleri kullanıcı arayüzüne yükler."""
        try:
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
            self.start_speed.setText(params.get('start_speed', "10000"))
            self.max_speed.setText(params.get('max_speed', "50000"))
            self.speed_increment.setText(params.get('speed_increment', "5000"))
            
            # Punteriz Ayarları
            self.punteriz_enabled.setChecked(params.get('punteriz_enabled', False))
            self.punteriz_start.setEnabled(self.punteriz_enabled.isChecked())
            self.punteriz_end.setEnabled(self.punteriz_enabled.isChecked())
            self.punteriz_start.setText(params.get('punteriz_start', "0"))
            self.punteriz_end.setText(params.get('punteriz_end', "0"))
            
            # Üst İp Sıkma Bobini Ayarları
            self.bobbin_enabled.setChecked(params.get('bobbin_enabled', False))
            self.bobbin_reset_value.setEnabled(self.bobbin_enabled.isChecked())
            self.bobbin_reset_value.setText(params.get('bobbin_reset_value', "1"))
        except Exception as e:
            self.show_error(f"Parametreler yüklenirken hata oluştu: {str(e)}")
    
    def set_gcode_content(self, content):
        """G-Code içeriğini text alanına yükler."""
        self.text_area.setText(content)
    
    def get_gcode_content(self):
        """Text alanındaki G-Code içeriğini alır."""
        return self.text_area.toPlainText()
    
    def show_message(self, title, message, icon=QMessageBox.Information):
        """Mesaj kutusu gösterir."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()
    
    def show_error(self, message):
        """Hata mesajı gösterir."""
        self.show_message(
            LanguageManager.get_text('msg_error', self.current_language), 
            message, 
            QMessageBox.Critical
        )
    
    def show_warning(self, message):
        """Uyarı mesajı gösterir."""
        self.show_message(
            LanguageManager.get_text('msg_warning', self.current_language), 
            message, 
            QMessageBox.Warning
        )
    
    def show_info(self, message):
        """Bilgi mesajı gösterir."""
        self.show_message(
            LanguageManager.get_text('msg_info', self.current_language), 
            message, 
            QMessageBox.Information
        ) 