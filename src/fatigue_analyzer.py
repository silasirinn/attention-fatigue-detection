class FatigueAnalyzer:
    def __init__(self, ear_threshold=0.25, consecutive_frames_threshold=15):
        """
        Yorgunluk analizi için eşik değerleri.
        :param ear_threshold: Göz kapalı sayılacak EAR sınırı
        :param consecutive_frames_threshold: Kaç kare (frame) boyunca kapalı kalırsa uyarı verecek
        """
        self.ear_threshold = ear_threshold
        self.consecutive_frames_threshold = consecutive_frames_threshold
        self.closed_frames_counter = 0

    def analyze(self, ear_value):
        """
        Anlık EAR değerine göre yorgunluk/uyku durumunu analiz eder.
        :param ear_value: Anlık hesaplanan EAR değeri
        :return: (is_fatigued, message)
        """
        is_fatigued = False
        message = ""

        if ear_value < self.ear_threshold:
            self.closed_frames_counter += 1
            if self.closed_frames_counter >= self.consecutive_frames_threshold:
                is_fatigued = True
                message = "Yorgunluk / Uykulu: Göz kapanma süresi arttı!"
        else:
            self.closed_frames_counter = max(0, self.closed_frames_counter - 1)
            
        return is_fatigued, message

    def get_fatigue_score(self):
        """
        Kapanma sayacına bağlı basit bir yorgunluk skoru (0-100) döndürür.
        """
        score = (self.closed_frames_counter / self.consecutive_frames_threshold) * 100
        return min(100.0, score)
