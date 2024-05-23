import os
import zipfile
from zipfile import ZipFile
import subprocess
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
import pandas as pd
import numpy as np
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
from utils import remove_special_chars, normalize_str_categorical, regular_camel_case, regular_snake_case, remove_accents_cols, load_df_to_sql
from variables import sql_connid_postgrest

# variables
schema = 'etl_kaggle'
table = 'global_economic_ind'
tmp_table = "tmp_" + table
fact_table = "fact_" + table
sp_name = "sp_load_" + fact_table


TAGS = ['python_data_flow']
DAG_ID = 'kaggle_dataset'
DAG_DESCRIPTION = '''Dag Proyecto'''
DAG_SCHEDULE = None
default_args = {
    "start_date": datetime(2024,1,1)
}
retries = 4
retry_delay = timedelta(minutes=5)

def extract_task():
    api = KaggleApi()
    api.authenticate()

    subprocess.run("kaggle datasets download -d prasad22/global-economy-indicators -p /opt/airflow/data", shell=True, check=True)

    filename = '/opt/airflow/data/global-economy-indicators.zip'

    with zipfile.ZipFile(filename, 'r') as zip:
        for nombre_archivo in zip.namelist():
            print(nombre_archivo)
        print('hecho')

def transform_task ():
    df = pd.read_csv('/opt/airflow/data/global-economy-indicators.zip', encoding='utf-8')

    df.columns = remove_accents_cols(df.columns)
    df.columns = remove_special_chars(df.columns)
    df.columns = regular_snake_case(df.columns)

    df = df.rename(
        columns={
            'countryid': 'country_id',
            'agriculture,_hunting,_forestry,_fishing_(isic_a_b)': 'agriculture,hunting,forestry,fishing(isic_a_b)',
            'gross_fixed_capital_formation_(including_acquisitions_less_disposals_of_valuables)': 'gross_fixed_capital_formation',
            'household_consumption_expenditure_(including_non_profit_institutions_serving_households)': 'household_consumption_expenditure',
            'mining,_manufacturing,_utilities_(isic_c_e)': 'mining,_manufacturing,_utilities(isic_c_e)',
            'transport,_storage_and_communication_(isic_i)': 'transport,storage_and_communication(isic_i)',
            'wholesale,_retail_trade,_restaurants_and_hotels_(isic_g_h)': 'wholesale,retail_trade,restaurants_and_hotels(isic_g_h)',

        }
    )
    # Convertir tipos de datos a tipos nativos de Python
    df = df.astype({
        'country_id': 'int',
        'year': 'int',
        'ama_exchange_rate': 'float',
        'imf_based_exchange_rate': 'float',
        'population': 'int',
        'per_capita_gni': 'int',
        'agriculture,hunting,forestry,fishing(isic_a_b)': 'float',
        'changes_in_inventories': 'float',
        'construction_(isic_f)': 'float',
        'exports_of_goods_and_services': 'float',
        'final_consumption_expenditure': 'float',
        'general_government_final_consumption_expenditure': 'float',
        'gross_capital_formation': 'float',
        'gross_fixed_capital_formation': 'float',
        'household_consumption_expenditure': 'float',
        'imports_of_goods_and_services': 'float',
        'manufacturing_(isic_d)': 'float',
        'mining,_manufacturing,_utilities(isic_c_e)': 'float',
        'other_activities_(isic_j_p)': 'float',
        'total_value_added': 'float',
        'transport,storage_and_communication(isic_i)': 'float',
        'wholesale,retail_trade,restaurants_and_hotels(isic_g_h)': 'float',
        'gross_national_income(gni)_in_usd': 'float',
        'gross_domestic_product_(gdp)': 'float'
    }).convert_dtypes()

    print(df)
    print(df.columns)
    print(df.dtypes)
    print(df.info())

    if ~df.empty and len(df.columns) >0:
        load_df_to_sql(df, schema, tmp_table, sql_connid_postgrest)

    return df    
    

dag = DAG(
    dag_id = DAG_ID,
    description = DAG_DESCRIPTION,
    catchup = False,
    schedule_interval = DAG_SCHEDULE,
    max_active_runs = 1,
    dagrun_timeout = 200000,
    default_args = default_args,
    tags = TAGS
)

with dag as dag:
    start_task = EmptyOperator(
        task_id = 'inicia_proceso'
    )

    extract_task = PythonOperator(
        task_id = 'extraccion',
        python_callable = extract_task,
        retries = retries,
        retry_delay = retry_delay
    )

    transform_task = PythonOperator(
        task_id = 'transformacion',
        python_callable = transform_task,
        retries = retries,
        retry_delay = retry_delay
    )

    load_task = PostgresOperator(task_id='load_task',
                                    postgres_conn_id=sql_connid_postgrest,
                                    autocommit=True,
                                    sql=f"call {schema}.{sp_name}()",
                                    dag=dag
    )

    end_task = EmptyOperator(
        task_id = 'finaliza_proceso'
    )

start_task >> extract_task >> transform_task >> load_task >> end_task