<p align="right">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/logo_blanc.png?raw=true" alt="Logo Caroline Ménard" width="120">
</p>

# Customer Insight Dashboard
**Contexte:** *Ce projet est une adaptation d’un outil développé dans un contexte professionnel réel. Entreprise B2B, offrant un accès à des services via une plateforme web.  
Chaque client y est représenté par une **équipe** regroupant plusieurs **utilisateurs finaux**, aux profils et usages variés.*


Pour des raisons évidentes de **confidentialité** et de **sécurité**, l’ensemble du code a été modifié et les données utilisées dans cette version sont **entièrement synthétiques**.

➡️ Si cela vous intéresse, le notebook `synthetic_data_generator.ipynb` explique comment ces données simulées ont été construites.

---
## Présentation du projet:
Ce projet propose une **petite application locale**, avec un environnement léger (📦 Python 3.9.12 + `requirements.txt`) conçu pour être utilisé par des équipes en lien direct avec les clients, notamment :

  > - Responsables clientèle <br>
  > - Customer Success Managers <br>
  > - Chargé(e)s de support ou d’onboarding

🎯 Son objectif principal : améliorer la qualité de l’accompagnement client, en particulier durant les phases sensibles comme l’onboarding, la prise en main du produit, et le suivi post-lancement.
🔍 Ce que permet ce dashboard :

  Suivre l’activité des utilisateurs de manière simple et visuelle

  > - Repérer des profils “super users” (interlocuteurs à l’aise avec le produit, souvent moteurs au sein de leur équipe)
  > - Identifier des équipes peu actives, potentiellement en difficulté dans l’usage de la plateforme
  > -  Explorer les interactions avec le produit pour afin de repérer des fonctionnalités peu utilisées, peut-être mal connues ou mal présentées lors des formations
  > -  Exporter les données au format Excel et générer un rapport PDF en un clic — pratique pour les profils non techniques.

**Tout cela en conciliant :**
> - Le respect de l’intimité utilisateur (les logs sont volontairement **minimalistes**)
> - Et la capacité à réagir plus intelligemment aux besoins de ses clients grâce à une interface **ergonomique et synthétique**

# Installation et lancement:
**Python 3.9.12 recommandé.** <br>

- Installation des requirements <br>
`pip install -r requirements.txt` <br>

- Demarrage du dashboard: <br>
`streamlit run J_Dashboard.py`

# Description de l'application:
## Page d'accueil:
🔁 Bouton de rafraîchissement des données (en bas de page) :
Ce bouton permet de recharger les données affichées dans le dashboard.

  >💡 Dans le projet réel, ce bouton déclenche un appel sécurisé vers les APIs internes pour interroger la base de données métier et récupérer les dernières activités.

