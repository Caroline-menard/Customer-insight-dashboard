<p align="right">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/logo_blanc.png?raw=true" alt="Logo Caroline Ménard" width="120">
</p>

🇬🇧 [View the English version](README.en.md)


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

 **Son objectif principal :** améliorer la qualité de l’accompagnement client, en particulier durant les phases sensibles comme l’onboarding, la prise en main du produit, et le suivi post-lancement.

 **Ce que permet ce dashboard :**

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

# Description de l'application
## Page d'accueil:
🔁 Bouton de rafraîchissement des données (en bas de page) :
Ce bouton permet de recharger les données affichées dans le dashboard.

  >💡 Dans le projet réel, ce bouton déclenche un appel sécurisé vers les APIs internes pour interroger la base de données métier et récupérer les dernières activités.
<p align="center">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/Capture%20d%E2%80%99e%CC%81cran%202025-05-13%20a%CC%80%2022.10.25.png?raw=true" alt="Page d'accueil" width="800">
</p>

## Check-up général
La page Check-up général donne une vue synthétique de l’état d’activité global sur la plateforme.

Elle contient notamment :

   - **Des indicateurs clés :**

     > - Nombre total de teams
     > - Nombre de teams actives sur les 30 derniers jours
     > - nombre de teams inactives sur les 6 derniers mois
     > - La dernière activité détectée : nom de l’équipe la plus récemment active et date correspondante

  -  **Les dernières équipes arrivées :** tableau listant les teams récemment intégrées, leur effectif et leur date d’arrivée

  - **Un graphique de la répartition de la date de derniére activité par équipe.**

🛎️ Cette page permet à un Customer Success Manager ou un responsable produit d’avoir en un coup d'œil une idée de l’engagement global des clients, et de repérer rapidement les signaux faibles (arrivées récentes à suivre, inactivité prolongée…).

<p align="center">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/Capture%20d%E2%80%99e%CC%81cran%202025-05-13%20a%CC%80%2022.17.52.png?raw=true" alt="Check-up general" width="800">
</p>

## Zoom sur les Teams 
La page Zoom sur les Teams permet d’explorer en détail l’activité de chaque équipe cliente.

Fonctionnalités principales :

  > - Un vue globale des Teams les plus actives *(screen1)* <br> 
  > -  Filtrage dynamique des équipes et affichage de sa composition. *(screen2)* <br> 
  > -  Visualisation  des comportements (volume d’actions, type d’activité, derniers accès…) *(screen3 & 4)*<br>
  > - Identification des “super users” au sein de chaque équipe <br>
  > -  Génération automatique d’un rapport d’activité PDF en un clic, intégrant : <br>
         >  Un rapport global sur les 30 derniers jours.<br>
         >  Des mini-rapports détaillés pour chaque équipe 'ajoutée'.<br>
         Fonction de génération du pdf dans `Utils.rapport_generator.py` 

➡️ Un exemple de fichier généré est disponible dans le dossier `Rapports/` sous le nom `rapport_client_{date}.pdf.`

`screen1`
<p align="center">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/Capture%20d%E2%80%99e%CC%81cran%202025-05-13%20a%CC%80%2022.28.15.png?raw=true" alt="Screen1" width="500">
</p>

`screen2`
<p align="center">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/Capture%20d%E2%80%99e%CC%81cran%202025-05-13%20a%CC%80%2022.28.59.png?raw=true" alt="Screen2" width="500">
</p>

`screen3`
<p align="center">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/Capture%20d%E2%80%99e%CC%81cran%202025-05-13%20a%CC%80%2022.29.25.png?raw=true" alt="Screen3" width="500">
</p>

`screen4`
<p align="center">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/Capture%20d%E2%80%99e%CC%81cran%202025-05-13%20a%CC%80%2022.29.38.png?raw=true" alt="Screen4" width="500">
</p>

(*) *Le type d'interactions présentées ici sont elles aussi fictives.*

## Zoom sur le type d'interaction
Cette page permet de filtrer l’activité par type d’interaction (ex : recherche, export, chatbot...)
Elle affiche le volume total de cette activité sur les 30 derniers jours, ainsi que les équipes les plus concernées par ce type d’usage.

## Page de téléchargement:
Cette page permet d’exporter les données d’activité au format Excel, pour une analyse complémentaire.
Le fichier peut être filtré par équipe, par utilisateur, et par période, afin de ne récupérer que les informations pertinentes.

📎 Ce format est particulièrement utile pour les équipes non techniques ou pour préparer un reporting client rapide.

## Page "Glossaire"
Cette page présente les définitions des typologies d’interaction utilisées dans le dashboard.
Les catégories affichées sont ici fictives, mais elles permettent d’assurer une meilleure compréhension des résultats pour les utilisateurs non techniques. 
Les définitions sont stockées dans le fichier `Utils.utils.py`


# 🔎 Pour aller plus loin

À partir de ce type de données d’activité, il serait possible d’appliquer des algorithmes non supervisés (comme le clustering) afin d’identifier des profils d’usage d’équipe.

Cela permettrait par exemple de :

  - Repérer des équipes très autonomes, nécessitant peu de support ou d’accompagnement 

  - Détecter des équipes centrées sur un type d’usage particulier (ex. recherche, export…) et leur proposer des fonctionnalités complémentaires ciblées 

  - Identifier des équipes en sous-utilisation de la plateforme, et ajuster les actions de Customer Success en conséquence.

Ce type d’analyse peut enrichir considérablement les actions de suivi client et favoriser un accompagnement personnalisé à grande échelle.
