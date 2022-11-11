import argparse
import sys
from retrievers import dataset
import os
from db import dataset_processor
import logging_wrapper


class Brazil:
    def __init__(self):
        logging_wrapper.initialize()

        parser = argparse.ArgumentParser(
            description='The brazil 2022 elections tool',
            usage='''python brazil.py <command> [<args>]

        The most commonly used git commands are:
           download-files             Downloads election data
           process-files              Process the downloaded files and compile the results to the database 
        ''')

        parser.add_argument('command', help='Subcommand to run')

        args = parser.parse_args(sys.argv[1:2])
        command = args.command.replace('-', '_')
        if not hasattr(self, command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, command)()

    @staticmethod
    def download_files():
        parser = argparse.ArgumentParser(
            description='Downloads election data')

        parser.add_argument("--turn", default="all")
        parser.add_argument("--out", default="")

        args = parser.parse_args(sys.argv[2:])

        if len(args.out) > 0 and not os.path.exists(args.out):
            sys.stderr.write(f"ERROR: invalid output path {args.out}\n")
            exit(1)

        if args.turn == "all":
            dataset.download_all_files(args.out)
        elif args.turn == "1":
            dataset.download_1t_files(args.out)
        elif args.turn == "2":
            dataset.download_2t_files(args.out)
        else:
            sys.stderr.write(f"ERROR: invalid turn {args.turn}\n")
            exit(1)

    @staticmethod
    def process_files():
        parser = argparse.ArgumentParser(
            description='Process th downloaded files and compile the results to the database')

        parser.add_argument("--path", default='.')

        args = parser.parse_args(sys.argv[2:])

        if not os.path.exists(args.path):
            sys.stderr.write(f"ERROR: invalid path {args.path}\n")
            exit(1)

        dataset_processor.process_files(args.path)


if __name__ == '__main__':
    Brazil()
