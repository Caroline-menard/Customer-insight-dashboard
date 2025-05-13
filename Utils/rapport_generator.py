from datetime import datetime, timedelta
from pathlib import Path
import base64
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns
import pandas as pd
from Utils.utils import SUPER_USER
from xhtml2pdf import pisa

# --- donwload data ---
CACHE_DIR = Path("data_cache")

table_team = pd.read_parquet(CACHE_DIR / "teams.parquet")
###=>['team_id', 'team_name', 'user_id', 'join_date', 'last_login_date','user']
actions = pd.read_parquet(CACHE_DIR / "actions.parquet")
###==>['team_id', 'user_id', 'action', 'action_date']
global_df = pd.read_parquet(CACHE_DIR / "global.parquet")
##==>['team_id', 'team_name', 'effectif', 'join_date', 'last_login_date','last_action_date', 'last_move_date']

SUPER_USER = SUPER_USER["nb_action"]
                            
### ───────────────────────────────
### 🗓️ 1. Période analysée
### ───────────────────────────────
def build_user_team_dict():
    """
    Construit un dictionnaire {user_id: {"user": nom, "team_name": team}} à partir d'un DataFrame.
    """
    return {
        row["user_id"]: {
            "user": row["user"],
            "team_name": row["team_name"]
        }
        for _, row in table_team.iterrows()
    }

def get_periode_analyse():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)
    return f"Du {start_date.strftime('%d %B %Y')} au {end_date.strftime('%d %B %Y')}"

### ───────────────────────────────
### 🖼️ 2. Logo encodé
### ───────────────────────────────

def encode_logo(path="motherbase.png", width=80):
    """Encode l’image du logo pour affichage HTML inline."""
    img_bytes = Path(path).read_bytes()
    b64 = base64.b64encode(img_bytes).decode()
    return f'<img src="data:image/png;base64,{b64}" width="{width}" style="float: right;" />'

### ───────────────────────────────
### 📊 3. Graphe global base64
### ───────────────────────────────

def get_base64_chart(fig):
    """Encode une figure matplotlib au format base64 (PNG)."""
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    return b64

### ───────────────────────────────
### 📄 4. Bloc HTML - entête
### ───────────────────────────────

def render_entete_html():
    logo = encode_logo()
    periode = get_periode_analyse()
    return f"""
    <div style="padding-bottom: 1rem; border-bottom: 1px solid #ccc;">
        {logo}
        <h1 style="color: #2c3e50;">Rapport activité client</h1>
        <p style="font-size: 1rem; color: #2c3e50;"><i>Période analysée :</i> <b>{periode}</b></p>
    </div>
    """

### ───────────────────────────────
### 📌 5.  Bloc "Super users"
### ───────────────────────────────

def get_superuser_icon_b64(path="icones/super_user.png"):
    """Encode une icône super user au format base64 (pour insertion HTML)."""
    img_bytes = Path(path).read_bytes()
    return base64.b64encode(img_bytes).decode()

def render_super_users_html():
    """
    Génère un bloc HTML stylé listant les super users (utilisateurs ayant fait plus de SUPER_USER actions).
    
    Args:
        actions (pd.DataFrame): Table contenant les colonnes 'user_id' et 'action_date'.
        SUPER_USER (int): Seuil d'activité pour être considéré comme super user.
        user_team_dict (dict): Dictionnaire {user_id: {"user": nom, "team_name": nom_team}}.
    
    Returns:
        str: Bloc HTML prêt à être injecté dans le rapport.
    """
    user_team_dict =  build_user_team_dict()
    # 1. Filtrer les actions sur les 30 derniers jours
    date_fin = datetime.today()
    date_debut = date_fin - timedelta(days=30)
    recent = actions[
        pd.to_datetime(actions["action_date"]) >= date_debut
    ]
    
    # 2. Compter les actions par utilisateur
    action_counts = recent["user_id"].value_counts()
    
    # 3. Garder ceux au-dessus du seuil
    super_users = action_counts[action_counts >= SUPER_USER]
    if super_users.empty:
        return """
        <div style="border: 1px solid #ccc; padding: 1rem; border-radius: 10px; background-color: #fdfdfd;">
            <h3 style="color: #6FBFA5;">🌟 Supers users</h3>
            <p>Aucun super user sur la période du {:%d %b %Y} au {:%d %b %Y}.</p>
        </div>
        """.format(date_debut, date_fin)

    # 4. Générer le HTML
    bloc_html = f"""
    <div style="border: 1px solid #6FBFA5;
                background-color: #f5fefc;
                padding: 1.2rem;
                border-radius: 10px;
                margin: 1.5rem 0;
                box-shadow: 0 1px 5px rgba(0,0,0,0.1);">
        <h3 style="color: #2c3e50; margin-top: 0;">
            <img src="data:image/png;base64,{get_superuser_icon_b64()}"
                 width="22" style="vertical-align: middle; margin-right: 8px;" />
            Supers users du {date_debut.strftime('%d %b %Y')} au {date_fin.strftime('%d %b %Y')}
        </h3>
    """

    for user_id, count in super_users.items():
        user_info = user_team_dict.get(user_id, {"user": "Utilisateur inconnu", "team_name": "?"})
        bloc_html += f"""
        <p style="margin: 0.3rem 0; font-size: 0.95rem;">
            <strong>{user_info['user']}</strong> ({count} actions) — <em>{user_info['team_name']}</em>
        </p>
        """

    bloc_html += "</div>"
    return bloc_html


### ───────────────────────────────
### 📌 5.bis info général
### ───────────────────────────────

def render_global_infos(action_table, date_debut, date_fin, top_n=15):
    """
    Génère un bloc HTML contenant :
    - Une synthèse texte
    - Le graph des activités par jour (30 jours)
    - Le barplot horizontal des équipes les plus actives
    """
    # 1. Préparer les dates
   
    actions["action_date"] = pd.to_datetime(actions["action_date"])
    recent = actions[actions["action_date"] >= date_debut]

    # Synthèse
    nb_teams = recent["team_id"].nunique()
    nb_users = recent["user_id"].nunique()
    nb_actions = len(recent)
    
    # 2. Activités par jour
    per_day = recent.groupby("action_date").size().reset_index(name="nb_actions")

    fig1, ax1 = plt.subplots(figsize=(6, 3.5))
    ax1.bar(per_day["action_date"].dt.strftime("%d %b"), per_day["nb_actions"], color="#6FBFA5", alpha=0.8, width=0.3)
    ax1.set_title(f"Activité globale par jour: Depuis le {date_debut.date()}")
    ax1.set_ylabel("Nombre d’actions")
    ax1.set_xlabel("Date")
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    plt.xticks(rotation=45,fontsize = 8)
    fig1.tight_layout()

    b64_1 = get_base64_chart(fig1)

    # 3. Equipes les plus actives
    team_counts = recent.groupby("team_name").size().sort_values(ascending=False).head(top_n)

    fig2, ax2 = plt.subplots(figsize=(6, 4.5))
    team_counts.sort_values().plot.barh(ax=ax2, color="#6FBFA5", alpha=0.6)
    ax2.set_title(f"👥 Les équipes les plus actives ({(date_fin - date_debut).days} derniers jours)")
    ax2.set_xlabel("Nombre d’actions")
    ax2.set_ylabel("")
    ax2.grid(axis="x", linestyle="--", alpha=0.3)
    fig2.tight_layout()

    b64_2 = get_base64_chart(fig2)
    
    # 4 type d'activités
    # Regroupement
    type_counts = recent["action"].value_counts().sort_values(ascending=False)

    # 🎨 Palette sobre
    palette = sns.color_palette("Greens", len(type_counts))[::-1]

    # Création du graphique
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=type_counts.values, y=type_counts.index, palette=palette, ax=ax3)
    ax3.set_xlabel("Nombre d’actions")
    ax3.set_ylabel("Type d’action")
    ax3.set_title("Répartition des types d’action sur la période")
    ax3.grid(axis="x", linestyle="--", alpha=0.3)
    plt.tight_layout()

    b64_3 = get_base64_chart(fig3)
    
    # 4. Bloc HTML
    html = f"""
    <div style="border: 1px solid #ddd; padding: 1rem; border-radius: 10px; background-color: #f9f9f9; margin-bottom: 2rem;">
        <h2 style="color:#2c3e50;">📊 Vue d'ensemble (du {date_debut.strftime('%d %b %Y')} au {date_fin.strftime('%d %b %Y')})</h2>
        <p><b>🔢 Nombre total d’actions :</b> {nb_actions}<br>
           <b>👤 Utilisateurs impliqués :</b> {nb_users}<br>
           <b>🏢 Équipes concernées :</b> {nb_teams}</p>

        <h4 style="margin-top:2rem;">Évolution des activités</h4>
        <img src="data:image/png;base64,{b64_1}" style="max-width:100%; height:auto;" />

        <h4 style="margin-top:2rem;">Équipes les plus actives</h4>
        <img src="data:image/png;base64,{b64_2}" style="max-width:100%; height:auto;" />
        
        <h4 style="margin-top:2rem;">Répartition du type d'activité</h4>
        <img src="data:image/png;base64,{b64_3}" style="max-width:100%; height:auto;" />

    </div>
    """
    return html


### ───────────────────────────────
### 🧾 6. Construction du PDF
### ───────────────────────────────
def build_pdf(html_blocks, output_path="rapport_client.pdf"):
    """Assemble les blocs HTML + entête pour générer un PDF propre."""
    action_table = actions.copy()
    date_str = datetime.today().strftime("%Y-%m-%d")
    date_debut = datetime.today() - timedelta(days=30)
    date_fin = datetime.today()

    # Entête + bloc d'infos globales
    header = render_entete_html()  # déjà codé
    bloc_infos = render_global_infos(action_table, date_debut, date_fin)
    bloc_superusers = render_super_users_html()
    # mini rapports ajoutés
    body = "".join(html_blocks) 

    html_full = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 12pt;
                color: #2c3e50;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
            }}
            img {{
                max-width: 100%;
            }}
            .section {{
                margin-bottom: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="section">{header}</div>
        <div class="section">{bloc_infos}</div>
        <hr style="border: none; border-top: 1px solid #ccc; margin: 1.5rem 0;" />
        <div class="section">{bloc_superusers}</div>
        <hr style="border: none; border-top: 1px solid #ccc; margin: 1.5rem 0;" />
        <h1> Rapports individuels ajoutés…</h1>
        <div class="section">{body}</div>
    </body>
    </html>
    """

    # Génération PDF
    with open(output_path, "wb") as f:
        pisa.CreatePDF(html_full, dest=f)

    return output_path
