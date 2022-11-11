import logging


def initialize():
    logging.basicConfig(filename='log.txt', level=logging.INFO)


def error(msg, print_console=False):
    logging.error(msg)
    if print_console:
        print(f'ERROR: {msg}')


def info(msg, print_console=False):
    logging.info(msg)
    if print_console:
        print(f'INFO: {msg}')
