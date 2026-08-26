import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


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
                "Analyse des données",
                "Analyse Taxis"
            ],
            icons=[
                "bar-chart",
                "taxi-front"
            ],
            default_index=0
        )


    # =========================================================
    # PAGE ANALYSE DES DONNÉES - FLIGHTS
    # =========================================================

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


    # =========================================================
    # PAGE ANALYSE TAXIS
    # =========================================================

    elif selected_page == "Analyse Taxis":

        # 1. CHARGEMENT DES DONNÉES
        df_taxis = pd.read_excel(
            "taxis.xlsx",
            engine="openpyxl"
        )

        st.title(
            "Dashboard Analyse Taxis - Laurie & Ilyes"
        )

        st.write(
            "Bienvenue sur cette application interactive "
            "dédiée à l'analyse des données de taxis."
        )


        # 2. FILTRE PAR QUARTIER
        st.sidebar.header("Filtres Taxis")

        choix_outil = st.sidebar.selectbox(
            "Choisissez votre quartier de prise en charge :",
            df_taxis["pickup_borough"]
            .dropna()
            .unique()
            .tolist()
        )


        df_taxis_filtre = df_taxis[
            df_taxis["pickup_borough"] == choix_outil
        ]


        # 3. FILTRE PAR ZONE
        zones_disponibles = (
            df_taxis_filtre["pickup_zone"]
            .dropna()
            .unique()
            .tolist()
        )


        zone_choisi = st.sidebar.selectbox(
            "Choisissez une zone de prise en charge :",
            zones_disponibles
        )


        df_taxis_filtre = df_taxis_filtre[
            df_taxis_filtre["pickup_zone"] == zone_choisi
        ]


        # 4. INFORMATIONS GÉNÉRALES
        st.subheader(
            f"Courses dans {zone_choisi}"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Nombre total de courses",
                len(df_taxis_filtre)
            )


        with col2:

            if "trip_distance" in df_taxis_filtre.columns:

                st.metric(
                    "Distance moyenne",
                    f"{df_taxis_filtre['trip_distance'].mean():.2f}"
                )


        with col3:

            if "total_amount" in df_taxis_filtre.columns:

                st.metric(
                    "Prix moyen",
                    f"${df_taxis_filtre['total_amount'].mean():.2f}"
                )


        # 5. AFFICHAGE DES DONNÉES
        with st.expander(
            "Afficher les données filtrées"
        ):

            st.dataframe(
                df_taxis_filtre.head(100),
                use_container_width=True
            )


        # 6. CHOIX DES VARIABLES X ET Y
        st.subheader("Analyse X / Y")


        colonnes_numeriques = (
            df_taxis_filtre
            .select_dtypes(include="number")
            .columns
            .tolist()
        )


        if len(colonnes_numeriques) >= 2:

            col_x, col_y = st.columns(2)


            with col_x:

                variable_x = st.selectbox(
                    "Choisissez la variable X :",
                    colonnes_numeriques,
                    index=0
                )


            with col_y:

                variable_y = st.selectbox(
                    "Choisissez la variable Y :",
                    colonnes_numeriques,
                    index=1
                )


            # GRAPHIQUE PLOTLY
            st.subheader(
                f"Relation entre {variable_x} et {variable_y}"
            )


            fig = px.scatter(
                df_taxis_filtre,
                x=variable_x,
                y=variable_y,
                title=(
                    f"{variable_y} en fonction de "
                    f"{variable_x}"
                ),
                trendline="ols"
            )


            fig.update_layout(
                height=600,
                xaxis_title=variable_x,
                yaxis_title=variable_y
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        else:

            st.warning(
                "Il n'y a pas suffisamment de variables "
                "numériques pour créer un graphique X/Y."
            )


        # MATRICE DE CORRÉLATION
        st.subheader(
            "Matrice de corrélation"
        )


        if len(colonnes_numeriques) >= 2:

            correlation = df_taxis_filtre[
                colonnes_numeriques
            ].corr()


            fig_corr = px.imshow(
                correlation,
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                title="Matrice de corrélation"
            )


            fig_corr.update_layout(
                height=700
            )


            st.plotly_chart(
                fig_corr,
                use_container_width=True
            )


        else:

            st.warning(
                "Il n'y a pas suffisamment de variables "
                "numériques pour calculer une matrice "
                "de corrélation."
            )
