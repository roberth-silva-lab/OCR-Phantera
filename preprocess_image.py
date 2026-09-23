import cv2
import numpy as np

def preprocess_image(placa):
   
    gray = cv2.cvtColor(placa, cv2.COLOR_BGR2GRAY)

    
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

 
    bin_adapt = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        19, 9
    )

    
    _, bin_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    final = cv2.bitwise_or(bin_adapt, bin_otsu)

    return final
