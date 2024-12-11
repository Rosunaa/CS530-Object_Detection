from ultralytics import YOLO

# Boot up YOLO PyTorch model
model = YOLO("yolo11n.pt")

# Convert model to NCNN format
model.export(format="ncnn", imgsz=640)  