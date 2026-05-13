import math
import numpy as np
import cv2

def euclidean_distance(point1, point2):
    """İki nokta (x, y) arasındaki Öklid mesafesini hesaplar."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_landmark_coords(landmark, image_width, image_height):
    """MediaPipe landmark nesnesini piksel koordinatlarına dönüştürür."""
    return (int(landmark.x * image_width), int(landmark.y * image_height))

def draw_text_with_background(img, text, position, font_scale=0.7, 
                              font_thickness=2, text_color=(255, 255, 255), 
                              bg_color=(0, 0, 0)):
    """Görüntü üzerine okunabilirliği artırmak için arka planlı metin çizer."""
    x, y = position
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    
    # Arka plan dikdörtgeni
    cv2.rectangle(img, (x, y - text_height - 5), (x + text_width, y + baseline + 5), bg_color, cv2.FILLED)
    
    # Metin
    cv2.putText(img, text, position, font, font_scale, text_color, font_thickness)
    return img
