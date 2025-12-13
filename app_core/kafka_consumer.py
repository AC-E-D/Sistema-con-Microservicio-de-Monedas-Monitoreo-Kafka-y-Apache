# app_core/kafka_consumer.py
import os
import sys
from pathlib import Path
import json
import logging
from kafka import KafkaConsumer

# =======================
#  CONFIG LOGGING
# =======================
logger = logging.getLogger("kafka")

# =======================
#  CORRECCIÓN DE RUTAS
# =======================
BASE_DIR = Path(__file__).resolve().parents[1]  # carpeta evaluacion 3
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mi_proyecto.settings")

import django
django.setup()

from app_core.models import EventoKafka, Producto

# =======================
#  CONFIG CONSUMIDOR
# =======================
TOPIC = "evaluacion3"
BOOTSTRAP_SERVERS = ["localhost:9092"]

# consumer group → REQUISITO para 10 pts (balanceo básico)
CONSUMER_GROUP = "consumidores_evaluacion3"


def main():
    logger.info("Consumidor Kafka inicializando…")

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=CONSUMER_GROUP,  # ✔ para 10 pts
    )

    logger.info("📥 Consumidor Kafka escuchando eventos…")

    for msg in consumer:
        data = msg.value
        logger.info(f"📨 Mensaje recibido (offset={msg.offset}): {data}")

        try:
            # buscar producto asociado
            producto_obj = None
            if "id" in data:
                try:
                    producto_obj = Producto.objects.get(id=data["id"])
                except Producto.DoesNotExist:
                    producto_obj = None

            # guardar evento
            EventoKafka.objects.create(
                accion=data.get("action", "desconocido"),
                datos=data,
                usuario=data.get("usuario", ""),
                producto=producto_obj
            )

            logger.info("💾 Evento guardado correctamente en EventoKafka")

        except Exception as e:
            logger.error(
                {
                    "evento": "kafka_event_error",
                    "topic": msg.topic,
                    "offset": msg.offset,
                    "error": str(e),
                }
            )
            print(f"⚠️ Error guardando evento: {e}")


if __name__ == "__main__":
    main()
