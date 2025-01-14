import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
from gcode_processor import GCodeProcessor
from multi_route_processor import MultiRouteProcessor

class GCodeEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("G-CODE Düzenleyici")
        self.processor = GCodeProcessor()
        
        # Ana pencere boyutunu ayarla
        self.root.geometry("950x850")
        
        # Ana çerçeve
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid yapılandırması
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=3)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=0)  # Butonlar için sabit yükseklik
        
        # Sol ve sağ panel oluştur
        self.left_panel = ttk.Frame(self.main_frame)
        self.right_panel = ttk.Frame(self.main_frame)
        self.left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        self.right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Stil ayarları
        style = ttk.Style()
        style.configure('Action.TButton', padding=10, font=('Helvetica', 10, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 11, 'bold'))
        style.configure('Parameter.TLabelframe', padding=10)
        
        # Buton durumu için flag
        self.is_first_generation = True
        
        # Panel oluşturma
        self.create_parameter_inputs()
        self.create_right_panel()
        self.load_default_parameters()

    def create_parameter_inputs(self):
        # Ana parametre çerçevesi
        main_param_frame = ttk.Frame(self.left_panel)
        main_param_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.left_panel.rowconfigure(0, weight=1)
        self.left_panel.columnconfigure(0, weight=1)
        
        # Üst kısım (scrollable alan)
        scroll_frame = ttk.LabelFrame(main_param_frame, text="Parametreler", style='Parameter.TLabelframe')
        scroll_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0,10))
        scroll_frame.columnconfigure(0, weight=1)
        scroll_frame.rowconfigure(0, weight=1)
        
        # Scrollable canvas oluştur
        canvas = tk.Canvas(scroll_frame)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Canvas'ı yapılandır
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel binding
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        ttk.Label(scrollable_frame, text="G-Code Başlangıç Parametreleri:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0,5))
        self.start_params_text = scrolledtext.ScrolledText(scrollable_frame, width=30, height=4)
        self.start_params_text.grid(row=1, column=0, pady=(0, 10))
        
        ttk.Label(scrollable_frame, text="Rota Başlangıç Parametreleri:", style='Header.TLabel').grid(row=4, column=0, sticky=tk.W, pady=(0,5))
        self.route_start_params_text = scrolledtext.ScrolledText(scrollable_frame, width=30, height=4)
        self.route_start_params_text.grid(row=5, column=0, pady=(0, 10))
        
        ttk.Label(scrollable_frame, text="İp Kesme Parametreleri:", style='Header.TLabel').grid(row=8, column=0, sticky=tk.W, pady=(0,5))
        self.thread_cut_params_text = scrolledtext.ScrolledText(scrollable_frame, width=30, height=2)
        self.thread_cut_params_text.grid(row=9, column=0, pady=(0, 10))
        
        # G-Code Sonu Parametreleri
        ttk.Label(scrollable_frame, text="G-Code Sonu Parametreleri:", style='Header.TLabel').grid(row=6, column=0, sticky=tk.W, pady=(0,5))
        self.end_params_text = scrolledtext.ScrolledText(scrollable_frame, width=30, height=4)
        self.end_params_text.grid(row=7, column=0, pady=(0, 10))
        
        # Punteriz bölümü
        ttk.Label(scrollable_frame, text="Punteriz:", style='Header.TLabel').grid(row=10, column=0, sticky=tk.W, pady=(0,5))
        
        # Punteriz frame
        punteriz_frame = ttk.Frame(scrollable_frame)
        punteriz_frame.grid(row=11, column=0, sticky=tk.W, pady=(0, 10))
        
        # Checkbox için BooleanVar
        self.punteriz_enabled = tk.BooleanVar()
        self.punteriz_enabled.set(False)
        
        # Checkbox
        self.punteriz_checkbox = ttk.Checkbutton(
            punteriz_frame, 
            text="Aktif", 
            variable=self.punteriz_enabled,
            command=self.toggle_punteriz_input
        )
        self.punteriz_checkbox.grid(row=0, column=0, padx=(0, 10))
        
        # Dikiş Başı Punteriz
        ttk.Label(punteriz_frame, text="Dikiş Başı:").grid(row=0, column=1, padx=(0, 5))
        self.punteriz_start = ttk.Entry(punteriz_frame, width=5, state='disabled')
        self.punteriz_start.grid(row=0, column=2, padx=(0, 20))
        self.punteriz_start.insert(0, "0")
        
        # Dikiş Sonu Punteriz
        ttk.Label(punteriz_frame, text="Dikiş Sonu:").grid(row=0, column=3, padx=(0, 5))
        self.punteriz_end = ttk.Entry(punteriz_frame, width=5, state='disabled')
        self.punteriz_end.grid(row=0, column=4)
        self.punteriz_end.insert(0, "0")
        
        ttk.Separator(scrollable_frame, orient='horizontal').grid(row=12, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # İğne pozisyonları
        ttk.Label(scrollable_frame, text="İğne Batma ve Geri Çekilme Pozisyonları:", style='Header.TLabel').grid(row=13, column=0, sticky=tk.W, pady=(0,5))
        
        # Z değerleri için frame
        z_positions_frame = ttk.Frame(scrollable_frame)
        z_positions_frame.grid(row=14, column=0, sticky=tk.W, pady=(0, 10))
        
        # Batma pozisyonu
        ttk.Label(z_positions_frame, text="Batma:").grid(row=0, column=0, padx=(0,5))
        self.needle_down_pos = ttk.Entry(z_positions_frame, width=10)
        self.needle_down_pos.grid(row=0, column=1, padx=(0,20))
        
        # Geri çekilme pozisyonu
        ttk.Label(z_positions_frame, text="Geri Çekilme:").grid(row=0, column=2, padx=(0,5))
        self.needle_up_pos = ttk.Entry(z_positions_frame, width=10)
        self.needle_up_pos.grid(row=0, column=3)
        
        ttk.Separator(scrollable_frame, orient='horizontal').grid(row=15, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Dikiş Hızı Kontrolü bölümü
        ttk.Label(scrollable_frame, text="Dikiş Hızı Kontrolü:", style='Header.TLabel').grid(row=16, column=0, sticky=tk.W, pady=(0,5))
        
        # Hız değerleri için frame
        speed_frame = ttk.Frame(scrollable_frame)
        speed_frame.grid(row=17, column=0, sticky=tk.W, pady=(0, 10))
        
        # Başlangıç Hızı
        ttk.Label(speed_frame, text="Başlangıç Hızı (F):").grid(row=0, column=0, padx=(0,5))
        self.start_speed = ttk.Entry(speed_frame, width=10)
        self.start_speed.grid(row=0, column=1, padx=(0,10))
        self.start_speed.insert(0, "10000")
        
        # Maksimum Hız
        ttk.Label(speed_frame, text="Maksimum Hız (F):").grid(row=1, column=0, padx=(0,5))
        self.max_speed = ttk.Entry(speed_frame, width=10)
        self.max_speed.grid(row=1, column=1, padx=(0,10))
        self.max_speed.insert(0, "50000")
        
        # Artış Hızı
        ttk.Label(speed_frame, text="Artış Hızı (F):").grid(row=2, column=0, padx=(0,5))
        self.speed_increment = ttk.Entry(speed_frame, width=10)
        self.speed_increment.grid(row=2, column=1, padx=(0,10))
        self.speed_increment.insert(0, "5000")
        
        ttk.Separator(scrollable_frame, orient='horizontal').grid(row=18, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Üst İp Sıkma Bobini bölümü
        ttk.Label(scrollable_frame, text="Üst İp Sıkma Bobini (M118-M119):", style='Header.TLabel').grid(row=19, column=0, sticky=tk.W, pady=(0,5))
        
        # Checkbox ve değer girme alanı için frame
        bobbin_frame = ttk.Frame(scrollable_frame)
        bobbin_frame.grid(row=20, column=0, sticky=tk.W, pady=(0, 10))
        
        # Checkbox için StringVar
        self.bobbin_enabled = tk.BooleanVar()
        self.bobbin_enabled.set(False)
        
        # Checkbox
        self.bobbin_checkbox = ttk.Checkbutton(
            bobbin_frame, 
            text="Aktif", 
            variable=self.bobbin_enabled,
            command=self.toggle_bobbin_input
        )
        self.bobbin_checkbox.grid(row=0, column=0, padx=(0, 10))
        
        # Reset değeri için label
        ttk.Label(bobbin_frame, text="Kaç Satır Sonra Resetlensin:").grid(row=0, column=1, padx=(0, 5))
        
        # Reset değeri için entry
        self.bobbin_reset_value = ttk.Entry(bobbin_frame, width=10, state='disabled')
        self.bobbin_reset_value.grid(row=0, column=2)
        
        ttk.Separator(scrollable_frame, orient='horizontal').grid(row=21, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Makine Kalibrasyon Değerleri
        ttk.Label(scrollable_frame, text="Makine Kalibrasyon Değerleri:", style='Header.TLabel').grid(row=22, column=0, sticky=tk.W, pady=(0,5))
        
        # X ve Y değerleri için frame
        calibration_frame = ttk.Frame(scrollable_frame)
        calibration_frame.grid(row=23, column=0, sticky=tk.W, pady=(0, 10))
        
        # X değeri
        ttk.Label(calibration_frame, text="X:").grid(row=0, column=0, padx=(0,5))
        self.calibration_x = ttk.Entry(calibration_frame, width=15)
        self.calibration_x.grid(row=0, column=1, padx=(0,20))
        
        # Y değeri
        ttk.Label(calibration_frame, text="Y:").grid(row=0, column=2, padx=(0,5))
        self.calibration_y = ttk.Entry(calibration_frame, width=15)
        self.calibration_y.grid(row=0, column=3)
        
        # Canvas ve scrollbar'ı yerleştir
        canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Alt kısım (butonlar) - yatay düzenleme ve sabit genişlik
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10, padx=5)
        
        # Her sütuna eşit ağırlık ver
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)
        
        # Buton genişliği için minimum piksel değeri
        button_width = 20
        
        # Tüm butonları yan yana yerleştir ve sabit genişlik ver
        self.update_button = ttk.Button(button_frame, 
                                      text="G-Code Oluştur",
                                      width=button_width,
                                      style='Action.TButton',
                                      command=self.update_parameters)
        self.update_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, 
                  text="Parametreleri Sıfırla",
                  width=button_width,
                  style='Action.TButton',
                  command=self.reset_parameters).grid(row=0, column=1, padx=5)
                  
        ttk.Button(button_frame, 
                  text="Dosya Yükle",
                  width=button_width,
                  style='Action.TButton',
                  command=self.load_file).grid(row=0, column=2, padx=5)
                  
        ttk.Button(button_frame, 
                  text="Dosya Kaydet",
                  width=button_width,
                  style='Action.TButton',
                  command=self.save_file).grid(row=0, column=3, padx=5)
        
        # Grid yapılandırması
        main_param_frame.columnconfigure(0, weight=1)
        main_param_frame.rowconfigure(0, weight=1)
        main_param_frame.rowconfigure(1, weight=0)  # Butonlar için sabit yükseklik

    def create_right_panel(self):
        # Ana sağ panel çerçevesi
        main_right_frame = ttk.Frame(self.right_panel)
        main_right_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # G-Code içeriği için frame
        content_frame = ttk.LabelFrame(main_right_frame, text="G-Code İçeriği", style='Parameter.TLabelframe')
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0,10))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Text alanı
        self.text_area = scrolledtext.ScrolledText(content_frame, width=50, height=40)
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Grid yapılandırması
        self.right_panel.columnconfigure(0, weight=1)
        self.right_panel.rowconfigure(0, weight=1)
        main_right_frame.columnconfigure(0, weight=1)
        main_right_frame.rowconfigure(0, weight=1)

    def load_default_parameters(self):
        try:
            with open('parameters.json', 'r') as file:
                params = json.load(file)
                
                # G-Code Başlangıç Parametreleri
                start_params = '\n'.join(params.get('start_params', []))
                self.start_params_text.delete('1.0', tk.END)
                self.start_params_text.insert('1.0', start_params)
                
                # Rota Başlangıç Parametreleri
                route_start_params = '\n'.join(params.get('route_start_params', []))
                self.route_start_params_text.delete('1.0', tk.END)
                self.route_start_params_text.insert('1.0', route_start_params)
                
                # İp Kesme Parametreleri
                thread_cut_params = '\n'.join(params.get('thread_cut_params', []))
                self.thread_cut_params_text.delete('1.0', tk.END)
                self.thread_cut_params_text.insert('1.0', thread_cut_params)
                
                # G-Code Sonu Parametreleri
                end_params = '\n'.join(params.get('end_params', []))
                self.end_params_text.delete('1.0', tk.END)
                self.end_params_text.insert('1.0', end_params)
                
                # Z pozisyonları
                z_positions = params.get('z_positions', {"needle_down": "Z3", "needle_up": "Z30"})
                self.needle_down_pos.delete(0, tk.END)
                self.needle_down_pos.insert(0, z_positions["needle_down"])
                
                self.needle_up_pos.delete(0, tk.END)
                self.needle_up_pos.insert(0, z_positions["needle_up"])
                
                # Makine Kalibrasyon Değerleri
                machine_calibration = params.get('machine_calibration', {"x_value": "21.57001", "y_value": "388.6"})
                self.calibration_x.delete(0, tk.END)
                self.calibration_x.insert(0, machine_calibration["x_value"])
                
                self.calibration_y.delete(0, tk.END)
                self.calibration_y.insert(0, machine_calibration["y_value"])
                
        except Exception as e:
            messagebox.showerror("Hata", f"Parametreler yüklenirken hata oluştu: {str(e)}")

    def update_parameters(self):
        try:
            # Kalibrasyon değerlerini al
            calibration_x = self.calibration_x.get().strip()
            calibration_y = self.calibration_y.get().strip()
            
            # Z pozisyonlarını al
            needle_down = self.needle_down_pos.get().strip()
            needle_up = self.needle_up_pos.get().strip()
            
            # Üst İp Sıkma Bobini ayarlarını al
            bobbin_enabled = self.bobbin_enabled.get()
            bobbin_reset_value = self.bobbin_reset_value.get().strip() if bobbin_enabled else "1"
            
            # Punteriz ayarlarını al
            punteriz_enabled = self.punteriz_enabled.get()
            punteriz_start = self.punteriz_start.get().strip() if punteriz_enabled else "0"
            punteriz_end = self.punteriz_end.get().strip() if punteriz_enabled else "0"
            
            # Diğer parametreleri güncelle
            self.processor.start_params = self.start_params_text.get('1.0', tk.END).strip().split('\n')
            self.processor.route_start_params = self.route_start_params_text.get('1.0', tk.END).strip().split('\n')
            self.processor.thread_cut_params = self.thread_cut_params_text.get('1.0', tk.END).strip().split('\n')
            self.processor.end_params = self.end_params_text.get('1.0', tk.END).strip().split('\n')
            
            # Kalibrasyon, Z değerleri ve Bobini ayarlarını güncelle
            self.processor.update_calibration_values(calibration_x, calibration_y)
            self.processor.update_z_positions(needle_down, needle_up)
            self.processor.update_bobbin_settings(bobbin_enabled, bobbin_reset_value)
            
            # Punteriz ayarlarını güncelle
            self.processor.update_punteriz_settings(punteriz_enabled, punteriz_start, punteriz_end)
            
            # Hız ayarlarını al ve doğrula
            start_speed = self.start_speed.get().strip()
            max_speed = self.max_speed.get().strip()
            speed_increment = self.speed_increment.get().strip()
            
            # Hız ayarlarını güncelle
            self.processor.update_speed_settings(start_speed, max_speed, speed_increment)
            
            # Mevcut içeriği güncelle
            if self.text_area.get('1.0', tk.END).strip():
                self.process_file()
                
                # G-Code butonu -> Parametreleri Güncelle
                if self.is_first_generation:
                    self.update_button.configure(text="Parametreleri Güncelle")
                    self.is_first_generation = False
                
                messagebox.showinfo("Başarılı", "Parametreler güncellendi.")
            else:
                messagebox.showwarning("Uyarı", "İşlenecek G-Code içeriği bulunamadı. Lütfen önce bir dosya yükleyin.")
                
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {str(e)}")

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
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', '\n'.join(raw_content))
            
            # Buton metnini sıfırla
            self.update_button.configure(text="G-Code Oluştur")
            self.is_first_generation = True
            
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya yüklenirken hata oluştu: {str(e)}")

    def save_file(self):
        try:
            # Şu anki tarihi al ve formatla
            from datetime import datetime
            current_time = datetime.now()
            filename = current_time.strftime("%y_%m_%d_%H_%M_%S.nc")
            
            # gcode klasörünü kontrol et ve yoksa oluştur
            import os
            gcode_dir = "gcode"
            if not os.path.exists(gcode_dir):
                os.makedirs(gcode_dir)
            
            # Tam dosya yolunu oluştur
            filepath = os.path.join(gcode_dir, filename)
            
            # İçeriği kaydet
            content = self.text_area.get('1.0', tk.END)
            with open(filepath, 'w') as file:
                file.write(content)
            messagebox.showinfo("Başarılı", f"Dosya başarıyla kaydedildi:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken hata oluştu: {str(e)}")

    def process_file(self):
        try:
            # Text alanındaki içeriği al
            content = self.text_area.get('1.0', tk.END)
            
            # MultiRouteProcessor'ı başlat
            multi_processor = MultiRouteProcessor()
            
            # İçeriği rotalara ayır
            routes = []
            current_route = []
            route_number = 1
            
            for line in content.strip().split('\n'):
                if line.startswith('%'):
                    if current_route:
                        routes.append(current_route)
                    current_route = [line]
                    route_number += 1
                else:
                    current_route.append(line)
            
            # Son rotayı ekle
            if current_route:
                routes.append(current_route)
            
            # G-Code oluştur
            final_content = []
            
            # G-Code başlangıç parametreleri
            final_content.extend(self.processor.start_params)
            
            # Her rotayı işle
            for index, route in enumerate(routes, 1):
                # Rota başlığı
                final_content.append(route[0])  # % Rota No N
                
                # G01 G90 F10000 veya F10000
                if index == 1:
                    final_content.append("G01 G90 F10000")
                else:
                    final_content.append("F10000")
                
                # İlk koordinat
                first_coord = route[1]
                final_content.append(first_coord)
                
                # Rota başlangıç parametreleri
                final_content.extend([
                    "M114",
                    "G04 P200"
                ])
                
                # Bobbin kontrolü
                if self.processor.bobbin_enabled:
                    final_content.append("M118")
                    final_content.append(self.processor.z_positions["needle_down"])
                    if int(self.processor.bobbin_reset_value) == 1:
                        final_content.append("M119")
                    final_content.append(self.processor.z_positions["needle_up"])
                    if int(self.processor.bobbin_reset_value) == 2:
                        final_content.append("M119")
                else:
                    final_content.extend([
                        self.processor.z_positions["needle_down"],
                        self.processor.z_positions["needle_up"]
                    ])
                
                # Koordinatları işle
                coordinates = [line for line in route[1:] if line.strip().startswith('X')]
                
                if self.processor.punteriz_enabled:
                    # Punteriz işlemi - tüm koordinatları koruyarak
                    punteriz_lines = self.processor.apply_punteriz(coordinates)
                    if punteriz_lines:
                        final_content.extend(punteriz_lines)
                    else:
                        # Punteriz işlemi başarısız olursa normal işleme devam et
                        for i in range(1, len(coordinates)):
                            coord_line = coordinates[i]
                            coord_line += f" {self.processor.z_positions['needle_down']}"
                            speed = self.processor.calculate_speed(i-1, len(coordinates)-1)
                            if i == 1 or speed is not None:
                                coord_line += f" F{speed if speed else self.processor.start_speed}"
                            final_content.append(coord_line)
                            if i < len(coordinates) - 1:
                                final_content.append(self.processor.z_positions["needle_up"])
                else:
                    # Normal işlem - hız kontrolü ile
                    for i in range(1, len(coordinates)):
                        speed = self.processor.calculate_speed(i-1, len(coordinates)-1)
                        coord_line = coordinates[i]
                        coord_line += f" {self.processor.z_positions['needle_down']}"
                        if i == 1 or speed is not None:
                            coord_line += f" F{speed if speed else self.processor.start_speed}"
                        final_content.append(coord_line)
                        if i < len(coordinates) - 1:
                            final_content.append(self.processor.z_positions["needle_up"])
                
                # İp kesme parametreleri
                final_content.extend(self.processor.thread_cut_params)
            
            # G-Code sonlandırma parametreleri
            final_content.extend(self.processor.end_params)
            
            # Sonucu göster
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', '\n'.join(final_content))
            
            # Buton metnini güncelle
            if self.is_first_generation:
                self.update_button.configure(text="Parametreleri Güncelle")
                self.is_first_generation = False
                
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {str(e)}")

    def reset_parameters(self):
        """Tüm parametreleri varsayılan değerlerine sıfırla"""
        try:
            # parameters.json dosyasından varsayılan değerleri yükle
            with open('parameters.json', 'r') as file:
                params = json.load(file)
                
                # G-Code Başlangıç Parametreleri
                start_params = '\n'.join(params.get('start_params', []))
                self.start_params_text.delete('1.0', tk.END)
                self.start_params_text.insert('1.0', start_params)
                
                # Rota Başlangıç Parametreleri
                route_start_params = '\n'.join(params.get('route_start_params', []))
                self.route_start_params_text.delete('1.0', tk.END)
                self.route_start_params_text.insert('1.0', route_start_params)
                
                # İp Kesme Parametreleri
                thread_cut_params = '\n'.join(params.get('thread_cut_params', []))
                self.thread_cut_params_text.delete('1.0', tk.END)
                self.thread_cut_params_text.insert('1.0', thread_cut_params)
                
                # G-Code Sonu Parametreleri
                end_params = '\n'.join(params.get('end_params', []))
                self.end_params_text.delete('1.0', tk.END)
                self.end_params_text.insert('1.0', end_params)
                
                # Z pozisyonları
                z_positions = params.get('z_positions', {"needle_down": "Z3", "needle_up": "Z30"})
                self.needle_down_pos.delete(0, tk.END)
                self.needle_down_pos.insert(0, z_positions["needle_down"])
                
                self.needle_up_pos.delete(0, tk.END)
                self.needle_up_pos.insert(0, z_positions["needle_up"])
                
                # Makine Kalibrasyon Değerleri
                machine_calibration = params.get('machine_calibration', {"x_value": "21.57001", "y_value": "388.6"})
                self.calibration_x.delete(0, tk.END)
                self.calibration_x.insert(0, machine_calibration["x_value"])
                
                self.calibration_y.delete(0, tk.END)
                self.calibration_y.insert(0, machine_calibration["y_value"])
                
                # Hız Ayarları
                self.start_speed.delete(0, tk.END)
                self.start_speed.insert(0, "10000")
                
                self.max_speed.delete(0, tk.END)
                self.max_speed.insert(0, "50000")
                
                self.speed_increment.delete(0, tk.END)
                self.speed_increment.insert(0, "5000")
                
                # Punteriz Ayarları
                self.punteriz_enabled.set(False)
                self.punteriz_start.configure(state='disabled')
                self.punteriz_end.configure(state='disabled')
                self.punteriz_start.delete(0, tk.END)
                self.punteriz_start.insert(0, "0")
                self.punteriz_end.delete(0, tk.END)
                self.punteriz_end.insert(0, "0")
                
                # Üst İp Sıkma Bobini Ayarları
                self.bobbin_enabled.set(False)
                self.bobbin_reset_value.configure(state='disabled')
                self.bobbin_reset_value.delete(0, tk.END)
                self.bobbin_reset_value.insert(0, "1")
                
                # Buton metnini sıfırla
                self.update_button.configure(text="G-Code Oluştur")
                self.is_first_generation = True
                
                messagebox.showinfo("Başarılı", "Parametreler varsayılan değerlere sıfırlandı.")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Parametreler sıfırlanırken hata oluştu: {str(e)}")

    def toggle_bobbin_input(self):
        """Checkbox durumuna göre input alanını etkinleştir/devre dışı bırak"""
        if self.bobbin_enabled.get():
            # Checkbox seçildiğinde
            self.bobbin_reset_value.configure(state='normal')
            # Boşsa varsayılan değer olarak 1 gir
            if not self.bobbin_reset_value.get().strip():
                self.bobbin_reset_value.insert(0, "1")
        else:
            # Checkbox seçimi kaldırıldığında
            self.bobbin_reset_value.configure(state='disabled')

    def toggle_punteriz_input(self):
        """Checkbox durumuna göre input alanlarını etkinleştir/devre dışı bırak"""
        if self.punteriz_enabled.get():
            # Checkbox seçildiğinde
            self.punteriz_start.configure(state='normal')
            self.punteriz_end.configure(state='normal')
            # Boşsa varsayılan değer olarak 1 gir
            if not self.punteriz_start.get().strip():
                self.punteriz_start.insert(0, "1")
            if not self.punteriz_end.get().strip():
                self.punteriz_end.insert(0, "1")
        else:
            # Checkbox seçimi kaldırıldığında
            self.punteriz_start.configure(state='disabled')
            self.punteriz_end.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = GCodeEditorGUI(root)
    root.mainloop() 