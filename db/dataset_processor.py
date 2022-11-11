from more_itertools import chunked

from db import dao, database_connection
from extraction import raw_extractor
from extraction import voting_extractor
import logging_wrapper


def process_raw_files(base_path, conn):
    extractor = raw_extractor.Extractor()
    files = extractor.extract(base_path)

    raw_data_dao = dao.RawDataDao()

    chunk_size = 1000
    for file in files:
        file_name = file[0]
        if raw_data_dao.already_imported(conn, file_name):
            logging_wrapper.info(f'File {file_name} already processed. Skipping...', print_console=True)
            continue

        for chunk in chunked(file[1], chunk_size):
            logging_wrapper.info('Writing partial result to the database')
            raw_data_dao.bulk_insert(conn, chunk, page_size=chunk_size)

        raw_data_dao.insert_processed(conn, file_name)


def process_voting_file(base_path, conn):
    voting_dao = dao.VotingDao()
    already_imported = voting_dao.already_imported(conn)
    if already_imported:
        logging_wrapper.info('Voting data was already imported. Skipping...', print_console=True)
        return

    extractor = voting_extractor.Extractor()
    extracted_file_path = extractor.extract(base_path)

    logging_wrapper.info('Writing votings to the database', print_console=True)
    voting_dao.import_data(conn, extracted_file_path)


def process_files(base_path):
    logging_wrapper.info('Starting file processing', print_console=True)

    db_conn = database_connection.DatabaseConnection()
    db_conn.create_db_if_not_exists()

    conn = db_conn.connect()

    process_raw_files(base_path, conn)
    process_voting_file(base_path, conn)

    logging_wrapper.info('Process finished', print_console=True)
