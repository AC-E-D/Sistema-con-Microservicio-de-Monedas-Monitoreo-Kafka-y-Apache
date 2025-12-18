# Sistema con Microservicio de Monedas, Kafka y Apache

---

## Descripción del Proyecto

Este proyecto corresponde a un **sistema backend desarrollado en Django**, que implementa una **arquitectura distribuida basada en microservicios**, mensajería asincrónica y componentes de infraestructura reales.

El proyecto integra:

* Backend principal en **Django**
* **Microservicio independiente de monedas internacionales** (API REST)
* **Apache Kafka** para mensajería distribuida
* **Zookeeper** para la coordinación de Kafka
* **Apache HTTP Server** configurado como servidor web
* Certificados SSL para comunicación HTTPS
* Ejecución distribuida mediante múltiples procesos simultáneos

---

## Arquitectura del Sistema

El sistema se ejecuta mediante **cinco procesos independientes**, cada uno con una responsabilidad específica:

1. **Apache HTTP Server** (HTTPS y certificados)
2. **Zookeeper** (coordinación de Kafka)
3. **Kafka Broker** (mensajería)
4. **Microservicio de Monedas Internacionales**
5. **Backend Django**

Cada componente se ejecuta en su propio proceso y terminal, demostrando una arquitectura desacoplada y realista.

---

## Tecnologías Utilizadas

### Backend Principal

* Python 3.10+
* Django
* Django REST Framework

### Microservicios

* Python
* API REST para conversión de monedas internacionales

### Mensajería

* Apache Kafka 3.7.0
* Zookeeper (incluido con Kafka)
* kafka-python

### Infraestructura

* Apache HTTP Server 2.4 (Windows)
* HTTPS con certificados SSL
* Entornos virtuales Python (venv)

---

## Requisitos Previos (OBLIGATORIOS)

⚠️ **Este proyecto no funciona únicamente con Python.**

Requiere software externo instalado manualmente.

### Software necesario

| Software           | Versión recomendada | URL de descarga                                                                              |
| ------------------ | ------------------- | -------------------------------------------------------------------------------------------- |
| Python             | 3.10 o superior     | [https://www.python.org/downloads/](https://www.python.org/downloads/)                       |
| Apache Kafka       | 3.7.0               | [https://archive.apache.org/dist/kafka/3.7.0/](https://archive.apache.org/dist/kafka/3.7.0/) |
| Zookeeper          | Incluido con Kafka  | [https://kafka.apache.org/downloads](https://kafka.apache.org/downloads)                     |
| Apache HTTP Server | 2.4                 | [https://httpd.apache.org/download.cgi](https://httpd.apache.org/download.cgi)               |
| Git                | Última versión      | [https://git-scm.com/downloads](https://git-scm.com/downloads)                               |

---

## Instalación del Proyecto

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/AC-E-D/Sistema-con-Microservicio-de-Monedas-Monitoreo-Kafka-y-Apache.git
cd Sistema-con-Microservicio-de-Monedas-Monitoreo-Kafka-y-Apache
```

---

## Configuración del Entorno Python

```bash
python -m venv env
```

### Activar entorno virtual

**Windows**

```bash
env\Scripts\activate
```

**Linux / macOS**

```bash
source env/bin/activate
```

---

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

---

## Configuración de Apache HTTP Server

Dentro del repositorio se incluye el archivo **`httpd.conf`** ya configurado para el proyecto.

### Pasos:

1. Instalar Apache HTTP Server 2.4
2. Ubicar la carpeta de instalación (por ejemplo: `C:\Apache24\`)
3. Copiar el archivo `httpd.conf` del proyecto
4. Reemplazar el archivo:

```text
Apache24\conf\httpd.conf
```

Este archivo ya contiene:

* Configuración HTTPS
* Rutas a certificados SSL
* Parámetros necesarios para el proyecto

---

## Configuración y Ejecución de Kafka

### 2️⃣ Iniciar Zookeeper

```powershell
C:\kafka\kafka_2.13-3.7.0> bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

### 3️⃣ Iniciar Kafka Broker

```powershell
C:\kafka\kafka_2.13-3.7.0> bin\windows\kafka-server-start.bat config\server.properties
```

---

## Ejecución del Microservicio de Monedas

Desde la carpeta del microservicio (evaluacion 3\microservicios\monedas_service):

```powershell
python main.py
```

Este proceso debe mantenerse ejecutándose.

---

## Ejecución del Backend Django

### Migraciones

```bash
python manage.py migrate
```
o
```bash
python3 manage.py migrate
```

### Iniciar servidor Django

```bash
python manage.py runserver 127.0.0.1:8000
```
o
```bash
python3 manage.py runserver 127.0.0.1:8000
```

---

## Acceso al Sistema

Una vez que todos los servicios estén ejecutándose correctamente, el cliente puede acceder al sistema desde un navegador web.

### URL del sistema (HTTPS)

```text
https://localhost/
```

### URL alternativa directa a Django (solo backend)

```text
http://127.0.0.1:8000/
```

### URL del Microservicio de Monedas

```text
http://127.0.0.1:8001/
```

---

## Credenciales de Acceso

El sistema ya incluye credenciales de prueba preconfiguradas:

* **Usuario:** Alex
* **Contraseña:** 12345678Aa

Estas credenciales permiten al cliente acceder al sistema sin configuraciones adicionales.

---

```bash
python manage.py migrate
```

### Iniciar servidor Django

```bash
python manage.py runserver 127.0.0.1:8000
```

---

## Ejecución de Apache

Desde la carpeta `bin` de Apache (\Apache24\bin):

```powershell
.\httpd.exe
```

---

## Orden Correcto de Ejecución

1. Apache HTTP Server
2. Zookeeper
3. Kafka Broker
4. Microservicio de Monedas
5. Backend Django

⚠️ Todos los procesos deben mantenerse activos simultáneamente.

---

## Notas Importantes

* El proyecto requiere **múltiples terminales abiertas**
* Cada servicio es independiente
* Si un proceso se detiene, la funcionalidad asociada deja de estar disponible
* El uso de HTTP puede generar advertencias por certificados autofirmados

---

## Autor

Proyecto desarrollado por **Alex Cuevas Danyau**
