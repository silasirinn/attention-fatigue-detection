import cv2
import mediapipe as mp
from .utils import get_landmark_coords

class FaceDetector:
    def __init__(self, max_num_faces=1, refine_landmarks=True):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=refine_landmarks,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def process_frame(self, frame):
        """
        RGB kareyi işler ve landmark'ları çıkarır.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        return results

    def get_landmarks_coords(self, results, frame_shape):
        """
        MediaPipe landmark nesnelerini piksel koordinatları listesine dönüştürür.
        Eğer yüz bulunamazsa None döner.
        """
        h, w, _ = frame_shape
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0] # İlk yüzü alıyoruz
            coords = [get_landmark_coords(landmark, w, h) for landmark in face_landmarks.landmark]
            return coords
        return None

    def draw_landmarks(self, frame, results):
        """
        Tespit edilen yüz ağını (mesh) orijinal görüntü üzerine çizer.
        """
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style())
        return frame
