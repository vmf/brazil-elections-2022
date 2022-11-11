import psycopg2
from psycopg2 import extras
import logging_wrapper


class RawDataDao:

    @staticmethod
    def bulk_insert(conn, raw_info_list, page_size):
        machines_id_dict = {'UE2009': 1, 'UE2010': 2, 'UE2011': 3, 'UE2013': 4, 'UE2015': 5, 'UE2020': 6}

        dict_list = []
        for raw_info in raw_info_list:
            dict_list.append({'cd_municipio': raw_info.city_code, 'nr_zona': raw_info.election_zone_code,
                              'nr_secao': raw_info.election_section_code,
                              'nr_local_votacao': raw_info.election_local_code,
                              'nome_arquivo_fonte': raw_info.source_file_name,
                              'id_modelo_urna': machines_id_dict[raw_info.machine_model]})

        query = """
                INSERT INTO votacao_secao_urna (cd_municipio, nr_zona, nr_secao, nr_local_votacao, nome_arquivo_fonte, 
                               id_modelo_urna) 
                VALUES (%(cd_municipio)s, %(nr_zona)s, %(nr_secao)s, 
                %(nr_local_votacao)s, %(nome_arquivo_fonte)s, %(id_modelo_urna)s) 
                ON CONFLICT (cd_municipio, nr_zona, nr_secao, nr_local_votacao) DO 
                UPDATE SET nome_arquivo_fonte = votacao_secao_urna.nome_arquivo_fonte || ';' || %(nome_arquivo_fonte)s, 
                modelo_urna_incerto = CASE WHEN (votacao_secao_urna.modelo_urna_incerto 
                   IS TRUE OR votacao_secao_urna.id_modelo_urna != 2) THEN TRUE ELSE FALSE END, 
                id_modelo_urna = CASE WHEN (votacao_secao_urna.modelo_urna_incerto 
                   IS TRUE OR votacao_secao_urna.id_modelo_urna != 2) THEN NULL 
                 ELSE votacao_secao_urna.id_modelo_urna END;
                """

        cursor = conn.cursor()
        try:
            extras.execute_batch(cursor, query, dict_list, page_size)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logging_wrapper.error(error)
            conn.rollback()
            cursor.close()
            return 1
        logging_wrapper.info('execute_batch() done')
        cursor.close()

    @staticmethod
    def already_imported(conn, file_name):
        sql = f"""
        SELECT *
        FROM votacao_secao_urna_controle
        WHERE nome_arquivo_fonte = '{file_name}' AND status = 'OK'
        """

        cursor = conn.cursor()
        try:
            cursor.execute(sql, [])
            return cursor.fetchone() is not None
        except (Exception, psycopg2.DatabaseError) as error:
            logging_wrapper.error(error)
            conn.rollback()
        finally:
            cursor.close()

    @staticmethod
    def insert_processed(conn, file_name):
        sql = f"""
                INSERT INTO votacao_secao_urna_controle (status, nome_arquivo_fonte)
                VALUES ('OK', '{file_name}');
               """

        cursor = conn.cursor()
        try:
            cursor.execute(sql, [])
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logging_wrapper.error(error)
            conn.rollback()
        finally:
            cursor.close()


class VotingDao:

    @staticmethod
    def import_data(conn, file_path):
        copy_sql = """
                       CREATE TEMP TABLE tmp
                        (
                            DT_GERACAO                TEXT,
                            HH_GERACAO                TEXT,
                            ANO_ELEICAO               INTEGER,
                            CD_TIPO_ELEICAO           INTEGER,
                            NM_TIPO_ELEICAO           TEXT,
                            NR_TURNO                  INTEGER,
                            CD_ELEICAO                INTEGER,
                            DS_ELEICAO                TEXT,
                            DT_ELEICAO                TEXT,
                            TP_ABRANGENCIA            TEXT,
                            SG_UF                     TEXT,
                            SG_UE                     TEXT,
                            NM_UE                     TEXT,
                            CD_MUNICIPIO              INTEGER,
                            NM_MUNICIPIO              TEXT,
                            NR_ZONA                   INTEGER,
                            NR_SECAO                  INTEGER,
                            CD_CARGO                  INTEGER,
                            DS_CARGO                  TEXT,
                            NR_VOTAVEL                INTEGER,
                            NM_VOTAVEL                TEXT,
                            QT_VOTOS                  INTEGER,
                            NR_LOCAL_VOTACAO          INTEGER,
                            SQ_CANDIDATO              REAL,
                            NM_LOCAL_VOTACAO          TEXT,
                            DS_LOCAL_VOTACAO_ENDERECO TEXT
                        );    

                        COPY tmp FROM stdin WITH CSV HEADER
                        DELIMITER as ';';

                        INSERT INTO votacao_secao (dt_hh_geracao, ano_eleicao, nr_turno, dt_eleicao, sg_uf, sg_ue, nm_ue, cd_municipio,
                               nm_municipio, nr_zona, nr_secao, id_votacao_secao_cargo, id_votacao_secao_candidato,
                               qt_votos, nr_local_votacao, nm_local_votacao,
                               ds_local_votacao_endereco, id_votacao_secao_urna)
                        SELECT to_timestamp(tmp.dt_geracao || ' ' || tmp.hh_geracao, 'dd-mm-yyyy HH24:MI:SS'),
                               ano_eleicao,
                               nr_turno,
                               to_date(dt_eleicao, 'dd-mm-yyyy'),
                               sg_uf,
                               sg_ue,
                               nm_ue,
                               tmp.cd_municipio,
                               nm_municipio,
                               tmp.nr_zona,
                               tmp.nr_secao,
                               cd_cargo,
                               vsc.id,
                               qt_votos,
                               tmp.nr_local_votacao,
                               nm_local_votacao,
                               ds_local_votacao_endereco,
                               vsu.id
                        FROM tmp
                                 INNER JOIN votacao_secao_candidato vsc
                                            ON tmp.nr_votavel = vsc.nr_votavel
                                 LEFT JOIN votacao_secao_urna vsu
                                           ON tmp.cd_municipio = vsu.cd_municipio AND tmp.nr_zona = vsu.nr_zona AND
                                              tmp.nr_secao = vsu.nr_secao AND tmp.nr_local_votacao = vsu.nr_local_votacao;

                        INSERT INTO votacao_secao_controle (status) VALUES ('OK');
                       """

        cursor = conn.cursor()
        with open(file_path, 'r', encoding='latin-1') as f:
            try:
                cursor.copy_expert(sql=copy_sql, file=f)
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                logging_wrapper.error(error)
                conn.rollback()
            finally:
                cursor.close()

    @staticmethod
    def already_imported(conn):
        sql = "SELECT * FROM votacao_secao_controle WHERE status = 'OK'"

        cursor = conn.cursor()
        try:
            cursor.execute(sql, [])
            return cursor.fetchone() is not None
        except (Exception, psycopg2.DatabaseError) as error:
            logging_wrapper.error(error)
            conn.rollback()
        finally:
            cursor.close()
