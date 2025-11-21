import cv2

def processar_contornos(img_original, img_processada):
    contornos, _ = cv2.findContours(img_processada, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    possiveis_placas = []

    for contorno in contornos:

        perimetro = cv2.arcLength(contorno, True)
        aprox = cv2.approxPolyDP(contorno, 0.02 * perimetro, True)
        area = cv2.contourArea(contorno)
        x, y, w, h = cv2.boundingRect(contorno)

        
        if h > w: continue
        if h < (w * 0.2): continue
        if area < 10000 or area > 70000: continue
        if not (4 <= len(aprox) <= 10): continue

        cv2.drawContours(img_original, [aprox], -1, (0,255,0), 2)

        recorte = img_original[y:y+h, x:x+w]

     
        rec_gray = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
        _, rec_bin = cv2.threshold(rec_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        possiveis_placas.append((recorte, rec_bin))

    return possiveis_placas
