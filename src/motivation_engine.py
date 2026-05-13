import random

class MotivationEngine:
    def __init__(self):
        """
        Kullanıcının durumuna ve aktivitesine göre motivasyon mesajları üretir.
        """
        pass

    def get_message(self, state, user_context):
        """
        Mevcut duruma göre mesaj döndürür.
        :param state: "Dikkatli", "Dikkati Dağılmış", "Yorgun / Uykulu"
        :param user_context: dict, "activity" ve "goal" içerir
        :return: Motivasyon mesajı (string)
        """
        activity = user_context.get("activity", "Genel odaklanma")
        goal = user_context.get("goal", "").strip()
        
        goal_text = f" Unutma, hedefin: '{goal}'." if goal else ""

        if state == "Yorgun / Uykulu":
            messages = [
                "Gözlerinde yorgunluk belirtileri var. 5 dakikalık kısa bir mola performansını artırabilir.",
                "Ekrana çok uzun süre baktın gibi görünüyor. Gözlerini dinlendirmenin vakti gelmiş olabilir.",
                f"Yorgun görünüyorsun. Hedefine ({goal}) sağlıklı ulaşmak için biraz dinlenmelisin." if goal else "Yorgun görünüyorsun. Kısa bir mola iyi gelecektir."
            ]
            return random.choice(messages)
            
        elif state == "Dikkati Dağılmış":
            if activity == "Sınava hazırlanıyorum":
                base_msgs = [
                    "Dikkatin biraz dağıldı. Sınav başarısı için odağını toplamalısın.",
                    "Başka yerlere bakıyorsun. Haydi, sınava hazırlanmaya geri dönelim!"
                ]
            elif activity == "Kod yazıyorum":
                base_msgs = [
                    "Bug'lar seni bekliyor! Kodlamaya geri dönmelisin.",
                    "Dikkatin dağıldı. Ekrana dön ve kodunu yazmaya devam et."
                ]
            elif activity == "Kitap okuyorum":
                base_msgs = [
                    "Kitaptan uzaklaştın gibi görünüyor. Sayfalar seni bekliyor.",
                    "Okuma ritmini kaybetme, hadi kitaba geri dön."
                ]
            else:
                base_msgs = [
                    "Dikkatin biraz dağıldı. Kısa bir toparlanma ile devam edebilirsin.",
                    "Odağını kaybetmiş görünüyorsun. Lütfen çalışmana geri dön."
                ]
            
            msg = random.choice(base_msgs) + goal_text
            return msg
            
        else: # Dikkatli
            messages = [
                "Harika gidiyorsun. Odağını koruyarak hedefine yaklaşıyorsun.",
                "Süper! Tamamen odaklanmış durumdasın.",
                f"İşte böyle! '{goal}' hedefine emin adımlarla ilerliyorsun." if goal else "İşte böyle! Mükemmel odaklanma."
            ]
            return random.choice(messages)
