import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from rasterio.plot import show
from sklearn.cluster import KMeans

st.markdown("# Machine Learning Plots Clustering")
st.sidebar.markdown("# Machine Learning Plots Clustering")


#To generate a model we need a dataframe in wich each pixel (coordinate) has all the associated indexes. For this, we modify our existing dataframes by using the melting method so we can merge them.
st.subheader("Dataframe con índices calculados")
try:
    ndvi_melt = st.session_state.ndvi.reset_index().melt(id_vars='index', ignore_index=False)
    ndvi_melt.columns = ['x', 'y', 'NDVI']
    gndvi_melt = st.session_state.gndvi.reset_index().melt(id_vars='index', ignore_index=False)
    gndvi_melt.columns = ['x', 'y', 'GNDVI']
    dvi_melt = st.session_state.dvi.reset_index().melt(id_vars='index', ignore_index=False)
    dvi_melt.columns = ['x', 'y', 'DVI']
    #Creating and populating a dataframe with each Vegetation Index value for each pixel point
    df_indices = ndvi_melt.merge(gndvi_melt, on=['x', 'y'])
    df_indices = df_indices.merge(dvi_melt, on=['x', 'y'])
    st.session_state.df_indices = df_indices
    df_indices
except:
    st.text("Falta calcular uno de los indices.")

#Now we can begin to create and evaluate some machine learning models.
st.subheader("Unsupervised Models Clustering")
st.markdown("### K-Means")

evaluar_clusters = st.button("Evaluar N clusters")

data = st.session_state.df_indices.values
st.session_state.df_indices.data = data

if evaluar_clusters:
    st.text("Gráficando...")
    # Determining the ideal cluster number
    wcss = []
    for k in range(1, 10):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)
    fig, ax = plt.subplots()
    plt.plot(range(1, 10), wcss, marker='o')
    plt.title('Método del Codo')
    plt.xlabel('Número de clusters (K)')
    st.pyplot(fig)

#From the previous graph we can define 4 as the ideal number of clusters but we should leave that choice to the user.

n_clusters = st.number_input("Indicar número de clusters a utilizar.", value=4)


if st.button("Modelar y Asignar Clusters"):
    km = KMeans(n_clusters, random_state=182)
    km.fit(data)
    # Get cluster assignment labels
    labels = km.labels_
    # Format results as a DataFrame
    labels_km = pd.DataFrame([st.session_state.df_indices.index,labels]).T
    labels_km.columns = ['x,y','cluster']
    #Merge the labels to the data frame
    df_km = st.session_state.df_indices.merge(labels_km[['cluster']],left_index=True, right_index=True, how = 'left')
    st.session_state.df_km = df_km
    df_km

    #Graph the means of each cluster to visualize differences.
if st.button("Graficar medias"):

    df_km = st.session_state.df_km
    #Graph the means of NDVI and GNDVI

    df_means = df_km[['cluster', 'NDVI', 'GNDVI']].groupby('cluster').mean()
    df_means  
    x = np.arange(len(df_means))
    width = 0.25 
    multiplier = 0
    fig, ax = plt.subplots()
    for attribute, measurement in df_means.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1
    ax.set_ylabel('Valor')
    ax.set_title('Media de cada Indice por cluster')
    ax.legend(loc='upper left', ncols=2)
    st.pyplot(fig)

    #DVI
    df_means = df_km[['cluster', 'DVI']].groupby('cluster').mean()
    df_means
    #Graph the means
    x = np.arange(len(df_means))
    width = 0.25
    multiplier = 0

    fig, ax = plt.subplots()
    
    for attribute, measurement in df_means.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1
    ax.set_ylabel('Valor')
    ax.set_title('Media de cada Indice por cluster')
    ax.legend(loc='upper left', ncols=1)
    st.pyplot(fig)

if st.button("Graficar clusters"):
    st.text("Graficando...")
    df_km = st.session_state.df_km
    #Plot the clusters on the grid to visualize the different areas on the crops
    fig, ax = plt.subplots(figsize=(25, 25))
    sc = ax.scatter(df_km['y'], df_km['x'], c=df_km['cluster'], alpha=1, cmap='RdYlGn')
    ax.legend(*sc.legend_elements(), title='clusters')
    ax.set_title('K-Means generated clusters on Vegetative Indices')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    st.pyplot(fig)









