import datetime, asyncio, pkg_resources
from boldigger.boldblast_coi import fasta_to_string, post_request, as_session, save_as_df, save_results, fasta_rewrite, excel_converter
from boldigger_cline.login import login
from tqdm import tqdm
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

def main(username, password, fasta_path, output_path, query_length):

    ## import data needed for the requests
    certs = pkg_resources.resource_filename(__name__, 'data/certs.pem')

    ## define some variables needed for the layout
    session = login(username, password, certs)
    querys, sequences_names = fasta_to_string(fasta_path, query_length)

    ## request as long as there are querys left
    for query in tqdm(querys, desc = 'Requesting BOLD'):
        while True:
            try:
                tqdm.write('%s: Requesting BOLD. This will take a while.' % datetime.datetime.now().strftime("%H:%M:%S"))

                ## collect IDS result urls from BOLD
                links = post_request(query, session)

                ## download data from the fetched links
                tqdm.write('%s: Downloading results.' % datetime.datetime.now().strftime("%H:%M:%S"))
                tables = asyncio.run(as_session(links))

                ## parse the returned html
                tqdm.write('%s: Parsing html.' % datetime.datetime.now().strftime("%H:%M:%S"))
                result = save_as_df(tables, sequences_names[querys.index(query)])

                ## save results in resultfile
                tqdm.write('%s: Saving results.' % datetime.datetime.now().strftime("%H:%M:%S"))
                save_results(result, fasta_path, output_path)

            except (ValueError, ReadTimeout, ConnectionError):
                tqdm.write('%s: BOLD did not respond! Retrying.' % datetime.datetime.now().strftime("%H:%M:%S"))
                continue
            break

        ## remove found OTUS from fasta and write it into a new one
        tqdm.write('%s: Removing finished OTUs from fasta.' % datetime.datetime.now().strftime("%H:%M:%S"))
        fasta_rewrite(fasta_path, query_length)

    ## convert results to excel when download is finished
    tqdm.write('%s: Converting the data to excel.' % datetime.datetime.now().strftime("%H:%M:%S"))
    excel_converter(fasta_path, output_path)

    print('%s: Done. Close to continue.' % datetime.datetime.now().strftime("%H:%M:%S"))
