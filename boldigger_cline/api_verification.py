from boldigger.api_verification import tqdm_joblib, extract_data, request, refresh_data
import datetime, contextlib, requests_html, joblib, json, openpyxl, psutil
import PySimpleGUI as sg
import pandas as pd
import numpy as np
from tqdm import tqdm
from joblib import Parallel, delayed
from Bio.SeqIO.FastaIO import SimpleFastaParser
from boldigger.boldblast_coi import slices


## main function to control the flow of the program
def main(xlsx_path, fasta_path):
    ## collect the data
    print(
        "{}: Starting API verification.".format(
            datetime.datetime.now().strftime("%H:%M:%S")
        )
    )
    print(
        "{}: Collection OTUs without species level identification and high similarity.".format(
            datetime.datetime.now().strftime("%H:%M:%S")
        )
    )
    raw_data, data_to_check, seq_dict = extract_data(xlsx_path, fasta_path)

    if not raw_data.empty:
        print(
            "{}: Starting to query the API.".format(
                datetime.datetime.now().strftime("%H:%M:%S")
            )
        )

        session = requests_html.HTMLSession()

        with tqdm_joblib(
            tqdm(desc="Calling API", total=len(list(seq_dict.items())))
        ) as progress_bar:
            result = Parallel(n_jobs=psutil.cpu_count())(
                delayed(request)(item, session) for item in list(seq_dict.items())
            )

        ## remove all hits that did not match
        result = [res for res in result if res != None]
        print(
            "{}: Collected {} additional species names.".format(
                datetime.datetime.now().strftime("%H:%M:%S"), len(result)
            )
        )
        print(
            "{}: Starting to update the dataset.".format(
                datetime.datetime.now().strftime("%H:%M:%S")
            )
        )

        corrected_data = refresh_data(result, raw_data, data_to_check, session)

        print(
            "{}: Saving the corrected dataset.".format(
                datetime.datetime.now().strftime("%H:%M:%S")
            )
        )

        with pd.ExcelWriter(
            xlsx_path, mode="a", if_sheet_exists="replace", engine="openpyxl"
        ) as writer:
            corrected_data.to_excel(
                writer, sheet_name="BOLDigger hit - API corrected", index=False
            )

        # ## save output
        # wb = openpyxl.load_workbook(xlsx_path)
        # writer = pd.ExcelWriter(xlsx_path, engine = 'openpyxl')
        # writer.book = wb

        # corrected_data.to_excel(writer, sheet_name = 'BOLDigger hit - API corrected', index = False)
        # wb.save(xlsx_path)
        # writer.close()

        print("{}: Done.".format(datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        print(
            "%s: No BOLDigger hits found. Please add these tophits first. Close to continue."
            % datetime.datetime.now().strftime("%H:%M:%S")
        )
