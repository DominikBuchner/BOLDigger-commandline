import requests_html, openpyxl, ntpath, os, datetime, pkg_resources
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as BSoup
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
from openpyxl.utils.dataframe import dataframe_to_rows
from boldigger.boldblast_coi import slices, fasta_to_string, requests, fasta_rewrite
from boldigger.boldblast_its import save_as_df, save_results
from boldigger.boldblast_rbcl import post_request
from boldigger_cline.login import login
from boldigger_cline.boldblast_coi import requests
from tqdm import tqdm

def main(username, password, fasta_path, output_path, query_length):

    ## import data needed for the requests
    certs = pkg_resources.resource_filename(__name__, 'data/certs.pem')

    ## create session for identificaton engine to save userdata
    session = login(username, password, certs)
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

            ## try to get a answer from bold server, repeat in case of timeout
            try:
                links = post_request(query, session)
            except ConnectionError:
                tqdm.write('%s: ConnectionError, BOLD did not respond properly: Trying to reconnect.' % datetime.datetime.now().strftime("%H:%M:%S"))
                error_count += 1
                continue
            except ReadTimeout:
                tqdm.write('%s: Readtimeout, BOLD did not respond in time: Trying to reconnect.' % datetime.datetime.now().strftime("%H:%M:%S"))
                error_count += 1
                continue
            break
        else:
            error = True

        if not error:
            ## download data from the fetched links
            html_list = requests(links)

            ## parse the returned html
            tqdm.write('%s: Parsing html.' % datetime.datetime.now().strftime("%H:%M:%S"))
            dataframes = save_as_df(html_list, sequences_names[querys.index(query)])

            ## save results in resultfile
            tqdm.write('%s: Saving results.' % datetime.datetime.now().strftime("%H:%M:%S"))
            save_results(dataframes, fasta_path, output_path)

            ## remove found OTUS from fasta and write it into a new one
            tqdm.write('%s: Removing finished OTUs from fasta.' % datetime.datetime.now().strftime("%H:%M:%S"))
            fasta_rewrite(fasta_path, query_length)

        else:
            tqdm.write('%s: Too many bad connections. Try a smaller batch size. Close to continue.' % datetime.datetime.now().strftime("%H:%M:%S"))
            sys.exit()

    if not error:
        tqdm.write('%s: Done.' % datetime.datetime.now().strftime("%H:%M:%S"))
