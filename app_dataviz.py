import streamlit as st 
import pandas as pd 
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