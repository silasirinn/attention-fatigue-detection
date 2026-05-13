import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_AVFOUNDATION)

        if not self.cap.isOpened():
            raise Exception(
                "Kamera açılamadı! Lütfen kamera iznini ve bağlantıyı kontrol edin."
            )

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def read_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return False, None

        ret, frame = self.cap.read()

        if not ret or frame is None:
            return False, None

        frame = cv2.flip(frame, 1)

        return True, frame

    def stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None