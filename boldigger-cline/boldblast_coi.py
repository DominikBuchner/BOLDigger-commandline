import requests_html, openpyxl, ntpath, os, datetime
import numpy as np
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup as BSoup
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
from openpyxl.utils.dataframe import dataframe_to_rows
from boldigger.boldblast_coi import slices, fasta_to_string, post_request, save_as_df, save_results, fasta_rewrite
from boldigger-cline.login import login
from tqdm import tqdm

def requests(url_list):

    html = []

    with requests_html.HTMLSession() as session:
        for url in url_list:
            r = session.get(url)
            html.append(r.text)

    return html

def main(username, password, fasta_path, output_path, query_length):

    ## create session for identificaton engine to save userdata
    session = login(username, password)
    querys, sequences_names = fasta_to_string(fasta_path, query_length)

    ## flags to check request status
    error = False

    ## request as long as there are querys left
    for query in tqdm(querys, desc = 'Requesting BOLD'):

        ## stop if there are 3 connectionerrors or timeouts
        error_count = 0

        ## request until you get a good answer from the server
        while error_count < 3:
            tqdm.write('%s: Requesting BOLD. This will take a while.' % datetime.datetime.now().strftime("%H:%M:%S"))
