from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import matplotlib.pyplot as plt
import base64
import streamlit.components.v1 as components
from pathlib import Path
import base64
import html

CACHE_DIR = Path("data_cache")

# 💅 Appliquer le style CSS global
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Logo ---
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
titre,mb, = st.columns([4,1])
with mb:
    logo = Image.open("fake_logo.png")
    st.image(logo, width=100)

team =  pd.read_parquet(CACHE_DIR / "global.parquet")
team["last_move_date"] = pd.to_datetime(team["last_move_date"])
team["join_date"] = pd.to_datetime(team["join_date"])
today = datetime.today()
thirty_days_ago = today - timedelta(days=30)
six_months_ago = today - timedelta(days=180)

# Métriques
nb_teams = len(team)
active_teams = team[team["last_move_date"] >= thirty_days_ago].shape[0]
inactive_teams = team[team["last_move_date"] < six_months_ago].shape[0]
last_team = team.sort_values("join_date", ascending=False).iloc[0]

# --- MISE EN PAGE ---
with titre:
    st.markdown("""
    <h1 style="font-size: 2.5rem; font-weight: 600; margin-bottom: 1rem; ">
        🩺 Check-up général
    </h1>
    """, unsafe_allow_html=True)

#_______________________________________________________________
# --- Metrics generale ---
#_______________________________________________________________
st.markdown("""
<h3 style="font-size: 1.4rem; font-weight: 500; margin-bottom: 0rem;text-decoration: underline;">
    💡 Quelques chiffres :
</h3>
""", unsafe_allow_html=True)
# LIGNE 1
col1, col2,col3 = st.columns(3)
with col1:
    st.metric("Nombre de teams", nb_teams)
with col2:
    st.metric("Teams actives (30 jours)", active_teams)
with col3:
    st.metric("Teams inactives (6 mois)", inactive_teams)
# LIGNE 2
space, col3, space2 = st.columns([1.5,3,1.5])
last_active_team = team.sort_values("last_move_date", ascending=False).iloc[0]
with col3:
    st.metric(
        "Dernière activité détectée",
        last_active_team["team_name"],
        last_active_team["last_move_date"].strftime("%Y-%m-%d")
    )


st.divider()
#_______________________________________________________________
# --- Tableau : dernière équipe arrivée ---
#_______________________________________________________________

st.markdown("""
<h3 style="font-size: 1.4rem; font-weight: 500; margin-bottom: 0rem; text-decoration: underline;">
    🆕 Les dernières arrivées à bord :
</h3>
""", unsafe_allow_html=True)
# Trier les 4 dernières arrivées
last_teams = team.sort_values("join_date", ascending=False).head(4)

# Affichage stylisé en HTML
# Génération dynamique du tableau HTML
table_html = f"""
<div style="background-color: #f9f9f9; border-radius: 10px; padding: 20px; 
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); margin-top: 20px;">
    <style>
        .styled-table {{
            border-collapse: collapse;
            width: 100%;
            font-family: sans-serif;
        }}
        .styled-table th {{
            background-color: #5E9E89;
            color: white;
            text-align: center;
            padding: 12px;
            font-size: 16px;
        }}
        .styled-table td {{
            padding: 10px;
            font-size: 15px;
            text-align: center;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
    <table class="styled-table">
        <thead>
            <tr>
                <th>Nom de la team</th>
                <th>Effectifs</th>
                <th>Date d'arrivée</th>
            </tr>
        </thead>
        <tbody>
"""

for _, row in last_teams.iterrows():
    team_name = html.escape(str(row['team_name']))
    effectif = row['effectif']
    join_date = pd.to_datetime(row['join_date']).strftime('%d %b %Y')

    table_html += f"""
        <tr>
            <td>{team_name}</td>
            <td>{effectif}</td>
            <td>{join_date}</td>
        </tr>
    """

# Fermeture
table_html += """
        </tbody>
    </table>
</div>
"""

# Affichage dans Streamlit
components.html(table_html, height=300, scrolling=True)


#_______________________________________________________________
# --- Barplot : activité par semaine ---
#_______________________________________________________________
st.markdown("""
<h3 style="font-size: 1.4rem; font-weight: 500; margin-bottom: 0rem; text-decoration: underline;">
    🏃‍♀️ ça bouge en ce moment ?
</h3>
""", unsafe_allow_html=True)

# 1. S'assurer que last_move_date est bien en datetime
team["last_move_date"] = pd.to_datetime(team["last_move_date"], errors='coerce')

# 2. Filtrer les 6 dernières semaines
six_weeks_ago = datetime.today() - timedelta(weeks=4)
recent_moves = team[team["last_move_date"] >= six_weeks_ago].copy()

# 3. Grouper par semaine
recent_moves["semaine"] = recent_moves["last_move_date"].dt.to_period("D").apply(lambda r: r.start_time)

# 4. Compter les équipes par semaine
weekly_counts = recent_moves.groupby("semaine").size().reset_index(name="nb_équipes")

# 5. Barplot
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(weekly_counts["semaine"].astype(str), weekly_counts["nb_équipes"], color="#6FBFA5"
      ,width=0.3, alpha=0.7)
ax.set_title("Répartition des dernières activités par équipes (4 semaines)")
ax.set_xlabel("Semaine")
ax.set_ylabel("Nombre d’équipes actives")
ax.yaxis.grid(True, linestyle="--", color="gray", alpha=0.6)
ax.set_axisbelow(True) 
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)