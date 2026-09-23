import easyocr
import re

reader = easyocr.Reader(['en'], gpu=True)

def regex_antiga(texto):
    padrao = r'[A-Z]{3}\d{4}'
    r = re.findall(padrao, texto)
    return r[0] if r else None

def regex_mercosul(texto):
    padrao = r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}'
    r = re.findall(padrao, texto)
    return r[0] if r else None

def aplicar_ocr_easy(img_bin):
    resultados = reader.readtext(img_bin, detail=0)

    if not resultados:
        return None

    texto = resultados[0].upper().strip()
    texto = texto.replace(" ", "")

    placa = regex_mercosul(texto)
    if placa:
        return placa

    placa = regex_antiga(texto)
    if placa:
        return placa

    return None
