# Sistema de Inventario con API de Monedas, Kafka y Monitoreo

---

## Descripción del Proyecto

Este proyecto es un **sistema de inventario desarrollado en Django**, que integra:

- CRUD de productos con autenticación
- API REST de conversión de monedas internacionales
- Integración con Apache Kafka (productores y consumidores)
- Monitoreo en tiempo real (CPU, RAM, logs y eventos Kafka)
- Servido mediante **Nginx como reverse proxy HTTPS**
- Manejo profesional de errores y logging

El sistema está diseñado con **arquitectura profesional**, separación de responsabilidades y preparado para entornos reales.

---

## Tecnologías Utilizadas

### Backend

- Python 3.10+
- Django
- Django REST Framework
- drf-spectacular (Swagger / OpenAPI)

### Mensajería

- Apache Kafka 2.6.x (recomendado)
- Zookeeper
- kafka-python

### Infraestructura

- Nginx 1.24+ / 1.29.x
- HTTPS con certificados SSL (autofirmados para entorno académico)

---

## Requisitos Previos (IMPORTANTE)

⚠️ **Este proyecto requiere software externo además de los paquetes Python.**

### Software obligatorio (NO incluido en `requirements.txt`)

Debes instalar manualmente:

| Software        | Versión recomendada |
|-----------------|---------------------|
| Python          | 3.10 o superior     |
| Apache Kafka    | 3.7.0               |
| Zookeeper       | Incluido con Kafka  |
| Nginx           | 1.24+ / 1.29.x      |
| Git             | Última versión      |

---

## Instalación del Proyecto

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/AC-E-D/Sistema-de-Inventario-con-API-de-monedas-internacionales-y-monitoreo.git
cd Sistema-de-Inventario-con-API-de-monedas-internacionales-y-monitoreo
```

## Configuración del Entorno Python
Windows / Linux
```bash
python -m venv env
```
o
```bash
python3 -m venv env
```

Activar entorno virtual

Windows

```bash
env\Scripts\activate
```
Linux / macOS

```bash
source env/bin/activate
```

## Instalar dependencias Python
```bash
pip install -r requirements.txt
```

## Instalación y Configuración de Kafka
## 2️⃣ Descargar Apache Kafka

Descargar Kafka 3.7.0 desde:
https://archive.apache.org/dist/kafka/3.7.0/kafka_2.13-3.7.0.tgz


⚠️ Versiones más nuevas pueden causar incompatibilidades con kafka-python.

Extraer Kafka en cualquier carpeta, por ejemplo:

C:\kafka\ (Windows)

/opt/kafka/ (Linux)

## 3️⃣ Iniciar Zookeeper

Windows
```bash
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

Linux
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```
## 4️⃣ Iniciar Kafka Broker

Windows
```bash
bin\windows\kafka-server-start.bat config\server.properties
```

Linux
```bash
bin/kafka-server-start.sh config/server.properties
```
## 5️⃣ Iniciar Kafka Consumer del proyecto

Desde la carpeta del proyecto:
```bash
python app_core/kafka_consumer.py
```
o
```bash
python kafka_consumer.py
```

Este proceso debe quedar ejecutándose.

Configuración y Ejecución de Django
Migraciones
```bash
python manage.py migrate
```
Crear superusuario (opcional, ya viene con db con credenciales. Estan al final de este read me)
```bash
python manage.py createsuperuser
```
Iniciar Django (backend)
```bash
python manage.py runserver 127.0.0.1:8000
```

Django debe estar ejecutándose antes de iniciar Nginx.

## Instalación y Configuración de Nginx
## 6️⃣ Descargar Nginx

Windows

https://nginx.org/en/download.html


Extraer, por ejemplo en:

C:\nginx\


Linux
```bash
sudo apt install nginx
```

## 7️⃣ Configurar Nginx

Usar el archivo nginx.conf incluido en la carpeta raíz del proyecto. Luego de descompirmir el archivo descargado de la página de nginx, copiar nginx.conf dentro de la carpeta conf, esta ultima esta en el mismo lugar que nginx.exe.

Este archivo:

- Habilita HTTPS

- Usa certificados locales

- Actúa como reverse proxy hacia Django

## 8️⃣ Iniciar Nginx

Windows

nginx.exe


Linux
```bash
sudo systemctl start nginx
```

Orden Correcto de Ejecución
1. Zookeeper
2. Kafka Broker
3. Kafka Consumer
4. Django (runserver)
5. Nginx


Nginx es el último componente en ejecutarse, ya que depende del backend activo.

---

# Acceso al Sistema

Una vez todo esté ejecutándose correctamente:

URL principal
https://localhost/

Dashboard de monitoreo
https://localhost/app_core/monitor/

URL Swagger (para pruebas de API)
https://localhost/swagger/

URL Redoc (para registros)
https://localhost/redoc/

## Credenciales de Prueba
- Usuario: Alex
- Contraseña: 12345678Aa

## Notas sobre HTTPS

- El sistema usa certificados SSL autofirmados

- El navegador mostrará “No seguro”, lo que es correcto

- La comunicación sí está cifrada

---

# Proyecto hecho Alex Cuevas Danyau
