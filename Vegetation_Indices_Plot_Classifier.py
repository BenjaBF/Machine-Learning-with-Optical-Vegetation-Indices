!pip install gdown
!pip install PIL
import streamlit as st
import gdown
from PIL import Image, ImageOps
import matplotlib.pylab as plt
from sklearn.cluster import KMeans
import rasterio
from rasterio.plot import show
from tempfile import NamedTemporaryFile
import os

@st.cache_resource
def cargar_imagen(file):
    imagen = rasterio.open(file)
    return imagen

st.markdown("# Clasificador de terrenos según Indices Vegetativos \n ### Vegetation Indices Plot Classifier")
st.sidebar.markdown("# Cargar Capas / Load Layers")

st.header("Carga de Capas")


cargar_web = st.button("Cargar imágenes de prueba desde la web (Load web examples)")

if cargar_web:
    #Lead RGB Image
    st.text("Cargando imágen RGB")
    url_test_rgb = "https://drive.google.com/uc?id=1Xi1iI_GftGTxo-GN7cqWCiplhyrkDBAk"
    output = 'rgb.JPG'
    gdown.download(url_test_rgb, output)
    rgb = Image.open('rgb.JPG')
    st.subheader("Imagen RGB")
    st.session_state.rgb = rgb
    rgb

    #Load Red image tif test file.
    st.text("Cargando capa Roja/Red")
    url_test_r = "https://drive.google.com/uc?id=1Xj_2AbeIn92fYAuLE_82VThyq_QliIpB"
    output = "red.TIF"
    gdown.download(url_test_r, output)
    red = cargar_imagen('red.TIF')
    st.subheader("Capa Roja/Red")
    fig, ax = plt.subplots()
    show(red, ax=ax)
    st.pyplot(fig)
    st.write(f"Number of bands: {red.count}, Width: {red.width}, Height: {red.height}")
    st.session_state.red = red

    #Load Green image tif test file.
    st.text("Cargando capa Verde/Green")
    url_test_g = "https://drive.google.com/uc?id=1Xqi9gvmxBLNOmigfRgtJ7gIYvEuYxR5H"
    output = "gre.TIF"
    gdown.download(url_test_g, output)
    green = cargar_imagen('gre.TIF')
    st.subheader("Capa Verde/Green")
    fig, ax = plt.subplots()
    show(green, ax=ax)
    st.pyplot(fig)
    st.write(f"Number of bands: {green.count}, Width: {green.width}, Height: {green.height}")
    st.session_state.green = green

    #Load Near Infrared image tif test file.
    st.text("Cargando capa Infrarrojo Cercano/Near Infrared Reflectance")
    url_test_nir = "https://drive.google.com/uc?id=1XnV4DFgixYrAZfO0L89RfiV4RS5puhnn"
    output = "nir.TIF"
    gdown.download(url_test_nir, output)
    nir = cargar_imagen('nir.TIF')
    st.subheader("Capa Infrarrojo Cercano/Near Infrared Reflectance")
    fig, ax = plt.subplots()
    show(nir, ax=ax)
    st.pyplot(fig)
    st.write(f"Number of bands: {nir.count}, Width: {nir.width}, Height: {nir.height}")
    st.session_state.nir = nir


if not cargar_web:
    test_rgb = st.file_uploader("Carga manual de imagen RGB", type="JPEG")
    test_r = st.file_uploader("Carga manual de capa Roja/Red", type=["tif", "tiff"])
    test_g = st.file_uploader("Carga manual de capa Verde/Green", type=["tif"])
    test_nir = st.file_uploader("Carga manual de capa Infrarrojo Cercano/Near Infrared Reflectance", type=["tif"])

    if test_rgb is not None:
        st.subheader("Imágen RGB")      
        rgb = Image.open(test_rgb)
        st.session_state.rgb = rgb
        rgb

    #Load Red image tif test file.
    if test_r is not None:
        red = cargar_imagen(test_r)
        st.subheader("Capa Roja/Red")
        fig, ax = plt.subplots()
        show(red, ax=ax)
        st.pyplot(fig)
        st.write(f"Number of bands: {red.count}, Width: {red.width}, Height: {red.height}")
        st.session_state.red = red

    #Load Green image tif test file.
    if test_g is not None:
        green = cargar_imagen(test_g)
        st.subheader("Capa Verde/Green")
        fig, ax = plt.subplots()
        show(green, ax=ax)
        st.pyplot(fig)
        st.write(f"Number of bands: {green.count}, Width: {green.width}, Height: {green.height}")
        st.session_state.green = green


    #Load Near Infrared image tif test file.
    if test_nir is not None:
        nir = cargar_imagen(test_nir)
        st.subheader("Capa Infrarrojo Cercano/Near Infrared Reflectance")
        fig, ax = plt.subplots()
        show(nir, ax=ax)
        st.pyplot(fig)
        st.write(f"Number of bands: {nir.count}, Width: {nir.width}, Height: {nir.height}")
        st.session_state.nir = nir





