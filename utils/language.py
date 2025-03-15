class LanguageManager:
    """
    Uygulama için dil desteği sağlayan yardımcı sınıf.
    """
    
    # Dil çevirileri
    translations = {
        # Menü çevirileri
        'menu_file': {
            'tr': 'Dosya',
            'en': 'File'
        },
        'menu_edit': {
            'tr': 'Düzen',
            'en': 'Edit'
        },
        'menu_language': {
            'tr': 'Dil',
            'en': 'Language'
        },
        'menu_help': {
            'tr': 'Yardım',
            'en': 'Help'
        },
        'menu_load_file': {
            'tr': 'Dosya Yükle',
            'en': 'Load File'
        },
        'menu_save_file': {
            'tr': 'Dosya Kaydet',
            'en': 'Save File'
        },
        'menu_exit': {
            'tr': 'Çıkış',
            'en': 'Exit'
        },
        'menu_generate_gcode': {
            'tr': 'G-Code Oluştur',
            'en': 'Generate G-Code'
        },
        'menu_reset_parameters': {
            'tr': 'Parametreleri Sıfırla',
            'en': 'Reset Parameters'
        },
        'menu_about': {
            'tr': 'Hakkında',
            'en': 'About'
        },
        
        # Başlık çevirileri
        'title_parameters': {
            'tr': 'G-CODE Editor Parametreleri',
            'en': 'G-CODE Editor Parameters'
        },
        'title_output': {
            'tr': 'G-CODE Çıktısı',
            'en': 'G-CODE Output'
        },
        
        # Grup başlıkları
        'group_start_params': {
            'tr': 'G-Code Başlangıç Parametreleri',
            'en': 'G-Code Start Parameters'
        },
        'group_route_start_params': {
            'tr': 'Rota Başlangıç Parametreleri',
            'en': 'Route Start Parameters'
        },
        'group_thread_cut_params': {
            'tr': 'İp Kesme Parametreleri',
            'en': 'Thread Cut Parameters'
        },
        'group_end_params': {
            'tr': 'G-Code Sonu Parametreleri',
            'en': 'G-Code End Parameters'
        },
        'group_punteriz': {
            'tr': 'Punteriz',
            'en': 'Punteriz'
        },
        'group_needle_positions': {
            'tr': 'İğne Batma ve Geri Çekilme Pozisyonları',
            'en': 'Needle Down and Up Positions'
        },
        'group_speed_control': {
            'tr': 'Dikiş Hızı Kontrolü',
            'en': 'Sewing Speed Control'
        },
        'group_bobbin': {
            'tr': 'Üst İp Sıkma Bobini (M118-M119)',
            'en': 'Upper Thread Tightening Bobbin (M118-M119)'
        },
        'group_calibration': {
            'tr': 'Makine Kalibrasyon Değerleri',
            'en': 'Machine Calibration Values'
        },
        'group_gcode_content': {
            'tr': 'G-Code İçeriği',
            'en': 'G-Code Content'
        },
        
        # Etiket çevirileri
        'label_active': {
            'tr': 'Aktif',
            'en': 'Active'
        },
        'label_stitch_start': {
            'tr': 'Dikiş Başı:',
            'en': 'Stitch Start:'
        },
        'label_stitch_end': {
            'tr': 'Dikiş Sonu:',
            'en': 'Stitch End:'
        },
        'label_needle_down': {
            'tr': 'Batma:',
            'en': 'Down:'
        },
        'label_needle_up': {
            'tr': 'Geri Çekilme:',
            'en': 'Up:'
        },
        'label_start_speed': {
            'tr': 'Başlangıç Hızı (F):',
            'en': 'Start Speed (F):'
        },
        'label_max_speed': {
            'tr': 'Maksimum Hız (F):',
            'en': 'Maximum Speed (F):'
        },
        'label_speed_increment': {
            'tr': 'Artış Hızı (F):',
            'en': 'Speed Increment (F):'
        },
        'label_bobbin_reset': {
            'tr': 'Kaç Satır Sonra Resetlensin:',
            'en': 'Reset After Lines:'
        },
        'label_x': {
            'tr': 'X:',
            'en': 'X:'
        },
        'label_y': {
            'tr': 'Y:',
            'en': 'Y:'
        },
        'label_lines': {
            'tr': 'Satır:',
            'en': 'Lines:'
        },
        'label_ready': {
            'tr': 'Hazır',
            'en': 'Ready'
        },
        'label_editing': {
            'tr': 'Düzenleniyor',
            'en': 'Editing'
        },
        
        # Buton çevirileri
        'button_generate': {
            'tr': 'G-Code Oluştur',
            'en': 'Generate G-Code'
        },
        'button_reset': {
            'tr': 'Parametreleri Sıfırla',
            'en': 'Reset Parameters'
        },
        'button_load': {
            'tr': 'Dosya Yükle',
            'en': 'Load File'
        },
        'button_save': {
            'tr': 'Dosya Kaydet',
            'en': 'Save File'
        },
        
        # Mesaj çevirileri
        'msg_language_changed': {
            'tr': 'Dil değiştirildi',
            'en': 'Language changed'
        },
        'msg_language_changed_text': {
            'tr': 'Dil {} olarak değiştirildi.',
            'en': 'Language changed to {}.'
        },
        'msg_about_title': {
            'tr': 'G-CODE Editor Hakkında',
            'en': 'About G-CODE Editor'
        },
        'msg_about_text': {
    'tr': (
        "G-CODE Editor v1.0\n\n"
        "Bu uygulama, G-CODE dosyalarını düzenlemek ve işlemek için gelişmiş ve kullanıcı dostu bir arayüz sunarak "
        "verimliliği ve hassasiyeti artırır.\n\n"
        "Geliştirici: Mustafa Kürşad BAŞER\n"
        "© 2025 Tüm hakları saklıdır."
    ),
    'en': (
        "G-CODE Editor v1.0\n\n"
        "This application offers a sophisticated and user-friendly interface for editing and processing G-CODE files, "
        "providing enhanced efficiency and precision.\n\n"
        "Developed by Mustafa Kürşad BAŞER\n"
        "© 2025 All rights reserved."
    )
}
,
        'msg_file_loaded': {
            'tr': 'Rotalar başarıyla yüklendi.',
            'en': 'Routes loaded successfully.'
        },
        'msg_file_saved': {
            'tr': 'Dosya başarıyla kaydedildi:\n{}',
            'en': 'File saved successfully:\n{}'
        },
        'msg_gcode_generated': {
            'tr': 'G-Code oluşturuldu.',
            'en': 'G-Code generated.'
        },
        'msg_parameters_reset': {
            'tr': 'Parametreler varsayılan değerlere sıfırlandı.',
            'en': 'Parameters reset to default values.'
        },
        'msg_error': {
            'tr': 'Hata',
            'en': 'Error'
        },
        'msg_warning': {
            'tr': 'Uyarı',
            'en': 'Warning'
        },
        'msg_info': {
            'tr': 'Bilgi',
            'en': 'Information'
        },
        'msg_no_content': {
            'tr': 'İşlenecek G-Code içeriği bulunamadı. Lütfen önce bir dosya yükleyin.',
            'en': 'No G-Code content found to process. Please load a file first.'
        },
        'msg_no_content_save': {
            'tr': 'Kaydedilecek G-Code içeriği bulunamadı.',
            'en': 'No G-Code content found to save.'
        }
    }
    
    @staticmethod
    def get_text(key, lang='tr'):
        """Belirtilen dilde metni döndürür."""
        if key in LanguageManager.translations:
            return LanguageManager.translations[key].get(lang, LanguageManager.translations[key]['tr'])
        return key 