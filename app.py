import streamlit as st
import cv2
import time

from src.camera import Camera
from src.face_detector import FaceDetector
from src.feature_extractor import FeatureExtractor
from src.fatigue_analyzer import FatigueAnalyzer
from src.attention_analyzer import AttentionAnalyzer
from src.user_context import UserContext
from src.motivation_engine import MotivationEngine
from src.utils import draw_text_with_background


st.set_page_config(
    page_title="Dikkat & Yorgunluk Tespit",
    page_icon="👁️",
    layout="wide"
)

# --- Session State Başlatma ---
if "run_camera" not in st.session_state:
    st.session_state.run_camera = False

if "user_context" not in st.session_state:
    st.session_state.user_context = UserContext()

if "motivation_engine" not in st.session_state:
    st.session_state.motivation_engine = MotivationEngine()


# --- Sidebar ---
st.sidebar.title("Ayarlar ve Hedefler")
st.sidebar.markdown("Lütfen mevcut çalışma durumunuzu belirtin.")

activity_options = [
    "Ders çalışıyorum",
    "Kod yazıyorum",
    "Kitap okuyorum",
    "Sınava hazırlanıyorum",
    "Genel odaklanma"
]

selected_activity = st.sidebar.selectbox(
    "Şu anda ne yapıyorsun?",
    activity_options
)

user_goal = st.sidebar.text_input(
    "Kısa bir hedef cümlesi girin:",
    placeholder="Örn: Bugün Python modülünü bitireceğim"
)

st.session_state.user_context.update_context(selected_activity, user_goal)

st.sidebar.markdown("---")
st.sidebar.subheader("Hedef Özeti")
st.sidebar.info(
    f"**Aktivite:** {selected_activity}\n\n"
    f"**Hedef:** {user_goal if user_goal else 'Belirtilmedi'}"
)


# --- Ana Ekran ---
st.title("Gerçek Zamanlı Dikkat ve Yorgunluk Tespit Sistemi")

st.markdown("""
Bu sistem, webcam görüntünüz üzerinden yüz hatlarınızı analiz ederek
**dikkat dağınıklığı** ve **yorgunluk** durumunuzu gerçek zamanlı olarak tespit eder.
""")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Kamera Görüntüsü")
    camera_placeholder = st.empty()

    start_col, stop_col = st.columns(2)

    if start_col.button("Kamerayı Başlat", type="primary"):
      st.session_state.run_camera = True

if stop_col.button("Kamerayı Durdur"):
      st.session_state.run_camera = False

with col2:
    st.subheader("Anlık Durum")
    status_placeholder = st.empty()

    st.subheader("AI Koç Mesajı")
    coach_placeholder = st.empty()

    st.subheader("Skorlar")
    attention_bar = st.progress(100, text="Dikkat Skoru")
    fatigue_bar = st.progress(0, text="Yorgunluk Skoru")


# --- Ana Video İşleme Döngüsü ---
if st.session_state.run_camera:
    camera = Camera(1)

    try:
        camera.start()
    except Exception as e:
        st.error(f"Kamera hatası: {e}")
        st.session_state.run_camera = False
        st.stop()

    detector = FaceDetector()
    extractor = FeatureExtractor()
    fatigue_analyzer = FatigueAnalyzer(
        ear_threshold=0.22,
        consecutive_frames_threshold=10
    )
    attention_analyzer = AttentionAnalyzer(
        pitch_threshold=20.0,
        yaw_threshold=25.0
    )

    prev_time = time.time()
    coach_update_time = time.time()
    current_status = "Dikkatli"
    coach_placeholder.info("Sistem başlatılıyor...")

    while st.session_state.run_camera:
        ret, frame = camera.read_frame()

        if not ret or frame is None:
            st.error(
                "Görüntü alınamadı. Lütfen kamera iznini ve bağlantısını kontrol edin."
            )
            st.session_state.run_camera = False
            break

        frame_shape = frame.shape
        results = detector.process_frame(frame)
        coords = detector.get_landmarks_coords(results, frame_shape)

        is_fatigued = False
        is_distracted = False
        fatigue_msg = ""
        dist_msg = ""

        if coords:
            # Göz açıklık oranı analizi
            ear = extractor.extract_eye_aspect_ratio(coords)
            is_fatigued, fatigue_msg = fatigue_analyzer.analyze(ear)

            # Baş pozisyonu analizi
            pitch, yaw, roll = extractor.estimate_head_pose(coords, frame_shape)
            is_distracted, dist_msg = attention_analyzer.analyze(
                face_detected=True,
                pitch=pitch,
                yaw=yaw
            )

            # Landmark çizimi
            frame = detector.draw_landmarks(frame, results)

            cv2.putText(
                frame,
                f"EAR: {ear:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Pitch: {pitch:.1f} Yaw: {yaw:.1f}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        else:
            is_distracted, dist_msg = attention_analyzer.analyze(
                face_detected=False
            )

        # Durum belirleme
        if is_fatigued:
            current_status = "Yorgun / Uykulu"
            alert_msg = fatigue_msg
            box_color = "red"
        elif is_distracted:
            current_status = "Dikkati Dağılmış"
            alert_msg = dist_msg
            box_color = "orange"
        else:
            current_status = "Dikkatli"
            alert_msg = "Kullanıcı dikkatli görünüyor."
            box_color = "green"

        # Görüntü üzerine durum yazısı ekleme
        if coords:
            if current_status == "Yorgun / Uykulu":
                text_color = (0, 0, 255)
            elif current_status == "Dikkati Dağılmış":
                text_color = (0, 165, 255)
            else:
                text_color = (0, 255, 0)

            draw_text_with_background(
                frame,
                current_status,
                (10, frame_shape[0] - 20),
                bg_color=(50, 50, 50),
                text_color=text_color
            )

        # Streamlit görüntü gösterimi
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        camera_placeholder.image(
            frame_rgb,
            channels="RGB",
            use_column_width=True
        )

        # UI güncellemeleri
        if time.time() - prev_time > 0.5:
            prev_time = time.time()

            status_html = f"""
            <div style='padding:15px; border-radius:10px; background-color:{box_color};
            color:white; font-size:18px; text-align:center;'>
                <b>{current_status}</b><br>
                <span style='font-size:14px'>{alert_msg}</span>
            </div>
            """

            status_placeholder.markdown(status_html, unsafe_allow_html=True)

            att_score = attention_analyzer.get_attention_score()
            fat_score = fatigue_analyzer.get_fatigue_score()

            attention_bar.progress(
                int(att_score),
                text=f"Dikkat Skoru: %{int(att_score)}"
            )

            fatigue_bar.progress(
                int(fat_score),
                text=f"Yorgunluk Skoru: %{int(fat_score)}"
            )

        # AI koç mesajı
        if time.time() - coach_update_time > 5.0:
            coach_update_time = time.time()
            coach_msg = st.session_state.motivation_engine.get_message(
                current_status,
                st.session_state.user_context.get_context()
            )
            coach_placeholder.info(coach_msg)

    camera.stop()