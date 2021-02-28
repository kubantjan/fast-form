import argparse
import logging
import os

from fast_form.outputting.utils_for_main import load_paths_for_processing_config, process_to_validation_excel, \
    process_to_final_excel

with open('../VERSION') as version_file:
    VERSION = version_file.read().strip()


def get_parser():
    """
    Creates a new argument parser.
    """
    par = argparse.ArgumentParser('fast-form')
    version = '%(prog)s ' + VERSION
    par.add_argument('--version', '-v', action='version', version=version)
    par.add_argument('--path_to_path_config',
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
                     default=os.path.join(os.path.dirname(__file__), "tests", "form1_for_test", "path_config.json"))
    par.add_argument('--final-step',
                     action='store_true',
                     default=False,
                     help='If provided, the program will run the final step and output the final excel based on the'
                          'validation excel')
    par.add_argument('--verbose',
                     action='store_true',
                     default=False,
                     help='If provided, the program output verbosely what is happening')
    return par


if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(name)s %(message)s',
        level=logging.INFO if not args.verbose else logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(__name__)
    logger.info("Starting app, loading tools needed for processing")

    paths_for_processing = load_paths_for_processing_config(args.path_to_path_config)
    if not args.final_step:
        process_to_validation_excel(paths_for_processing)
    else:
        process_to_final_excel(paths_for_processing)
