import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement direct du dataset "flights" depuis GitHub 
@st.cache_data 
def load_data(): 
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv" 
    return pd.read_csv(url) 
df_flights = load_data()

st.subheader("Aperçu des données") 
st.dataframe(df_flights.head(10)) 
# Affichage de KPI 
total_passengers = df_flights["passengers"].sum() 
st.metric(label="Total de passagers historiques", 
value=f"{total_passengers:,}")

df_flights = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborndata/master/flights.csv")
# Préparation des données : évolution annuelle du total des passagers
annual_passengers = df_flights.groupby("year")["passengers"].sum()
st.subheader("Évolution du trafic aérien (Bar Chart natif)")
st.bar_chart(annual_passengers)

df_iris = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborndata/master/iris.csv")
st.subheader("Distribution par espèce (Seaborn)")
# 1. Création explicite de la figure
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=df_iris, x="species", y="sepal_length", ax=ax,
palette="viridis")
ax.set_title("Longueur moyenne des sépales par espèce")
# 2. Rendu dans Streamlit
st.pyplot(fig)
