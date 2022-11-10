import psycopg2
import sys


class DatabaseConnection:

    param_dic = {
        "host": "localhost",
        "database": "eleicoes_brasil_2022",
        "user": "brasil",
        "password": "brasil2022"
    }

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**self.param_dic)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            sys.exit(1)
        print("Connection successful")
        return conn

