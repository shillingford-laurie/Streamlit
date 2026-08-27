# 📊 Dashboard Data Flights — Analyse interactive du trafic aérien

Application web interactive de visualisation de données développée avec **Streamlit** et déployée sur **Streamlit Cloud**.

🔗 **Accès direct à l'application : [https://dashboard-data-flights.streamlit.app/](https://dashboard-data-flights.streamlit.app/)**

---

## 📖 Le projet en bref

Ce projet transforme le dataset **flights** (trafic aérien de 1949 à 1960 — 144 observations, 40 363 passagers cumulés) en un **tableau de bord interactif** accessible depuis un simple navigateur.

L'objectif : **démocratiser l'exploration de la donnée** — filtrer, analyser et visualiser le trafic aérien sans écrire une ligne de code, ni rien installer.

**Fonctionnalités principales :**

- 📈 **KPI en temps réel** — total de passagers recalculé selon les filtres actifs
- 🎚️ **Filtres interactifs** — plage d'années (1949–1960) et sélection du mois
- 📊 **Bar chart** — évolution annuelle du trafic (composant natif Streamlit)
- 📉 **Courbe temporelle** — évolution mensuelle des données filtrées
- 🔥 **Heatmap saisonnière** — répartition mois × année (seaborn), activable par case à cocher
- 🔐 **Connexion sécurisée** — accès avec identifiant et mot de passe, rôles utilisateur / administrateur

---

## 🔑 Comment se connecter

### Trame à suivre

1. **Ouvrir l'application** via le lien : [https://dashboard-data-flights.streamlit.app/](https://dashboard-data-flights.streamlit.app/)
2. **Patienter** quelques secondes pendant le réveil de l'application (l'hébergement gratuit met l'app en veille après inactivité)
3. **Saisir l'identifiant et le mot de passe** dans l'écran de connexion (voir les comptes de démonstration ci-dessous)
4. **Explorer le dashboard** : ajuster les filtres (années, mois), cocher la case pour afficher la heatmap, et observer la mise à jour instantanée des KPI et graphiques

### Comptes de démonstration

Les identifiants sont issus du fichier `accounts.csv` du projet :

| Profil | Identifiant | Mot de passe | Rôle |
|---|---|---|---|
| 👤 Utilisateur | `utilisateur` | `mdp123` | Consultation du dashboard |
| 🛡️ Administrateur | `admin` | `admin123` | Gestion complète de l'application |

> ⚠️ **Note :** il s'agit d'identifiants de démonstration pour un projet pédagogique. Ne jamais versionner de vrais mots de passe en clair dans un dépôt Git — en production, utilisez un gestionnaire de secrets.

---

## 🛠️ Technologies utilisées

| Outil | Rôle |
|---|---|
| **Python** | Langage principal de l'analyse |
| **pandas** | Chargement, filtrage et agrégation des données |
| **Streamlit** | Framework de l'application web (pur Python, sans HTML/CSS/JS) |
| **seaborn / matplotlib** | Visualisations avancées (heatmap annotée) |
| **Git & GitHub** | Versioning du code et hébergement du dépôt |
| **Streamlit Cloud** | Déploiement continu et gratuit — l'app se met à jour à chaque `git push` |

---

## 💻 Lancer le projet en local

```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd <dossier-du-projet>

# 2. Installer les dépendances
pip install streamlit pandas seaborn matplotlib

# 3. Lancer l'application
streamlit run app_dataviz.py
```

L'application s'ouvre alors automatiquement dans le navigateur à l'adresse `http://localhost:8501`.
