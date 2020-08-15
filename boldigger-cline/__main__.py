import pkg_resources, argparse

## import data needed for the requests
certs = pkg_resources.resource_filename(__name__, 'data/certs.pem')

## main function to run and control the flow of bldigger-cline
def main():
    ## collect and parse the cline arguments
    parser = argparse.ArgumentParser(prog = 'boldigger-cline', description = 'BOLDigger as a command line tool, https://github.com/DominikBuchner/BOLDigger-commandline')
    subparsers = parser.add_subparsers(dest = 'function')

    ## group parsers that accept the same arguments
    ## identification engines
    parser_ie_coi = subparsers.add_parser('ie_coi', help = 'COI identification engine')
    parser_ie_its = subparsers.add_parser('ie_its', help = 'ITS identification engine')
    parser_ie_rbcl = subparsers.add_parser('ie_rbcl', help = 'rbcl identification engine')

    for subparser in [parser_ie_coi, parser_ie_its, parser_ie_rbcl]:
        subparser.add_argument('username', help = 'Username for boldsystems login')
        subparser.add_argument('password', help = 'Password for boldsystems login')
        subparser.add_argument('fasta_path', help = 'Path to the fasta file to be blasted')
        subparser.add_argument('output_folder', help = 'Path to the output folder')
        subparser.add_argument('batch_size', type = int, default = 100, nargs = '?', help = 'Batch size to be blasted.')

    ## metadata code
    parser_add_data = subparsers.add_parser('add_metadata', help = 'additional data download')

    ## top hit selection
    parser_first_hit = subparsers.add_parser('first_hit', help = 'use the first hit as top hit')
    parser_jamp_hit = subparsers.add_parser('jamp_hit', help = 'determine the top hit with the JAMP method')
    parser_digger_hit = subparsers.add_parser('digger_hit', help = 'determine the top hit with the BOLDigger method')

    for subparser in [parser_add_data, parser_first_hit, parser_jamp_hit, parser_digger_hit]:
        parser_add_data.add_argument('xlsx_path', help = 'Path to the BOLDresults file')
        parser_add_data.add_argument('output_folder', help = 'Path to the output folder')


    ## add version control
    parser.add_argument('--version', action='version', version= '1.0.0')

    ## parse the arguments
    args = parser.parse_args()

    ## search engine for coi
    if parser.function == 'ie_coi':
        pass

    ## search engine for its
    if parser.function == 'ie_its':
        pass

    ## search engine for rbcL
    if parser.function == 'ie_rbcl':
        pass

    ## additional data
    if parser.function == 'add_metadata':
        pass

    ## hit selection
    if parser.function == 'first_hit':
        pass

    if parser.function == 'jamp_hit':
        pass

    if parser.function == 'digger_hit':
        pass

## run only if called as a toplevel script
if __name__ == "__main__":
    main()
