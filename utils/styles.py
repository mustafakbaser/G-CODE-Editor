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
        """Modern, yumuşak buton stilini döndürür."""
        return """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
                min-height: 40px;
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
                font-weight: bold;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 1.5ex;
                padding-top: 15px;
                background-color: #FFFFFF;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: #FFFFFF;
                color: #1976D2;
            }
        """
    
    @staticmethod
    def get_text_edit_style():
        """QTextEdit stilini döndürür."""
        return """
            QTextEdit {
                background-color: white;
                color: #333333;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                padding: 8px;
                selection-background-color: #2196F3;
                selection-color: white;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QTextEdit:focus {
                border: 1px solid #2196F3;
            }
        """
    
    @staticmethod
    def get_line_edit_style():
        """QLineEdit stilini döndürür."""
        return """
            QLineEdit {
                background-color: white;
                color: #333333;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                padding: 8px;
                selection-background-color: #2196F3;
                selection-color: white;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
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
                spacing: 10px;
                color: #333333;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #E0E0E0;
                background-color: white;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #2196F3;
                background-color: #2196F3;
                border-radius: 4px;
                image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cG9seWxpbmUgcG9pbnRzPSIyMCA2IDkgMTcgNCAxMiI+PC9wb2x5bGluZT48L3N2Zz4=);
            }
            QCheckBox::indicator:hover {
                border: 2px solid #2196F3;
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
                font-weight: normal;
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