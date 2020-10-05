"""
Count number of pages in all 'requete' files.
"""

import os
import sys
import pandas as pd
from PyPDF2 import PdfFileReader
from tqdm import tqdm
from pathlib import Path

sys.path.append(os.path.dirname(__file__))
# os.chdir(os.path.dirname(__file__))

input_dir_1 = "X:\Extraction_PDF_series"
#input_dir_2 = "X:\Extraction_PDF_vrac"
#input_dir_3 = "C:\Users\jassu-ondo\Documents\projet_juradinfo_ia\data\skipper\requetes"

output_dir = Path("C:\Users\jassu-ondo\Documents\projet_juradinfo_ia\data\analyses")

if __name__ == "__main__":
    
	df_requetes = pd.DataFrame(columns=['requete_number', 'file_location', 'data_source', 'page_count'])

	# input 1
	data_source = "pdf_serie"
	for root, _, files in (os.walk(input_dir_1)):
		for name in files:
			if name.endswith(".pdf"):
				print("-- Treating", name)
				requete_number = name.split("_")[1]
				file_location = os.path.abspath(os.path.join(root, name))
				pdf=PdfFileReader(open(file_location,'rb'))
				page_count = pdf.getNumPages()
				df_requetes = df_requetes.append(
				{'requete_number':requete_number, 'file_location':file_location, 'data_source':data_source, 'page_count':page_count}, ignore_index=True)
	"""
	# input 2 
	l_pattern = ["_rep_", "_refere", "_requete", "_recours", "_req", "_memoire"] 
	data_source = "pdf_vrac"
	for root, dirs, _ in tqdm(os.walk(input_dir_2)):
		for dir_name in dirs:
			dir_location = os.path.abspath(os.path.join(root, dir_name))
			for _, files in os.walk(dir_location):
				for name in files:
					if  any(x in name for x in l_pattern) and name.endswith("pdf"):
						requete_number = dir_name
						file_location = os.path.abspath(os.path.join(dir_location, name))
						pdf=PdfFileReader(open(file_location,'rb'))
						page_count = pdf.getNumPages()
						df_requetes = df_requetes.append({'requete_number':requete_number, 'file_location':file_location, 'data_source':data_source, 'page_count':page_count}, ignore_index=True)
		
	# input 3
	l_pattern = ["_rep_", "_refere", "_requete", "_recours", "_req", "_memoire"] 
	data_source = "pdf_vrac"
	for root, dirs, _ in tqdm(os.walk(input_dir_3)):
		for dir_name in dirs:
			dir_location = os.path.abspath(os.path.join(root, dir_name))
			for _, files in os.walk(dir_location):
				for name in files:
					if  any(x in name for x in l_pattern) and name.endswith("pdf"):
						requete_number = dir_name
						file_location = os.path.abspath(os.path.join(dir_location, name))
						pdf=PdfFileReader(open(file_location,'rb'))
						page_count = pdf.getNumPages()
						df_requetes = df_requetes.append({'requete_number':requete_number, 'file_location':file_location, 'data_source':data_source, 'page_count':page_count}, ignore_index=True)
	"""
	df_requetes.to_excel(os.path.join(output_dir, "requetes_page_count.xlsx"), sheet_name="data", index=False)