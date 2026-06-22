import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2

st.set_page_config(
    page_title="Croquis a Plano",
    layout="wide"
)

st.title("Croquis a Plano Automático")

@st.cache_resource
def cargar_ocr():
    return easyocr.Reader(['en'])

archivo = st.file_uploader(
    "Sube una imagen",
    type=["jpg", "jpeg", "png"]
)

if archivo is not None:

    imagen = Image.open(archivo)

    img = np.array(imagen)

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    st.subheader("Imagen Original")
    st.image(img, use_container_width=True)

    # ==========================
    # Escala de grises
    # ==========================

    gris = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # ==========================
    # Suavizado
    # ==========================

    blur = cv2.GaussianBlur(
        gris,
        (5, 5),
        0
    )

    # ==========================
    # Limpieza del croquis
    # ==========================

    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    st.subheader("Croquis Limpio")
    st.image(
        thresh,
        use_container_width=True
    )

    # ==========================
    # Detectar líneas
    # ==========================

    lineas = cv2.HoughLinesP(
        thresh,
        1,
        np.pi / 180,
        threshold=50,
        minLineLength=50,
        maxLineGap=20
    )

    # ==========================
    # Plano limpio
    # ==========================

    plano = np.ones(
        (img.shape[0], img.shape[1], 3),
        dtype=np.uint8
    ) * 255

    if lineas is not None:

        for linea in lineas:

            x1, y1, x2, y2 = linea[0]

            cv2.line(
                plano,
                (x1, y1),
                (x2, y2),
                (0, 0, 0),
                2
            )

    st.subheader("Plano Generado")
    st.image(
        plano,
        use_container_width=True
    )

    # ==========================
    # OCR MEDIDAS
    # ==========================

    st.subheader("Medidas Detectadas")

    try:

        reader = cargar_ocr()

        resultados = reader.readtext(img)

        encontrados = False

        for r in resultados:

            texto = r[1]
            confianza = r[2]

            if confianza > 0.30:

                encontrados = True

                st.write(
                    f"Texto: {texto} | Confianza: {round(confianza,2)}"
                )

        if not encontrados:
            st.warning(
                "No se detectaron medidas o textos."
            )

    except Exception as e:

        st.error(
            f"Error OCR: {str(e)}"
        )

