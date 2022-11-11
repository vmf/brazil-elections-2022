import os
from zipfile import ZipFile
import logging_wrapper


class Extractor:

    @staticmethod
    def extract(base_path):
        base_path_final = os.path.join(base_path, 'data/download')
        file_path = os.path.join(base_path_final, 'votacao_secao_2022_BR.zip')

        csv_file_name = 'votacao_secao_2022_BR.csv'
        output_path = os.path.join(base_path_final, csv_file_name)

        if os.path.exists(output_path):
            logging_wrapper.info(f"File {csv_file_name} is already extracted. Skipping...", print_console=True)
            return output_path

        logging_wrapper.info(f"Opening zip file {file_path}", print_console=True)
        with ZipFile(file_path) as zip_file:
            logging_wrapper.info(f"Extracting {csv_file_name} from zip file", print_console=True)
            zip_file.extract(csv_file_name, base_path_final)

        return output_path
