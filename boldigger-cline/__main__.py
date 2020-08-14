import pkg_resources, argparse

## import data needed for the requests
certs = pkg_resources.resource_filename(__name__, 'data/certs.pem')

## run only if called as a toplevel script
if __name__ == "__main__":

    ## collect and parse the cline arguments
    parser = argparse.ArgumentParser()

    ## positional arguments, e.g. function to be called by boldigger
    parser.add_argument('function', choices = ['boldblast_coi',
                                               'boldblast_its',
                                               'boldblast_rbcl',
                                               'additional_data',
                                               'first_hit',
                                               'jamp_hit',
                                               'digger_sort'],
                                               nargs = '?',
                                               default = None,
                                               help = 'The different functions of BOLDigger-cline')

    ## keyword arguments e.g. flags used by the positional arguments
    parser.add_argument('-un', '--username', help = 'Username argument')
    parser.add_argument('-pw', '--password', help = 'Password argument')
    parser.add_argument('-fp', '--fasta_path', help = 'Specify the fasta file path here')
    parser.add_argument('-xp', '--xlsx_path', help = 'Specify the xlsx file path here')
    parser.add_argument('-out', '--output_folder', help = 'Specify the output folder here')

    ## ADD REAL DISTRIBUTION CODE HERE ##

    parser.add_argument('--version', action = 'version', version = '1.0.0', help = 'Display the installed version of BOLDigger-cline')

    ## collect all commandline arguments
    args = parser.parse_args()

    ## logic of boldigger-cline
