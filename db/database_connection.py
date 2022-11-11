import psycopg2
import sys
import logging_wrapper


class DatabaseConnection:
    app_db_param_dic = {
        "host": "localhost",
        "database": "eleicoes_brasil_2022",
        "user": "brasil",
        "password": "brasil2022"
    }

    sys_db_param_dic = {
        "host": "localhost",
        "database": "postgres",
        "user": "brasil",
        "password": "brasil2022"
    }

    def create_db_if_not_exists(self):
        conn = None
        try:
            logging_wrapper.info(f"Checking database [{self.app_db_param_dic['database']}]",
                                 print_console=True)
            conn = psycopg2.connect(**self.sys_db_param_dic)
            conn.autocommit = True

            sql = f"""
                select datname from pg_database where datname = '{self.app_db_param_dic['database']}';
            """

            with conn.cursor() as cursor:
                cursor.execute(sql, [])
                if cursor.fetchone():
                    return

                sql = f"""
                        create database {self.app_db_param_dic['database']};
                    """
                cursor.execute(sql)
        except (Exception, psycopg2.DatabaseError) as error:
            logging_wrapper.error(error, print_console=True)
            sys.exit(1)
        finally:
            if conn:
                conn.close()

        logging_wrapper.info("Database created successfully", print_console=True)
        self.create_schema()

    def create_schema(self):
        logging_wrapper.info('Attempting to create schema', print_console=True)
        conn = self.connect()
        with conn.cursor() as cursor:
            try:
                cursor.execute(open("resources/create_schema.sql", "r").read())
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                logging_wrapper.error(error, print_console=True)
                conn.close()
                sys.exit(1)
            finally:
                conn.close()

        logging_wrapper.info('Schema created successfully', print_console=True)

    def connect(self):
        conn = None
        try:
            logging_wrapper.info('Connecting to the PostgreSQL database...', print_console=True)
            conn = psycopg2.connect(**self.app_db_param_dic)
        except (Exception, psycopg2.DatabaseError) as error:
            logging_wrapper.error(error)
            sys.exit(1)
        logging_wrapper.info("Connection successful", print_console=True)
        return conn
