import asyncio
import cv2
import base64
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

from src.camera import Camera
from src.face_detector import FaceDetector
from src.feature_extractor import FeatureExtractor
from src.fatigue_analyzer import FatigueAnalyzer
from src.attention_analyzer import AttentionAnalyzer
from src.motivation_engine import MotivationEngine
from src.user_context import UserContext

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

camera = Camera(1)
detector = FaceDetector()
extractor = FeatureExtractor()
fatigue_analyzer = FatigueAnalyzer(ear_threshold=0.22, consecutive_frames_threshold=10)
attention_analyzer = AttentionAnalyzer(pitch_threshold=20.0, yaw_threshold=25.0)
motivation_engine = MotivationEngine()
user_context = UserContext()
user_context.update_context("Genel odaklanma", "Üretken bir gün")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        camera.start()
    except Exception as e:
        print(f"Camera start error: {e}")
        return

    coach_update_time = time.time()
    current_status = "Dikkatli"
    
    try:
        while True:
            ret, frame = camera.read_frame()
            if not ret or frame is None:
                await asyncio.sleep(0.1)
                continue

            frame_shape = frame.shape
            results = detector.process_frame(frame)
            coords = detector.get_landmarks_coords(results, frame_shape)

            is_fatigued = False
            is_distracted = False
            fatigue_msg = ""
            dist_msg = ""
            ear = 0.0
            pitch = 0.0
            yaw = 0.0

            if coords:
                ear = extractor.extract_eye_aspect_ratio(coords)
                is_fatigued, fatigue_msg = fatigue_analyzer.analyze(ear)

                pitch, yaw, roll = extractor.estimate_head_pose(coords, frame_shape)
                is_distracted, dist_msg = attention_analyzer.analyze(
                    face_detected=True, pitch=pitch, yaw=yaw
                )
                
                # Draw landmarks on frame
                frame = detector.draw_landmarks(frame, results)
            else:
                is_distracted, dist_msg = attention_analyzer.analyze(face_detected=False)

            if is_fatigued:
                current_status = "Yorgun / Uykulu"
                alert_msg = fatigue_msg
            elif is_distracted:
                current_status = "Dikkati Dağılmış"
                alert_msg = dist_msg
            else:
                current_status = "Dikkatli"
                alert_msg = "Kullanıcı dikkatli görünüyor."

            # Encode frame to base64
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
            frame_b64 = base64.b64encode(buffer).decode('utf-8')

            att_score = attention_analyzer.get_attention_score()
            fat_score = fatigue_analyzer.get_fatigue_score()

            coach_msg = ""
            if time.time() - coach_update_time > 10.0:
                coach_update_time = time.time()
                coach_msg = motivation_engine.get_message(current_status, user_context.get_context())

            data = {
                "image": frame_b64,
                "status": current_status,
                "alert_msg": alert_msg,
                "attention_score": att_score,
                "fatigue_score": fat_score,
                "metrics": {
                    "ear": float(ear),
                    "pitch": float(pitch),
                    "yaw": float(yaw)
                },
                "coach_msg": coach_msg
            }
            
            await websocket.send_json(data)
            await asyncio.sleep(0.05) # ~20fps target

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        camera.stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
