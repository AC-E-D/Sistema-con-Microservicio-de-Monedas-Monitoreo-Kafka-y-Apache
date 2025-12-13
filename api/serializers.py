# api/serializers.py

from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    """Serializer vacío para endpoints que no requieren datos."""
    pass


class MonedaResponseSerializer(serializers.Serializer):
    """Define la estructura de la respuesta de la API de monedas."""
    base = serializers.CharField()
    rates = serializers.DictField(
        child=serializers.FloatField(),
        required=False
    )
    conversion_result = serializers.FloatField(
        allow_null=True
    )
    error = serializers.CharField(
        required=False
    )
