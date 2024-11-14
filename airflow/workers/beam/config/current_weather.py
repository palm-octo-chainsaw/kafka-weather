import json
import apache_beam as beam
from quixstreams import Application


class TransformWeatherData(beam.DoFn):
    def process(self, element):
        element.pop('current_units', None)
        current_temp = element.pop('current')
        element.update(current_temp)
        return [element]


class CurrentWeatherToKafka(beam.DoFn):
    def process(self, element):
        app = Application(
            broker_address='kafka0:29092',
            loglevel='DEBUG'
        )
        app.topic('current-weather', value_deserializer='json')

        with app.get_producer() as producer:
            producer.produce(
                topic='current-weather',
                key='Sofia',
                value=json.dumps(element)
            )
        return [element]
