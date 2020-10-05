import os
import sys
from tqdm import tqdm
import pandas as pd
from pathlib import Path
sys.path.append(os.path.dirname(__file__))

input_dir_1 = Path("X:/Extraction_PDF_series")
input_dir_2 = Path("X:/Extraction_PDF_vrac")
output_dir = Path("C:/Users/jassu-ondo/Documents/projet_juradinfo_ia/data/analyses")

input_meta_data_file = Path("C:/Users/jassu-ondo/Documents/projet_juradinfo_ia/data/analyses/anal_metadata.xlsx")
input_meta_data_file_sheet = "data_dedoublonnees"

# retrieve requetes
df_requetes = pd.DataFrame(columns=['num_dossier', 'file_location', 'data_source'])
## input 1
data_source = "pdf_series"
for root, _, files in (os.walk(input_dir_1)):
	for name in files:
		if name.endswith(".pdf"):
			# print("-- Treating", name)
			requete_number = name.split("_")[1]
			file_location = os.path.abspath(os.path.join(root, name))
			dict_requete = {'num_dossier':int(requete_number), 'file_location':file_location, 'data_source':data_source}
			df_requetes = df_requetes.append(dict_requete, ignore_index=True)	
## input 2
l_pattern = ["_rep_", "_refere", "_requete", "_recours", "_req", "_memoire"] 
data_source = "pdf_vrac"
list_dir = [dir for dir in os.listdir(input_dir_2) if os.path.isdir(os.path.join(input_dir_2, dir))]
for dir in tqdm(list_dir):
	dir_location = os.path.join(input_dir_2, dir)
	dict_requete = {'num_dossier':int(dir), 'data_source':data_source}
	list_files = [f for f in os.listdir(dir_location) if os.path.isfile(os.path.join(dir_location, f))]
	for file in list_files:
		name = file
		if  any(x in name for x in l_pattern) and name.endswith("pdf"):
			file_location = os.path.join(dir_location, file)
			dict_requete['file_location'] = str(file_location) 
			df_requetes = df_requetes.append(dict_requete, ignore_index=True)
## typage colonne
df_requetes['num_dossier'] = df_requetes['num_dossier'].astype('int')

# order by num_dossier ascending
df_requetes = df_requetes.sort_values("num_dossier", ascending=True)

# looking for duplicates num_dossier
df_requetes["nb_doublons"] = df_requetes.groupby("num_dossier")["num_dossier"].transform('count')

# drop duplicates
df_requetes_dedoublonnee = df_requetes.drop_duplicates("num_dossier").drop(["nb_doublons"], axis=1)

# import meta data
df_meta_data = pd.read_excel(input_meta_data_file, input_meta_data_file_sheet)

# join requetes with meta data
df_requetes_meta_data = df_requetes_dedoublonnee.merge(df_meta_data, on=["num_dossier"], how='left')
						
# export excel
writer = pd.ExcelWriter(os.path.join(output_dir, "anal_requetes.xlsx"), engine='xlsxwriter')
df_requetes.to_excel(writer, sheet_name="data", index=False)
df_requetes_dedoublonnee.to_excel(writer, sheet_name="data_dedoublonnees", index=False)
df_requetes_meta_data.to_excel(writer, sheet_name="join_metadata", index=False)
writer.save()
