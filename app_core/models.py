from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone


class Producto(models.Model):
    """
    Producto básico con validaciones, índices y constraint mínimo.
    - nombre: único (evita duplicados lógicos)
    - precio: Decimal >= 0
    - stock: int >= 0
    - creador: FK al User (nullable para no romper si borran usuarios)
    """
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos'
    )
    creado_at = models.DateTimeField(auto_now_add=True)
    actualizado_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado_at']
        indexes = [
            models.Index(fields=['nombre'], name='idx_producto_nombre'),
            models.Index(fields=['precio'], name='idx_producto_precio'),
            models.Index(fields=['-creado_at'], name='idx_producto_creado_at'),
        ]
        constraints = [
            # unique already enforced by unique=True, pero también muestro cómo sería:
            models.UniqueConstraint(fields=['nombre'], name='unique_producto_nombre'),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.id})"


class EventoKafka(models.Model):
    """
    Evento guardado por el consumer:
    - datos: JSON con payload original
    - producto: FK opcional para relacionar el evento con un producto
    - usuario: string (quien disparó el evento, si viene)
    - accion: tipo de evento (creado/editar/eliminar)
    """
    accion = models.CharField(max_length=50, db_index=True)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos'
    )
    datos = models.JSONField()
    usuario = models.CharField(max_length=150, blank=True)
    creado_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_at']
        indexes = [
            models.Index(fields=['creado_at'], name='idx_eventokafka_creado_at'),
            models.Index(fields=['accion'], name='idx_eventokafka_accion'),
        ]

    def __str__(self):
        return f"EventoKafka {self.accion} ({self.id})"
