import openpyxl, datetime
import pandas as pd
from boldigger.jamp_hit import get_data, jamp_hit, get_threshold
from boldigger.digger_sort import get_full_data, add_flags, save_results

## main function to control the flow
def main(xlsx_path):

    ## determine hits the JAMP way
    print('%s: Opening resultfile.' % datetime.datetime.now().strftime("%H:%M:%S"))
    otu_dfs = get_data(xlsx_path)

    if otu_dfs != 'Wrong file':
        print('%s: Filtering data for JAMP hits.' % datetime.datetime.now().strftime("%H:%M:%S"))
        jamp_hits = [jamp_hit(otu) for otu in otu_dfs]

        ## get the full data for flagging
        print('%s: Extracting additional data.' % datetime.datetime.now().strftime("%H:%M:%S"))
        full_data = get_full_data(xlsx_path)

        if get_full_data(xlsx_path) != 'No metadata':
            ## flag every hit
            print('%s: Flagging the hits.' % datetime.datetime.now().strftime("%H:%M:%S"))
            for i in range(len(jamp_hits)):
                jamp_hits[i]['Flags'] = add_flags(jamp_hits[i], full_data[i])

            ## save results
            print('%s: Saving result to new tab.' % datetime.datetime.now().strftime("%H:%M:%S"))
            output = pd.concat(jamp_hits).reset_index(drop = True)
            save_results(xlsx_path, output)

            print('%s: Done. Close to continue.' % datetime.datetime.now().strftime("%H:%M:%S"))

        else:
            print('%s: No additional data found. Run again after the additional data download. Close to continue.' % datetime.datetime.now().strftime("%H:%M:%S"))

    else:
        print('%s: Wrong file format. Close to continue.' % datetime.datetime.now().strftime("%H:%M:%S"))
