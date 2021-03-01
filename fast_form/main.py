import argparse
import logging
import os
import shutil

from fast_form.outputting.utils_for_main import load_paths_for_processing_config, process_to_validation_excel, \
    process_to_final_excel


def init(_):
    shutil.rmtree('fast-form-data', ignore_errors=True)
    path_to_test_folder = os.path.join(os.path.dirname(__file__), "tests", "form1_for_test")
    shutil.copytree(path_to_test_folder, "./fast-form-data/")


def extract(args):
    paths_for_processing = load_paths_for_processing_config(args.path_to_path_config)
    process_to_validation_excel(paths_for_processing)


def finalize(args):
    paths_for_processing = load_paths_for_processing_config(args.path_to_path_config)
    process_to_final_excel(paths_for_processing)


def get_parser():
    """
    Creates a new argument parser.
    """
    par = argparse.ArgumentParser('fast-form')
    subparsers = par.add_subparsers(title='subcommands')
    init_subparser = subparsers.add_parser('init', help='Creates data directory - bootstraps project structure')
    init_subparser.set_defaults(func=init)

    extract_subparser = subparsers.add_parser('extract', help='Extracts data from questionares and creates validation excel')
    extract_subparser.set_defaults(func=extract)

    finalize_subparser = subparsers.add_parser('finalize', help='Parses validation excel to produce finalized output. One questionare per line')
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
        subparser_processing.add_argument('--path_to_path_config',
                                          type=str,
                                          help="""Path to config file with paths to template pdf, leaving blank will run the file with
                          default configuration on path path_config.json. Required paths are:
                            {
                                "template_path": "path",
                                "form_structure_config_path": "path",
                                "folder_with_documents_path": "path",
                                "final_excel_path": "path"
                            }
                            """,
                                          default=os.path.join("fast-form-data", "path_config.json"))

    return par


def fast_form():
    parser = get_parser()
    args = parser.parse_args()
    if args.version:
        print("This will print version of this program in the future")
    else:
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(name)s %(message)s',
            level=logging.INFO if not args.verbose else logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S')

        logger = logging.getLogger(__name__)
        logger.info("Starting app, loading tools needed for processing")
        if args.__contains__("func"):
            args.func(args)
        else:
            parser.print_help()


if __name__ == '__main__':
    fast_form()
