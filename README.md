Data-Profiler IoT – Observabilité & Performance

Description du projet
Ce projet d'Observabilité Experte a pour objectif d'analyser 50 rapports d'exécution IoT (logs JSON) pour identifier les goulots d'étranglement (hotspots). Il permet de transformer des données brutes en un diagnostic visuel et chiffré pour faciliter la prise de décision automatisée.

 Architecture du projet

Le système suit une chaîne de valeur rigoureuse : JSON Raw Logs → Pandas → Data Analytics → Plotly → Streamlit.

Extraction & Ingestion (pipeline_iot.py) :

Parcours automatisé du dossier set_4.

Gestion robuste des erreurs via try/except pour isoler les fichiers corrompus.

Extraction des run_info, execution_trace et link_data vers des fichiers CSV.

Visualisation Interactive (app.py) :

Dashboard Streamlit intégrant des KPIs globaux et un filtrage dynamique par Run ID.

 Diagnostic de Performance 

L'analyse statistique sur l'ensemble du dataset a permis d'identifier précisément le goulot d'étranglement :

Bottleneck identifié : B_AGGREGATE_01 (ou B_AGGREGATE_02 selon le run).

Constat : La classe AGGREGATE présente les latences les plus critiques (moyenne > 36s).

 Installation et Lancement
1️ Cloner le repository

Bash
git clone https://github.com/cedricntep204-lang/PT_IOT.git
cd PT_IOT
2️ Configurer l'environnement Conda

Bash
conda create -n graph-profiler python=3.11 -y
conda activate graph-profiler

3️ Installer les dépendances

Bash
pip install -r requirements.txt

4️ Exécuter le projet

Générer les données : python pipeline_iot.py

Lancer le Dashboard : streamlit run app.py

Fonctionnalités du Dashboard

Indicateurs globaux : Temps moyen et volume de runs traités.

Timeline d'exécution : Diagramme de Gantt interactif via Plotly.

Analyse de dispersion : Box plots identifiant la stabilité par classe de traitement.

Contributions

Cedric : Architecture du projet, pipeline d’analyse ETL, gestion Git.

Evan : Développement du dashboard Streamlit et logique UI.

Ali : Visualisations expertes (Plotly) et amélioration de l'UX.

Mohamed : Tests de robustesse et validation des données.