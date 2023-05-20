import datetime
import psycopg2
from pyhive import hive  # or import hive or import trino
import pandas as pd
import numpy as np

def foo():
    conn = hive.Connection(host='localhost', port=10000, database='project')
    cursor = conn.cursor()
    mart1 = pd.read_sql("SELECT * FROM mart_1", conn)
    mart2 = pd.read_sql("SELECT * FROM mart_2", conn)
    mart3 = pd.read_sql("SELECT * FROM mart_3", conn)

    conn = psycopg2.connect(host="92.51.39.232", port=5432, database="default_db", user="gen_user", password="bigdataprojectpass")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS mart1")
    cursor.execute("DROP TABLE IF EXISTS mart2")
    cursor.execute("DROP TABLE IF EXISTS mart3")
    query = """
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
    cursor.execute(query)
    query = """
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
    cursor.execute(query)
    query = """
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
    cursor.execute(query)

    i = 0
    query = 'INSERT INTO mart1 (id, price, district, rooms, total_area, current_floor, max_floor, build_year, bath, repair, window_type, places_total) VALUES'
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
            query = query + '\n' + '(' + table_elem + ')'
        else:
            query = query + query + ',' + '\n' + '(' + table_elem + ')'
        i += 1
        #query = f'INSERT INTO aparts_dds values ({table_elem})'
    cursor.execute(query)

    i = 0
    query = 'INSERT INTO mart2 (id, price, address, district, rooms, current_floor, max_floor, build_year, bath, repair, window_type, total, kills, harm, theft, robbery, brigandage, cameras) VALUES'
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
            query = query + '\n' + '(' + table_elem + ')'
        else:
            query = query + ',' + '\n' + '(' + table_elem + ')'
        i += 1
        #query = f'INSERT INTO aparts_dds values ({table_elem})'
    cursor.execute(query)

    i = 0
    query = 'INSERT INTO mart3 (id, price, district, rooms, total_area, current_floor, max_floor, build_year, bath, repair, window_type) VALUES'
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
            query = query + '\n' + '(' + table_elem + ')'
        else:
            query = query + ',' + '\n' + '(' + table_elem + ')'
        i += 1
        #query = f'INSERT INTO aparts_dds values ({table_elem})'
    cursor.execute(query)
    conn.commit()
    conn.close()


conn = hive.Connection(host='localhost', port=10000, database='project')
cursor = conn.cursor()
mart2 = pd.read_sql("SELECT * FROM mart_2", conn)
conn.commit()
conn.close()
conn = psycopg2.connect(host="92.51.39.232", port=5432, database="default_db", user="gen_user", password="bigdataprojectpass")
cursor = conn.cursor()
for elem in mart2.values:
    query = 'INSERT INTO mart2 (id, price, address, district, rooms, current_floor, max_floor, build_year, bath, repair, window_type, total, street, kills, harm, theft, robbery, brigandage, cameras) VALUES'
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
    query = query + "(" + table_elem + ")"
    cursor.execute(query)
conn.commit()
conn.close()