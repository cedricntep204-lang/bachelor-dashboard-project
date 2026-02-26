import json
import os
import pandas as pd

# --------------------------
# 1️⃣ Configuration
# --------------------------
dossier_json = "set_4"
data_list = []
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
            
            run_id = data.get("run_info", {}).get("run_id", "UNKNOWN")
            execution_trace = data.get("execution_trace", [])

            for bloc in execution_trace:
                data_list.append({
                    "run_id": run_id,
                    "block_id": bloc.get("block_id", ""),
                    "class": bloc.get("class", ""),
                    "duration_ms": bloc.get("duration_ms", 0)
                })
            
            print(f"{nom_fichier} chargé avec succès")

        except Exception as e:
            print(f"Erreur avec {nom_fichier}: {e}")
            fichiers_corrompus.append(nom_fichier)

# --------------------------
# 3️⃣ Création du DataFrame
# --------------------------
df = pd.DataFrame(data_list)
print("\nAperçu des données extraites :")
print(df.head())

# Sauvegarde complète
df.to_csv("extracted_blocks.csv", index=False)
print("\nToutes les données valides ont été sauvegardées dans 'extracted_blocks.csv'")

# --------------------------
# 4️⃣ Analyse : stats par bloc
# --------------------------
stats_blocs = df.groupby("block_id")["duration_ms"].agg(["mean", "max"]).reset_index()
stats_blocs.to_csv("stats_blocs.csv", index=False)
print("\nStats des blocs sauvegardées dans 'stats_blocs.csv'")

# --------------------------
# 5️⃣ Top 3 blocs les plus lents
# --------------------------
top_3_lents = stats_blocs.sort_values("mean", ascending=False).head(3)
top_3_lents.to_csv("top_3_blocs_lents.csv", index=False)
print("\nTop 3 blocs les plus lents sauvegardés dans 'top_3_blocs_lents.csv'")
print(top_3_lents)

# --------------------------
# 6️⃣ Résumé des fichiers corrompus
# --------------------------
if fichiers_corrompus:
    print("\n Fichiers corrompus détectés :")
    for f in fichiers_corrompus:
        print(f"- {f}")
else:
    print("\n Aucun fichier corrompu détecté")