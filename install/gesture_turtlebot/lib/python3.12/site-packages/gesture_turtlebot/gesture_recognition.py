import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
import urllib.request
import os

class GestureRecognitionNode(Node):
    def __init__(self):
        super().__init__('gesture_recognition')
        self.publisher = self.create_publisher(String, '/gesture', 10)
        self.timer = self.create_timer(0.1, self.process_frame)

        # OpenCV webcam
        self.cap = cv2.VideoCapture(0)

        # Download the hand landmark model if not present
        model_path = os.path.expanduser('~/.mediapipe/hand_landmarker.task')
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        if not os.path.exists(model_path):
            self.get_logger().info('Downloading hand landmarker model...')
            urllib.request.urlretrieve(
                'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task',
                model_path
            )
            self.get_logger().info('Model downloaded.')

        # Set up HandLandmarker
        options = HandLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=model_path),
            running_mode=RunningMode.IMAGE,
            num_hands=2,
            min_hand_detection_confidence=0.7
        )
        self.landmarker = HandLandmarker.create_from_options(options)
        self.get_logger().info('Gesture recognition node started')

    def classify_gesture(self, hand_landmarks):
        lm = hand_landmarks

        fingers_up = []
        for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:
            fingers_up.append(lm[tip].y < lm[pip].y)

        # Thumb check — tip x < ip x for right hand (mirrored)
        thumb_up = lm[4].x < lm[3].x

        count = sum(fingers_up)

        if count == 0 and not thumb_up:
            return 'FORWARD'        # fist ✊
        elif count == 4:
            return 'STOP'           # open palm 🖐
        elif fingers_up[0] and not any(fingers_up[1:]):
            return 'TURN_LEFT'      # index only ☝️
        elif fingers_up[0] and fingers_up[1] and not any(fingers_up[2:]):
            return 'TURN_RIGHT'     # peace ✌️
        elif thumb_up and not any(fingers_up):
            return 'SPAWN_TB2'      # thumbs up 👍
        else:
            return 'STOP'

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        results = self.landmarker.detect(mp_image)

        gesture = 'STOP'

        if results.hand_landmarks and results.handedness:
            for hand_landmarks, handedness in zip(results.hand_landmarks, results.handedness):
                # Right hand filter (mirrored — MediaPipe "Left" = your right)
                label = handedness[0].category_name
                if label == 'Left':
                    gesture = self.classify_gesture(hand_landmarks)

                    # Draw landmarks manually
                    for lm in hand_landmarks:
                        h, w, _ = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

                cv2.putText(frame, f'Hand: {label}', (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        msg = String()
        msg.data = gesture
        self.publisher.publish(msg)

        cv2.putText(frame, f'Gesture: {gesture}', (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Gesture Recognition', frame)
        cv2.waitKey(1)

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.landmarker.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = GestureRecognitionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()