from more_itertools import chunked

from db import bulk_insert, database_connection
from extraction import raw_extractor
import logging


def process_files(base_path):
    extractor = raw_extractor.Extractor()
    files = extractor.extract(base_path)

    conn = database_connection.DatabaseConnection().connect()

    logging.info('Starting file processing')
    chunk_size = 1000
    for file in files:
        for chunk in chunked(file, chunk_size):
            logging.info('Writing partial result to the database')
            bulk_insert.raw_data_bulk_insert(conn, chunk, page_size=chunk_size)

    logging.info('Process finished')


