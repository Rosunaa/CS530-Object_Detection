# CS530-Object_Detection
Hardware used
 - Raspberry pi 4 model B
 - Raspberry pi Camera model 2
 - PIR Sensor (used in yolo2.py)

Software
 - Python 3.7
 - YOLO model by Ultralytics
 - OpenCV (cv2)
 - COCO Library
 - RPi.GPIO
 - picamera2

Steps:
- You will need the latest version of OS (Bookworm)
- Create a virtual Environment by writing in the terminal: python3 -m venv --system-site-packages "name_here"
- Then boot it up by typing: source "name_here"/bin/activate
- Now download the YOLO model: pip install ultralytics[export]
- Reboot your device and then open up Thonny (Python IDE)
- Make sure to be in regular mode and then change your interpreter to the python version from the Virtual Environment
- You can now try out the program given on this project

About the programs
- ncnn conversion: Better optimization for raspberry pi models.
- yolo.py: General object detection.
- yolo2.py: Specific object detection such as bottle, person, etc. It will also count how many times a certain detection appears with the help of PIR sensor.
