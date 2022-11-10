import psycopg2
from psycopg2 import extras
import logging


def raw_data_bulk_insert(conn, raw_info_list, page_size):
    machines_id_dict = {'UE2009': 1, 'UE2010': 2, 'UE2011': 3, 'UE2013': 4, 'UE2015': 5, 'UE2020': 6}

    dict_list = []
    for raw_info in raw_info_list:
        dict_list.append({'cd_municipio': raw_info.city_code, 'nr_zona': raw_info.election_zone_code,
                          'nr_secao': raw_info.election_section_code, 'nr_local_votacao': raw_info.election_local_code,
                          'nome_arquivo_fonte': raw_info.source_file_name,
                          'id_modelo_urna': machines_id_dict[raw_info.machine_model]})

    query = "insert into votacao_secao_urna (cd_municipio, nr_zona, nr_secao, nr_local_votacao, nome_arquivo_fonte, " \
            "               id_modelo_urna) " \
            "values (%(cd_municipio)s, %(nr_zona)s, %(nr_secao)s, " \
            "%(nr_local_votacao)s, %(nome_arquivo_fonte)s, %(id_modelo_urna)s) " \
            "ON CONFLICT (cd_municipio, nr_zona, nr_secao, nr_local_votacao) DO " \
            "UPDATE SET nome_arquivo_fonte = votacao_secao_urna.nome_arquivo_fonte || ';' || %(nome_arquivo_fonte)s, " \
            "modelo_urna_incerto = CASE WHEN (votacao_secao_urna.modelo_urna_incerto " \
            "   IS TRUE OR votacao_secao_urna.id_modelo_urna != 2) THEN TRUE ELSE FALSE END, " \
            "id_modelo_urna = CASE WHEN (votacao_secao_urna.modelo_urna_incerto " \
            "   IS TRUE OR votacao_secao_urna.id_modelo_urna != 2) THEN NULL " \
            " ELSE votacao_secao_urna.id_modelo_urna END;"

    cursor = conn.cursor()
    try:
        extras.execute_batch(cursor, query, dict_list, page_size)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        conn.rollback()
        cursor.close()
        return 1
    logging.info('execute_batch() done')
    cursor.close()
