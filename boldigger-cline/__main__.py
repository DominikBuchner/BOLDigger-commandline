import pkg_resources, argparse

## import data needed for the requests
certs = pkg_resources.resource_filename(__name__, 'data/certs.pem')

## run only if called as a toplevel script
if __name__ == "__main__":

    ## collect and parse the cline arguments
    parser = argparse.ArgumentParser(prog = 'BOLDigger commandline', description = 'BOLDigger as a command line tool')
    subparsers = parser.add_subparsers()

    parser_bb_coi = subparsers.add_parser('bb_coi', help = 'COI identification engine')
    parser_bb_its = subparsers.add_parser('bb_its', help = 'ITS identification engine')
    parser_bb_rbcl = subparsers.add_parser('bb_rbcl', help = 'rbcl identification engine')
    parser_add_data = subparsers.add_parser('add_metadata', help = 'additional data download')
    parser_first_hit = subparsers.add_parser('first_hit', help = 'use the first hit as top hit')
    parser_jamp_hit = subparsers.add_parser('jamp_hit', help = 'determine the top hit with the JAMP method')
    parser_digger_hit = subparsers.add_parser('digger_hit', help = 'determine the top hit with the BOLDigger method')

    ## add version control
    parser.add_argument('--version', action='version', version= '1.0.0')

    ## parse the arguments
    args = parser.parse_args()
