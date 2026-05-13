class UserContext:
    def __init__(self):
        """
        Kullanıcının mevcut aktivitesini ve hedefini saklar.
        """
        self.activity = "Genel odaklanma"
        self.goal = ""
        self.start_time = None

    def update_context(self, activity, goal):
        """
        Kullanıcının aktivite ve hedefini günceller.
        :param activity: Seçilen aktivite (Örn: Ders çalışıyorum)
        :param goal: Kullanıcı hedefi (Örn: 30 sayfa kitap okuyacağım)
        """
        self.activity = activity
        self.goal = goal

    def get_context(self):
        return {
            "activity": self.activity,
            "goal": self.goal
        }
