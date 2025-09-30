import os
import cv2
import numpy as np
from ultralytics import YOLO
import easyocr
from datetime import datetime
from collections import deque

MODELO_YOLO = "runs/detect/train/weights/best.pt"
modelo = YOLO(MODELO_YOLO)


reader = easyocr.Reader(['en'], gpu=True)

CAMINHO_PROJETO = os.path.join(os.path.expanduser("~"), "Desktop", "OCR-Esdras")
os.makedirs(CAMINHO_PROJETO, exist_ok=True)

CSV_FILE = os.path.join(CAMINHO_PROJETO, "OCR.csv")
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w") as f:
        f.write("Tipo,Data,Hora,Placa,Código\n")

ULTIMAS_PLACAS = deque(maxlen=20)

def ajustar_placa(placa):
    try:
        if placa.shape[1] < 200:
            escala = 2
            placa = cv2.resize(placa, (placa.shape[1]*escala, placa.shape[0]*escala), interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(placa, cv2.COLOR_BGR2GRAY)

        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)

        kernel_tophat = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))
        tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel_tophat)
        gray = cv2.add(gray, tophat)

        gray = cv2.bilateralFilter(gray, 11, 17, 17)

        kernel_sharp = np.array([[0, -1, 0],
                                 [-1, 5, -1],
                                 [0, -1, 0]])
        gray = cv2.filter2D(gray, -1, kernel_sharp)

        kernel_morph = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel_morph)

        gray = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

        bin_adapt = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 19, 9
        )

        _, bin_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        final = cv2.bitwise_or(bin_adapt, bin_otsu)

        return final
    except Exception as e:
        print(f"[ERRO Ajuste placa]: {e}")
        return placa


def corrigir_perspectiva(frame, box):
    
    x1, y1, x2, y2 = map(int, box)
    placa = frame[y1:y2, x1:x2]
    if placa.size == 0:
        return None

    h, w = placa.shape[:2]
    src_pts = np.array([[0,0],[w,0],[w,h],[0,h]], dtype="float32")
    dst_pts = np.array([[0,0],[w,0],[w,h],[0,h]], dtype="float32")
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    return cv2.warpPerspective(placa, M, (w,h))


def ler_placa(placa_img):
    try:
        img_proc = ajustar_placa(placa_img)
        resultados = reader.readtext(img_proc, detail=0)
        if not resultados:
            return None

        texto = resultados[0].upper().strip()
        texto = (texto.replace("O", "0")
                       .replace("I", "1")
                       .replace("Z", "2")
                       .replace("S", "5")
                       .replace("|", "1")
                       .replace(" ", ""))

        if not any(c.isdigit() for c in texto):
            return None

        return texto
    except Exception as e:
        print(f"[ERRO OCR]: {e}")
        return None


def salvar(frame, placa_corrigida, texto):
    if texto in ULTIMAS_PLACAS:
        return

    agora = datetime.now()
    data = agora.strftime("%d-%m-%Y")
    hora = agora.strftime("%H-%M-%S")

    
    nome_frame = f"Frame_{texto}_{data}_{hora}.jpg"
    caminho_frame = os.path.join(CAMINHO_PROJETO, nome_frame)
    cv2.imwrite(caminho_frame, frame)

    
    nome_placa = f"Placa_{texto}_{data}_{hora}.jpg"
    caminho_placa = os.path.join(CAMINHO_PROJETO, nome_placa)
    cv2.imwrite(caminho_placa, placa_corrigida)

    
    with open(CSV_FILE, "a") as f:
        f.write(f"PASSEIO,{data},{hora},{texto},00\n")

    ULTIMAS_PLACAS.append(texto)
    print(f"[SALVO] {texto} -> {nome_placa}")


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro: nao foi possivel abrir a webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar video")
        break

    resultados = modelo.predict(source=frame, conf=0.4, verbose=False)
    placas_detectadas = []

    for result in resultados[0].boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])
        conf = float(result.conf[0])
        if conf < 0.4:
            continue

        placa_corrigida = corrigir_perspectiva(frame, [x1, y1, x2, y2])
        if placa_corrigida is None:
            continue

        texto = ler_placa(placa_corrigida)
        if texto and len(texto) >= 5:
            placas_detectadas.append((texto, placa_corrigida))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, texto, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    for texto, placa_corrigida in placas_detectadas:
        salvar(frame, placa_corrigida, texto)

    cv2.imshow("Deteccao de Placas", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
