import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Configuration de la page
st.set_page_config(layout="wide")
st.title("Tableau de bord - Performance IoT")

# 1. Charger les données
try:
    df = pd.read_csv("extracted_blocks.csv")
except FileNotFoundError:
    st.error("Le fichier 'extracted_blocks.csv' est introuvable. Assurez-vous que le script de traitement a été lancé.")
    st.stop()

# 2. KPIs 
col1, col2 = st.columns(2)
with col1:
    st.metric("Temps moyen global", f"{df['duration_ms'].mean():.2f} ms")
with col2:
    # Compte le nombre de runs uniques
    st.metric("Total runs analysés", len(df['run_id'].unique()))

# 3. Sélecteur de Run
run_id = st.selectbox("Sélectionner un Run ID", df["run_id"].unique())
df_run = df[df["run_id"] == run_id]

# 4. Gantt Chart (Correction de la Visualisation Experte)
st.subheader(f"Timeline pour le run : {run_id}")

# Tri des blocs par step pour respecter l'ordre d'exécution
df_run = df_run.sort_values(by="step")

# Création de timestamps de début et fin pour la visualisation
start_time = datetime.datetime(2026, 1, 1, 0, 0, 0)
df_run['start_time'] = start_time
df_run['end_time'] = df_run['start_time'] + pd.to_timedelta(df_run['duration_ms'], unit='ms')

# Création du graphique Gantt
fig = px.timeline(
    df_run, 
    x_start="start_time", 
    x_end="end_time", 
    y="block_id", 
    title="Timeline de l'exécution",
    hover_data=["duration_ms"] # Affiche la durée au survol
)
fig.update_yaxes(autorange="reversed") # Pour avoir le premier bloc en haut
st.plotly_chart(fig, use_container_width=True)