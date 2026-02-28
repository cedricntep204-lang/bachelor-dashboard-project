#  Tableau de Bord – Performance IoT

##  Description du projet

Ce projet a pour objectif d’analyser des logs d’exécution IoT à partir de fichiers JSON, d’extraire des métriques de performance et de les visualiser via un dashboard interactif développé avec Streamlit.

Le système se compose de deux parties principales :
- Un pipeline d’analyse de données (pipeline_iot.py)
- Un dashboard interactif (app.py)

---

##  Architecture du projet

1. Extraction des données JSON
2. Analyse des performances :
   - Informations globales des runs (run_info)
   - Chronologie d’exécution (execution_trace)
   - Analyse des flux (link_data)
3. Génération de fichiers CSV
4. Visualisation interactive via Streamlit

---

##  Fonctionnalités du Dashboard

- Indicateurs globaux (temps moyen, nombre de runs)
- Sélection dynamique d’un Run ID
- Timeline d’exécution (diagramme de Gantt)
- Top 3 blocs les plus lents
- Répartition SUCCESS vs ERROR
- Moyenne des performances par type de classe

---

##  Installation

### 1️ Cloner le repository

```bash
git clone <url>
cd bachelor-dashboard-project

### 2 Créer et activer l’environnement
conda create -n graph-profiler python=3.10
conda activate graph-profiler
pip install pandas streamlit

### 3 Lancer le pipeline
python pipeline_iot.py

### 4 Lancer le dashboard
streamlit run app.py


Contributions: 
Cedric : Structure du projet, pipeline d’analyse, gestion Git, coordination
Evan :Développement du dashboard Streamlit
Ali :
Mohamed :