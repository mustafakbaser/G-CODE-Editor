import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from gcode_processor import GCodeProcessor

class GCodeEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("G-CODE Düzenleyici")
        self.processor = GCodeProcessor()
        
        # Ana çerçeve
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Dosya işlemleri
        ttk.Button(self.main_frame, text="Dosya Yükle", command=self.load_file).grid(row=0, column=0, pady=5)
        ttk.Button(self.main_frame, text="Dosya Kaydet", command=self.save_file).grid(row=0, column=1, pady=5)
        
        # Parametre girişleri
        self.create_parameter_inputs()
        
        # Metin alanı
        self.text_area = tk.Text(self.main_frame, width=60, height=20)
        self.text_area.grid(row=2, column=0, columnspan=2, pady=5)
        
        # İşlem düğmesi
        ttk.Button(self.main_frame, text="Düzenle", command=self.process_file).grid(row=3, column=0, columnspan=2, pady=5)

    def create_parameter_inputs(self):
        param_frame = ttk.LabelFrame(self.main_frame, text="Parametreler", padding="5")
        param_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Parametre dosyası yükleme
        ttk.Button(param_frame, text="Parametre Dosyası Yükle", 
                  command=self.load_parameters).grid(row=0, column=0, columnspan=2, pady=5)

    def load_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("G-CODE dosyaları", "*.nc;*.gcode"), ("Tüm dosyalar", "*.*")])
        if filename:
            try:
                with open(filename, 'r') as file:
                    content = file.read()
                    self.text_area.delete('1.0', tk.END)
                    self.text_area.insert('1.0', content)
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

    def load_parameters(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON dosyaları", "*.json"), ("Tüm dosyalar", "*.*")])
        if filename:
            try:
                self.processor.load_parameters(filename)
                # Parametre yüklendiğinde mevcut koordinatları işle
                content = self.text_area.get('1.0', tk.END)
                self.processor.reset_route_counter()
                processed_content = self.processor.process_gcode(content)
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert('1.0', processed_content)
                messagebox.showinfo("Başarılı", "Parametreler başarıyla yüklendi ve uygulandı.")
            except Exception as e:
                messagebox.showerror("Hata", f"Parametreler yüklenirken hata oluştu: {str(e)}")

    def process_file(self):
        try:
            content = self.text_area.get('1.0', tk.END)
            self.processor.reset_route_counter()
            processed_content = self.processor.process_gcode(content)
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', processed_content)
            messagebox.showinfo("Başarılı", "G-CODE başarıyla düzenlendi.")
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GCodeEditorGUI(root)
    root.mainloop() 