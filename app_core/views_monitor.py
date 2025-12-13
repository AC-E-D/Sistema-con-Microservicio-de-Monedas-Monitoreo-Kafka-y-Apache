# app_core/views_monitor.py
import json
import psutil
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from pathlib import Path

logger = logging.getLogger("app_core")

LOG_DIR = Path(settings.LOG_DIR)


def leer_log_seguro(path, lineas=5):
    """
    Lee un archivo de log sin fallar por caracteres inválidos.
    Devuelve las últimas 'lineas' líneas.
    """
    try:
        if path.exists():
            return path.read_text(encoding="utf-8", errors="replace").splitlines()[-lineas:]
        return []
    except Exception as e:
        return [f"Error leyendo log: {str(e)}"]


def monitor_dashboard(request):
    """
    Retorna el HTML del dashboard de monitoreo.
    """
    return render(request, "app_core/monitor.html")


def monitor_data(request):
    """
    Retorna métricas en tiempo real en formato JSON.
    Siempre debe devolver datos válidos.
    """
    try:
        # CPU y RAM
        cpu = psutil.cpu_percent(interval=0.3)
        ram = psutil.virtual_memory().percent

        # Logs Kafka y errores
        kafka_lines = leer_log_seguro(LOG_DIR / "kafka.log")
        error_lines = leer_log_seguro(LOG_DIR / "errors.log")

        return JsonResponse({
            "cpu": cpu,
            "ram": ram,
            "kafka": kafka_lines,
            "errors": error_lines
        })

    except Exception as e:
        logger.error(f"Error en monitor_data: {str(e)}")
        return JsonResponse({
            "cpu": 0,
            "ram": 0,
            "kafka": [],
            "errors": [f"Error interno: {str(e)}"]
        }, status=500)
