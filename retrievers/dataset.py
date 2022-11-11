import os
import sys
from . import downloader

BRAZILIAN_STATES = [
    'AC',
    'AL',
    'AP',
    'AM',
    'BA',
    'CE',
    'DF',
    'ES',
    'GO',
    'MA',
    'MS',
    'MT',
    'MG',
    'PA',
    'PB',
    'PR',
    'PE',
    'PI',
    'RJ',
    'RN',
    'RS',
    'RO',
    'RR',
    'SC',
    'SP',
    'SE',
    'TO'
]

BWEB_BASE_URL = 'https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/buweb/'
MACHINE_RAW_BASE_URL = 'https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/arqurnatot/'


def download_state_files(base_url, file_pattern, output_path, progress_desc):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    count = 0
    states_len = len(BRAZILIAN_STATES)
    for state in BRAZILIAN_STATES:
        file_name = file_pattern.replace('[STATE]', state)
        url = base_url + file_name

        output_file = os.path.join(output_path, file_name)
        if os.path.exists(output_file):
            sys.stdout.write(f"File {file_name} already downloaded. Skipping...\n")
            count += 1
            continue

        count += 1
        downloader.download_file(url, output_file, f"[{count}/{states_len}] - {progress_desc} ")


def download_1t_bweb_files(output_path):
    file_pattern = 'bweb_1t_[STATE]_311020221535.zip'
    output_path_final = os.path.join(output_path, 'data/download/bweb')
    download_state_files(BWEB_BASE_URL, file_pattern, output_path_final, 'Retrieving 1T bweb file')


def download_2t_bweb_files(output_path):
    file_pattern = 'bweb_2t_[STATE]_311020221535.zip'
    output_path_final = os.path.join(output_path, 'data/download/bweb')
    download_state_files(BWEB_BASE_URL, file_pattern, output_path_final, 'Retrieving 2T bweb file')


def download_votings(output_path):
    output_path_final = os.path.join(output_path, 'data/download')

    if not os.path.exists(output_path_final):
        os.makedirs(output_path_final)

    url = 'https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2022_BR.zip'
    file_name = 'votacao_secao_2022_BR.zip'

    output_file = os.path.join(output_path_final, file_name)
    if os.path.exists(output_file):
        sys.stdout.write(f"File {file_name} already downloaded. Skipping...\n")
        return

    downloader.download_file(url, output_file, "[Retrieving votings from 2022] ")


def download_1t_turn_raw_files(output_path):
    file_pattern = 'bu_imgbu_logjez_rdv_vscmr_2022_1t_[STATE].zip'
    output_path_final = os.path.join(output_path, 'data/download/machine_raw')
    download_state_files(MACHINE_RAW_BASE_URL, file_pattern, output_path_final, 'Retrieving 1T raw file')


def download_2t_turn_raw_files(output_path):
    file_pattern = 'bu_imgbu_logjez_rdv_vscmr_2022_2t_[STATE].zip'
    output_path_final = os.path.join(output_path, 'data/download/machine_raw')
    download_state_files(MACHINE_RAW_BASE_URL, file_pattern, output_path_final, 'Retrieving 2T raw file')


def download_1t_files(output_path):
    download_1t_turn_raw_files(output_path)
    download_votings(output_path)


def download_2t_files(output_path):
    download_2t_turn_raw_files(output_path)
    download_votings(output_path)


def download_all_files(output_path):
    download_1t_turn_raw_files(output_path)
    download_2t_turn_raw_files(output_path)
    download_votings(output_path)