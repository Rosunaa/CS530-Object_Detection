import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

import RPi.GPIO as GPIO
import time

# Define GPIO pin for the PIR sensor
PIR_PIN = 17  # Replace with your chosen GPIO pin
GPIO.setmode(GPIO.BCM)  # Use Broadcom GPIO pin numbering
GPIO.setup(PIR_PIN, GPIO.IN)  # Set PIR_PIN as input

# Initialize the Picamera2 object
picam2 = Picamera2()
# Set the resolution and format for the camera preview
picam2.preview_configuration.main.size = (640, 640)  # 640x640 resolution
picam2.preview_configuration.main.format = "RGB888"  # RGB format
# Align and configure the camera
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()  # Start the camera

# Load the YOLOv model with pre-trained weights (COCO Library)
model = YOLO("yolov8s-worldv2.pt")
model.set_classes(["person"]) # Set the model to detect only 'person' objects
person_count = 0  # Variable to keep track of detected persons

while True:
    # Check if the PIR sensor detects motion
    if GPIO.input(PIR_PIN):  # When motion is detected
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Run YOLO model on the captured frame
        results = model(frame, imgsz=320)  # Process frame at 320x320 resolution

        # Extract detections and filter for 'person' class
        detections = results[0].boxes.data  # Get detection boxes
        detected_persons = [d for d in detections if d[5] == "person"]  # Adjust for model output format

        # Increment the person count if detections are found
        if len(detected_persons) > 0:
            person_count += len(detected_persons)

        # Annotate the frame with detections
        annotated_frame = results[0].plot()

        # Display the person count on the annotated frame
        text = f'Persons: {person_count}'  # Text to display
        font = cv2.FONT_HERSHEY_SIMPLEX  # Font for the text
        text_size = cv2.getTextSize(text, font, 1, 2)[0]  # Calculate text size
        text_x = annotated_frame.shape[1] - text_size[0] - 10  # Position (x) 10px from right edge
        text_y = text_size[1] + 50  # Position (y) 50px from top edge
        # Draw the text on the frame
        cv2.putText(annotated_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Display the annotated frame in a window
        cv2.imshow("Camera", annotated_frame)

    # Entering 'e' quits the program
    if cv2.waitKey(1) == ord("e"):
        break

# Stop the camera and release resources
picam2.stop()
# Close all OpenCV windows
cv2.destroyAllWindows()
# Reset GPIO settings
GPIO.cleanup()
