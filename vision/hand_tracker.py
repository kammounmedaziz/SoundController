import cv2
import mediapipe as mp
from collections import deque
import math

class HandTracker:
    """
    Class for detecting hands and calculating finger distances using Mediapipe.
    """

    def __init__(self, max_hands=1, smoothing_frames=10):
        """
        Initialize the HandTracker.

        Args:
            max_hands (int): Maximum number of hands to detect.
            smoothing_frames (int): Number of frames to smooth the distance over.
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        self.distances = deque(maxlen=smoothing_frames)

    def detect_hand(self, frame):
        """
        Detect hands in the frame.

        Args:
            frame: The input frame from the webcam.

        Returns:
            list: List of detected hands with landmarks.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results.multi_hand_landmarks if results.multi_hand_landmarks else []

    def get_thumb_index_distance(self, hand_landmarks, frame_width, frame_height):
        """
        Calculate the Euclidean distance between thumb and index finger tips.

        Args:
            hand_landmarks: The landmarks of the hand.
            frame_width (int): Width of the frame.
            frame_height (int): Height of the frame.

        Returns:
            float: Distance in pixels.
        """
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

        thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
        index_x, index_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)

        distance = math.sqrt((thumb_x - index_x)**2 + (thumb_y - index_y)**2)
        self.distances.append(distance)
        return sum(self.distances) / len(self.distances) if self.distances else 0

    def is_fist(self, hand_landmarks):
        """
        Check if the hand is making a fist (all fingers closed).

        Args:
            hand_landmarks: The landmarks of the hand.

        Returns:
            bool: True if fist detected.
        """
        # Check if all finger tips are below their PIP joints (for hand facing camera)
        fingers = [
            (self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.INDEX_FINGER_PIP),
            (self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
            (self.mp_hands.HandLandmark.RING_FINGER_TIP, self.mp_hands.HandLandmark.RING_FINGER_PIP),
            (self.mp_hands.HandLandmark.PINKY_TIP, self.mp_hands.HandLandmark.PINKY_PIP),
        ]
        for tip, pip in fingers:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                return False
        # Thumb check: if thumb tip is to the right of thumb IP (for right hand)
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
        if thumb_tip.x > thumb_ip.x:
            return False
        return True

    def draw_landmarks(self, frame, hand_landmarks):
        """
        Draw hand landmarks on the frame.

        Args:
            frame: The frame to draw on.
            hand_landmarks: The landmarks to draw.
        """
        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)