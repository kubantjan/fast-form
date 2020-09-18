import argparse

from outputting.ouput_data import output_data
from outputting.process_document import process_document

if __name__ == '__main__':
    # parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", '-c', help="Pass config file.")
    parser.add_argument("--document", '-d', help="Pass the image file.")
    args = parser.parse_args()

    form_data = process_document(args.config, args.document)
    filename = output_data(form_data, args.document)
