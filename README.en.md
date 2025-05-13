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
