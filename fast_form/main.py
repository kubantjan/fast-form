import argparse
import logging
import os
import shutil

from fast_form.outputting.utils_for_main import load_paths_for_processing_config, process_to_validation_excel, \
    process_to_final_excel, SHEET_WITH_RESULTS

INIT_DATA_FOLDER = 'fast-form-data'


def init(_):
    shutil.rmtree(INIT_DATA_FOLDER, ignore_errors=True)
    path_to_test_folder = os.path.join(os.path.dirname(__file__), "tests", "form1_for_test")
    shutil.copytree(path_to_test_folder, INIT_DATA_FOLDER)
    print(f"The program was successfully initialized. Folder {os.path.join(os.getcwd(), INIT_DATA_FOLDER)} "
          f"was created and it is filled with example data. \n\nYou can either run it as is or fill in your own data")


def extract(args):
    paths_for_processing = load_paths_for_processing_config(args.root_data_folder)
    print("Running data extraction process")
    process_to_validation_excel(paths_for_processing)
    print(
        f"Data was successfully extracted to validation excel:"
        f" {os.path.join(os.getcwd(), paths_for_processing.validation_excel_path)}")


def finalize(args):
    paths_for_processing = load_paths_for_processing_config(args.root_data_folder)
    print(f"Running data finalization process. Processing data from validation excel: "
          f"{os.path.join(os.getcwd(), paths_for_processing.validation_excel_path)}")
    process_to_final_excel(paths_for_processing)
    print(f"Validation excel was sucessfully processed and data from it are in the sheet '{SHEET_WITH_RESULTS}'"
          f" in the final excel:"
          f" {os.path.join(os.getcwd(), paths_for_processing.final_excel_path)}")


def get_parser():
    """
    Creates a new argument parser.
    """
    par = argparse.ArgumentParser('fast-form')
    subparsers = par.add_subparsers(title='subcommands')
    init_subparser = subparsers.add_parser('init', help='Creates data directory - bootstraps project structure')
    init_subparser.set_defaults(func=init)

    extract_subparser = subparsers.add_parser('extract',
                                              help='Extracts data from questionares and creates validation excel')
    extract_subparser.set_defaults(func=extract)

    finalize_subparser = subparsers.add_parser('finalize',
                                               help='Parses validation excel to produce finalized output.'
                                                    ' One questionare per line')
    finalize_subparser.set_defaults(func=finalize)

    par.add_argument('--version',
                     action='store_true',
                     default=False,
                     help='If provided, the program outputs version.')

    par.add_argument('--verbose',
                     action='store_true',
                     default=False,
                     help='If provided, the program output verbosely what is happening')

    for subparser_processing in [finalize_subparser, extract_subparser]:
        subparser_processing.add_argument('--root_data_folder',
                                          type=str,
                                          help=f"""Path to config file with paths to template pdf, l
                                          leaving blank will run the file with
                          default configuration: Root path: {os.path.join(os.getcwd(), INIT_DATA_FOLDER)}
                           path config is always assumed to be in root folder, called path_config.json. 
                           And has to look as below:
                            {{
                                "template_path": "path",
                                "form_structure_config_path": "path",
                                "folder_with_documents_path": "path",
                                "final_excel_path": "path"
                            }}
                            """,
                                          default=os.path.join( "fast-form-data", "path_config.json"))

    return par


def fast_form():
    parser = get_parser()
    args = parser.parse_args()
    if args.version:
        print("This program is running correctly, current version is 0.3.1")
    else:
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(name)s %(message)s',
            level=logging.INFO if not args.verbose else logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S')
        if args.__contains__("func"):
            try:
                args.func(args)
            except ValueError as e:
                print(f"Something was wrong: {e}")
        else:
            parser.print_help()


if __name__ == '__main__':
    fast_form()
