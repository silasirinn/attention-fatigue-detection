class AttentionAnalyzer:
    def __init__(self, pitch_threshold=20.0, yaw_threshold=25.0):
        """
        Dikkat analizi için eşik değerleri (Derece cinsinden).
        :param pitch_threshold: Başın yukarı/aşağı tolerans açısı
        :param yaw_threshold: Başın sağa/sola tolerans açısı
        """
        self.pitch_threshold = pitch_threshold
        self.yaw_threshold = yaw_threshold
        self.distracted_frames = 0
        self.attention_score = 100.0

    def analyze(self, face_detected, pitch=0.0, yaw=0.0):
        """
        Yüz görünürlüğü ve baş açısına göre dikkat durumunu değerlendirir.
        :param face_detected: Ekranda yüz var mı?
        :param pitch: Yukarı/Aşağı baş açısı
        :param yaw: Sağa/Sola baş açısı
        :return: (is_distracted, message)
        """
        is_distracted = False
        message = ""

        if not face_detected:
            self.distracted_frames += 1
            is_distracted = True
            message = "Dikkati Dağılmış: Yüz kameradan uzaklaştı!"
        else:
            # Açıların mutlak değeri üzerinden kontrol
            if abs(pitch) > self.pitch_threshold or abs(yaw) > self.yaw_threshold:
                self.distracted_frames += 1
                is_distracted = True
                message = "Dikkati Dağılmış: Kullanıcı başka yöne bakıyor!"
            else:
                self.distracted_frames = max(0, self.distracted_frames - 1)

        # Basit bir dikkat skoru güncellemesi
        if is_distracted:
            self.attention_score = max(0.0, self.attention_score - 2.0)
        else:
            self.attention_score = min(100.0, self.attention_score + 1.0)

        return is_distracted, message

    def get_attention_score(self):
        return self.attention_score
