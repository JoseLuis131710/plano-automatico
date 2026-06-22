import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="Croquis a Plano")

st.title("Croquis a Plano Automático")

archivo = st.file_uploader(
    "Sube una imagen",
    type=["jpg", "jpeg", "png"]
)

if archivo is not None:

    imagen = Image.open(archivo)

    img = np.array(imagen)

    st.subheader("Imagen Original")
    st.image(img)

    # Escala de grises
    gris = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Suavizado
    blur = cv2.GaussianBlur(gris, (5,5), 0)

    # Umbral adaptativo
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    st.subheader("Croquis Limpio")
    st.image(thresh)

    # Detectar líneas
    lineas = cv2.HoughLinesP(
        thresh,
        1,
        np.pi/180,
        threshold=50,
        minLineLength=50,
        maxLineGap=20
    )

    plano = np.ones((img.shape[0], img.shape[1], 3), dtype=np.uint8) * 255

    if lineas is not None:
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]

            cv2.line(
                plano,
                (x1, y1),
                (x2, y2),
                (0,0,0),
                2
            )

    st.subheader("Plano Generado")
    st.image(plano)
st.subheader("Medidas Detectadas")

reader = easyocr.Reader(['en'])

resultados = reader.readtext(img)

for r in resultados:

    texto = r[1]
    confianza = r[2]

    if confianza > 0.3:
        st.write(
            f"Texto: {texto} | Confianza: {round(confianza,2)}"
        )

