import streamlit as st 
import pandas as pd 

# Titre principal de la page 
st.title("Mon Premier Dashboard Streamlit ")        
# Texte de présentation 
st.write("Bienvenue sur cette application interactive dédiée à l'analyse de données.")

import streamlit as st 

# Hiérarchie des titres
st.title("Titre Principal (H1)") 
st.header("Titre de Section (H2)") 
st.subheader("Sous-titre (H3)") 

# Texte simple et Markdown 
st.text("Ceci est un texte brut sans mise en forme.") 
st.markdown("On peut utiliser le **gras**, l' *italique* et du :rainbow:[texte en couleur].") 

# Affichage polyvalent avec st.write() 
st.write("`st.write()` est une fonction universelle : elle affiche du texte, des dataframes, des dicts ou des graphiques.")

# Bouton simple 
if st.button("Cliquez ici"): 
    st.success("Bouton cliqué avec succès !") 

st.divider()  # Ligne de séparation visuelle 

# Case à cocher (Checkbox) 
afficher_details = st.checkbox("Afficher plus d'informations") 
if afficher_details: 
    st.info("Voici des détails supplémentaires affichés dynamiquement.") 

# Bouton Radio (Choix unique) 
reponse = st.radio(
    "Quel est votre niveau d'expérience en Python ?", 
    ["Débutant", "Intermédiaire", "Avancé"] 
) 
st.write(f"Niveau sélectionné : **{reponse}**") 

# Menu déroulant (Selectbox) 
choix_outil = st.selectbox(
    "Choisissez votre outil de visualisation préféré :", 
    ["Seaborn", "Matplotlib", "Plotly", "Power BI"] 
) 
st.write(f"Vous avez choisi : **{choix_outil}**") 