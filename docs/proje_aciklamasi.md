# Gerçek Zamanlı Dikkat ve Yorgunluk Tespit Sistemi

## Projenin Amacı ve Kapsamı
Bu proje, bilgisayarlı görü (Computer Vision) teknikleri kullanarak gerçek zamanlı video akışı üzerinden kullanıcının dikkat ve yorgunluk durumunu analiz etmeyi amaçlar. Günümüzde uzun süreli ekran başında çalışma, odak kaybına ve yorgunluğa neden olabilmektedir. Bu sistem, kullanıcının durumunu algılayarak ona özel motivasyon ve toparlanma bildirimleri sunar.

Özellikle sistemin sadece bir "tespit" aracı olmaktan çıkıp bir **"AI Koçu"** gibi davranmasını sağlayan `MotivationEngine` yapısı, kullanıcının belirlediği hedeflere ve seçtiği aktiviteye göre kişiselleştirilmiş geri bildirim üretir.

## Mimari ve Kullanılan Yöntemler

Proje şu anda **Kural Tabanlı (Rule-based)** bir yaklaşımla çalışmaktadır. İleride makine öğrenmesi modellerinin (örneğin LSTM, Random Forest) entegre edilebilmesi için kod yapısı olabildiğince modüler tutulmuştur.

### 1. Göz Açıklık Oranı (Eye Aspect Ratio - EAR)
MediaPipe Face Mesh tarafından sağlanan 468 yüz koordinatından (landmark) sağ ve sol göz çevresindekiler alınır. EAR formülü kullanılarak gözlerin ne kadar açık olduğu hesaplanır. 
Eğer EAR değeri belirlenen bir eşiğin (threshold) altına düşer ve bu durum belirli bir süre devam ederse (örneğin 10-15 kare boyunca), sistem kullanıcının "Yorgun / Uykulu" olduğuna karar verir.

### 2. Baş Pozu Tahmini (Head Pose Estimation)
Yüzün genel yönelimini bulmak için standart bir 3D yüz modeli ile görüntü üzerindeki 2D landmarklar (Burun ucu, çene, göz ve ağız kenarları) eşleştirilir. `cv2.solvePnP` kullanılarak başın sağa/sola (Yaw), yukarı/aşağı (Pitch) ve yatırma (Roll) açıları hesaplanır.
Eğer kullanıcı uzun süre kameraya doğrudan bakmıyorsa (açılar çok büyürse) veya ekranda bir yüz bulunamazsa, sistem "Dikkati Dağılmış" durumuna geçer.

### 3. Kullanıcı Bağlamı ve Motivasyon Motoru
Sistem, arayüz üzerinden kullanıcının şu anda ne yaptığını (Aktivite) ve kısa vadeli hedefini alır. 
Eğer bir dikkat dağınıklığı tespit edilirse, `MotivationEngine` devreye girerek seçilen aktivite tipine (örneğin "Kod yazıyorum" vs "Ders çalışıyorum") uygun olarak toparlanmayı hatırlatacak, kişiselleştirilmiş Türkçe motivasyon mesajları üretir.

## Dosya Yapısı

- `src/camera.py`: Kamera açma/kapama ve kare okuma işlemleri.
- `src/face_detector.py`: MediaPipe Face Mesh entegrasyonu.
- `src/feature_extractor.py`: Landmarklar üzerinden EAR ve Baş Pozu algoritmalarının implementasyonu.
- `src/fatigue_analyzer.py`: EAR değerinin zamansal takibi ve yorgunluk teşhisi.
- `src/attention_analyzer.py`: Baş açılarına ve yüz görünürlüğüne göre dikkat teşhisi.
- `src/user_context.py`: Kullanıcının hedefi ve aktivite durumunu tutan veri yapısı.
- `src/motivation_engine.py`: Duruma ve bağlama göre kişiselleştirilmiş "AI Koç" mesajı üreten birim.
- `app.py`: Streamlit ile hazırlanmış ana arayüz dosyasıdır, tüm bileşenlerin birbiriyle konuşmasını sağlar.
