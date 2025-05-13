from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import matplotlib.pyplot as plt
import base64
import seaborn as sns
import streamlit.components.v1 as components
from pathlib import Path
import base64
from Utils.utils import GLOSSAIRE_ACTIONS
import seaborn as sns
import html


# 💅 Appliquer le style CSS global
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Logo ---
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
titre,mb, = st.columns([4,1])
with mb:
    logo = Image.open("motherbase.png")
    st.image(logo, width=100)
# --- MISE EN PAGE ---
with titre:
    st.markdown("""
    <h1 style="font-size: 2.5rem; font-weight: 600; margin-bottom: 1rem; ">
        🔎 Zoom sur les activités
    </h1>
    """, unsafe_allow_html=True)    
    

CACHE_DIR = Path("data_cache")

#table_team = pd.read_parquet(CACHE_DIR / "teams.parquet")
action_table = pd.read_parquet(CACHE_DIR / "actions.parquet")

# Date du jour et seuil à 30 jours
today = pd.to_datetime("today").normalize()
action_table["action_date"] = pd.to_datetime(action_table["action_date"])
date_debut = today - timedelta(days=30)

# 👉 Filtrer action_table sur les 30 derniers jours
recent_actions = action_table[action_table["action_date"] >= date_debut]

st.markdown("#### 📊 Volume d’activité par type (30 derniers jours)")

# Comptage des actions par type
actions_by_type = recent_actions["action"].value_counts().sort_values(ascending=True)

fig0, ax0 = plt.subplots(figsize=(8, 4))
ax0.barh(actions_by_type.index, actions_by_type.values, color="#6FBFA5")
ax0.set_xlabel("Nombre d’actions")
ax0.set_ylabel("Type d’activité")
ax0.set_title("Répartition des types d’action sur la période")
ax0.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
st.pyplot(fig0)



# Sélection du type d’activité
activity_list = sorted(recent_actions["action"].unique())
selected_action = st.selectbox("🔎 Choisis un type d’activité à explorer :", activity_list)

# Affiche la définition si connue
definition = GLOSSAIRE_ACTIONS.get(selected_action, "Pas de définition disponible pour cette activité.")
st.markdown(f"""
<div style="background-color: #edf4ef; border-left: 5px solid #6FBFA5; padding: 1rem; margin-bottom: 1.2rem;">
<b>Définition :</b><br>{definition}
</div>
""", unsafe_allow_html=True)

# Filtrer les données
df_selected = recent_actions[recent_actions["action"] == selected_action]

# 📈 Activité jour par jour
st.markdown(f"##### 📅 Répartition quotidienne: {selected_action.capitalize()}")

df_by_day = df_selected.groupby("action_date").size().reset_index(name="Nombre d’actions")
fig1, ax1 = plt.subplots(figsize=(6, 3))
ax1.bar(df_by_day["action_date"].astype(str), df_by_day["Nombre d’actions"], color="#6FBFA5", alpha=0.7, width=0.2)
ax1.set_xlabel("Date")
ax1.set_ylabel("Nombre d’actions")
ax1.grid(axis="y", linestyle="--", alpha=0.3)
plt.xticks(rotation=45,fontsize=6)
plt.tight_layout()
st.pyplot(fig1)

# 📊 Répartition par team
st.markdown(f"##### 🏢 Répartition par équipe: {selected_action.capitalize()}")

df_by_team = df_selected.groupby("team_name").size().reset_index(name="Nombre d’actions")
df_by_team = df_by_team.sort_values("Nombre d’actions", ascending=True)

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.barh(df_by_team["team_name"], df_by_team["Nombre d’actions"], color="#6FBFA5",
         alpha=0.7, height=0.2)
ax2.set_xlabel("Nombre d’actions")
ax2.set_ylabel("Équipe")
ax2.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
st.pyplot(fig2)
