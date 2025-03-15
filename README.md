# Modern G-CODE Editor Uygulaması

Bu uygulama, G-CODE dosyalarını düzenlemek ve işlemek için geliştirilmiş modern bir arayüz sunar. PyQt5 kütüphanesi kullanılarak oluşturulmuştur ve MVC (Model-View-Controller) tasarım deseni ile geliştirilmiştir.

## Özellikler

- Modern ve kullanıcı dostu arayüz
- MVC tasarım deseni ile modüler yapı
- Açık tema (light mode) desteği
- Tam ekran açılış
- Parametreleri kolayca düzenleme imkanı
- G-CODE dosyalarını yükleme ve kaydetme
- Rota işleme ve koordinat kalibrasyonu
- Punteriz ve Üst İp Sıkma Bobini ayarları
- Dikiş hızı kontrolü
- Otomatik parametre kaydetme ve yükleme

## Proje Yapısı

Uygulama, MVC (Model-View-Controller) tasarım deseni kullanılarak geliştirilmiştir:

- **models/**: Veri ve iş mantığı
  - `gcode_model.py`: G-CODE verilerini ve işlemlerini yöneten model sınıfı

- **views/**: Kullanıcı arayüzü
  - `main_view.py`: Ana görünüm sınıfı

- **controllers/**: Model ve View arasındaki iletişim
  - `main_controller.py`: Ana controller sınıfı

- **utils/**: Yardımcı sınıflar ve fonksiyonlar
  - `styles.py`: Stil yönetimi için yardımcı sınıf

## Klasör Yapısı

Uygulama aşağıdaki klasörleri kullanır:

- **Rotalar/**: Rota dosyalarının bulunduğu klasör (otomatik oluşturulur)
- **gcode_output/**: Oluşturulan G-CODE dosyalarının kaydedildiği klasör (otomatik oluşturulur)

## Kurulum

1. Gerekli kütüphaneleri yükleyin:
```
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:
```
python main.py
```

veya `run_app.bat` dosyasını çalıştırın.

## Kullanım

1. **Parametreleri Ayarlama**: Sol paneldeki parametreleri ihtiyacınıza göre düzenleyin.
2. **Dosya Yükleme**: "Dosya Yükle" butonuna tıklayarak Rotalar klasöründeki .nc dosyalarını yükleyin.
3. **G-CODE Oluşturma**: "G-Code Oluştur" butonuna tıklayarak parametreleri uygulayın ve G-CODE'u oluşturun.
4. **Dosya Kaydetme**: "Dosya Kaydet" butonuna tıklayarak oluşturulan G-CODE'u gcode_output klasörüne kaydedin.

## Parametre Yönetimi

Uygulama, parameters.json dosyasını kullanarak parametreleri otomatik olarak yükler ve kaydeder. Bu dosya, uygulama klasöründe bulunur ve aşağıdaki parametreleri içerir:

- G-Code Başlangıç Parametreleri
- Rota Başlangıç Parametreleri
- İp Kesme Parametreleri
- G-Code Sonu Parametreleri
- Z Pozisyonları
- Makine Kalibrasyon Değerleri

## Geliştirme

Bu uygulama, Tkinter tabanlı eski sürümün PyQt5 ile modernize edilmiş ve MVC tasarım deseni ile yeniden yapılandırılmış halidir. Aynı işlevselliği korurken daha profesyonel, modüler ve kullanıcı dostu bir arayüz sunmaktadır. 