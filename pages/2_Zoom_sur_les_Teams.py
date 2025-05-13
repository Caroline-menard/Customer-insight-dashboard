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

def render_custom_chart(title, fig):
    # Convertir fig en image encodée
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", transparent=True)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)

    # HTML avec conteneur stylé
    html = f"""
<div class="graph-container" style="text-align: center;">
    <h3>{title}</h3>
    <img src="data:image/png;base64,{b64}" 
         style="max-width:100%; height:auto; max-height:400px; display: inline-block;" />
</div>
"""
    st.markdown(html, unsafe_allow_html=True)
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
        🔎 Zoom sur les teams
    </h1>
    """, unsafe_allow_html=True)

    
# --- donwload data ---
CACHE_DIR = Path("data_cache")

table_team = pd.read_parquet(CACHE_DIR / "teams.parquet")
action_table = pd.read_parquet(CACHE_DIR / "actions.parquet")

with st.expander("ℹ️ Comment fonctionne cette page ?", expanded=False):
    st.markdown("""
    <div style="background-color: #edf4ef; 
                border: 3px solid #6FBFA5; 
                padding: 1rem; 
                border-radius: 8px;
                font-size: 0.95rem;
                color: #2c3e50;
                font-family: 'Segoe UI', sans-serif;">
    
    Tu peux générer ici un <strong>rapport d’activité sur les 30 derniers jours</strong> 🗓️.<br><br>

    Il sera composé :
    <ul>
        <li>de quelques <strong>graphiques généraux</strong> 📊</li>
        <li>de la liste des <strong>super users</strong> 🏆</li>
        <li>et des <strong>mini-rapports d'équipes</strong> que tu auras ajoutés</li>
    </ul>

    <hr style="margin: 0.7rem 0;" />

    👉 <strong>Pour ajouter un mini-rapport d’équipe :</strong><br>
    1. Sélectionne une <strong>team</strong> via le menu déroulant<br>
    2. Clique sur <em>"Ajouter ce résumé au rapport global"</em> (bouton en bas à gauche)<br>
    <em>Tu peux en ajouter autant que tu veux !</em><br><br>

    ✅ <strong>Quand tu as terminé</strong> :<br>
    - Clique sur <em>"Générer le rapport PDF"</em><br>
    - Puis sur <em>"Télécharger le rapport final"</em><br><br>

    Et voilà, ton rapport est prêt à briller ✨

    </div>
    """, unsafe_allow_html=True)
#_______________________________________________________________
# --- Barplot : team les plus actives ---
#_______________________________________________________________
# 1. S'assurer que la date est bien au format datetime
action_table["action_date"] = pd.to_datetime(action_table["action_date"])

# 2. Filtrer les x derniers jours
two_weeks_ago = datetime.today() - timedelta(days=30)
recent_actions = action_table[action_table["action_date"] >= two_weeks_ago]

# 3. Compter les actions par team_name
activity_by_team = recent_actions.groupby("team_name").size().reset_index(name="nb_actions")

# 4. Trier et prendre les 10 plus actives
top_teams = activity_by_team.sort_values("nb_actions", ascending=False).head(15)

# 5. Barplot
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(top_teams["team_name"], top_teams["nb_actions"], color="#6FBFA5"
      , alpha=0.7)
ax.xaxis.grid(True, linestyle="--", color="gray", alpha=0.6)
ax.invert_yaxis()  # pour avoir les plus actives en haut
ax.set_xlabel("Nombre d'actions")
ax.set_title(" Les équipes les plus actives (30 derniers jours)")
plt.tight_layout()

st.pyplot(fig)
#_______________________________________________________________
# --- Selection et vue de la team ---
#_______________________________________________________________

st.markdown("""
<em>👀 Choisis une team pour voir qui fait quoi par ici…👇🙃</em>
""", unsafe_allow_html=True)



team_info = table_team.groupby("team_id").agg({
    "team_name": "first",
    "user_id": "count",  # pour effectif
    "join_date": "min"
}).reset_index()

team_info = team_info.rename(columns={"user_id": "effectif"})
team_info = team_info.sort_values("team_name", ascending=True)

options = team_info["team_id"].tolist()
labels = [
    f"{row['team_name']} – {row['effectif']} membres – {pd.to_datetime(row['join_date']).strftime('%Y-%m-%d')}"
    for _, row in team_info.iterrows()
]

selected_team_id = st.selectbox(
    "Sélectionne une équipe :", 
    options=options,
    format_func=lambda x: labels[options.index(x)]
)

team = table_team.loc[table_team.team_id==selected_team_id].copy()
team_action = action_table.loc[action_table.team_id ==selected_team_id].copy()
team_action["action_date"] = pd.to_datetime(team_action["action_date"])
# 1. Dernière action de chaque utilisateur
last_actions = team_action.groupby("user_id")["action_date"].max().reset_index()
last_actions = last_actions.rename(columns={"action_date": "last_action_date"})

# 2. Fusionner dans le DataFrame de la team
team = team.merge(last_actions, on="user_id", how="left")
# 1. Filtrer les actions sur les n derniers jours
n_jours = 30
one_week_ago = datetime.today() - timedelta(days=n_jours)
recent_actions = team_action[team_action["action_date"] >= one_week_ago]

# 2. Compter les actions par user
action_counts = recent_actions.groupby("user_id").size().reset_index(name=f"actions_{n_jours}j")

# 3. Fusionner avec le df team
team = team.merge(action_counts, on="user_id", how="left")

# 4. Remplacer les NaN par 0 (aucune action)
team[f"actions_{n_jours}j"] = team[f"actions_{n_jours}j"].fillna(0).astype(int)
team = team.sort_values(by="last_action_date",ascending=False)


#_______________________________________________________________
# --- Bloque équipe ---
#_______________________________________________________________

st.markdown(f"""
<div style="border: 1px solid #6FBFA5;
            background-color: #f5fefc;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
            margin-bottom: 1rem;
            font-size: 1.2rem;
            font-weight: 600;
            color: #3f7366;
            box-shadow: 0 1px 5px rgba(0,0,0,0.35)">
    TEAM: {team['team_name'].iloc[0]}
</div>
""", unsafe_allow_html=True)

# Conteneur général
block_html = """
<div style="border: 1px solid #e0e0e0;
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            font-family: 'Segoe UI', sans-serif;
            color: #2c3e50;
            margin-bottom: 1rem;">
"""

# Boucle des utilisateurs
for _, row in team.iterrows():
    name = row['user']
    date_in = pd.to_datetime(row['join_date']).strftime('%d %b %Y')
    last_action = pd.to_datetime(row['last_action_date']).strftime('%d %b %Y') if pd.notnull(row['last_action_date']) else "Inactif"
    j7 = int(row[f'actions_{n_jours}j']) if pd.notnull(row[f'actions_{n_jours}j']) else 0
    if last_action == "Inactif":
        color = "#e74c3c"  # rouge
    else:
        color = "#27ae60"  # vert
        
    icon_html = get_encoded_icon("icones/super_user.png", width=65) if j7 >= SUPER_USER["nb_action"] else "" 
    
    block_html += f"""
    <div style="margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px dashed #ddd;">
        <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.3rem;">
    {name}            {icon_html}
</div>
        <div style="height: 10px;"></div> 
        <div style="font-size: 0.95rem; margin-bottom: 0.2rem;">
            <span style="font-weight:600;"> Date d’arrivée :&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> {date_in}
        </div>
        <div style="font-size: 0.95rem; margin-bottom: 0.2rem;">
    <span style="font-weight:600;">Dernière activité:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
    <span style="color: {color}; font-weight: 500;">{last_action}</span>
</div>
        <div style="font-size: 0.95rem;">
            <span style="font-weight:600;"> Activités ({n_jours} jours) :&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> {j7}
        </div>
    </div>
    """

block_html += "</div>"
components.html(block_html, height=400, scrolling=True)
#_______________________________________________________________
# --- Derniers graphiques---------
#_______________________________________________________________

if len(recent_actions)==0: 
    st.markdown("""
<div style="
    background-color: #fff6f6;
    color: #a94442;
    border: 1px solid #f2dede;
    padding: 1rem;
    border-radius: 10px;
    font-size: 0.95rem;
    text-align: center;
    margin-top: 1rem;
">
    😕 Oups… aucune activité à afficher sur les 30 derniers jours.
</div>
""", unsafe_allow_html=True)

else:
    actions_per_day = recent_actions.groupby(recent_actions["action_date"].dt.date).size().reset_index(name="nb_actions")
    actions_by_type = recent_actions["action"].value_counts()

    # 🎨 Palette verte
    colors = sns.color_palette("Greens", len(actions_by_type))[::-1]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(actions_per_day["action_date"].astype(str), actions_per_day["nb_actions"], color="#6FBFA5", alpha=0.7,width=0.3)
    
    ax.set_ylabel("Nombre d'actions")
    ax.set_xlabel("Date")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.xticks(rotation=45, ha="right",fontsize=6)
    ax.set_axisbelow(True) 
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    render_custom_chart("Activité quotidienne sur les 30 derniers jours", fig)

#-------------------------------------------------------------
#       piechart
#-------------------------------------------------------------
    # Calcule les pourcentages
    total = actions_by_type.sum()
    labels_with_pct = [f"{label} ({count / total:.1%})" for label, count in actions_by_type.items()]

    fig2, ax2 = plt.subplots(figsize=(4, 4))
    wedges, _ = ax2.pie(
        actions_by_type,
        labels=None,  # plus d'étiquettes sur le donut
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.4)
    )

    # Légende externe avec % intégré
    ax2.legend(
        wedges,
        labels_with_pct,
        title="Types d’action",
        loc="center left",
        bbox_to_anchor=(-0.65, 0.5),
        frameon=True,
        fontsize=7,
        title_fontsize=10
    )
    ax2.set_title("Répartition du type d’activité")
    ax2.axis('equal')
    st.pyplot(fig2)

#-------------------------------------------------------------
#       Resumé
#-------------------------------------------------------------

# 1. Données générales
team_name = team["team_name"].iloc[0]
nb_total = len(team)
super_user_row = team[team[f'actions_{n_jours}j'] >= SUPER_USER["nb_action"]].sort_values(f'actions_{n_jours}j', ascending=False).head(1)
active_users = team[(team[f'actions_{n_jours}j'] > 0) & (team[f'actions_{n_jours}j'] < SUPER_USER["nb_action"])]
inactive_users = team[team[f'actions_{n_jours}j'] == 0]

# 2. Jours d’activité uniques sur 30 jours
activity_days = sorted(set(recent_actions["action_date"].dt.strftime('%Y-%m-%d')))
days_str = ", ".join(activity_days)

# 3. Top 3 activités hors "Other"
#-------------------------------------------------------------
#      titre apperçu 
#-------------------------------------------------------------
st.markdown(f"""
<h3 style="font-size: 1.3rem; font-weight: 600; margin-top: 1.5rem; border-bottom: 2px solid #6FBFA5; padding-bottom: 0.3rem;">
    🔍 Aperçu du mini-rapport pour la team: {team_name}
</h3>
""", unsafe_allow_html=True)

filtered_actions = recent_actions[recent_actions["action"] != 'logs']
top_actions = (
    filtered_actions["action"]
    .value_counts()
    .head(4)
    .index.tolist()
)
actions_str = ", ".join(top_actions)


if  super_user_row.empty:
    super_html = "Aucun"
else:
    super_html = ".".join([f"<li>{row['user']} ({row[f'actions_{n_jours}j']} actions)</li>" for _, row in super_user_row.iterrows()])
# 4. Encodage logo super user (si besoin)
img_bytes = Path("icones/super_user.png").read_bytes()
b64_img = base64.b64encode(img_bytes).decode()
# 5. Composition du résumé
st.markdown(f"""
<div style="background-color: #f5fefc;
            border: 1px solid #6FBFA5;
            padding: 1.2rem;
            border-radius: 10px;
            margin-top: 1rem;
            font-family: 'Segoe UI', sans-serif;
            color: #2c3e50;
            font-size: 0.95rem;">


<h4 style="margin-top: 0;">📍 Résumé – {team_name}</h4>

<b>👥 Composition :</b> {nb_total} membres<br><br>

<span style="display: inline-flex; align-items: center;">
    <img src="data:image/png;base64,{b64_img}" width="40" style="margin-right: 6px;" />
    <b>Super user :</b>
</span> {super_html}<br><br>

<b>🟢 Utilisateurs actifs ({len(active_users)}) :</b>
<ul style="margin-top: 0;">
{''.join([f"<li>{row['user']} ({row[f'actions_{n_jours}j']} actions)</li>" for _, row in active_users.iterrows()])}
</ul>

<b>🔴 Utilisateurs inactifs ({len(inactive_users)}) :</b>
<ul style="margin-top: 0;">
{''.join([f"<li>{row['user']}</li>" for _, row in inactive_users.iterrows()])}
</ul>

<b>📅 Jours d’activité :</b> {days_str}<br>
<b>📌 Activités préférées :</b> {actions_str}

</div>
""", unsafe_allow_html=True)

#-------------------------------------------------------------
#       ajout au rapport
#-------------------------------------------------------------
if "rapport_html_blocks" not in st.session_state:
    st.session_state.rapport_html_blocks = []
if "rapport_teams_names" not in st.session_state:
    st.session_state.rapport_teams_names = []
col_action = f"actions_{n_jours}j"    
html_block = html_block = f"""
<div style="font-family: 'Segoe UI', sans-serif; color: #2c3e50; font-size: 0.95rem; margin-top: 1.5rem;">

    <h4 style="margin-top: 0; margin-bottom: 1rem; color: #2c3e50;">
        ■ Résumé – {team_name}
    </h4>

    <p><b>■ Composition :</b> {nb_total} membre{'s' if nb_total > 1 else ''}</p>

    <p style="margin: 0.6rem 0 0.3rem 0; display: flex; align-items: center;">
        <img src="data:image/png;base64,{b64_img}" width="20" style="margin-right: 6px;" />
        <b>Super user :</b>
    </p>
    <ul style="margin: 0.2rem 0 1rem 1.2rem;">
        <li>{super_html} </li>
    </ul>

    <p><b>■ Utilisateurs actifs ({len(active_users)}) :</b></p>
    <ul style="margin: 0.2rem 0 1rem 1.2rem;">
        {''.join([f"<li>{row['user']} ({row[col_action]} action(s))</li>" for _, row in active_users.iterrows()])}
    </ul>

    <p><b>■ Utilisateurs inactifs ({len(inactive_users)}) :</b></p>
    <ul style="margin: 0.2rem 0 1rem 1.2rem;">
        {''.join([f"<li>{row['user']}</li>" for _, row in inactive_users.iterrows()])}
    </ul>

    <p><b>📅 Jours d’activité :</b> {days_str}</p>
    <p><b>📌 Activités préférées :</b> {actions_str}</p>

    <hr style="border: none; border-top: 1px solid #ddd; margin: 2rem 0 1rem 0;" />
</div>
"""
st.markdown("""
<small style="font-size: 0.9rem; color: #444;">
🛈 Cliquez ici pour ajouter ce mini-rapport d’équipe au rapport global téléchargeable.
</small>
""", unsafe_allow_html=True)

# Compteur d'équipes déjà ajoutées
nb_equipes = len(st.session_state.rapport_html_blocks)
noms_equipes = ", ".join(st.session_state.rapport_teams_names)

st.markdown(f"""
<small style="font-size: 0.9rem; color: #6FBFA5;">
✅ {nb_equipes} équipe(s) ajoutée(s) au rapport jusqu’ici.<br>
📋 <b>Équipes :</b> {noms_equipes}
</small>
""", unsafe_allow_html=True)

if st.button("📎 Ajouter ce résumé au rapport global"):
    st.session_state.rapport_html_blocks.append(html_block)
    st.session_state.rapport_teams_names.append(team_name)
    st.success("Résumé ajouté au rapport global ! 💾")
    
    
#-------------------------------------------------------------
#       télécharger le rapport
#-------------------------------------------------------------
# Vérifie qu’on a bien des blocs
if st.session_state.get("rapport_html_blocks"):

    st.markdown("### 📤 Générer et télécharger le rapport final")

    if st.button("📄 Générer le rapport PDF"):
        output_path = build_pdf(
            html_blocks=st.session_state["rapport_html_blocks"],
            output_path=f"Rapports/Rapport_client_{datetime.today().strftime('%Y-%m-%d')}.pdf"
        )
        with open(output_path, "rb") as f:
            st.download_button("📥 Télécharger le rapport final", f, file_name=Path(output_path).name)


else:
    st.info("Aucun mini-rapport d’équipe n’a encore été ajouté.")