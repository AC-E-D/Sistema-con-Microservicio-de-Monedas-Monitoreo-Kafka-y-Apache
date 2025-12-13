#!/usr/bin/env python3
# services/kafka_consumer.py
import os
import django
import json
import logging
import time

# Ajustar si tu proyecto settings tiene otro nombre diferente a mi_proyecto.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from django.conf import settings
from kafka import KafkaConsumer

# Intentamos importar el modelo EventoKafka si existe
try:
    from app_core.models import EventoKafka
except Exception:
    EventoKafka = None

logger = logging.getLogger('kafka_consumer')
logger.setLevel(logging.INFO)

# log file en la raíz del proyecto /logs/kafka_consumer.log
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
fh = logging.FileHandler(os.path.join(log_dir, 'kafka_consumer.log'))
fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(fh)

def run_consumer():
    servers = getattr(settings, 'KAFKA_BOOTSTRAP_SERVERS', ['localhost:9092'])
    topic = getattr(settings, 'KAFKA_TOPIC', 'eventos_producto')
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.info(f'Listening to topic {topic} on {servers}')
    for msg in consumer:
        try:
            data = msg.value
            logger.info(f"Received message: {data}")
            # Guardar en DB si el modelo existe
            if EventoKafka is not None:
                try:
                    EventoKafka.objects.create(topic=msg.topic, payload=data)
                except Exception as e:
                    logger.exception(f'Could not save EventoKafka: {e}')
        except Exception as e:
            logger.exception(f'Error processing message: {e}')

if __name__ == '__main__':
    while True:
        try:
            run_consumer()
        except Exception as e:
            logger.exception(f'Consumer crashed, restarting in 5s: {e}')
            time.sleep(5)
