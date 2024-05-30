# les imports
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# memoire cache
if 'df' not in st.session_state:
    chemin = Path(__file__).parent
    fichier_data = chemin / "data" / "df_acti.csv"
    df = pd.read_csv(fichier_data, sep = ",")
    st.session_state['df'] = df
else:
    df = st.session_state['df']

df = df.dropna(subset=['Latitude', 'Longitude'])
df = df.drop(columns=['Unnamed: 0'])

# Configuration initiale
st.set_page_config(
    page_title="Main page", layout="wide", initial_sidebar_state="expanded"
)
# Menu sidebar
with st.sidebar:
    st.write("Faite votre séléction :")
    with st.expander("Commune :"):
        commune_list = df["Commune"].unique().tolist()
        commune_list.insert(0, "Toutes les communes")
        selected_commune = st.radio("Commune :", commune_list)
    with st.expander("Type d'activité :"):
        type_acti_list = df["Type-Activité"].unique().tolist()
        type_acti_list.insert(0, "Tous types d'activités")
        selected_type_acti = st.radio("Type d'activité :", type_acti_list)

    with st.expander("Tableau de données"):
        df_filtered_raw = df.copy()
        if selected_commune != "Toutes les communes":
            df_filtered_raw = df_filtered_raw[df_filtered_raw["Commune"] == selected_commune]
        if selected_type_acti != "Tous types d'activités":
            df_filtered_raw = df_filtered_raw[df_filtered_raw["Type-Activité"] == selected_type_acti]

    with st.expander("Activité :"):
        acti_list = df_filtered_raw["Activité"].unique().tolist()
        acti_list.insert(0, "Toutes activités")
        selected_activites = st.multiselect("Activité :", acti_list, default=["Toutes activités"])

    df_filtered = df_filtered_raw.copy()
    if "Toutes activités" not in selected_activites:
        df_filtered = df_filtered[df_filtered["Activité"].isin(selected_activites)]

st.header("Carte des activités en Loire-Atlantique")
st.text("N'oubliez pas de sélectionner votre activité en bas pour trouver les hébergements")

# Affichage de la carte dans Streamlit
col_carte = st.columns([0.8 , 0.2])
with col_carte[0]:
    if selected_commune == "Toutes les communes":
        fig = px.scatter_mapbox(
            df_filtered,
            lat="Latitude",
            lon="Longitude",
            color="Activité",
            hover_name="Nom de l'établissement",
            zoom=8
        )
    else:
        fig = px.scatter_mapbox(
            df_filtered,
            lat="Latitude",
            lon="Longitude",
            color="Activité",
            hover_name="Nom de l'établissement",
            hover_data={
            'Adresse mail': True,
            'Tél': True,
            'Site Web': True
                        },
            zoom=12
        ).update_traces(marker={"size": 15})

    # Définir le style de la carte
    fig.update_layout(
        mapbox_style="carto-positron",
        width=800,
        height=650,
        showlegend=False
    )

    # Afficher la figure dans Streamlit
    st.plotly_chart(fig)

columns_to_show = ["Nom de l'établissement", "Adresse de l'établissement", "Adresse mail", "Tél", "Site Web"]
available_columns = [col for col in columns_to_show if col in df_filtered.columns]

# Créer le DataFrame avec les colonnes disponibles
df_show = df_filtered[available_columns]

# Afficher le DataFrame dans Streamlit

st.write("Quel établissement vous intéresse ?")
with st.expander("Nom de l'établissement :"):
    etab_list = df_filtered["Nom de l'établissement"].unique().tolist()
    etab_list.insert(0, "Pas de sélection")
    selected_etab = st.radio("Nom de l'établissement :", etab_list)
    df_reco = df_filtered.copy()
    if selected_etab != "Pas de sélection":
        df_reco = df_reco[df_reco["Nom de l'établissement"] == selected_etab]

if selected_etab == "Pas de sélection":
    st.write("Choisissez un  pour la recommandation")
else:
    st.write(f"""Vous avez choisi {df_reco.iloc[0]["Nom de l'établissement"]}\n
    L'adresse est le {df_reco.iloc[0]["Adresse de l'établissement"]}\n
    L'adresse mail est le {df_reco.iloc[0]["Adresse mail"]}\n
    Joignable au {df_reco.iloc[0]["Tél"]}\n
    Site internet {df_reco.iloc[0]["Site Web"]}\n
    {df_reco.iloc[0]["Complément_1"]}\n
    {df_reco.iloc[0]["Complément_2"]}\n
    NaN signifie que la donnée n'a pas été entrée.\n
    \n
    \n
    Rendez-vous sur la page hébergement pour voir les hébergements les plus proches.
    """)


st.session_state.df_reco = df_reco