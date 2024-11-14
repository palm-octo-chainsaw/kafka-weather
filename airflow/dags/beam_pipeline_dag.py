from airflow import DAG
from airflow.models import Variable
from airflow.providers.apache.beam.operators.beam import BeamRunPythonPipelineOperator
from airflow.providers.apache.kafka.operators.consume import ConsumeFromTopicOperator
from datetime import datetime, timedelta


KAFKA_CONFIG = {
    'bootstrap.servers': 'kafka0:29092',
    'group.id': 'airflow-consumer-group',
    'auto.offset.reset': 'earliest',
}
TOPIC_NAME = "current-weather"
GROUP_ID = "airflow-group"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 11, 13, 0, 0, 00),
}

beam_kafka_producer = Variable.get('kafka-weather-producer')


with DAG('beam_kafka_jobs',
         default_args=default_args,
         description='Run Beam Kafka Producer and Consumer Jobs',
         schedule_interval='50 * * * *',
         catchup=False,
         ) as dag:

    run_beam_kafka_producer = BeamRunPythonPipelineOperator(
        task_id='run_beam_kafka_producer',
        py_file=beam_kafka_producer,
        runner="DirectRunner",
        py_interpreter='python3.8',
    )

    run_beam_kafka_consumer = ConsumeFromTopicOperator(
        task_id='consume_from_kafka',
        kafka_config_id='kafka_default',
        topics=[TOPIC_NAME],
        apply_function='',
        apply_function_kwargs={"prefix": "consumed:::"},
        max_messages=10,
        max_batch_size=1,
        poll_timeout=10,
        consumer_config={'bootstrap.servers': 'kafka0:9092',
                         'group.id': 'current-weather-to-postgre',
                         'auto.offset.reset': 'smallest'},
        commit_cadence="never"
    )

    run_beam_kafka_producer
