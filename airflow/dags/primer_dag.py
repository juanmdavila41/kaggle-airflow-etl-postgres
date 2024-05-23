from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

TAGS = ['python_data_flow']
DAG_ID = 'primer_dag'
DAG_DESCRIPTION = '''primer dag en el curso de airflow'''
DAG_SCHEDULE = "0 9 * * *"
default_args = {
    "start_date": datetime(2024,1,1)
}
retries = 4
retry_delay = timedelta(minutes=5)

def execute_task ():
    print('Hola Mundo')

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

    transform_task = PythonOperator(
        task_id = 'transformacion',
        python_callable = execute_task,
        retries = retries,
        retry_delay = retry_delay
    )

    end_task = EmptyOperator(
        task_id = 'finaliza_proceso'
    )

start_task >> transform_task >> end_task