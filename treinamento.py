from ultralytics import YOLO


modelo = YOLO('yolov8n.pt')


data_config = 'C:/Users/WorkStation/Desktop/OCR-Esdras/data.yaml'  


modelo.train(data=data_config, epochs=150, imgsz=640)
