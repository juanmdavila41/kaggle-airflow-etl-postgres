import csv
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.parser import parse
from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.wasb_hook import WasbHook
from variables import sql_connid_postgrest

from airflow.hooks.base_hook import BaseHook
import imaplib
import email
import os
import logging

wb = WasbHook(wasb_conn_id= 'mass_blob')


def postgresql_df(sql_query, **args):
    sql_conn_id = args.get('sql_conn_id',sql_connid_postgrest)
    print('in utils',sql_conn_id )
    sql_conn = PostgresHook.get_connection(sql_conn_id)
    hook = sql_conn.get_hook()
    return hook.get_pandas_df(sql=sql_query)

# Función para cargar DataFrame en SQL
def load_df_to_sql(df, schema, sql_table, sql_connid_postgrest):
    """Función para cargar un archivo de Excel en una tabla de SQL"""
    rows = df.to_records(index=False)
    rows_list = list(rows)
    row_list2 = [
        tuple(
            None if pd.isnull(item) else item for item in row
        ) for row in rows_list
    ]
    
    # Conexión a PostgreSQL
    sql_conn = PostgresHook(sql_connid_postgrest)
    
    # Truncar la tabla antes de cargar los datos
    sql_conn.run(f'TRUNCATE TABLE {schema}.{sql_table}', autocommit=True)
    
    # Insertar filas en la tabla
    sql_conn.insert_rows(f'{schema}.{sql_table}', row_list2)

def normalize_str_categorical(df_serie,func_type='upper'):
  if func_type == 'upper':
    return df_serie.str.upper().str.strip()
  elif func_type == 'lower':
    return df_serie.str.lower().str.strip()

def remove_special_chars(df_cols):
    return df_cols.str.replace(r'[$@&/.:-]',' ', regex=True)

def regular_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def regular_snake_case(df_cols):
    cols = df_cols.str.replace('ñ','ni')
    cols = cols.str.lower().str.replace('/',' ').str.replace('.',' ').str.strip()
    cols = cols.str.replace(r'\s+',' ',regex=True)
    cols = cols.str.replace(' ','_')
    return cols

def remove_accents_cols(df_cols):
    return df_cols.str.replace('ñ','ni').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')