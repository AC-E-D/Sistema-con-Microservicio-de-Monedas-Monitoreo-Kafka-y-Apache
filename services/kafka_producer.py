# services/kafka_producer.py
import json
import logging
from django.conf import settings
from kafka import KafkaProducer
from kafka.errors import KafkaError

logger = logging.getLogger('kafka_producer')

def _get_producer():
    servers = getattr(settings, 'KAFKA_BOOTSTRAP_SERVERS', ['localhost:9092'])
    return KafkaProducer(
        bootstrap_servers=servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        api_version=(0, 10)  # compatible con Kafka 3.x
    )

def enviar_evento_kafka(evento, topic=None):
    """
    Enviar evento (dict) a Kafka. No lanza excepción si falla, solo logea.
    """
    if topic is None:
        topic = getattr(settings, 'KAFKA_TOPIC', 'eventos_producto')
    try:
        producer = _get_producer()
        fut = producer.send(topic, evento)
        record_metadata = fut.get(timeout=10)
        logger.info(f"Evento enviado a topic={record_metadata.topic} partition={record_metadata.partition} offset={record_metadata.offset}")
    except KafkaError as e:
        logger.exception(f"Error enviando evento a Kafka: {e}")
    except Exception as e:
        logger.exception(f"Error inesperado en enviar_evento_kafka: {e}")
