from outputting.ouput_data import output_data, save_data
from outputting.process_document import process_document

config_path = "./real_forms/justyna_dotazniky/path_config.json"
document_path = "/home/honza/Downloads/PID-5 1.pdf"

if __name__ == '__main__':
    form_data = process_document(config_path, document_path=document_path)
    df, images = output_data(form_data)
    save_data(df, images, document_path=document_path)
