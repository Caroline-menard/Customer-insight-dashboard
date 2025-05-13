<p align="right">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/logo_blanc.png?raw=true" alt="Logo Caroline Ménard" width="120">
</p>

# Customer Insight Dashboard

*This project is an adaptation of a tool originally developed in a real professional environment.*
**The context:** a B2B company providing access to services through a web-based platform.
Each client is represented by a team made up of multiple end users with varied usage patterns and profiles.

For obvious **security** and **confidentiality** reasons, the entire codebase has been adjusted, and the data used in this version is entirely synthetic.

➡️ If you're curious, the notebook `synthetic_data_generator.ipynb` explains how the simulated dataset was generated.

---
# Project Overview

This project offers a lightweight local application designed for teams working directly with clients.
It runs in a minimal environment (📦 Python 3.9.12 + requirements.txt) and is aimed at:

  > - Account managers <br>
  > - Customer Success Managers <br>
  > - Support and onboarding specialists

 **Main objective:**
To improve the quality of client support, particularly during sensitive phases such as onboarding, product adoption, and post-launch follow-up.

**What this dashboard enables:**

  > - Track user activity in a clear and visual way <br>
  > - Identify “super users” — confident product users who often act as internal champions <br>
 >  - Spot inactive teams who may be facing difficulties in adopting the platform <br>
  > - Explore how the product is used to identify underused features, which may have been poorly introduced during onboarding <br>
> -   Export filtered data in Excel format and generate a PDF activity report in one click — ideal for non-technical stakeholders

**All while balancing:**

  > - User privacy, thanks to intentionally minimalist log data <br>
  > - And the ability to respond more intelligently to client needs, via a streamlined and ergonomic interface

# Installation & Launch

- Recommended Python version: 3.9.12

- Make sure you are in the root directory of the project before running the commands.

- Install dependencies <br>
`pip install -r requirements.txt`

- Launch the dashboard <br>
`streamlit run J_Dashboard.py`

# Application Description

## Home Page:

🔁 **Data refresh button** (located at the bottom of the page):  
This button allows users to reload the data displayed in the dashboard.

> 💡 In the real (confidential) version of the project, this button triggers a **secure call to internal APIs** in order to query the production database and retrieve the latest activity logs.
<p align="center">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/Capture%20d%E2%80%99e%CC%81cran%202025-05-13%20a%CC%80%2022.10.25.png?raw=true" alt="Page d'accueil" width="800">
</p>

## General Check-up

The **General Check-up** page provides a high-level overview of global client activity on the platform.

It includes:

- **Key indicators:**

  > - Total number of teams  
  > - Number of teams active in the past 30 days  
  > - Number of teams inactive for over 6 months  
  > - Last recorded activity: the most recently active team and the corresponding date  

- **Recently onboarded teams:**  
  A table listing the most recently created teams, with their size and join date

- **A chart showing the distribution of the last activity date per team**

🛎️ This page allows a **Customer Success Manager** or **Product Owner** to get, at a glance, an overview of client engagement levels — and to quickly identify early warning signs (recent sign-ups to monitor, prolonged inactivity, etc.).

<p align="center">
  <img src="https://github.com/Caroline-menard/-Caroline-menard/blob/main/Capture%20d%E2%80%99e%CC%81cran%202025-05-13%20a%CC%80%2022.17.52.png?raw=true" alt="Check-up general" width="800">
</p>

## Zoom on Teams

The **Zoom on Teams** page allows for a detailed exploration of each client team's activity.

Main features:

> - A global view of the most active teams *(screen1)*  
> - Dynamic filtering of teams and display of team composition *(screen2)*  
> - Visualization of user behavior (volume of actions, types of activity, last access, etc.) *(screen3 & 4)*  
> - Identification of “super users” within each team  
> - One-click generation of a **PDF activity report**, which includes:  

> > - A global summary covering the last 30 days  
 > > - Individual mini-reports for each 'added' team  
 > > - The PDF generation logic is handled in `Utils/rapport_generator.py`

➡️ A sample generated file is available in the `Rapports/` folder, under the name `rapport_client_{date}.pdf`.

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

(*) *The interaction types presented here are also fictitious.*

## Zoom on Interaction Type

This page allows filtering of activity by **type of interaction** (e.g. search, export, chatbot...).  
It displays the **total volume** of the selected interaction type over the past 30 days, as well as the **teams most actively using it**.

---

## Download Page

This page allows you to **export activity data in Excel format** for further analysis.  
The file can be filtered **by team**, **by user**, and **by time period**, to extract only the relevant information.

📎 This export format is particularly useful for **non-technical teams** or for preparing a quick **client-facing report**.

---

## Glossary Page

This page presents **definitions for the different interaction categories** used in the dashboard.  
The categories shown are **fictitious**, but help provide **better understanding** of the data for non-technical users.  
Definitions are stored in the file: `Utils/utils.py`.

# 🔎 Going Further

Based on this type of activity data, it would be possible to apply **unsupervised learning algorithms** (such as clustering) to identify **team usage profiles**.

This could, for example, help to:

- Detect **highly autonomous teams** that require little support or follow-up  
- Identify teams with **focused usage patterns** (e.g. search, export…) and suggest targeted complementary features  
- Spot **under-engaged teams** and adapt Customer Success actions accordingly

Such analysis could greatly enhance client follow-up strategies and enable **personalized support at scale**.


