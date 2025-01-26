import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from rasterio.plot import show

#Normalized difference vegetation index (NDVI)
@st.cache_data
def calcular_ndvi(r_array, nir_array):
    ndvi = (nir_array - r_array)/(nir_array + r_array)
    ndvi_df = pd.DataFrame(ndvi)
    return ndvi_df

#Difference Vegetation Index (DVI)
@st.cache_data
def calcular_dvi(r_array, nir_array):
    dvi = nir_array - r_array
    dvi_df = pd.DataFrame(dvi)
    return dvi_df

#Green Normalized Difference Vegetation Index (GNDVI)
@st.cache_data
def calcular_gndvi(g_array, nir_array):
    gndvi = (nir_array - g_array)/(nir_array + g_array)
    gndvi_df = pd.DataFrame(gndvi)
    return gndvi_df

st.markdown("# Calculadora de Indices Vegetativos")
st.sidebar.markdown("# Calculadora de Índices Vegetativos")


#Load dataframes from loaded rasters
banda_roja = st.session_state.red.read(1)
banda_verde = st.session_state.green.read(1)
banda_nir = st.session_state.nir.read(1)

#Create arrays with the values of every image as floats for calculations.
r_array = np.array(banda_roja)
r_array = r_array.astype(float)
g_array = np.array(banda_verde)
g_array = g_array.astype(float)
nir_array = np.array(banda_nir)
nir_array = nir_array.astype(float)


#Calculating first index: NDVI and saving it as a dataframe for easier manipulation.
if st.button("Calcular NDVI"):
    st.subheader("Dataframe NDVI")
    ndvi_df = calcular_ndvi(r_array, nir_array)
    st.session_state.ndvi = ndvi_df
    ndvi_df
    #Plotting NDVI
    st.subheader("Gráfica NDVI")
    fig, ax = plt.subplots()
    sns.heatmap(st.session_state.ndvi, cmap='RdYlGn', vmin = 0, vmax = 1)
    plt.title("NDVI")
    st.pyplot(fig)

if st.button("Calcular DVI"):
    st.subheader("Dataframe DVI")
    dvi_df = calcular_dvi(r_array, nir_array)
    st.session_state.dvi = dvi_df
    dvi_df
    #Plotting NDVI
    st.subheader("DVI")
    fig, ax = plt.subplots()
    sns.heatmap(st.session_state.dvi, cmap='RdYlGn', vmin = 0, vmax = 1)
    plt.title("Gráfica DVI")
    st.pyplot(fig)

if st.button("Calcular GNDVI"):
    st.subheader("Dataframe GNDVI")
    gndvi_df = calcular_gndvi(g_array, nir_array)
    st.session_state.gndvi = gndvi_df
    gndvi_df
    #Plotting NDVI
    st.subheader("GNDVI")
    fig, ax = plt.subplots()
    sns.heatmap(st.session_state.gndvi, cmap="Greens", vmin = 0, vmax = 1)
    plt.title("Gráfica GNDVI")
    st.pyplot(fig)





