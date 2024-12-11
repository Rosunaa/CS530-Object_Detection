import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

# Initialize the Picamera2 object
picam2 = Picamera2()
# Set the resolution and format for the camera preview
picam2.preview_configuration.main.size = (640, 640)  # 640x640 resolution
picam2.preview_configuration.main.format = "RGB888"  # RGB format

# Align and configure the camera
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()  # Start the camera

# Boot up YOLO model version 11 w/ncnn
model = YOLO("yolo11n_ncnn_model")

while True:
    # Get frame from the camera
    frame = picam2.capture_array()
    
    # Run YOLO model on the captured frame and store the results
    results = model(frame) #(imgsz = 320) for more fps
    
    # Output data
    annotated_frame = results[0].plot()
    
    # Get inference time
    inference_time = results[0].speed['inference']
    fps = 1000 / inference_time  # Convert to milliseconds
    text = f'FPS: {fps:.1f}'

    # Define font and position
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = annotated_frame.shape[1] - text_size[0] - 10  # 10 pixels from the right
    text_y = text_size[1] + 10  # 10 pixels from the top

    # Draw the text on the annotated frame
    cv2.putText(annotated_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow("Camera", annotated_frame)

    # Enter 'e' to exit program
    if cv2.waitKey(1) == ord("e"):
        break

# Close windows
cv2.destroyAllWindows()