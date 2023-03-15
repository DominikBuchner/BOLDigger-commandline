import openpyxl, requests_html, datetime, sys
from more_itertools import unique_everseen
from boldigger.boldblast_coi import slices
from bs4 import BeautifulSoup as BSoup
from boldigger.additional_data import retrieve_process_ids, save_results
from tqdm import tqdm


## function to loop through the process IDs and call the BOLD API  for additional data
## will return a dict in form of {Process ID: [BOLD Record ID, BIN, Sex, Life stage, Country, Identifier, Identification method, Institution storing]}
def get_data(process_ids):
    ## slice the process ids in parts of 100 to get the maximum out of API calls
    process_ids = list(slices(process_ids, 100))

    ## open a new html session
    with requests_html.HTMLSession() as session:
        ## initialize the final dict output
        process_id_dict = {}

        for id_pack in tqdm(process_ids, desc="Download status"):
            ## request the data, retry if the request failes
            while True:
                try:
                    resp = session.get(
                        "http://www.boldsystems.org/index.php/API_Public/specimen?ids="
                        + "|".join(id_pack)
                    )
                except:
                    continue
                break

            ## use beautifulsoup to find all records in the response
            soup = BSoup(resp.text, "xml")
            records = soup.find_all("record")

            ## loop through records to extract interesting data
            for count in range(len(records)):
                tags = [
                    "processid",
                    "record_id",
                    "bin_uri",
                    "sex",
                    "lifestage",
                    "country",
                    "identification_provided_by",
                    "identification_method",
                    "institution_storing",
                ]

                ## search the data encapsuled by each tag
                specimen_data = [
                    records[count].find(tag) if records[count].find(tag) != None else ""
                    for tag in tags
                ]

                ## extract the texts from these tags
                specimen_data = [
                    datapoint.text if datapoint != "" else ""
                    for datapoint in specimen_data
                ]

                ## append a link to the specimen page to the results if user is interested in looking up even more data
                specimen_data.append(
                    "http://www.boldsystems.org/index.php/MAS_DataRetrieval_OpenSpecimen?selectedrecordid="
                    + specimen_data[1]
                )

                ## put the data in a dictionary in form of processID: [listofinformation]
                process_dict = {specimen_data[0]: specimen_data[1:]}

                ## update the final output
                process_id_dict.update(process_dict)

    return process_id_dict


## main function to controll the flow
def main(xlsx_path):
    ## Give user output
    tqdm.write(
        "%s: Extracting process ID's." % datetime.datetime.now().strftime("%H:%M:%S")
    )

    ## catch any wrong file formats here to avoid crash
    try:
        wb, process_ids, type = retrieve_process_ids(xlsx_path)
    except ValueError:
        tqdm.write("Wrong file format. Close to continue.")
        sys.exit()

    ## collect the data from BOLD
    tqdm.write(
        "%s: Downloading additional data."
        % datetime.datetime.now().strftime("%H:%M:%S")
    )
    additional_data = get_data(process_ids)

    ## saving the data according to type
    tqdm.write("%s: Saving the results." % datetime.datetime.now().strftime("%H:%M:%S"))
    save_results(wb, additional_data, xlsx_path, type)

    ## get events (just closing) and values
    tqdm.write(
        "%s: Done. Close to continue." % datetime.datetime.now().strftime("%H:%M:%S")
    )
