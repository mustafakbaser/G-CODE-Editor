import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
from gcode_processor import GCodeProcessor

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
        scroll_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5,0))
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
        
        ttk.Label(scrollable_frame, text="Rota Başlangıç Parametreleri:", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(0,5))
        self.route_start_params_text = scrolledtext.ScrolledText(scrollable_frame, width=30, height=4)
        self.route_start_params_text.grid(row=3, column=0, pady=(0, 10))
       
        # Bu silinecek
        ttk.Label(scrollable_frame, text="Rota Sonu Parametreleri:", style='Header.TLabel').grid(row=4, column=0, sticky=tk.W, pady=(0,5))
        self.route_end_params_text = scrolledtext.ScrolledText(scrollable_frame, width=30, height=4)
        self.route_end_params_text.grid(row=5, column=0, pady=(0, 10))
        
        ttk.Label(scrollable_frame, text="G-Code Sonu Parametreleri:", style='Header.TLabel').grid(row=6, column=0, sticky=tk.W, pady=(0,5))
        self.end_params_text = scrolledtext.ScrolledText(scrollable_frame, width=30, height=4)
        self.end_params_text.grid(row=7, column=0, pady=(0, 10))
        
        ttk.Label(scrollable_frame, text="İp Kesme Parametreleri:", style='Header.TLabel').grid(row=8, column=0, sticky=tk.W, pady=(0,5))
        self.thread_cut_params_text = scrolledtext.ScrolledText(scrollable_frame, width=30, height=2)
        self.thread_cut_params_text.grid(row=9, column=0, pady=(0, 10))
        
        ttk.Label(scrollable_frame, text="Güvenli G0 Rota Tayini:", style='Header.TLabel').grid(row=10, column=0, sticky=tk.W, pady=(0,5))
        self.safe_route_params_text = scrolledtext.ScrolledText(scrollable_frame, width=30, height=2)
        self.safe_route_params_text.grid(row=11, column=0, pady=(0, 10))

        ttk.Separator(scrollable_frame, orient='horizontal').grid(row=12, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # İğne Batma ve Geri Çekilme Pozisyonları: Z değerleri
        ttk.Label(scrollable_frame, text="İğne Batma Pozisyonu (Z3):", style='Header.TLabel').grid(row=13, column=0, sticky=tk.W, pady=(0,5))
        self.needle_down_pos = ttk.Entry(scrollable_frame, width=40)
        self.needle_down_pos.grid(row=14, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(scrollable_frame, text="İğnenin Geri Çekilme Pozisyonu (Z30):", style='Header.TLabel').grid(row=15, column=0, sticky=tk.W, pady=(0,5))
        self.needle_up_pos = ttk.Entry(scrollable_frame, width=40)
        self.needle_up_pos.grid(row=16, column=0, sticky=tk.W, pady=(0, 10))

        ttk.Separator(scrollable_frame, orient='horizontal').grid(row=17, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Üst İp Sıkma Bobini bölümü
        ttk.Label(scrollable_frame, text="Üst İp Sıkma Bobini (M118-M119):", style='Header.TLabel').grid(row=18, column=0, sticky=tk.W, pady=(0,5))
        
        # Checkbox ve değer girme alanı için frame
        bobbin_frame = ttk.Frame(scrollable_frame)
        bobbin_frame.grid(row=19, column=0, sticky=tk.W, pady=(0, 10))
        
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
        
        ttk.Separator(scrollable_frame, orient='horizontal').grid(row=20, column=0, sticky=(tk.W, tk.E), pady=10)

        # Makine Kalibrasyon Değerleri (X ve Y) - row numaralarını güncelle
        ttk.Label(scrollable_frame, text="Makine Kalibrasyon Değerleri:", style='Header.TLabel').grid(row=21, column=0, sticky=tk.W, pady=(0,5))
        
        # X ve Y değerleri için frame
        calibration_frame = ttk.Frame(scrollable_frame)
        calibration_frame.grid(row=22, column=0, sticky=tk.W, pady=(0, 10))
        
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
        
        # Alt kısım (butonlar)
        button_frame = ttk.Frame(main_param_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Üst sıra butonları
        top_button_frame = ttk.Frame(button_frame)
        top_button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        top_button_frame.columnconfigure(0, weight=1)
        top_button_frame.columnconfigure(1, weight=1)
        
        # G-Code Oluştur ve Parametreleri Sıfırla butonları
        self.update_button = ttk.Button(top_button_frame, 
                                      text="G-Code Oluştur",
                                      width=22,
                                      style='Action.TButton',
                                      command=self.update_parameters)
        self.update_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(top_button_frame, 
                  text="Parametreleri Sıfırla",
                  width=22,
                  style='Action.TButton',
                  command=self.reset_parameters).grid(row=0, column=1, padx=5)
        
        # Alt sıra butonları
        bottom_button_frame = ttk.Frame(button_frame)
        bottom_button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        bottom_button_frame.columnconfigure(0, weight=1)
        bottom_button_frame.columnconfigure(1, weight=1)
        
        # Dosya Yükle ve Kaydet butonları
        ttk.Button(bottom_button_frame, 
                  text="Dosya Yükle",
                  width=22,
                  style='Action.TButton',
                  command=self.load_file).grid(row=0, column=0, padx=5)
        
        ttk.Button(bottom_button_frame, 
                  text="Dosya Kaydet",
                  width=22,
                  style='Action.TButton',
                  command=self.save_file).grid(row=0, column=1, padx=5)
        
        # Grid yapılandırması
        main_param_frame.columnconfigure(0, weight=1)
        main_param_frame.rowconfigure(0, weight=1)
        main_param_frame.rowconfigure(1, weight=0)  # Butonlar için sabit yükseklik

    def create_right_panel(self):
        # Ana çerçeve
        main_right_frame = ttk.Frame(self.right_panel)
        main_right_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.right_panel.rowconfigure(0, weight=1)
        self.right_panel.columnconfigure(0, weight=1)
        
        # G-Code içerik alanı
        content_frame = ttk.LabelFrame(main_right_frame, text="G-Code İçeriği", style='Parameter.TLabelframe')
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        self.text_area = scrolledtext.ScrolledText(content_frame, width=50, height=40)
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Grid yapılandırması
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
                
                # Rota Sonu Parametreleri
                route_end_params = '\n'.join(params.get('route_end_params', []))
                self.route_end_params_text.delete('1.0', tk.END)
                self.route_end_params_text.insert('1.0', route_end_params)
                
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
            
            # Diğer parametreleri güncelle
            self.processor.start_params = self.start_params_text.get('1.0', tk.END).strip().split('\n')
            self.processor.route_start_params = self.route_start_params_text.get('1.0', tk.END).strip().split('\n')
            self.processor.route_end_params = self.route_end_params_text.get('1.0', tk.END).strip().split('\n')
            self.processor.thread_cut_params = self.thread_cut_params_text.get('1.0', tk.END).strip().split('\n')
            self.processor.end_params = self.end_params_text.get('1.0', tk.END).strip().split('\n')
            
            # Kalibrasyon, Z değerleri ve Bobini ayarlarını güncelle
            self.processor.update_calibration_values(calibration_x, calibration_y)
            self.processor.update_z_positions(needle_down, needle_up)
            self.processor.update_bobbin_settings(bobbin_enabled, bobbin_reset_value)
            
            # Mevcut içeriği güncelle
            self.process_file()
            
            # İlk kullanımdan sonra buton metnini güncelle
            if self.is_first_generation:
                self.update_button.configure(text="Parametreleri Güncelle")
                self.is_first_generation = False
            
            messagebox.showinfo("Başarılı", "Parametreler güncellendi.")
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {str(e)}")

    def load_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("G-CODE dosyaları", "*.nc;*.gcode"), ("Tüm dosyalar", "*.*")])
        if filename:
            try:
                with open(filename, 'r') as file:
                    content = file.read()
                    # İlk yüklemede koordinatları işle
                    processed_content = self.processor.load_file_content(content)
                    self.text_area.delete('1.0', tk.END)
                    self.text_area.insert('1.0', processed_content)
                    # Yeni dosya yüklendiğinde buton metnini sıfırla
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
            content = self.text_area.get('1.0', tk.END)
            self.processor.reset_route_counter()
            processed_content = self.processor.process_gcode(content)
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', processed_content)
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {str(e)}")

    def reset_parameters(self):
        try:
            self.load_default_parameters()
            self.update_parameters()
            messagebox.showinfo("Başarılı", "Parametreler varsayılan değerlere sıfırlandı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Parametreler sıfırlanırken hata oluştu: {str(e)}")

    def toggle_bobbin_input(self):
        """Checkbox durumuna göre input alanını etkinleştir/devre dışı bırak"""
        if self.bobbin_enabled.get():
            self.bobbin_reset_value.configure(state='normal')
        else:
            self.bobbin_reset_value.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = GCodeEditorGUI(root)
    root.mainloop() 