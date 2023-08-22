import pkg_resources, argparse
from boldigger_cline import (
    boldblast_coi,
    boldblast_its,
    boldblast_rbcl,
    additional_data,
    first_hit,
    jamp_hit,
    digger_sort,
    api_verification,
)


## main function to run and control the flow of bldigger-cline
def main():
    ## collect and parse the cline arguments
    parser = argparse.ArgumentParser(
        prog="boldigger-cline",
        description="BOLDigger as a command line tool, https://github.com/DominikBuchner/BOLDigger-commandline",
    )
    subparsers = parser.add_subparsers(dest="function")

    ## group parsers that accept the same arguments
    ## identification engines
    parser_ie_coi = subparsers.add_parser("ie_coi", help="COI identification engine")
    parser_ie_its = subparsers.add_parser("ie_its", help="ITS identification engine")
    parser_ie_rbcl = subparsers.add_parser("ie_rbcl", help="rbcl identification engine")

    for subparser in [parser_ie_coi, parser_ie_its, parser_ie_rbcl]:
        subparser.add_argument("username", help="Username for boldsystems login")
        subparser.add_argument("password", help="Password for boldsystems login")
        subparser.add_argument(
            "fasta_path", help="Path to the fasta file to be blasted"
        )
        subparser.add_argument("output_folder", help="Path to the output folder")
        subparser.add_argument(
            "batch_size",
            type=int,
            default=50,
            nargs="?",
            help="Batch size to be blasted.",
        )

    ## metadata code
    parser_add_data = subparsers.add_parser(
        "add_metadata", help="additional data download"
    )

    ## top hit selection
    parser_first_hit = subparsers.add_parser(
        "first_hit", help="use the first hit as top hit"
    )
    parser_jamp_hit = subparsers.add_parser(
        "jamp_hit", help="determine the top hit with the JAMP method"
    )
    parser_digger_hit = subparsers.add_parser(
        "digger_hit", help="determine the top hit with the BOLDigger method"
    )

    for subparser in [
        parser_add_data,
        parser_first_hit,
        parser_jamp_hit,
        parser_digger_hit,
    ]:
        subparser.add_argument("xlsx_path", help="Path to the BOLDresults file")

    ## add a parser for the api verfication
    parser_api_verification = subparsers.add_parser(
        "api_verification", help="run the api verification"
    )
    parser_api_verification.add_argument(
        "xlsx_path", help="Path to the BOLDResults file"
    )
    parser_api_verification.add_argument(
        "fasta_path", help="Path to the fasta file belonging to the BOLDResults file"
    )

    ## add version control
    parser.add_argument("--version", action="version", version="2.2.1")

    ## parse the arguments
    args = parser.parse_args()

    ## search engine for coi
    if args.function == "ie_coi":
        boldblast_coi.main(
            args.username,
            args.password,
            args.fasta_path,
            args.output_folder,
            args.batch_size,
        )

    ## search engine for its
    if args.function == "ie_its":
        boldblast_its.main(
            args.username,
            args.password,
            args.fasta_path,
            args.output_folder,
            args.batch_size,
        )

    ## search engine for rbcL
    if args.function == "ie_rbcl":
        boldblast_rbcl.main(
            args.username,
            args.password,
            args.fasta_path,
            args.output_folder,
            args.batch_size,
        )

    ## additional data
    if args.function == "add_metadata":
        additional_data.main(args.xlsx_path)

    ## hit selection
    if args.function == "first_hit":
        first_hit.main(args.xlsx_path)

    if args.function == "jamp_hit":
        jamp_hit.main(args.xlsx_path)

    if args.function == "digger_hit":
        digger_sort.main(args.xlsx_path)

    if args.function == "api_verification":
        api_verification.main(args.xlsx_path, args.fasta_path)


## run only if called as a toplevel script
if __name__ == "__main__":
    main()
