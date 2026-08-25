import streamlit as st 
import pandas as pd 

df = pd.read_excel("taxis.xlsx", engine="openpyxl")

# Titre principal de la page 
st.title("Dashboard Analyse Taxis - Laurie & Ilyes")        
# Texte de présentation 
st.write("Bienvenue sur cette application interactive dédiée à l'analyse de données.")


# Menu déroulant (Selectbox) 
choix_outil = st.selectbox("Choisissez votre quartier de prise en charge :", df["pickup_borough"].dropna().unique().tolist())
df_filtré = df[df["pickup_borough"] == choix_outil]
st.dataframe(df_filtré)


# Filtre dataFrame Arrondissement choisis
zone_choisi = st.selectbox("Choisissez un arrondissement de prise en charge :",df["pickup_zone"].dropna().tolist())

# Filtrer le dataframe
filtre_zone = df[df["pickup_zone"] == zone_choisi]

# Afficher les 5 premières lignes
st.subheader(f"Courses dans {zone_choisi}")
st.dataframe(filtre_zone.head(5))

# Métrique du nombre total de courses
st.metric("Nombre total de courses", len(filtre_zone))