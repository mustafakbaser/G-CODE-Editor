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
        self.main_frame.columnconfigure(1, weight=3)  # Sağ panel daha geniş
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
        # G-Code Başlangıç Parametreleri
        param_frame = ttk.LabelFrame(self.left_panel, text="Parametreler", style='Parameter.TLabelframe')
        param_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        ttk.Label(param_frame, text="G-Code Başlangıç Parametreleri:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0,5))
        self.start_params_text = scrolledtext.ScrolledText(param_frame, width=35, height=4)
        self.start_params_text.grid(row=1, column=0, pady=(0, 10))
        
        ttk.Label(param_frame, text="Rota Başlangıç Parametreleri:", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(0,5))
        self.route_start_params_text = scrolledtext.ScrolledText(param_frame, width=35, height=4)
        self.route_start_params_text.grid(row=3, column=0, pady=(0, 10))
        
        ttk.Label(param_frame, text="Rota Sonu Parametreleri:", style='Header.TLabel').grid(row=4, column=0, sticky=tk.W, pady=(0,5))
        self.route_end_params_text = scrolledtext.ScrolledText(param_frame, width=35, height=4)
        self.route_end_params_text.grid(row=5, column=0, pady=(0, 10))
        
        ttk.Label(param_frame, text="G-Code Sonu Parametreleri:", style='Header.TLabel').grid(row=6, column=0, sticky=tk.W, pady=(0,5))
        self.end_params_text = scrolledtext.ScrolledText(param_frame, width=35, height=4)
        self.end_params_text.grid(row=7, column=0, pady=(0, 10))
        
        ttk.Label(param_frame, text="İp Kesme Parametresi:", style='Header.TLabel').grid(row=8, column=0, sticky=tk.W, pady=(0,5))
        self.thread_cut_params_text = scrolledtext.ScrolledText(param_frame, width=35, height=2)
        self.thread_cut_params_text.grid(row=9, column=0, pady=(0, 10))
        
        ttk.Label(param_frame, text="Güvenli G0 Rota Tayini:", style='Header.TLabel').grid(row=10, column=0, sticky=tk.W, pady=(0,5))
        self.safe_route_params_text = scrolledtext.ScrolledText(param_frame, width=35, height=2)
        self.safe_route_params_text.grid(row=11, column=0, pady=(0, 10))
        
        # Buton çerçevesi
        button_frame = ttk.Frame(param_frame)
        button_frame.grid(row=12, column=0, pady=10)
        
        # Güncelleme butonu için sabit genişlik
        self.update_button = ttk.Button(button_frame, 
                                      text="G-Code Oluştur",
                                      width=20,  # Sabit genişlik
                                      style='Action.TButton',
                                      command=self.update_parameters)
        self.update_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text="Parametreleri Sıfırla",
                  width=20,  # Sabit genişlik 
                  style='Action.TButton',
                  command=self.reset_parameters).grid(row=0, column=1, padx=5)

    def create_right_panel(self):
        # Üst buton çerçevesi
        button_frame = ttk.Frame(self.right_panel)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        button_frame.columnconfigure(1, weight=1)  # Ortadaki boşluk için
        
        # Sol butonlar
        ttk.Button(button_frame, text="Dosya Yükle", 
                  style='Action.TButton',
                  command=self.load_file).grid(row=0, column=0, padx=5)
        
        # Sağ butonlar
        ttk.Button(button_frame, text="Dosya Kaydet", 
                  style='Action.TButton',
                  command=self.save_file).grid(row=0, column=2, padx=5)
        
        # G-Code içerik alanı
        content_frame = ttk.LabelFrame(self.right_panel, text="G-Code İçeriği", style='Parameter.TLabelframe')
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        self.text_area = scrolledtext.ScrolledText(content_frame, width=60, height=40)
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    def load_default_parameters(self):
        # G-Code Başlangıç Parametreleri
        start_params = '#MW6789 = 219\nM115\nG04 P200\nX5 Y26\nX50 Y50'
        self.start_params_text.delete('1.0', tk.END)
        self.start_params_text.insert('1.0', start_params)
        
        # Rota Başlangıç Parametreleri
        route_start_params = 'M114\nG04 P200\nM118\nZ3\nZ30\nM119'
        self.route_start_params_text.delete('1.0', tk.END)
        self.route_start_params_text.insert('1.0', route_start_params)
        
        # Rota Sonu Parametreleri
        route_end_params = '''G04 P50\nM124\nG04 P50\nM112\nG04 P150\nF2000\nZ1\nF10000
G04 P50\nM120\nG04 P500\nM121\nG04 P50\nM125\nG04 P50\nM113\nG04 P50\nG91\nG1
Z-5\nG04 P80\nM126\nG04 P100\nM127\nG04 P200\nG90\nZ0\nM115\nG04 P200'''
        self.route_end_params_text.delete('1.0', tk.END)
        self.route_end_params_text.insert('1.0', route_end_params)
        
        # G-Code Sonu Parametreleri
        end_params = '''G04 P50\nM124\nG04 P50\nM112\nG04 P150\nF2000\nZ1\nF10000
G04 P50\nM120\nG04 P500\nM121\nG04 P50\nM125\nG04 P50\nM113\nG04 P50\nG91\nG1
Z-5\nG04 P80\nM126\nG04 P100\nM127\nG04 P200\nG90\nZ0\nM115\nG04 P200\nF10000
X50 Y50\nX5 Y26\nM111\nM2'''
        self.end_params_text.delete('1.0', tk.END)
        self.end_params_text.insert('1.0', end_params)

    def update_parameters(self):
        try:
            # Parametreleri metin alanlarından al ve processor'a aktar
            self.processor.start_params = self.start_params_text.get('1.0', tk.END).strip().split('\n')
            self.processor.route_start_params = self.route_start_params_text.get('1.0', tk.END).strip().split('\n')
            self.processor.route_end_params = self.route_end_params_text.get('1.0', tk.END).strip().split('\n')
            self.processor.end_params = self.end_params_text.get('1.0', tk.END).strip().split('\n')
            
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
                    self.text_area.delete('1.0', tk.END)
                    self.text_area.insert('1.0', content)
                    # Yeni dosya yüklendiğinde buton metnini sıfırla
                    self.update_button.configure(text="G-Code Oluştur")
                    self.is_first_generation = True
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya yüklenirken hata oluştu: {str(e)}")

    def save_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".nc",
            filetypes=[("G-CODE dosyaları", "*.nc;*.gcode"), ("Tüm dosyalar", "*.*")])
        if filename:
            try:
                content = self.text_area.get('1.0', tk.END)
                with open(filename, 'w') as file:
                    file.write(content)
                messagebox.showinfo("Başarılı", "Dosya başarıyla kaydedildi.")
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

if __name__ == "__main__":
    root = tk.Tk()
    app = GCodeEditorGUI(root)
    root.mainloop() 