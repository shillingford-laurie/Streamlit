import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt


# Initialisation de la session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""


# Gestion des comptes 
@st.cache_data
def load_accounts():
    accounts_df = pd.read_csv("accounts.csv")
    accounts_df.columns = accounts_df.columns.str.strip()
    return accounts_df


def authenticate(username_input, password_input):

    # Vérification du compte admin via Streamlit Secrets
    if (
        username_input == st.secrets["admin"]["user"]
        and password_input == st.secrets["admin"]["password"]
    ):
        return True

    # Vérification des comptes utilisateurs via accounts.csv
    accounts_df = load_accounts()

    user_match = accounts_df[
        (accounts_df["nom"] == username_input)
        & (accounts_df["mot de passe"] == password_input)
    ]

    return not user_match.empty



# Page de connexion
if not st.session_state["logged_in"]:

    st.title("Connexion à l'Application")

    st.subheader(
        "Veuillez vous identifier pour accéder à l'application."
    )

    username_input = st.text_input("Nom d'utilisateur")

    password_input = st.text_input(
        "Mot de passe",
        type="password"
    )

    if st.button("Se connecter"):

        if authenticate(username_input, password_input):

            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input

            st.success(
                f"Bienvenue {username_input} !"
            )

            st.rerun()

        else:

            st.error(
                "Nom d'utilisateur ou mot de passe incorrect."
            )


# Application après connexion
else:

    # Chargement du dataset
    @st.cache_data
    def load_data():

        url = (
            "https://raw.githubusercontent.com/"
            "mwaskom/seaborn-data/master/flights.csv"
        )

        return pd.read_csv(url)


    df_flights = load_data()


    # Barre latérale
    with st.sidebar:

        st.write(
            f"Bienvenue **{st.session_state['username']}** !"
        )

        if st.button("Se déconnecter"):

            st.session_state["logged_in"] = False
            st.session_state["username"] = ""

            st.rerun()

        st.divider()

        selected_page = option_menu(
            menu_title="Navigation principale",
            options=[
                "Analyse des données"
            ],
            icons=[
                "bar-chart"
            ],
            default_index=0
        )


    # Page analyse des données
    if selected_page == "Analyse des données":

        st.title("Analyse des données")

        st.write(
            "Analyse du nombre de passagers aériens "
            "à partir du dataset Flights."
        )


        # Aperçu des données
        st.subheader("Aperçu des données")

        st.dataframe(
            df_flights.head(10)
        )


        # KPI total historique 
        total_passengers = df_flights["passengers"].sum()

        st.metric(
            label="Total de passagers historiques",
            value=f"{total_passengers:,}"
        )


        # Traffic aérien annuel
        annual_passengers = (
            df_flights
            .groupby("year")["passengers"]
            .sum()
        )

        st.subheader(
            "Évolution du trafic aérien"
        )

        st.bar_chart(
            annual_passengers
        )


        # Filtre par année
        annees = st.slider(
            "Sélectionnez une plage d'années",
            min_value=int(df_flights["year"].min()),
            max_value=int(df_flights["year"].max()),
            value=(
                int(df_flights["year"].min()),
                int(df_flights["year"].max())
            )
        )


        # Filtre par mois
        mois_options = (
            ["Tous les mois"]
            + df_flights["month"].unique().tolist()
        )

        mois_choisi = st.selectbox(
            "Choisissez un mois",
            mois_options
        )


        # Application des filtres
        df_filtre = df_flights[
            (df_flights["year"] >= annees[0])
            & (df_flights["year"] <= annees[1])
        ].copy()


        if mois_choisi != "Tous les mois":

            df_filtre = df_filtre[
                df_filtre["month"] == mois_choisi
            ].copy()


        # Affichage des données filtrées
        st.write(
            f"Données filtrées ({len(df_filtre)} lignes)"
        )

        st.dataframe(
            df_filtre
        )


        # KPI après filtrage
        total_passengers_filtered = (
            df_filtre["passengers"].sum()
        )

        st.metric(
            label="Nombre total de passagers",
            value=f"{total_passengers_filtered:,}"
        )


        # Évolution du nombre de passagers
        st.subheader(
            "Évolution du nombre de passagers"
        )


        # Conversion correcte année + mois en date
        df_filtre["date"] = pd.to_datetime(
            df_filtre["year"].astype(str)
            + "-"
            + df_filtre["month"]
            + "-01"
        )


        df_filtre = df_filtre.sort_values(
            "date"
        )


        st.line_chart(
            df_filtre.set_index("date")["passengers"]
        )


        # Heatmap
        if st.checkbox("Afficher la Heatmap"):

            pivot = df_filtre.pivot(
                index="month",
                columns="year",
                values="passengers"
            )


            fig, ax = plt.subplots(
                figsize=(12, 6)
            )


            sns.heatmap(
                pivot,
                annot=True,
                cmap="coolwarm",
                fmt=".0f",
                ax=ax
            )


            ax.set_title(
                "Nombre de passagers par mois et par année"
            )


            st.pyplot(fig)
