# Gerçek Zamanlı Dikkat ve Yorgunluk Tespit Sistemi 👁️

Bu proje, webcam üzerinden gerçek zamanlı yüz landmark (nokta) analizi yaparak kullanıcının **dikkat dağınıklığı** ve **yorgunluk/uyku** durumunu tespit eden bilgisayarlı görü tabanlı bir sistemdir. Aynı zamanda kullanıcının seçtiği çalışma aktivitesi ve hedefine göre **kişiselleştirilmiş motivasyon mesajları (AI Koçu)** üreterek odaklanmaya yardımcı olur.

## Proje Amacı
Gün boyu ekran başında çalışan, ders çalışan veya kod yazan bireylerin farkında olmadan yaşadığı dikkat kaybı ve uyku halini gerçek zamanlı tespit etmek, toparlanmaları için onlara hedeflerini hatırlatarak verimliliklerini artırmaktır.

## Kullanılan Teknolojiler
- **Python**: Ana programlama dili.
- **OpenCV**: Görüntü işleme ve baş pozisyonu (Head Pose Estimation) matematiksel hesaplamaları (`cv2.solvePnP`).
- **MediaPipe Face Mesh**: Yüksek performanslı, 468 noktalı gerçek zamanlı yüz analizi.
- **NumPy**: Landmark koordinatları arası Öklid mesafesi hesaplamaları (EAR - Eye Aspect Ratio hesabı için).
- **Streamlit**: Modern ve etkileşimli kullanıcı arayüzü.

## Sistem Mimarisi ve Özellikler
Bu sistem mevcut haliyle **kural tabanlı (rule-based)** ve matematiksel modeller üzerine kuruludur, ileride makine öğrenmesi modellerinin eklenebilmesi için modüler bir yapıda tasarlanmıştır.

1. **Yorgunluk Tespiti**: Göz açıklık oranı (EAR) belirli bir eşiğin altına düşerse ve bu kapalı kalma süresi artarsa sistem yorgunluk/uyku uyarısı verir.
2. **Dikkat Dağınıklığı Tespiti**: Burun, çene ve göz kenarlarından oluşan 3D-2D eşleştirmesi ile başın Yaw (sağa/sola) ve Pitch (yukarı/aşağı) açıları hesaplanır. Kullanıcı başka bir yöne bakıyorsa dikkat dağınıklığı tespit edilir.
3. **Kişiselleştirilmiş Motivasyon**: Kullanıcı, arayüzden mevcut aktivitesini (Örn: Sınava hazırlık, kod yazma) ve hedefini girer. Sistem durum analizine göre bu aktiviteye özel Türkçe uyarılarda bulunur.
4. **Gerçek Zamanlı Skorlama**: Kullanıcının dikkat ve yorgunluk skorları anlık olarak Streamlit arayüzünde gösterilir.

Daha fazla teknik detay için [docs/proje_aciklamasi.md](docs/proje_aciklamasi.md) dosyasına göz atabilirsiniz.

## Kurulum Adımları

1. Repoyu klonlayın veya indirin:
```bash
git clone <repo-url>
cd attention-fatigue-detection
```

2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

## Çalıştırma Komutları

Uygulamayı başlatmak için terminal veya komut satırına şu komutu girin:
```bash
streamlit run app.py
```
Açılan tarayıcı penceresinden (genellikle `http://localhost:8501`) uygulamanızı kullanmaya başlayabilirsiniz. Kamerayı başlatmak için "Kamerayı Başlat" butonuna tıklamanız yeterlidir.

## Ekran Görüntüsü
> (Projenizi çalıştırdıktan sonra buraya arayüzden alınmış bir ekran görüntüsünü (assets/demo_images/demo1.png) ekleyebilirsiniz.)

## Gelecek Geliştirmeler
- Elde edilen EAR ve baş pozisyonu verilerinin zaman serisi olarak kaydedilip bir **LSTM** veya **Random Forest** makine öğrenmesi modeli ile sınıflandırılması.
- Günlük verimlilik raporlarının grafiksel olarak sunulması.
- Göz kırpma frekansı (Blink Rate) analizinin sisteme dahil edilmesi.

---

### CV İçin Proje Açıklaması
**TR:**
*“OpenCV ve MediaPipe kullanarak webcam görüntüsü üzerinden yüz landmark analizi yapan, göz kapanma süresi ve baş pozisyonu gibi özelliklerden dikkat ve yorgunluk durumunu gerçek zamanlı sınıflandıran bilgisayarlı görü tabanlı bir sistem geliştirdim. İçerisinde, kullanıcının hedeflerine ve çalışma tipine göre dinamik geri bildirim sağlayan bir kural tabanlı motivasyon motoru bulunmaktadır.”*

**EN (For Resume):**
*“Developed a real-time computer vision system that analyzes facial landmarks, eye closure duration, and head position using OpenCV and MediaPipe to detect attention loss and fatigue from webcam input. Integrated a context-aware motivation engine providing personalized feedback based on user activity goals.”*
