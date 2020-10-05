import sys
import os
from pathlib import Path

sys.path.append(
    os.path.dirname(__file__)
)  # path of the directory containing the current file : os.path.dirname(__file__)

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import pandas as pd
from src.base.db import DataBase


OUTPUT_FOLDER = Path(
    "/home/vsiyou-fotso/meta_donnees_a_importer/"
)  # Veuillez renseigner le dossier où sera enregistré les méta-données
INPUT_FOLDER = Path("/home/vsiyou-fotso/meta_donnees_a_importer/")

db = DataBase.initialize()


df_skipper = pd.read_excel(
    os.path.join(INPUT_FOLDER, "Extraction_Series_SkipperTA.xlsx")
)
df_skipper = df_skipper.iloc[:, 0:8]
df_skipper["fichier"] = "Extraction_Series_SkipperTA.xlsx"

df_linky = pd.read_excel(os.path.join(INPUT_FOLDER, "Serie_LINKY.xlsx"))
df_linky = df_linky.iloc[:, 0:8]
df_linky["fichier"] = "Serie_LINKY.xlsx"

df_asa = pd.read_excel(os.path.join(INPUT_FOLDER, "Serie ASA.xlsx"))
df_asa = df_asa.iloc[:, 0:8]
df_asa["fichier"] = "Serie_ASA.xlsx"

df_amiant = pd.read_excel(os.path.join(INPUT_FOLDER, "Serie_Amiante.xlsx"))
df_amiant = df_amiant.iloc[:, 0:8]
df_amiant["fichier"] = "Serie_Amiante.xslx"

df_235ter = pd.read_excel(os.path.join(INPUT_FOLDER, "Serie_235TER_CGI.xlsx"))
df_235ter = df_235ter.iloc[:, 0:8]
df_235ter["fichier"] = "Serie_235TER_CGI.xlsx"


lst = [df_linky, df_asa, df_amiant, df_235ter]
df = df_skipper

for d in lst:
    df = df.append(d)

engine = db["engine"]
chunk_size = 50

# renommage des colonnes
df.columns = [
    "num_dossier",
    "ta",
    "date_enreg",
    "tete_serie",
    "num_serie",
    "nom_serie",
    "matiere",
    "dossier",
    "titre",
]

# Identification de doublons
df["doublon"] = df["num_dossier"].duplicated()

df.to_sql("tmp_metadata", engine, if_exists="replace", index=True, chunksize=chunk_size)
df.to_excel(
    os.path.join(OUTPUT_FOLDER, "tmp_metadata.xlsx"), sheet_name="data", index=False
)
