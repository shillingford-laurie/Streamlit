import streamlit as st 
import pandas as pd 
# Chargement direct du dataset "flights" depuis GitHub 
@st.cache_data 
def load_data(): 
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv" 
    return pd.read_csv(url) 
df_flights = load_data()

st.title("Organisation en Colonnes")
# Création de 3 colonnes de largeur égale
col1, col2, col3 = st.columns(3)
with col1:
 st.header("Métrique A")
 st.metric(label="Utilisateurs", value="1,200", delta="+5%")
with col2:
 st.header("Métrique B")
 st.metric(label="Revenu", value="45 000 €", delta="+12%")
with col3:
 st.header("Métrique C")
 st.metric(label="Conversion", value="3.2%", delta="-0.4%")

# La colonne 2 sera deux fois plus large que la colonne 1
col1, col2 = st.columns([1, 2])

st.subheader("Galerie Mascottes (3 images par ligne)")
# Liste des images d'exemple
image_urls = [
 "avion.jpg",
 "aeroport.jpg",
 "taxi.jpg"
]

# Affichage côte à côte sur 3 colonnes
cols = st.columns(3)
for index, url in enumerate(image_urls):
 with cols[index % 3]:
    st.image(url, use_column_width=True, caption=f"Photo {index + 1}")


st.subheader("Aperçu des données") 
st.dataframe(df_flights.head(10)) 
# Affichage de KPI 
total_passengers = df_flights["passengers"].sum() 
st.metric(label="Total de passagers historiques", 
value=f"{total_passengers:,}")
 
df_flights = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv") 
# Préparation des données : évolution annuelle du total des passagers 
annual_passengers = df_flights.groupby("year")["passengers"].sum() 
st.subheader("Évolution du trafic aérien (Bar Chart natif)") 
st.bar_chart(annual_passengers)

import streamlit as st
import pandas as pd

# --- Supposons que ton dataframe 'df' est déjà chargé ---
# Exemple de données fictives pour que le code tourne :
# df = pd.DataFrame({'year': [1949, 1949, 1950, 1960], 'month': [1, 2, 1, 12], 'passengers': [112, 118, 132, 432]})

st.title("Analyse des données")

# 1. Création du slider pour la plage d'années
# value=(1949, 1960) définit la plage par défaut sélectionnée
annees = st.slider(
    "Sélectionnez une plage d'années",
    min_value=1949,
    max_value=1960,
    value=(1949, 1960)
)

# 2. Création du selectbox pour le mois
# On crée une liste avec "Tous les mois" en première position, suivi des 12 mois
mois_options = ["Tous les mois"] + df_flights["month"].unique().tolist()
mois_choisi = st.selectbox("Choisissez un mois", mois_options)

# --- Application des filtres au DataFrame ---

# Filtre sur les années
# annees[0] est l'année min, annees[1] est l'année max
df_filtre = df_flights[(df_flights['year'] >= annees[0]) & (df_flights['year'] <= annees[1])]

# Filtre sur le mois (uniquement si l'utilisateur n'a pas choisi "Tous les mois")
if mois_choisi != "Tous les mois":
    df_filtre = df_filtre[df_filtre['month'] == mois_choisi]

# Affichage du résultat
st.write(f"Données filtrées ({len(df_filtre)} lignes: ")
st.dataframe(df_filtre)

total_passengers = df_filtre["passengers"].sum()

st.metric(
    label="Nombre total de passagers",
    value=f"{total_passengers:,}"
)

st.subheader("Évolution du nombre de passagers")

df_filtre["date"] = pd.to_datetime(
    df_filtre["year"].astype(str) + "-" + df_filtre["month"] + "-01"
)

df_filtre = df_filtre.sort_values("date")

st.line_chart(
    df_filtre.set_index("date")["passengers"]
)

if st.checkbox("Afficher la Heatmap"):

    pivot = df_filtre.pivot(
        index="month",
        columns="year",
        values="passengers"
    )

    import seaborn as sns
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.heatmap(
        pivot,
        annot=True,
        cmap="coolwarm",
        fmt=".0f",
        ax=ax
    )

    st.pyplot(fig)