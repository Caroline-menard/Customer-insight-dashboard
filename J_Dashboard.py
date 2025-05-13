from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
import base64
import streamlit.components.v1 as components
from pathlib import Path
import base64
from Utils.utils import fetch_teams_data, fetch_logs_data

# 💅 Appliquer le style CSS global
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Logo ---
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
space1,mb, space2 = st.columns([3,1,3])
with mb:
    logo = Image.open("fake_logo.png")
    st.image(logo, width=180)

st.session_state["data_loaded"] = True
# --- Message d'accueil ---
st.markdown("""
Bienvenue à bord, **J.** !  
Ce dashboard a été conçu pour **t’aider à repérer les utilisateurs actifs ou discrets** et à garder un œil sur les équipes de ta galaxie *companyName* 🚀

---

##### 🔍 Ce que tu peux faire ici :

- **Voir quelles équipes sont actives ou non** sur les  derniers mois  
- **Explorer la composition d’une équipe** et les dates de dernière activités  
- **Analyser l’activité d’un utilisateur** : fréquence, typologie d’actions...  
- **Télécharger facilement les données** au format Excel pour tes suivis

---

###### 🛠️ Comment fermer l’application dans ton terminal ?

Tape simplement dans ton terminal:
**Ctrl + C** puis **exit** """)



# 1. Encode la police en base64
def encode_font_to_base64(path):
    with open(path, "rb") as f:
        font_data = f.read()
    return base64.b64encode(font_data).decode()



CACHE_DIR = Path("data_cache")
CACHE_DIR.mkdir(exist_ok=True)


def charger_et_sauvegarder_les_donnees():
    with st.spinner("📦 Rafraîchissement des données en cours..."):
        df_teams = fetch_teams_data(return_user_table=True)
        ###=>['team_id', 'team_name', 'user_id', 'join_date', 'last_login_date','user']
        df_actions = fetch_logs_data()
        ###==>['team_id', 'user_id', 'action', 'action_date']
        df_global = fetch_teams_data()
        ##==>['team_id', 'team_name', 'effectif', 'join_date', 'last_login_date','last_action_date', 'last_move_date']
        df_teams.to_parquet(CACHE_DIR / "teams.parquet", index=False)
        df_actions.to_parquet(CACHE_DIR / "actions.parquet", index=False)
        df_global.to_parquet(CACHE_DIR / "global.parquet", index=False)
        (CACHE_DIR / "done.flag").touch()
    st.success("✅ Données mises à jour avec succès !")
    st.session_state["data_loaded"] = True

# Initialisation une seule fois
if "data_loaded" not in st.session_state:
    # Suppression des anciens fichiers
    for file in CACHE_DIR.glob("*.parquet"):
        file.unlink()
    (CACHE_DIR / "done.flag").unlink(missing_ok=True)
    charger_et_sauvegarder_les_donnees()
else:
    st.info("✅ Les données sont prêtes pour cette session.")


if st.button("🔁 Rafraîchir les données maintenant"):
    for file in CACHE_DIR.glob("*.parquet"):
        file.unlink()
    (CACHE_DIR / "done.flag").unlink(missing_ok=True)
    charger_et_sauvegarder_les_donnees()



st.divider()
st.markdown("""
<div style="text-align: center; font-size: 0.95rem; color: gray;">
    <em>🌱 Aucune data scientist n’a été maltraitée pendant l’élaboration de ce dashboard.🌱</em>
</div>
""", unsafe_allow_html=True)
st.divider()