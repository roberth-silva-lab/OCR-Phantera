import cv2
from ultralytics import YOLO


modelo = YOLO("runs/detect/train/weights/best.pt") 


cap = cv2.VideoCapture(0)

while True:
    
    ret, frame = cap.read()
    
  
    if not ret:
        print("Falha ao capturar o vídeo")
        break

    
    resultados = modelo(frame) 

    
    for result in resultados[0].boxes:
        
        x1, y1, x2, y2 = map(int, result.xyxy[0])  
        conf = result.conf[0]  
        cls = int(result.cls[0])  

        
        if conf >= 0.40:
           
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

         
            label = f"Classe {cls} ({conf*100:.1f}%)"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

 
    cv2.imshow("Webcam -Detectando", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
