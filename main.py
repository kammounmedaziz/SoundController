import cv2
from vision.hand_tracker import HandTracker
from system.volume_controller import VolumeController

def main():
    """
    Main function to run the volume control application.
    """
    # Initialize components
    tracker = HandTracker()
    controller = VolumeController()

    # Webcam capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Volume mapping parameters
    min_dist = 20  # Minimum distance in pixels
    max_dist = 200  # Maximum distance in pixels
    threshold = 5  # Minimum change in volume % to update

    prev_volume = controller.get_volume()
    last_direction = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)

        # Detect hands
        hands = tracker.detect_hand(frame)

        if hands:
            hand = hands[0]  # Use the first detected hand
            tracker.draw_landmarks(frame, hand)

            # Get smoothed distance
            distance = tracker.get_thumb_index_distance(hand, frame.shape[1], frame.shape[0])

            if min_dist <= distance <= max_dist:
                # Map distance to volume
                volume = int((distance - min_dist) / (max_dist - min_dist) * 100)
                volume = max(0, min(100, volume))

                # Update volume if change exceeds threshold
                if abs(volume - prev_volume) >= threshold:
                    controller.set_volume(volume)
                    last_direction = "UP" if volume > prev_volume else "DOWN"
                    prev_volume = volume

            # Check for fist gesture
            if tracker.is_fist(hand):
                if controller.is_muted():
                    controller.unmute()
                else:
                    controller.mute()

        # Display current volume
        current_vol = controller.get_volume()
        cv2.putText(frame, f"Volume: {current_vol}%", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Display direction if recently changed
        if last_direction:
            cv2.putText(frame, last_direction, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Clear direction after a few frames (optional)
            # For simplicity, keep it until next change

        cv2.imshow('Volume Control', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()