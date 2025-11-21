import os
import cv2
from ultralytics import YOLO
from preprocess_image import preprocess_image
from ocr_easy import aplicar_ocr_easy
from datetime import datetime
from collections import deque

BASE_DIR = r"C:\Users\WorkStation\Desktop\placas"


os.makedirs(BASE_DIR, exist_ok=True)


CSV_FILE = os.path.join(BASE_DIR, "OCR.csv")


if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w") as f:
        f.write("Tipo,Data,Hora,Placa,Codigo\n")

MODELO = "runs/detect/train/weights/best.pt"
modelo = YOLO(MODELO)

ULTIMAS_PLACAS = deque(maxlen=20)


def salvar(frame, placa, texto):
    if texto in ULTIMAS_PLACAS:
        return

    agora = datetime.now()
    dt = agora.strftime("%d-%m-%Y")
    hr = agora.strftime("%H-%M-%S")

    
    frame_name = f"Frame_{texto}_{dt}_{hr}.jpg"
    cv2.imwrite(os.path.join(BASE_DIR, frame_name), frame)

  
    placa_name = f"Placa_{texto}_{dt}_{hr}.jpg"
    cv2.imwrite(os.path.join(BASE_DIR, placa_name), placa)

   
    with open(CSV_FILE, "a") as f:
        f.write(f"PASSEIO,{dt},{hr},{texto},00\n")

    ULTIMAS_PLACAS.append(texto)
    print(f"[SALVO] {texto} | {placa_name}")


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar vídeo.")
        break


    resultados = modelo.predict(frame, conf=0.4, verbose=False)

    for box in resultados[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        placa = frame[y1:y2, x1:x2]
        if placa.size == 0:
            continue

      
        placa_proc = preprocess_image(placa)

   
        texto = aplicar_ocr_easy(placa_proc)

       
        if texto:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, texto, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            salvar(frame, placa, texto)

    cv2.imshow("OCR - YOLO + EasyOCR", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
