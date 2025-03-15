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
        palette.setColor(QPalette.Window, QColor(248, 248, 248))
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
        """Buton stilini döndürür."""
        return """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11pt;
                min-height: 20px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
                color: #757575;
            }
        """
    
    @staticmethod
    def get_group_style():
        """GroupBox stilini döndürür."""
        return """
            QGroupBox {
                font-weight: normal;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                margin-top: 20px;
                padding-top: 20px;
                background-color: #FFFFFF;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 10px;
                color: #1976D2;
                font-weight: bold;
                font-size: 10pt;
                margin-left: 10px;
                border-bottom: 1px solid #1976D2;
            }
        """
    
    @staticmethod
    def get_text_edit_style():
        """QTextEdit stilini döndürür."""
        return """
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
                background-color: #FFFFFF;
            }
        """
    
    @staticmethod
    def get_line_edit_style():
        """QLineEdit stilini döndürür."""
        return """
            QLineEdit {
                background-color: #FAFAFA;
                color: #212121;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                padding: 8px;
                selection-background-color: #2196F3;
                selection-color: white;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
                background-color: #FFFFFF;
            }
            QLineEdit:disabled {
                background-color: #F5F5F5;
                color: #9E9E9E;
            }
        """
    
    @staticmethod
    def get_checkbox_style():
        """QCheckBox stilini döndürür."""
        return """
            QCheckBox {
                spacing: 8px;
                color: #424242;
                font-size: 10pt;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #BDBDBD;
                border-radius: 3px;
                background-color: #FAFAFA;
            }
            QCheckBox::indicator:checked {
                background-color: #2196F3;
                border: 1px solid #2196F3;
                image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNGRkZGRkYiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cG9seWxpbmUgcG9pbnRzPSIyMCA2IDkgMTcgNCAxMiI+PC9wb2x5bGluZT48L3N2Zz4=);
            }
            QCheckBox::indicator:unchecked:hover {
                border: 1px solid #2196F3;
            }
            QCheckBox:disabled {
                color: #9E9E9E;
            }
        """
    
    @staticmethod
    def get_scroll_bar_style():
        """QScrollBar stilini döndürür."""
        return """
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 12px;
                margin: 0px 0px 0px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #BDBDBD;
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9E9E9E;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #F5F5F5;
                height: 12px;
                margin: 0px 0px 0px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #BDBDBD;
                min-width: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #9E9E9E;
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
                color: #424242;
                font-size: 10pt;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                padding: 2px;
            }
        """
    
    @staticmethod
    def get_splitter_style():
        """QSplitter stilini döndürür."""
        return """
            QSplitter::handle {
                background-color: #E0E0E0;
            }
            QSplitter::handle:horizontal {
                width: 2px;
            }
            QSplitter::handle:vertical {
                height: 2px;
            }
            QSplitter::handle:hover {
                background-color: #BDBDBD;
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
                font-size: 10pt;
            }
            QMainWindow {
                background-color: #F5F5F5;
            }
            QToolTip {
                background-color: #424242;
                color: white;
                border: none;
                padding: 5px;
                opacity: 200;
            }
        """)
        
        return app 