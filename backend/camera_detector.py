"""
Real-time camera-based detection system
Analyzes ESP32-CAM images to detect if cabin is occupied
"""
import cv2
import numpy as np
import requests
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class CameraDetector:
    """Detect cabin occupancy from camera feed"""
    
    def __init__(self):
        self.motion_threshold = 25  # Motion sensitivity
        self.min_area = 500  # Minimum motion area in pixels
        self.previous_frames = {}  # Store previous frames for each cabin
        
    def fetch_image(self, camera_url: str, timeout: int = 5):
        """Fetch image from ESP32-CAM"""
        try:
            response = requests.get(camera_url, timeout=timeout)
            if response.status_code == 200:
                # Convert to numpy array
                img_array = np.frombuffer(response.content, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                return img
            else:
                logger.warning(f"Camera returned status {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching image: {e}")
            return None
    
    def detect_motion(self, cabin_no: int, current_frame):
        """
        Detect motion between current and previous frame
        Returns: (is_active, confidence)
        """
        if current_frame is None:
            return False, 0.0
        
        # Convert to grayscale
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # Check if we have previous frame
        if cabin_no not in self.previous_frames:
            self.previous_frames[cabin_no] = gray
            return False, 0.0  # First frame, no comparison
        
        # Calculate difference
        frame_delta = cv2.absdiff(self.previous_frames[cabin_no], gray)
        thresh = cv2.threshold(frame_delta, self.motion_threshold, 255, cv2.THRESH_BINARY)[1]
        
        # Dilate to fill gaps
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Calculate total motion area
        total_motion_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= self.min_area:
                total_motion_area += area
        
        # Store current frame for next comparison
        self.previous_frames[cabin_no] = gray
        
        # Determine if active based on motion
        is_active = total_motion_area > self.min_area
        confidence = min(total_motion_area / 10000.0, 1.0)  # Normalize to 0-1
        
        return is_active, confidence
    
    def detect_brightness(self, frame):
        """
        Detect if lights are on (cabin occupied)
        Returns: brightness score 0-1
        """
        if frame is None:
            return 0.0
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate mean brightness
        mean_brightness = np.mean(gray)
        
        # Normalize to 0-1 (assuming 0-255 range)
        brightness_score = mean_brightness / 255.0
        
        return brightness_score
    
    def analyze_cabin(self, cabin_no: int, camera_url: str):
        """
        Complete cabin analysis
        Returns: {
            'is_active': bool,
            'confidence': float,
            'method': str,
            'brightness': float,
            'motion_detected': bool
        }
        """
        # Fetch current frame
        frame = self.fetch_image(camera_url)
        
        if frame is None:
            return {
                'is_active': False,
                'confidence': 0.0,
                'method': 'camera_offline',
                'brightness': 0.0,
                'motion_detected': False,
                'error': 'Camera offline or unreachable'
            }
        
        # Detect motion
        motion_detected, motion_confidence = self.detect_motion(cabin_no, frame)
        
        # Detect brightness
        brightness = self.detect_brightness(frame)
        
        # Decision logic: Active if motion detected OR lights are bright
        is_active = motion_detected or brightness > 0.4
        
        # Combined confidence
        confidence = max(motion_confidence, brightness)
        
        return {
            'is_active': is_active,
            'confidence': confidence,
            'method': 'motion_detection' if motion_detected else 'brightness_detection',
            'brightness': brightness,
            'motion_detected': motion_detected,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

# Global detector instance
detector = CameraDetector()
