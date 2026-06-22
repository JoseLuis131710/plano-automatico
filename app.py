import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.title("Croquis a Plano")

archivo = st.file_uploader(
    "Sube una imagen",
    type=["jpg", "jpeg", "png"]
)

if archivo is not None:

    imagen = Image.open(archivo)

    img = np.array(imagen)

    st.subheader("Imagen Original")
    st.image(img)

    gris = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    bordes = cv2.Canny(gris, 50, 150)

    st.subheader("Detección de Líneas")
    st.image(bordes)
