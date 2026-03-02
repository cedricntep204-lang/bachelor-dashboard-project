import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# Configuration de la page
st.set_page_config(layout="wide", page_title="Dashboard IoT")
st.title("Tableau de bord - Performance IoT")

# 1. Charger les données
try:
    df = pd.read_csv("extracted_blocks.csv")
    if 'status' not in df.columns:
        df['status'] = 'UNKNOWN'     #Evan (pour plus que ca affiche le message d'erreur)
    # Ajout Ali : Extraction du type de classe pour l'analyse globale
    df['class_type'] = df['block_id'].str.split('_').str[1].fillna('OTHER')
except FileNotFoundError:
    st.error("Le fichier 'extracted_blocks.csv' est introuvable.")
    st.stop()
  
# 2. --- ANALYSE STATISTIQUE GLOBALE --- # Cedric (Grâce au traitement global par Pandas, j'ai identifié que le bloc B_AGGREGATE_01 est le point critique du système avec une latence moyenne de 36s, ce qui impacte directement le temps total d'exécution des runs et la réactivité globale du système. En se concentrant sur l'optimisation de ce bloc, on pourrait potentiellement réduire significativement les temps d'exécution et améliorer la performance globale du système IoT.)
st.header("🔍 Diagnostic de Performance Global (50 Runs)")

# Calcul des stats sur TOUT le dataframe 'df'
global_stats = df.groupby("block_id")["duration_ms"].agg(["mean", "max"]).reset_index()
global_stats = global_stats.sort_values("mean", ascending=False).head(5)

col_glob1, col_glob2 = st.columns([1, 2])

with col_glob1:
    st.subheader("Bottleneck Identifié")
    # On récupère le nom du pire bloc
    worst_block = global_stats.iloc[0]["block_id"]
    worst_value = global_stats.iloc[0]["mean"]
    st.error(f"Le bloc le plus lent est : **{worst_block}**")
    st.metric("Latence Moyenne", f"{worst_value:.2f} ms")

with col_glob2:
    # Graphique des 5 blocs les plus lents sur tout le dataset
    fig_global = px.bar(
        global_stats, x='mean', y='block_id', orientation='h',
        title="Top 5 des latences moyennes (Global)",
        labels={'mean': 'Moyenne (ms)', 'block_id': 'ID du Bloc'},
        color='mean', color_continuous_scale='OrRd'
    )
    st.plotly_chart(fig_global, use_container_width=True)
st.divider()

# KPIs Généraux
col_kpi1, col_kpi2 = st.columns(2)
with col_kpi1:
    st.metric("Temps moyen global", f"{df['duration_ms'].mean():.2f} ms")
with col_kpi2:
    st.metric("Total runs analysés", len(df['run_id'].unique()))

# 3. Sélecteur de Run
run_id = st.selectbox("Sélectionner un Run ID", df["run_id"].unique())
df_run = df[df["run_id"] == run_id].sort_values(by="step")

# --- AJOUTS D'ALI : ANALYSES VISUELLES ---
st.divider()
col_left, col_right = st.columns(2)

with col_left:
    # Graphique SUCCESS vs ERROR (Basé sur df_run pour le run actuel)
    if 'status' in df_run.columns:
        stats = df_run['status'].value_counts()
        fig_pie = go.Figure(data=[go.Pie(
            labels=stats.index, 
            values=stats.values, 
            hole=.5,
            marker_colors=['#2ecc71', '#e74c3c']
        )])
        fig_pie.update_layout(title_text=f"Fiabilité du run : {run_id}")
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Colonne 'status' introuvable : impossible d'afficher le graphique de fiabilité.")

with col_right:
    # Top 3 blocs les plus lents du run
    top_3 = df_run.nlargest(3, 'duration_ms')
    fig_top = px.bar(
        top_3, x='duration_ms', y='block_id', orientation='h',
        color='duration_ms', color_continuous_scale='Reds',
        title="Top 3 des goulots d'étranglement (ms)"
    )
    fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top, use_container_width=True)

# 4. Gantt Chart (Timeline)
st.subheader(f"Timeline détaillée : {run_id}")
start_time = datetime.datetime(2026, 1, 1, 0, 0, 0)
df_run['start_time'] = start_time
# si la colonne status manque, on la crée pour éviter les erreurs
if 'status' not in df_run.columns:
    df_run['status'] = 'UNKNOWN'

df_run['end_time'] = df_run['start_time'] + pd.to_timedelta(df_run['duration_ms'], unit='ms')

fig_gantt = px.timeline(
    df_run, x_start="start_time", x_end="end_time", y="block_id", 
    color="status", # Couleur par statut pour l'UX
    color_discrete_map={"SUCCESS": "#2ecc71", "ERROR": "#e74c3c", "UNKNOWN": "#95a5a6"}
)
fig_gantt.update_yaxes(autorange="reversed")
st.plotly_chart(fig_gantt, use_container_width=True)

# 5. Analyse Globale (Moyenne par classe)
st.divider()
st.subheader("Analyse comparative par type de traitement")
fig_box = px.box(
    df, x='class_type', y='duration_ms', 
    color='class_type', title="Dispersion des performances par classe"
)
st.plotly_chart(fig_box, use_container_width=True)
