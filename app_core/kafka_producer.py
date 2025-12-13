# app_core/kafka_producers.py
import json
import logging
import time
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError, KafkaError

logger = logging.getLogger("kafka")


# ======================================================
#   FUNCIÓN PARA CREAR PRODUCTOR CON RECONEXIÓN SEGURA
# ======================================================
def create_producer():
    """
    Crea un KafkaProducer robusto:
    - Reintento automático
    - JSON serializer
    - Configuración segura
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers=["localhost:9092"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5,
            retry_backoff_ms=200,
            acks="all",
            linger_ms=10,
            request_timeout_ms=8000,
            max_block_ms=8000
        )
        logger.info("KafkaProducer inicializado correctamente.")
        return producer

    except Exception as e:
        logger.error(f"No se pudo inicializar KafkaProducer: {e}")
        return None


# Instancia global reutilizable
producer = create_producer()


# ======================================================
#   FUNCIÓN PARA REENVIAR EVENTOS A KAFKA
# ======================================================
def send_kafka_event(event: dict):
    """
    Envía un evento JSON a Kafka con:
    - logging estructurado
    - métricas de envío (latencia/tamaño)
    - reintento automático si el productor se cayó
    - manejo completo de excepciones
    """

    global producer
    inicio = time.time()

    # Si el producer está caído → intentar recrearlo
    if producer is None:
        logger.warning("KafkaProducer era None; intentando recrearlo...")
        producer = create_producer()
        if producer is None:
            logger.error("KafkaProducer NO disponible. Evento descartado.")
            return

    try:
        # Enviar evento
        future = producer.send("evaluacion3", event)
        result = future.get(timeout=6)  # esperar confirmación

        # Métricas
        latencia = round((time.time() - inicio) * 1000, 2)
        size_bytes = len(json.dumps(event).encode())

        logger.info({
            "evento": "kafka_producer_send",
            "topic": "evaluacion3",
            "size_bytes": size_bytes,
            "latency_ms": latencia,
            "status": "ok",
            "offset": result.offset
        })

    except KafkaTimeoutError as e:
        logger.error({
            "evento": "kafka_producer_timeout",
            "topic": "evaluacion3",
            "error": str(e)
        })

    except KafkaError as e:
        logger.error({
            "evento": "kafka_producer_error",
            "topic": "evaluacion3",
            "error": str(e)
        })

        # Intentar recrear el producer (broker puede haber caído)
        logger.warning("Intentando recrear KafkaProducer por error crítico...")
        producer = create_producer()

    except Exception as e:
        logger.error({
            "evento": "kafka_producer_exception",
            "topic": "evaluacion3",
            "error": str(e)
        })

        # Intentar recrear el producer también aquí
        logger.warning("Intentando recrear KafkaProducer tras excepción inesperada...")
        producer = create_producer()

    finally:
        # Intentar flush, nunca fallar
        try:
            producer.flush()
        except Exception:
            pass
