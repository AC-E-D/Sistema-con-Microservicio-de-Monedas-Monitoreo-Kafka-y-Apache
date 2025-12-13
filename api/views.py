# api/views.py
import json
import logging
import time
import requests

from kafka import KafkaProducer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied, BadRequest

logger = logging.getLogger("api")


# =======================================================
#   PRODUCTOR KAFKA
# =======================================================
def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",
        retries=5,
        retry_backoff_ms=200,
        linger_ms=10
    )


producer = get_kafka_producer()


def enviar_evento(topic, payload):
    inicio = time.time()
    try:
        future = producer.send(topic, payload)
        result = future.get(timeout=5)

        duracion = round((time.time() - inicio) * 1000, 2)

        logger.info({
            "evento": "kafka_producer_send",
            "topic": topic,
            "size_bytes": len(json.dumps(payload)),
            "latency_ms": duracion,
            "status": "ok",
            "offset": result.offset
        })

    except Exception as exc:
        logger.error({
            "evento": "kafka_producer_error",
            "topic": topic,
            "error": str(exc)
        })


# =======================================================
#   API DE MONEDAS
# =======================================================
class MonedasAPIView(APIView):
    """
    Servicio REST que entrega tasas internacionales de cambio
    y permite realizar conversión entre pares de monedas.
    """

    def get(self, request):
        # --- DEMO DE ERRORES PARA EL CRITERIO 8 ---
        if request.GET.get("error") == "400":
            raise BadRequest("Parámetros inválidos enviados por el cliente.")

        if request.GET.get("error") == "403":
            raise PermissionDenied("No tienes permisos para esta acción.")

        if request.GET.get("error") == "404":
            raise Http404("Recurso solicitado no existe.")

        if request.GET.get("error") == "500":
            raise Exception("Error interno simulado para pruebas.")

        # -------------------------------------------

        monto = request.GET.get("monto")
        origen = request.GET.get("origen")
        destino = request.GET.get("destino")

        EXTERNAL_API = "https://api.exchangerate-api.com/v4/latest/EUR"

        try:
            r = requests.get(EXTERNAL_API, timeout=5)
            r.raise_for_status()
            data = r.json()
        except Exception as exc:
            logger.error(f"Error consultando API externa: {exc}")
            return Response({
                "base": "EUR",
                "rates": {},
                "conversion_result": None,
                "error": "No se pudieron obtener las tasas internacionales."
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        rates = data.get("rates", {})
        conversion_result = None

        if monto and origen and destino:
            try:
                monto = float(monto)
                rate_origen = rates.get(origen)
                rate_destino = rates.get(destino)

                if rate_origen and rate_destino:
                    monto_eur = monto / rate_origen
                    conversion_result = monto_eur * rate_destino
                else:
                    logger.warning(f"Pares inválidos: {origen} → {destino}")

            except Exception as exc:
                logger.error(f"Error en cálculo de conversión: {exc}")

        # Evento Kafka
        enviar_evento("evaluacion3", {
            "action": "consulta_monedas",
            "parametros": {
                "monto": monto,
                "origen": origen,
                "destino": destino
            },
            "conversion": conversion_result
        })

        return Response({
            "base": "EUR",
            "rates": rates,
            "conversion_result": conversion_result
        }, status=200)
