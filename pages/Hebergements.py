import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors

# memoire cache
if 'df_h' not in st.session_state:
    chemin = Path.cwd()
    fichier_data = chemin / "data" / "Base_Hebergement_V2.csv"
    df_h = pd.read_csv(fichier_data, sep = ";", encoding='unicode_escape')
    st.session_state['df_h'] = df_h
else:
    df_h = st.session_state['df_h']

# Vérifier si 'selected_etab' est dans st.session_state
if 'selected_etab' in st.session_state:
    selected_etab = st.session_state['selected_etab']
    if selected_etab == "Pas de sélection":
        st.write("Aucun établissement sélectionné.")
    else:
        st.write(f"Établissement sélectionné : {selected_etab}")
else:
    st.write("Aucune sélection d'établissement trouvée.")

X = df_h[['Latitude', 'Longitude']]

# Ajuster le modèle KNN
knn = NearestNeighbors(n_neighbors=3)
knn.fit(X)

# import de la df_reco
if "df_reco" in st.session_state:
    df_reco = st.session_state.df_reco

    # SUITE DU CODE
    reco_coords = df_reco[['Latitude', 'Longitude']]

    # Trouver les voisins les plus proches pour les points de df_reco
    distances, indices = knn.kneighbors(reco_coords)

    # Créer une liste pour stocker les DataFrames des voisins
    nearest_neighbors_dfs = []

    # Parcourir chaque ensemble de voisins et créer un DataFrame
    for idx_list in indices:
        neighbors_df = df_h.iloc[idx_list]
        nearest_neighbors_dfs.append(neighbors_df)

    # Concatenation des DataFrames de voisins
    all_neighbors_df = pd.concat(nearest_neighbors_dfs).reset_index(drop=True)

    # Optionnel: ajouter des colonnes pour identifier le point de départ dans df_reco
    all_neighbors_df['Reco_Index'] = [i for i, idx_list in enumerate(indices) for _ in idx_list]

    # Définir les colonnes dans Streamlit
    col_carte = st.columns([0.8, 0.2])
    neighbors_rename_df = all_neighbors_df.rename(columns={
        'touristique': 'Type-Activité',
        'Type de l\'offre': 'Activité',
        'Adresse partie 2': 'Adresse de l\'établissement',
        'Code postal': 'Code postal',
        'Nom de la commune': 'Commune',
        'Code Insee de la Commune': 'Code insee',
        'Latitude': 'Latitude',
        'Longitude': 'Longitude',
        'localisation': 'localisation',
        'email': 'Adresse mail',
        'N� de t�l�phone mobile': 'Tél',
        'Url du site web': 'Site Web',
        'information 1': 'Complément_1',
        'information 2': 'Complément_2'})

    combined_df = pd.concat([df_reco, neighbors_rename_df], ignore_index=True)

    with col_carte[0]:
        # Créer la carte en fonction de la sélection
        if selected_etab == "Pas de sélection":
            fig = px.scatter_mapbox(
                df_h,
                lat="Latitude",
                lon="Longitude",
                color="Type de l'offre",
                hover_name="Nom de l'offre touristique",
                zoom=8
            )
        else:
            fig = px.scatter_mapbox(
                combined_df,
                lat="Latitude",
                lon="Longitude",
                hover_name="Nom de l'offre touristique",
                zoom=12
            )
        
        # Mettre à jour les traces pour changer l'icône des marqueurs
        fig.update_traces(marker=dict(size=15, opacity=0.7))

        # Définir le style de la carte
        fig.update_layout(
            mapbox_style="carto-positron",
            width=800,
            height=650,
            showlegend=False
        )

        # Afficher la figure dans Streamlit
        st.plotly_chart(fig)
    all_neighbors_df
else:
    #MESSAGE D'ERREUR
    st.error('Choisisez un établissement dans "Activitees"')
