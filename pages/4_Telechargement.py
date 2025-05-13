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
from Utils.utils import SUPER_USER
from Utils.rapport_generator import build_pdf
import html
import matplotlib.dates as mdates


# 💅 Appliquer le style CSS global
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
def get_encoded_icon(path, tooltip="Super utilisateur!!", width=40):
    img_bytes = Path(path).read_bytes()
    b64_img = base64.b64encode(img_bytes).decode()
    html = f"""
    <img src="data:image/png;base64,{b64_img}" title="{tooltip}"
         width="{width}" style="vertical-align: middle; margin-left: 6px;" />
    """
    return html

# --- donwload data ---
CACHE_DIR = Path("data_cache")

table_team = pd.read_parquet(CACHE_DIR / "teams.parquet")
action_table = pd.read_parquet(CACHE_DIR / "actions.parquet")

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
        Téléchargements
    </h1>
    """, unsafe_allow_html=True)
    
st.markdown(
    "<p style='font-size: 0.85rem; color: #6c757d; margin-top: 1rem;'>⬇️ Le bouton pour télécharger les données au format Excel est tout en bas à gauche !</p>",
    unsafe_allow_html=True
)   
#_____________________________________
# ----creation données----------------
#_____________________________________

df_actions_enriched = action_table.merge(
    table_team[["user_id", "user"]],
    on="user_id",
    how="left"
)

df_actions_enriched = df_actions_enriched[['user_id', 'user', 'team_id','team_name', 'action', 'action_date']].copy()

# S'assurer que action_date est bien en datetime
df_actions_enriched["action_date"] = pd.to_datetime(df_actions_enriched["action_date"])

# Définir la date de seuil (aujourd'hui - 60 jours)
#date_limite = datetime.today() - timedelta(days=60)


# Filtrer
recent_actions = df_actions_enriched.copy()
# Préparer les données agrégées par team
teams_summary = recent_actions.groupby("team_name").size().reset_index(name="nb_actions")
teams_summary["label"] = teams_summary["team_name"] + " — (" + teams_summary["nb_actions"].astype(str) + " actions)"
teams_summary = teams_summary.sort_values("team_name")

# Dictionnaire label -> nom brut
team_label_map = dict(zip(teams_summary["label"], teams_summary["team_name"]))

#_____________________________________
# ----selecteur 1:Teams----------------
#_____________________________________
# Multiselect équipes
selected_teams_labels = st.multiselect(
    "Sélectionnez une ou plusieurs équipes :",
    options=teams_summary["label"].tolist(),
)

# Conversion en noms réels
selected_teams = [team_label_map[label] for label in selected_teams_labels]
# Filtrer par équipes sélectionnées
filtered = recent_actions[recent_actions["team_name"].isin(selected_teams)]
#_____________________________________
# ----selecteur 2:Membres----------------
#_____________________________________


# Préparer les labels utilisateur
user_summary = filtered.groupby("user").size().reset_index(name="nb_actions")
user_summary["label"] = user_summary["user"] + " — (" + user_summary["nb_actions"].astype(str) + " actions)"
user_summary = user_summary.sort_values("user")

user_label_map = dict(zip(user_summary["label"], user_summary["user"]))

# Multiselect utilisateurs
selected_users_labels = st.multiselect(
    "Sélectionnez un ou plusieurs utilisateurs :", 
    options=user_summary["label"].tolist()
)
selected_users = [user_label_map[label] for label in selected_users_labels]
# Application du filtre utilisateur si sélection
if selected_users:
    filtered = filtered[filtered["user"].isin(selected_users)]
filtered = filtered.sort_values(by="action_date",ascending=False)
#_____________________________________
# ----selecteur 3:date----------------
#_____________________________________


# Sélection de la période
periode = st.selectbox("🗓️ Sélectionnez la période :", ["1 mois", "3 mois", "6 mois"])

# Calcul de la date seuil
nb_jours = {"1 mois": 30, "3 mois": 90, "6 mois": 180}[periode]
date_limite = datetime.today() - timedelta(days=nb_jours)

# Filtrage des données
df_filtred_date = filtered[filtered["action_date"] >= date_limite].copy()

#_____________________________________
# ----vue----------------
#_____________________________________
st.markdown(
    f"<p style='font-size: 0.85rem; color: #999;'>📄 {len(df_filtred_date)} lignes dans le Dataframe</p>",
    unsafe_allow_html=True
)
st.markdown("""
<h3 style="font-size: 1.3rem; font-weight: 600; margin-top: 1.5rem; border-bottom: 2px solid #6FBFA5; padding-bottom: 0.3rem;">
    🔍 Aperçu des données
</h3>
""", unsafe_allow_html=True)

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
                <th>Nom Utilisateur</th>
                <th>Date de l'activité</th>
                <th>Type d'activité</th>
            </tr>
        </thead>
        <tbody>
"""

for _, row in df_filtred_date.head(5).iterrows():
    team_name = html.escape(str(row['team_name']))
    user_name = row['user']
    action_date = pd.to_datetime(row['action_date']).strftime('%d %b %Y')
    action_type = row['action']

    table_html += f"""
        <tr>
            <td>{team_name}</td>
            <td>{user_name}</td>
            <td>{action_date}</td>
            <td>{action_type}</td>
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

#_____________________________________
# ----barplot----------------
#_____________________________________
if 'df_filtred_date' in locals() and not df_filtred_date.empty:
    # S'assurer que la colonne action_date est bien en datetime
    df_filtred_date["action_date"] = pd.to_datetime(df_filtred_date["action_date"])

    # Regroupement par jour
    actions_par_jour = df_filtred_date.groupby("action_date").size().reset_index(name="nb_actions")

    # Définir les bornes
    min_date = actions_par_jour["action_date"].min()
    max_date = actions_par_jour["action_date"].max()

    # Dates intermédiaires (un point par semaine)
    weekly_ticks = pd.date_range(start=min_date, end=max_date, freq="7D")

    # Ajout forcé des extrêmes
    xticks = list(weekly_ticks)
    if min_date not in xticks:
        xticks = [min_date] + xticks
    if max_date not in xticks:
        xticks = xticks + [max_date]

    # Création du barplot
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(actions_par_jour["action_date"], actions_par_jour["nb_actions"], 
           color="#6FBFA5", width=0.8, alpha=0.85)

    # Placement des ticks
    ax.set_xticks(xticks)
    ax.set_xticklabels([d.strftime("%d %b") for d in xticks], rotation=45, ha="right")
    plt.xticks(rotation=45)
    # Ajouts visuels
    ax.set_xlabel("Date")
    ax.set_ylabel("Nombre d'activités")
    ax.set_title("Activité quotidienne")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()

    # Affichage Streamlit
    st.pyplot(fig)
else:
    message_html = """
    <div style="
    background-color: #f2f2f2;
    border-left: 5px solid #d9d9d9;
    border-right: 4px solid #d9d9d9;
    border-top: 2px solid #d9d9d9;
    border-bottom: 2px solid #d9d9d9;
    padding: 1rem;
    border-radius: 8px;
    font-size: 0.95rem;
    color: #333;
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    margin-bottom: 1rem;">

    🔍 <strong>Astuce :</strong><br>
    Sélectionne une ou plusieurs équipes pour faire apparaître le graphique.<br>
    Promis, c’est magique ✨
    </div>
    """
    st.markdown(message_html, unsafe_allow_html=True)
#_____________________________________
# ----telechargement----------------
#_____________________________________

def convert_df_to_excel(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="actions_filtrees")
    buffer.seek(0)
    return buffer

excel_data = convert_df_to_excel(filtered)
now = datetime.now().strftime("%Y-%m-%d_%Hh%M")
filename = f"User_filtered_data_{now}.xlsx"
st.download_button(
    label="📥 Télécharger en Excel",
    data=excel_data,
    file_name=filename,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

