from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from Utils.utils import GLOSSAIRE_ACTIONS
import streamlit.components.v1 as components
from collections import OrderedDict
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
        🧩 Petit lexique des activités
    </h1>
    """, unsafe_allow_html=True)
    
st.markdown("""
<div style="background-color: #f5fefc;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            padding: 1rem; border-radius: 8px; font-size: 0.95rem;
            color: #2c3e50; margin-bottom: 2rem;">
 Ici, tu trouveras une petite définition pour chaque type d’action réalisée par les utilisateurs sur la plateforme.
C’est pratique pour bien comprendre ce que veulent dire tous les noms bizarres qu’on croise dans les graphes ! 😊
</div>
""", unsafe_allow_html=True)

#_______________________________________________________________
# ---Affichage des définitions---------
#_______________________________________________________________
GLOSSAIRE_ACTIONS_TRIE = OrderedDict(sorted(GLOSSAIRE_ACTIONS.items()))
# Glossaire avec fond vert pâle et séparateurs
glossaire_html = """
<div style="background-color:  #f5fefc; 
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            padding: 1.5rem; 
            border-radius: 10px;
            margin-top: 1rem;
            font-family: 'Segoe UI', sans-serif;
            font-size: 0.95rem;
            color: #2c3e50;">
"""

for i, (action, definition) in enumerate(GLOSSAIRE_ACTIONS_TRIE.items()):
    glossaire_html += f"""
    <div style="margin-bottom: 1.2rem;">
        <strong style="color: #3f7366;"> {action}</strong><br>
        <span>{definition}</span>
    </div>
    """

    # Ajouter un séparateur sauf après le dernier élément
    if i < len(GLOSSAIRE_ACTIONS) - 1:
        glossaire_html += """
        <hr style="border: none; border-top: 1px solid #88b29d; margin: 1rem 0;" />
        """

glossaire_html += "</div>"

components.html(glossaire_html, height=400, scrolling=True)