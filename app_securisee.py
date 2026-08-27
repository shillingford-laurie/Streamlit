import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu


# Initialisation de la session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""


# Chargement du fichier CSV
@st.cache_data
def load_accounts():
    accounts_df = pd.read_csv("accounts.csv")
    accounts_df.columns = accounts_df.columns.str.strip()
    return accounts_df


# Vérification des identifiants
def authenticate(username_input, password_input):
    accounts_df = load_accounts()

    user_match = accounts_df[
        (accounts_df["nom"] == username_input)
        & (accounts_df["mot de passe"] == password_input)
    ]

    return not user_match.empty



# Page de connexion
if not st.session_state["logged_in"]:

    st.title("Connexion à l'Application")
    st.subheader("Veuillez vous identifier pour accéder à l'application.")

    username_input = st.text_input("Nom d'utilisateur")
    password_input = st.text_input(
        "Mot de passe",
        type="password"
    )

    if st.button("Se connecter"):

        if authenticate(username_input, password_input):

            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input

            st.success(f"Bienvenue {username_input} !")

            st.rerun()

        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")


# Application après connexion
else:

    # Barre latérale : bienvenue + déconnexion
    with st.sidebar:

        st.write(
            f"Bienvenue **{st.session_state['username']}** !"
        )

        if st.button("Se déconnecter"):

            st.session_state["logged_in"] = False
            st.session_state["username"] = ""

            st.rerun()

        st.divider()

        # Menu de navigation
        selected_page = option_menu(
            menu_title="Navigation principale",
            options=[
                "Accueil",
                "Galerie Photos"
            ],
            icons=[
                "house",
                "images"
            ],
            default_index=0
        )

    # Page accueil
    if selected_page == "Accueil":

        st.title("Page d'Accueil")

        st.write(
            "Bienvenue sur l'application sécurisée."
        )

        st.write(
            "Vous êtes connecté et pouvez accéder "
            "aux différentes pages depuis le menu latéral."
        )

    # Page galerie photos
    elif selected_page == "Galerie Photos":

        st.title("Galerie Photos")

        st.write(
            "Voici une galerie de photos d'animaux "
            "disposées sur 3 colonnes."
        )

        # Création de 3 colonnes
        col1, col2, col3 = st.columns(3)

        # Première colonne
        with col1:
            st.image(
                "https://static.streamlit.io/examples/cat.jpg",
                caption="Chat",
                use_container_width=True
            )

        # Deuxième colonne
        with col2:
            st.image(
                "https://static.streamlit.io/examples/dog.jpg",
                caption="Chien",
                use_container_width=True
            )

        # Troisième colonne
        with col3:
            st.image(
                "https://static.streamlit.io/examples/owl.jpg",
                caption="Hibou",
                use_container_width=True
            )
