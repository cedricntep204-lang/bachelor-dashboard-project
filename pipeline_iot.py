import json
import os
import pandas as pd

# --------------------------
# 1️⃣ Configuration
# --------------------------
dossier_json = "set_4"

data_list = []
run_info_list = []
link_list = []
fichiers_corrompus = []

# --------------------------
# 2️⃣ Chargement et extraction
# --------------------------
for nom_fichier in os.listdir(dossier_json):

    if nom_fichier.endswith(".json"):
        chemin = os.path.join(dossier_json, nom_fichier)

        try:
            with open(chemin, "r") as f:
                data = json.load(f)

            # -------- RUN INFO --------
            run_info = data.get("run_info", {})

            run_id = run_info.get("run_id", "UNKNOWN")
            graph_id = run_info.get("graph_id", "UNKNOWN")
            status = run_info.get("status", "UNKNOWN")
            total_ms = run_info.get("total_ms", 0)
            timestamp = run_info.get("timestamp", "")

            run_info_list.append({
                "run_id": run_id,
                "graph_id": graph_id,
                "status": status,
                "total_ms": total_ms,
                "timestamp": timestamp
            })

            # -------- EXECUTION TRACE --------
            execution_trace = data.get("execution_trace", [])

            for step_index, bloc in enumerate(execution_trace):
                data_list.append({
                    "run_id": run_id,
                    "block_id": bloc.get("block_id", ""),
                    "class": bloc.get("class", ""),
                    "duration_ms": bloc.get("duration_ms", 0),
                    "step": step_index  # <--- On ajoute la colonne step ici
                })

                # Triggered links
                for link in bloc.get("triggered_links", []):
                    link_list.append({
                        "run_id": run_id,
                        "link_id": link,
                        "source_block": bloc.get("block_id", "")
                    })

            print(f"{nom_fichier} chargé avec succès")

        except Exception as e:
            print(f"Erreur avec {nom_fichier}: {e}")
            fichiers_corrompus.append(nom_fichier)

# --------------------------
# 3️⃣ DataFrames
# --------------------------
df_blocks = pd.DataFrame(data_list)
df_runs = pd.DataFrame(run_info_list)
df_links = pd.DataFrame(link_list)

# --------------------------
# 4️⃣ Sauvegarde données brutes
# --------------------------
df_blocks.to_csv("extracted_blocks.csv", index=False)
df_runs.to_csv("run_info_extracted.csv", index=False)
df_links.to_csv("link_data_extracted.csv", index=False)

print("\nFichiers d'extraction sauvegardés")

# --------------------------
# 5️⃣ Analyse blocs
# --------------------------
if not df_blocks.empty:

    stats_blocs = df_blocks.groupby("block_id")["duration_ms"].agg([
        "mean",
        "max",
        "count"
    ]).reset_index()

    stats_blocs.to_csv("stats_blocs.csv", index=False)

    top_3_lents = stats_blocs.sort_values("mean", ascending=False).head(3)
    top_3_lents.to_csv("top_3_blocs_lents.csv", index=False)

    print("\nStats blocs et top 3 lents calculés")

# --------------------------
# 6️⃣ Analyse runs
# --------------------------
if not df_runs.empty:

    print("\nStatistiques globales des runs :")
    print(f"Nombre total de runs : {len(df_runs)}")
    print(f"Temps moyen execution : {df_runs['total_ms'].mean():.2f} ms")
    print(f"Temps max execution : {df_runs['total_ms'].max()} ms")

    print("\nStatus distribution :")
    print(df_runs["status"].value_counts())

# --------------------------
# 7️⃣ Analyse links
# --------------------------
if not df_links.empty:

    link_stats = df_links.groupby("link_id").size().reset_index(name="activation_count")

    link_stats.to_csv("link_stats.csv", index=False)

    print("\nStatistiques des liens sauvegardées")

# --------------------------
# 8️⃣ Fichiers corrompus
# --------------------------
if fichiers_corrompus:
    print("\nFichiers corrompus détectés :")
    for f in fichiers_corrompus:
        print(f"- {f}")

else:
    print("\nAucun fichier corrompu détecté")