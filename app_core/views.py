from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm
from .kafka_producer import send_kafka_event
import requests
import logging

logger = logging.getLogger("app_core")

# =====================================================
# REDIRECCIÓN RAÍZ
# =====================================================
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("productos")
    return redirect("login")

# =====================================================
# MONEDAS – MISMO COMPORTAMIENTO QUE API DJANGO ORIGINAL
# =====================================================
@login_required
def consulta_monedas(request):
    MICROSERVICIO_URL = "http://127.0.0.1:5001/monedas"

    params = {
        "monto": request.GET.get("monto"),
        "origen": request.GET.get("origen"),
        "destino": request.GET.get("destino"),
    }

    try:
        r = requests.get(MICROSERVICIO_URL, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
    except Exception:
        logger.exception("Error consultando microservicio de monedas")
        return render(request, "app_core/monedas.html", {
            "rates": {},
            "base": "EUR",
            "conversion_result": None,
            "error": "No se pudo obtener información de monedas"
        })

    return render(request, "app_core/monedas.html", {
        "rates": data.get("rates", {}),
        "base": data.get("base", "EUR"),
        "monto": params["monto"],
        "origen": params["origen"],
        "destino": params["destino"],
        "conversion_result": data.get("conversion_result"),
    })

# =====================================================
# CRUD PRODUCTOS
# =====================================================
@login_required
def productos_view(request):
    productos = Producto.objects.all()
    return render(request, "app_core/productos.html", {"productos": productos})

@login_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creador = request.user
            producto.save()

            send_kafka_event({
                "accion": "crear_producto",
                "producto": producto.nombre,
                "usuario": request.user.username
            })

            messages.success(request, "Producto creado")
            return redirect("productos")
    else:
        form = ProductoForm()

    return render(request, "app_core/crear_producto.html", {"form": form})

@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()

            send_kafka_event({
                "accion": "editar_producto",
                "producto": producto.nombre,
                "usuario": request.user.username
            })

            messages.success(request, "Producto actualizado")
            return redirect("productos")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "app_core/editar_producto.html", {
        "form": form,
        "producto": producto
    })

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        send_kafka_event({
            "accion": "eliminar_producto",
            "producto": producto.nombre,
            "usuario": request.user.username
        })

        producto.delete()
        messages.success(request, "Producto eliminado")
        return redirect("productos")

    return render(request, "app_core/eliminar_producto.html", {
        "producto": producto
    })

# =====================================================
# AUTENTICACIÓN
# =====================================================
def login_view(request):
    if request.user.is_authenticated:
        return redirect("productos")

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("productos")
        messages.error(request, "Credenciales incorrectas")

    return render(request, "app_core/login.html")

def logout_view(request):
    auth_logout(request)
    return redirect("login")

# =====================================================
# HANDLERS DE ERROR (DEBUG = False)
# =====================================================
def error_400(request, exception=None):
    return render(request, "app_core/400.html", status=400)

def error_403(request, exception=None):
    return render(request, "app_core/403.html", status=403)

def error_404(request, exception=None):
    return render(request, "app_core/404.html", status=404)

def error_500(request):
    return render(request, "app_core/500.html", status=500)
