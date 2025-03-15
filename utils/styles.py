from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class StyleManager:
    """
    Uygulama stillerini yöneten yardımcı sınıf.
    """
    @staticmethod
    def get_light_palette():
        """Açık tema paleti oluşturur."""
        palette = QPalette()
        
        # Temel renkler
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, QColor(30, 30, 30))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(30, 30, 30))
        palette.setColor(QPalette.Text, QColor(30, 30, 30))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(30, 30, 30))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        return palette
    
    @staticmethod
    def get_button_style():
        """Modern, yumuşak buton stilini döndürür."""
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #999999;
            }
        """
    
    @staticmethod
    def get_group_style():
        """GroupBox stilini döndürür."""
        return """
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #f8f8f8;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 8px;
                background-color: #f8f8f8;
            }
        """
    
    @staticmethod
    def get_text_edit_style():
        """QTextEdit stilini döndürür."""
        return """
            QTextEdit {
                background-color: white;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTextEdit:focus {
                border: 1px solid #3498db;
            }
        """
    
    @staticmethod
    def get_line_edit_style():
        """QLineEdit stilini döndürür."""
        return """
            QLineEdit {
                background-color: white;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """
    
    @staticmethod
    def get_checkbox_style():
        """QCheckBox stilini döndürür."""
        return """
            QCheckBox {
                spacing: 8px;
                color: #333333;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #cccccc;
                background-color: white;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #3498db;
                background-color: #3498db;
                border-radius: 3px;
            }
        """
    
    @staticmethod
    def get_scroll_bar_style():
        """QScrollBar stilini döndürür."""
        return """
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f0f0f0;
                height: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """
    
    @staticmethod
    def get_label_style():
        """QLabel stilini döndürür."""
        return """
            QLabel {
                color: #333333;
                font-size: 9pt;
            }
        """
    
    @staticmethod
    def get_splitter_style():
        """QSplitter stilini döndürür."""
        return """
            QSplitter::handle {
                background-color: #cccccc;
            }
            QSplitter::handle:horizontal {
                width: 2px;
            }
            QSplitter::handle:vertical {
                height: 2px;
            }
        """
    
    @staticmethod
    def apply_application_style(app):
        """Uygulamaya tüm stilleri uygular."""
        app.setStyle("Fusion")
        app.setPalette(StyleManager.get_light_palette())
        
        # Genel stil
        app.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 9pt;
            }
        """)
        
        return app 