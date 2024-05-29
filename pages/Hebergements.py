import streamlit as st
import pandas as pd
from pathlib import Path


# memoire cache
if 'df_h' not in st.session_state:
    chemin = Path(__file__).parent
    fichier_data = chemin / "data" / "Base_Hebergement_V2.csv"
    df_h = pd.read_csv(fichier_data, sep = ",")
    st.session_state['df_h'] = df_h
else:
    df = st.session_state['df_h']
df_h = df_h.drop(columns=['Unnamed: 0'])

# import de la df_reco
if "df_reco" in st.session_state:
    df_reco = st.session_state.df_reco
    # SUITE DU CODE
    df_h['distance'] = df_h['Latitude'] + df_h['Longitude']
    df_h

else:
    #MESSAGE D'ERREUR
    st.error("Chargez des données")
