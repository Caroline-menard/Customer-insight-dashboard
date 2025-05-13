import numpy as np
import pandas as pd
from pathlib import Path

"""
🔒 About this file:

Originally, this module was designed to handle secure API requests to refresh and retrieve data from the company’s internal database.

Its main purpose was to allow on-demand data refresh without triggering an API call every time the user navigates through the dashboard.
Instead, data could be updated manually by clicking a refresh button on the homepage.

⚠️ For security reasons, all functions involving API communication have been intentionally hidden.
However, the overall structure and function naming have been preserved to give an overview of the intended logic.

This setup ensures that the current demo version remains faithful to the original architecture,
while fully replacing live queries with synthetic or local data.
"""

CACHE_DIR = Path("data_cache")



#importer les données
def execute_request(link,colunms_name):
    ''' 🔒 This function has been intentionally hidden for obvious security reasons.
    > Originally, it was used to query the company’s internal database via a secure API.
    > The current version of the project uses synthetic data instead, but the original logic remains fully compatible with a real API integration.

    > It returns the results as a `DataFrame`, with column names defined in the variable `columns_name`.  '''
    return None
   


def fetch_logs_data():
    ''' This function was originally responsible for retrieving data,
 formatting it, and returning the activity logs as a structured DataFrame.'''
    df_actions = pd.read_parquet(CACHE_DIR / "actions.parquet")
    return df_actions


def fetch_teams_data(return_user_table=None):
    '''This function use to returns general information about team composition and user'''
    df = pd.read_parquet(CACHE_DIR / "teams.parquet", index=False)
    if return_user_table:
        return  df
    
    team = pd.read_parquet(CACHE_DIR / "global.parquet", index=False)
    return team



#Minimum activity threshold required to be considered a super user (for 30 days ) 
SUPER_USER = {"nb_action":20}
GLOSSAIRE_ACTIONS = {
    "Export": "Téléchargement ou extraction de données depuis la plateforme.",
    "Basic search": "Recherche classique basée sur des mots-clés.",
    "Workspace": "Espace de travail personnel ou collaboratif utilisé pour organiser les éléments consultés.",
    "Visit page type A": "Consultation d’une page de type A (ex : page produit, fiche établissement...).",
    "Visit page type B": "Consultation d’une page de type B (ex : page utilisateur, profil, etc.).",
    "Visit page type C": "Consultation d’une page de type C (ex : page de synthèse, rapport, etc.).",
    "Articles": "Lecture/ ouverture ou recherche d’articles.",
    "Display on map": "Affichage d’informations géographiques sur une carte interactive.",
    "Similarity search": "Recherche avancée par similarité sémantique ou contextuelle.",
    "Chatbot": "Utilisation du chatbot pour poser une question ou obtenir une réponse automatique."
}

