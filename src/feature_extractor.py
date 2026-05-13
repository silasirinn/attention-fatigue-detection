import numpy as np
import cv2
from .utils import euclidean_distance

class FeatureExtractor:
    def __init__(self):
        # Sağ ve Sol göz MediaPipe landmark indeksleri
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        
        # Baş pozu (Head Pose) tahmini için kullanılacak temel 3D yüz noktaları (Örnek model)
        self.model_points = np.array([
            (0.0, 0.0, 0.0),             # Burun ucu
            (0.0, -330.0, -65.0),        # Çene
            (-225.0, 170.0, -135.0),     # Sol göz sol köşe
            (225.0, 170.0, -135.0),      # Sağ göz sağ köşe
            (-150.0, -150.0, -125.0),    # Sol ağız kenarı
            (150.0, -150.0, -125.0)      # Sağ ağız kenarı
        ])
        
        # MediaPipe karşılıkları
        self.POSE_LANDMARKS = [1, 152, 226, 446, 291, 61]

    def calculate_ear(self, eye_points):
        """
        Göz Açıklık Oranını (Eye Aspect Ratio - EAR) hesaplar.
        """
        # Dikey mesafeler
        v1 = euclidean_distance(eye_points[1], eye_points[5])
        v2 = euclidean_distance(eye_points[2], eye_points[4])
        
        # Yatay mesafe
        h = euclidean_distance(eye_points[0], eye_points[3])
        
        # EAR formülü
        ear = (v1 + v2) / (2.0 * h)
        return ear

    def extract_eye_aspect_ratio(self, landmarks_coords):
        """
        Sağ ve sol göz için EAR değerini hesaplayıp ortalamasını döndürür.
        """
        right_eye_points = [landmarks_coords[i] for i in self.RIGHT_EYE]
        left_eye_points = [landmarks_coords[i] for i in self.LEFT_EYE]
        
        ear_right = self.calculate_ear(right_eye_points)
        ear_left = self.calculate_ear(left_eye_points)
        
        return (ear_right + ear_left) / 2.0

    def estimate_head_pose(self, landmarks_coords, frame_shape):
        """
        Baş pozisyonunu (Pitch, Yaw, Roll) hesaplar.
        """
        image_points = np.array([landmarks_coords[i] for i in self.POSE_LANDMARKS], dtype="double")
        
        # Kamera matrisi (Yaklaşık değerler)
        focal_length = frame_shape[1]
        center = (frame_shape[1] / 2, frame_shape[0] / 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")
        
        dist_coeffs = np.zeros((4, 1))
        
        # PnP çözümü
        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
        )
        
        # Rotasyon vektörünü Euler açılarına çevirme (Pitch, Yaw, Roll)
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        proj_matrix = np.hstack((rotation_matrix, translation_vector))
        euler_angles = cv2.decomposeProjectionMatrix(proj_matrix)[6]
        
        pitch = euler_angles[0][0]
        yaw = euler_angles[1][0]
        roll = euler_angles[2][0]
        
        return pitch, yaw, roll
