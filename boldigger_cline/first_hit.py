import openpyxl, datetime
import pandas as pd
from boldigger.first_hit import first_hit

## main function to control the flow
def main(xlsx_path):

    print('%s: Opening resultfile.' % datetime.datetime.now().strftime("%H:%M:%S"))

    ## run first hit function
    print('%s: Filtering data.' % datetime.datetime.now().strftime("%H:%M:%S"))
    first_hit(xlsx_path)

    print('%s: Saving result to new tab.' % datetime.datetime.now().strftime("%H:%M:%S"))
    print('%s: Done. Close to continue.' % datetime.datetime.now().strftime("%H:%M:%S"))
