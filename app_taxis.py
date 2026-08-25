import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CHARGEMENT DES DONNÉES
df = pd.read_excel("taxis.xlsx", engine="openpyxl")

st.title("Dashboard Analyse Taxis - Laurie & Ilyes")

st.write(
    "Bienvenue sur cette application interactive dédiée à l'analyse des données de taxis."
)


# 2. FILTRE PAR QUARTIER
st.sidebar.header("Filtres")

choix_outil = st.sidebar.selectbox(
    "Choisissez votre quartier de prise en charge :",
    df["pickup_borough"].dropna().unique().tolist()
)

df_filtre = df[
    df["pickup_borough"] == choix_outil
]

# 3. FILTRE PAR ZONE
zones_disponibles = (
    df_filtre["pickup_zone"]
    .dropna()
    .unique()
    .tolist()
)

zone_choisi = st.sidebar.selectbox(
    "Choisissez une zone de prise en charge :",
    zones_disponibles
)

df_filtre = df_filtre[
    df_filtre["pickup_zone"] == zone_choisi
]


# 4. INFORMATIONS GÉNÉRALES
st.subheader(f"Courses dans {zone_choisi}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Nombre total de courses",
        len(df_filtre)
    )

with col2:
    if "trip_distance" in df_filtre.columns:
        st.metric(
            "Distance moyenne",
            f"{df_filtre['trip_distance'].mean():.2f}"
        )

with col3:
    if "total_amount" in df_filtre.columns:
        st.metric(
            "Prix moyen",
            f"${df_filtre['total_amount'].mean():.2f}"
        )


# 5. AFFICHAGE DES DONNÉES
with st.expander("Afficher les données filtrées"):
    st.dataframe(
        df_filtre.head(100),
        use_container_width=True
    )


# 6. CHOIX DES VARIABLES X ET Y
st.subheader("Analyse X / Y")


colonnes_numeriques = df_filtre.select_dtypes(
    include="number"
).columns.tolist()

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
        df_filtre,
        x=variable_x,
        y=variable_y,
        title=f"{variable_y} en fonction de {variable_x}",
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
        "Il n'y a pas suffisamment de variables numériques "
        "pour créer un graphique X/Y."
    )


# MATRICE DE CORRÉLATION
st.subheader("Matrice de corrélation")

if len(colonnes_numeriques) >= 2:

    correlation = df_filtre[
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
        "Il n'y a pas suffisamment de variables numériques "
        "pour calculer une matrice de corrélation."
    )
