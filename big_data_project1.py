import datetime
import psycopg2
from pyhive import hive  # or import hive or import trino
import pandas as pd
import numpy as np

from airflow import DAG


def odd_to_dds():
    conn = hive.Connection(host='hive-server', port=10000, database='project')
    cursor = conn.cursor()
    #query = "CREATE TABLE join_table AS SELECT aparts.id, price, metro, district, rooms, current_floor, max_floor, total, cameras FROM aparts JOIN districts ON districts.name = aparts.district"
    query = "SELECT * FROM aparts"

    data = pd.read_sql(query, conn)
    data = data[data['aparts.housing_type'] == 'Вторичка']
    data = data.drop(['aparts.id', 'aparts.description'], axis=1).drop_duplicates(ignore_index=True)
    data.reset_index(inplace=True)
    data = data.rename(columns = {'index':'id'})

    cursor.execute("DROP VIEW IF EXISTS mart_1")
    cursor.execute("DROP VIEW IF EXISTS mart_2")
    cursor.execute("DROP VIEW IF EXISTS mart_3")
    cursor.execute("DROP TABLE IF EXISTS aparts_dds")
    
    query = """
    CREATE TABLE IF NOT EXISTS aparts_dds (
        id int,
        price int,
        metro int,
        address string,
        district string,
        rooms int,
        total_area int,
        live_area int,
        kitchen_area int,
        current_floor int,
        max_floor int,
        build_year int,
        housing_type string,
        meter_cost int,
        bath string,
        repair string,
        window_type string,
        ceiling float
    )
    """

    cursor.execute(query)

    i = 0
    query = 'INSERT INTO aparts_dds VALUES'
    for elem in data.values:
        elem[3] = '"' + elem[3].replace('"', '') + '"'
        elem[4] = '"' + elem[4].replace('"', '') + '"'
        elem[12] = '"' + elem[12].replace('"', '') + '"'
        elem[14] = '"' + elem[14].replace('"', '') + '"'
        elem[15] = '"' + elem[15].replace('"', '') + '"'
        elem[16] = '"' + elem[16].replace('"', '') + '"'
        table_elem = ','.join(str(x) for x in elem).replace('nan', 'NULL').replace('.0', '')
        if i == 0:
            query = query + '\n' + '(' + table_elem + ')'
        else:
            query = query + ',' + '\n' + '(' + table_elem + ')'
        i += 1
        #query = f'INSERT INTO aparts_dds values ({table_elem})'
    cursor.execute(query)


def create_mart_1():
    conn = hive.Connection(host='hive-server', port=10000, database='project')
    cursor = conn.cursor()
    #query = "CREATE TABLE join_table AS SELECT aparts.id, price, metro, district, rooms, current_floor, max_floor, total, cameras FROM aparts JOIN districts ON districts.name = aparts.district"
    query = "CREATE VIEW IF NOT EXISTS mart_1 AS SELECT aparts_dds.id, price, district, rooms, total_area, current_floor, max_floor, build_year, bath, repair, window_type, places.places_total FROM aparts_dds JOIN places ON places.id = aparts_dds.id"
    cursor.execute(query)


def create_mart_2():
    conn = hive.Connection(host='hive-server', port=10000, database='project')
    cursor = conn.cursor()
    #query = "CREATE TABLE join_table AS SELECT aparts.id, price, metro, district, rooms, current_floor, max_floor, total, cameras FROM aparts JOIN districts ON districts.name = aparts.district"
    query = "CREATE VIEW IF NOT EXISTS mart_2 AS SELECT aparts_dds.id, price, address, district, rooms, current_floor, max_floor, build_year, bath, repair, window_type, total, street, kills, harm, theft, robbery, brigandage, cameras FROM aparts_dds JOIN districts ON districts.name = aparts_dds.district"
    cursor.execute(query)


def create_mart_3():
    conn = hive.Connection(host='hive-server', port=10000, database='project')
    cursor = conn.cursor()
    #query = "CREATE TABLE join_table AS SELECT aparts.id, price, metro, district, rooms, current_floor, max_floor, total, cameras FROM aparts JOIN districts ON districts.name = aparts.district"
    query = "CREATE VIEW IF NOT EXISTS mart_3 AS SELECT id, price, district, rooms, total_area, current_floor, max_floor, build_year, bath, repair, window_type FROM aparts_dds"
    cursor.execute(query)


def mart_to_bi():
    conn = hive.Connection(host='hive-server', port=10000, database='project')
    cursor = conn.cursor()
    mart1 = pd.read_sql("SELECT * FROM mart_1", conn)
    mart2 = pd.read_sql("SELECT * FROM mart_2", conn)
    mart3 = pd.read_sql("SELECT * FROM mart_3", conn)

    conn = psycopg2.connect(host="92.51.39.232", port=5432, database="default_db", user="gen_user", password="bigdataprojectpass")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS mart1")
    cursor.execute("DROP TABLE IF EXISTS mart2")
    cursor.execute("DROP TABLE IF EXISTS mart3")
    query1 = """
        CREATE TABLE IF NOT EXISTS mart1(
            id int,
            price int,
            district VARCHAR,
            rooms int,
            total_area int,
            current_floor int,
            max_floor int,
            build_year int,
            bath VARCHAR,
            repair VARCHAR,
            window_type VARCHAR,
            places_total int
        )
    """
    cursor.execute(query1)
    query2 = """
        CREATE TABLE IF NOT EXISTS mart2(
            id int,
            price int,
            address VARCHAR,
            district VARCHAR,
            rooms int,
            current_floor int,
            max_floor int,
            build_year int,
            bath VARCHAR,
            repair VARCHAR,
            window_type VARCHAR,
            total int,
            street int,
            kills int,
            harm int,
            theft int,
            robbery int,
            brigandage int,
            cameras int
        )
    """
    cursor.execute(query2)
    query3 = """
        CREATE TABLE IF NOT EXISTS mart3(
            id int,
            price int,
            district VARCHAR,
            rooms int,
            total_area int,
            current_floor int,
            max_floor int,
            build_year int,
            bath VARCHAR,
            repair VARCHAR,
            window_type VARCHAR
        )
    """
    cursor.execute(query3)

    i = 0
    query4 = 'INSERT INTO mart1 (id, price, district, rooms, total_area, current_floor, max_floor, build_year, bath, repair, window_type, places_total) VALUES'
    for elem in mart1.values:
        elem[2] = "'" + elem[2].replace('"', '') + "'"
        if elem[2] == "''":
            elem[2] = 'NULL'
        elem[8] = "'" + elem[8].replace('"', '') + "'"
        if elem[8] == "''":
            elem[8] = 'NULL'
        elem[9] = "'" + elem[9].replace('"', '') + "'"
        if elem[9] == "''":
            elem[9] = 'NULL'
        elem[10] = "'" + elem[10].replace('"', '') + "'"
        if elem[10] == "''":
            elem[10] = 'NULL'
        table_elem = ','.join(str(x) for x in elem).replace('nan', 'NULL').replace('.0', '')
        if i == 0:
            query4 = query4 + '\n' + '(' + table_elem + ')'
        else:
            query4 = query4 + query4 + ',' + '\n' + '(' + table_elem + ')'
        i += 1
        #query = f'INSERT INTO aparts_dds values ({table_elem})'
    cursor.execute(query4)

    i = 0
    query5 = 'INSERT INTO mart2 (id, price, address, district, rooms, current_floor, max_floor, build_year, bath, repair, window_type, total, kills, harm, theft, robbery, brigandage, cameras) VALUES'
    for elem in mart2.values:
        elem[2] = "'" + elem[2].replace('"', '') + "'"
        if elem[2] == "''":
            elem[2] = 'NULL'
        elem[3] = "'" + elem[3].replace('"', '') + "'"
        if elem[3] == "''":
            elem[3] = 'NULL'
        elem[8] = "'" + elem[8].replace('"', '') + "'"
        if elem[8] == "''":
            elem[8] = 'NULL'
        elem[9] = "'" + elem[9].replace('"', '') + "'"
        if elem[9] == "''":
            elem[9] = 'NULL'
        elem[10] = "'" + elem[10].replace('"', '') + "'"
        if elem[10] == "''":
            elem[10] = 'NULL'
        table_elem = ','.join(str(x) for x in elem).replace('nan', 'NULL').replace('.0', '')
        if i == 0:
            query5 = query5 + '\n' + '(' + table_elem + ')'
        else:
            query5 = query5 + ',' + '\n' + '(' + table_elem + ')'
        i += 1
        #query = f'INSERT INTO aparts_dds values ({table_elem})'
    cursor.execute(query5)

    i = 0
    query6 = 'INSERT INTO mart3 (id, price, district, rooms, total_area, current_floor, max_floor, build_year, bath, repair, window_type) VALUES'
    for elem in mart3.values:
        elem[2] = "'" + elem[2].replace('"', '') + "'"
        if elem[2] == "''":
            elem[2] = 'NULL'
        elem[8] = "'" + elem[8].replace('"', '') + "'"
        if elem[8] == "''":
            elem[8] = 'NULL'
        elem[9] = "'" + elem[9].replace('"', '') + "'"
        if elem[9] == "''":
            elem[9] = 'NULL'
        elem[10] = "'" + elem[10].replace('"', '') + "'"
        if elem[10] == "''":
            elem[10] = 'NULL'
        table_elem = ','.join(str(x) for x in elem).replace('nan', 'NULL').replace('.0', '')
        if i == 0:
            query6 = query6 + '\n' + '(' + table_elem + ')'
        else:
            query6 = query6 + ',' + '\n' + '(' + table_elem + ')'
        i += 1
        #query = f'INSERT INTO aparts_dds values ({table_elem})'
    cursor.execute(query6)
    conn.commit()
    conn.close()
    



with DAG("Big_Data_Project_1", description="my big data project 1", start_date=datetime.datetime(2023, 4, 12), schedule=None) as dag:
    from airflow.operators.bash import BashOperator
    from airflow.operators.empty import EmptyOperator
    from airflow.operators.python import PythonOperator

    start_task = EmptyOperator(task_id="start_task")
    odd_to_dds_task = PythonOperator(task_id="odd_to_dds", python_callable=odd_to_dds)
    create_mart_1_task = PythonOperator(task_id="create_mart_1", python_callable=create_mart_1)
    create_mart_2_task = PythonOperator(task_id="create_mart_2", python_callable=create_mart_2)
    create_mart_3_task = PythonOperator(task_id="create_mart_3", python_callable=create_mart_3)
    mart_to_bi_task = EmptyOperator(task_id="mart_to_bi")
    end_task = EmptyOperator(task_id="end_task")

    start_task >> odd_to_dds_task >> create_mart_1_task >> create_mart_2_task >> create_mart_3_task >> mart_to_bi_task >> end_task