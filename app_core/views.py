from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, EventoKafka
from .forms import ProductoForm
from .kafka_producer import send_kafka_event
import requests
import logging

logger = logging.getLogger("app_core")


# ==========================================
# REDIRECCIÓN RAÍZ INTELIGENTE
# ==========================================
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('productos')
    return redirect('login')


# ==========================================
# CONSULTA DE MONEDAS
# ==========================================
@login_required
def consulta_monedas(request):
    api_url = "http://127.0.0.1:8000/api/monedas/"
    params = request.GET

    try:
        response = requests.get(api_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.exception("Error consultando API interna de monedas: %s", e)
        # fallback: enviar contexto vacío al template con un mensaje
        return render(request, "app_core/monedas.html", {
            "error": "No se pudieron obtener las tasas internacionales. Intenta nuevamente.",
            "rates": {},
            "base": "EUR",
            "monto": request.GET.get("monto", ""),
            "origen": request.GET.get("origen", ""),
            "destino": request.GET.get("destino", ""),
            "conversion_result": None,
        })

    context = {
        "rates": data.get("rates", {}),
        "base": data.get("base", "EUR"),
        "monto": request.GET.get("monto", ""),
        "origen": request.GET.get("origen", ""),
        "destino": request.GET.get("destino", ""),
        "conversion_result": data.get("conversion_result", None),
    }

    return render(request, "app_core/monedas.html", context)


# ==========================================
# CRUD PRODUCTOS
# ==========================================
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creador = request.user
            producto.save()

            # Enviar evento a Kafka (no bloquear)
            try:
                send_kafka_event({
                    "action": "producto_creado",
                    "id": producto.id,
                    "nombre": producto.nombre,
                    "precio": float(producto.precio),
                    "stock": producto.stock,
                    "usuario": request.user.username
                })
            except Exception as e:
                logger.exception("Fallo enviando evento producto_creado a Kafka: %s", e)

            messages.success(request, 'Producto creado exitosamente')
            return redirect('productos')
        else:
            messages.error(request, 'Corrige los errores del formulario')
    else:
        form = ProductoForm()
    return render(request, 'app_core/crear_producto.html', {'form': form})


@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            # Kafka
            try:
                send_kafka_event({
                    "action": "producto_editado",
                    "id": producto.id,
                    "nombre": producto.nombre,
                    "precio": float(producto.precio),
                    "stock": producto.stock,
                    "usuario": request.user.username
                })
            except Exception as e:
                logger.exception("Fallo enviando evento producto_editado a Kafka: %s", e)

            messages.success(request, 'Producto actualizado')
            return redirect('productos')
        else:
            messages.error(request, 'Corrige los errores del formulario')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'app_core/editar_producto.html', {
        'form': form,
        'producto': producto
    })


@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        try:
            send_kafka_event({
                "action": "producto_eliminado",
                "id": producto.id,
                "nombre": producto.nombre,
                "usuario": request.user.username
            })
        except Exception as e:
            logger.exception("Fallo enviando evento producto_eliminado a Kafka: %s", e)

        producto.delete()
        messages.success(request, 'Producto eliminado')
        return redirect('productos')

    return render(request, 'app_core/eliminar_producto.html', {
        'producto': producto
    })


# ==========================================
# AUTENTICACIÓN
# ==========================================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('productos')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('productos')
        else:
            messages.error(request, "Credenciales incorrectas")

    return render(request, "app_core/login.html")


def logout_view(request):
    auth_logout(request)
    return redirect('login')


# ==========================================
# LISTAR PRODUCTOS
# ==========================================
@login_required
def productos_view(request):
    productos = Producto.objects.all()
    return render(request, "app_core/productos.html", {"productos": productos})


# ==========================================
# HANDLERS DE ERRORES PERSONALIZADOS
# ==========================================
def error_400(request, exception=None):
    logger.error("Handler 400: path=%s user=%s", getattr(request, 'path', ''), getattr(request.user, 'username', None))
    return render(request, "app_core/400.html", status=400)


def error_403(request, exception=None):
    logger.error("Handler 403: path=%s user=%s", getattr(request, 'path', ''), getattr(request.user, 'username', None))
    return render(request, "app_core/403.html", status=403)


def error_404(request, exception=None):
    logger.error("Handler 404: path=%s user=%s", getattr(request, 'path', ''), getattr(request.user, 'username', None))
    return render(request, "app_core/404.html", status=404)


def error_500(request):
    # No recibimos 'exception' en handler500 por diseño de Django
    logger.exception("Handler 500: error interno en la ruta: %s", getattr(request, 'path', ''))
    return render(request, "app_core/500.html", status=500)
