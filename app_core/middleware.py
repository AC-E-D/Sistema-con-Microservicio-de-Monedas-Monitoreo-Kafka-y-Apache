import logging
import traceback
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("app_core")

# Intentamos usar tu kafka_producer si existe
try:
    from .kafka_producer import send_kafka_event
    _KAFKA_AVAILABLE = True
except Exception:
    _KAFKA_AVAILABLE = False
    logger.warning("kafka_producer no disponible para ErrorReportingMiddleware")


class ErrorReportingMiddleware(MiddlewareMixin):
    """
    Middleware que intercepta excepciones no manejadas (500),
    registra en logs y envía un evento a Kafka (si está disponible).
    """

    def process_exception(self, request, exception):
        # timestamp
        ts = time.time()

        # traceback en texto
        tb = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))

        payload = {
            "evento": "error_500",
            "path": request.path,
            "method": request.method,
            "user": getattr(request.user, "username", None) if hasattr(request, "user") else None,
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
            "traceback": tb,
            "timestamp": ts,
        }

        # Log estructurado
        logger.error("Error crítico capturado: %s", payload)

        # Enviar a Kafka si está disponible (no bloquear si falla)
        if _KAFKA_AVAILABLE:
            try:
                send_kafka_event(payload)
                logger.info("Evento de error enviado a Kafka (error_500).")
            except Exception as e:
                logger.exception("Fallo enviando evento de error a Kafka: %s", e)

        # No devolvemos una Response: dejamos que Django maneje la 500 y muestre template 500.html
        return None
