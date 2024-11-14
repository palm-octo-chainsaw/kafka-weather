from airflow import DAG
from airflow.models import Variable
from airflow.providers.apache.beam.operators.beam import BeamRunPythonPipelineOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 11, 13, 0, 0, 00),
}

beam_kafka_consumer = Variable.get('beam_pipeline_py_file')


with DAG('beam_kafka_jobs',
         default_args=default_args,
         description='Run Beam Kafka Producer and Consumer Jobs',
         schedule_interval='50 * * * *',
         catchup=False,
         ) as dag:

    run_beam_kafka_producer = BeamRunPythonPipelineOperator(
        task_id='run_beam_kafka_producer',
        py_file=beam_kafka_consumer,
        runner="DirectRunner",
        py_interpreter='python3.8',
    )

    run_beam_kafka_producer
