# app_core/views_monitor.py
import json
import psutil
import logging
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from pathlib import Path

logger = logging.getLogger("app_core")

LOG_DIR = Path(settings.LOG_DIR)
MICROSERVICIO_MONEDAS = "http://127.0.0.1:5001/monedas"


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
    Métricas del sistema (YA EXISTENTES).
    """
    try:
        cpu = psutil.cpu_percent(interval=0.3)
        ram = psutil.virtual_memory().percent

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


def monitor_monedas(request):
    """
    NUEVO endpoint:
    Devuelve TODAS las monedas exactamente como en la API anterior,
    pero ahora vía microservicio.
    """
    try:
        r = requests.get(MICROSERVICIO_MONEDAS, timeout=5)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        logger.exception("Error obteniendo monedas desde microservicio")
        return JsonResponse({
            "base": "EUR",
            "rates": {}
        }, status=503)

    return JsonResponse({
        "base": data.get("base"),
        "rates": data.get("rates", {})
    })
