from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

EXTERNAL_API = "https://api.exchangerate-api.com/v4/latest/EUR"


@app.route("/monedas", methods=["GET"])
def monedas():
    """
    Microservicio de monedas:
    - Consume la MISMA API internacional que usaba Django antes
    - Devuelve TODAS las monedas (sin recortes)
    - Soporta conversión igual que el proyecto original
    """

    monto = request.args.get("monto", type=float)
    origen = request.args.get("origen")
    destino = request.args.get("destino")

    try:
        r = requests.get(EXTERNAL_API, timeout=5)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return jsonify({
            "base": "EUR",
            "rates": {},
            "conversion_result": None,
            "error": "Error consultando API internacional"
        }), 503

    rates = data.get("rates", {})
    conversion_result = None

    if monto and origen and destino:
        try:
            rate_origen = rates.get(origen)
            rate_destino = rates.get(destino)

            if rate_origen and rate_destino:
                monto_eur = monto / rate_origen
                conversion_result = monto_eur * rate_destino
        except Exception:
            conversion_result = None

    return jsonify({
        "base": "EUR",
        "rates": rates,
        "conversion_result": conversion_result
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
