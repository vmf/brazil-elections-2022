import io
import logging
import os
import re
from zipfile import ZipFile

import progressbar
import py7zr

from .model import RawDataInfo

MACHINE_MODEL_PATTERN = re.compile(b'Modelo de Urna: UE\\d{4}')
CITY_PATTERN = re.compile(b'Munic\xedpio: \\d+')
ELECTION_ZONE_PATTERN = re.compile(b'Zona Eleitoral: \\d+')
ELECTION_SECTION_PATTERN = re.compile(b'Se\xe7\xe3o Eleitoral: \\d+')
ELECTION_LOCAL_PATTERN = re.compile(b'Local de Vota\xe7\xe3o: \\d+')

CONTINGENCY_MACHINE_PATTERN = re.compile(b'Urna de conting\xeancia')
#MUST_HAVE1_PATTERN = re.compile(b'Gerando arquivo de resultado')


class Extractor:

    @staticmethod
    def extract_description_value(result):
        return result.group(0).decode('latin-1').split(':')[1].strip()

    @staticmethod
    def extract_info_from_bytes(self, dat_file_byte_arr, file_name):
        contingency_machine_result = CONTINGENCY_MACHINE_PATTERN.search(dat_file_byte_arr)
        if contingency_machine_result:
            return  # Urnas de contingência apresentam informações inválidas para extração

        # must_have1_result = MUST_HAVE1_PATTERN.search(dat_file_byte_arr)
        # if not must_have1_result:
        #     return  # Ajuda a descartar arquivos inválidos

        machine_model_result = MACHINE_MODEL_PATTERN.search(dat_file_byte_arr)
        if not machine_model_result:
            logging.error(f'Unable to find a match for the machine model in {file_name} file')
            return

        city_result = CITY_PATTERN.search(dat_file_byte_arr)
        if not city_result:
            logging.error(f'Unable to find a match for the city in {file_name} file')
            return

        election_zone_result = ELECTION_ZONE_PATTERN.search(dat_file_byte_arr)
        if not election_zone_result:
            logging.error(f'Unable to find a match for the election zone in {file_name} file')
            return

        election_section_result = ELECTION_SECTION_PATTERN.search(dat_file_byte_arr)
        if not election_section_result:
            logging.error(f'Unable to find a match for the election section in {file_name} file')
            return

        election_local_result = ELECTION_LOCAL_PATTERN.search(dat_file_byte_arr)
        if not election_local_result:
            logging.error(f'Unable to find a match for the election local in {file_name} file')
            return

        return RawDataInfo(machine_model=self.extract_description_value(machine_model_result),
                           city_code=int(self.extract_description_value(city_result)),
                           election_zone_code=int(
                               self.extract_description_value(election_zone_result)),
                           election_section_code=int(
                               self.extract_description_value(election_section_result)),
                           election_local_code=int(
                               self.extract_description_value(election_local_result)),
                           source_file_name=file_name)

    @staticmethod
    def extract_info_recursively(self, file_bytesio, file_name):
        with py7zr.SevenZipFile(file_bytesio, mode='r') as logjez_file:
            log_files = logjez_file.readall()

            log_file_key = 'logd.dat'

            if log_file_key in log_files:
                raw_data_info = self.extract_info_from_bytes(self, log_files[log_file_key].getbuffer().tobytes(),
                                                             file_name)
                if raw_data_info:
                    yield raw_data_info
            else:
                logging.error(f'Unable to find log file {log_file_key}')

            if len(log_files) > 1:
                jez_files = {k: v for k, v in log_files.items() if k.endswith('.jez')}
                for fname, bio in jez_files.items():
                    raw_data_info_list = self.extract_info_recursively(self, bio, file_name)
                    for raw_data_info in raw_data_info_list:
                        yield raw_data_info

    @staticmethod
    def extract_info_from_file(self, file_path, description):
        logging.info(f"INFO: Opening zip file {file_path}")
        with ZipFile(file_path) as zip_file:
            file_names = zip_file.namelist()
            logjez_files = list(filter(lambda name: name.endswith('logjez'), file_names))
            logjez_files_count = len(logjez_files)
            logging.info(f"INFO: Found {logjez_files_count} logjez files")

            widgets = [
                description, ' ',
                progressbar.Percentage(),
                ' (', progressbar.Counter(), f' of {logjez_files_count}', ')',
                ' [', progressbar.Timer(), ']',
                ' (', progressbar.ETA(), ')',
            ]

            with progressbar.ProgressBar(max_value=logjez_files_count, widgets=widgets) as bar:
                count = 0
                for file_name in logjez_files:
                    try:
                        content = zip_file.open(file_name).read()
                        # usa set  para remover duplicados
                        raw_data_info_list = set(self.extract_info_recursively(self, io.BytesIO(content), file_name))
                        if len(raw_data_info_list) > 0:
                            for raw_data_info in raw_data_info_list:
                                yield raw_data_info
                        else:
                            logging.error(f'Unable to extract raw data from file {file_name}')
                    except:
                        logging.error(f'An error occurred when extracting data from file {file_name}')

                    count += 1
                    bar.update(count)

    def extract(self, base_path):
        dir_list = os.listdir(base_path)
        dir_list_count = len(dir_list)
        count = 0

        for file in enumerate(dir_list):
            file_path = os.path.join(base_path, file[1])
            count += 1
            description = f'[{count} of {dir_list_count}] <{file[1]}>'
            yield self.extract_info_from_file(self, file_path, description)
