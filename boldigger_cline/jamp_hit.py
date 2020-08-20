import openpyxl, datetime
import pandas as pd
from boldigger.jamp_hit import get_threshold, get_data, jamp_hit, save_results

## main function
def main(xlsx_path):

    print('%s: Opening resultfile.' % datetime.datetime.now().strftime("%H:%M:%S"))
    otu_dfs = get_data(xlsx_path)

    if otu_dfs != 'Wrong file':
        print('%s: Filtering data.' % datetime.datetime.now().strftime("%H:%M:%S"))
        jamp_hits = [jamp_hit(otu) for otu in otu_dfs]
        output = pd.concat(jamp_hits).reset_index(drop = True)

        print('%s: Saving result to new tab.' % datetime.datetime.now().strftime("%H:%M:%S"))
        save_results(xlsx_path, output)

        print('%s: Done.' % datetime.datetime.now().strftime("%H:%M:%S"))

    else:
        print('%s: Wrong file format.' % datetime.datetime.now().strftime("%H:%M:%S"))
