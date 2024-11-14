import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from config.current_weather import CurrentWeatherToKafka, TransformWeatherData

from config.config import CurrentWeather


options = PipelineOptions(['--runner=DirectRunner'])


with beam.Pipeline(options=options) as p:
    producer = (
        p
        | 'Initialize' >> beam.Create([CurrentWeather().get_current_weather()])
        | 'Transform data' >> beam.ParDo(TransformWeatherData())
        | 'Load data to Kafka' >> beam.ParDo(CurrentWeatherToKafka())
    )
    producer | beam.Map(print)
