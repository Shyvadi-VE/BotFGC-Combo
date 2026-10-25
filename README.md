# 🥊 combo_fgc

Proyecto backend desarrollado con **Python** y **Django 5.1**, preparado para producción y desarrollo con **PostgreSQL**, contenedorizado con **Docker** y **Docker Compose**.

---

## 🚀 Tecnologías

- **Lenguaje:** Python 3.13
- **Framework Web:** Django 5.1
- **Base de Datos:** PostgreSQL 16
- **Driver PostgreSQL:** `psycopg` (Versión 3, con binarios optimizados)
- **Variables de Entorno:** `python-dotenv` y `dj-database-url`
- **Contenedores:** Docker & Docker Compose

---

## 📁 Estructura del Proyecto

```text
Combo_FGC/
│
├── .venv/                   # Entorno virtual de Python (ignorado por Git)
├── combo_fgc/               # Módulo principal de configuración Django
│   ├── __init__.py
│   ├── asgi.py              # Configuración ASGI para async
│   ├── settings.py          # Configuración de Django (env, DB, estáticos)
│   ├── urls.py              # Enrutamiento de URLs
│   └── wsgi.py              # Configuración WSGI
│
├── static/                  # Archivos estáticos globales (CSS, JS, imágenes)
├── templates/               # Plantillas HTML globales
├── media/                   # Archivos subidos por usuarios (ignorado en Git)
│
├── .dockerignore            # Archivos excluidos de la imagen Docker
├── .env                     # Variables de entorno locales (NO subir a Git)
├── .env.example             # Plantilla de variables de entorno de ejemplo
├── .gitignore               # Archivos y carpetas ignorados por Git
├── Dockerfile               # Definición de la imagen del contenedor web
├── docker-compose.yml       # Orquestación de servicios (web + PostgreSQL)
├── manage.py                # CLI de administración de Django
├── README.md                # Documentación del proyecto
└── requirements.txt         # Dependencias del proyecto
```

---

## 🛠️ Puesta en Marcha

Tienes dos alternativas para ejecutar el proyecto:

### Opción 1: Con Docker y Docker Compose (Recomendado)

Esta opción levanta automáticamente tanto **PostgreSQL** como el servidor de **Django**, sin necesidad de tener PostgreSQL instalado en tu máquina.

1. **Asegúrate de tener Docker Desktop en ejecución**.
2. **Construye y levanta los servicios**:
   ```bash
   docker compose up --build
   ```
3. **Ejecutar migraciones en el contenedor**:
   ```bash
   docker compose exec web python manage.py migrate
   ```
4. **Crear un superusuario de administración**:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
5. Accede en tu navegador a:
   - Sitio web: [http://localhost:8000](http://localhost:8000)
   - Panel de Administración: [http://localhost:8000/admin](http://localhost:8000/admin)

Para detener los contenedores:
```bash
docker compose down
```

---

### Opción 2: Entorno Local con `.venv`

El entorno virtual ya se encuentra creado y configurado en `.venv/`.

1. **Activar el entorno virtual**:
   - **En Windows (PowerShell):**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **En Windows (CMD):**
     ```cmd
     .\.venv\Scripts\activate.bat
     ```
   - **En Linux / macOS / Git Bash:**
     ```bash
     source .venv/bin/activate
     ```

2. **Instalar o verificar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la base de datos**:
   Asegúrate de que en tu archivo `.env` estén los datos correctos de tu servidor local de PostgreSQL:
   ```env
   DB_NAME=combo_fgc_db
   DB_USER=postgres
   DB_PASSWORD=tu_password
   DB_HOST=localhost
   DB_PORT=5432
   ```
   *(Si PostgreSQL local no está activo o dejas las variables de DB vacías, el proyecto alternará temporalmente a SQLite para pruebas).*

4. **Aplicar migraciones**:
   ```bash
   python manage.py migrate
   ```

5. **Crear superusuario**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```
   El servidor responderá en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 🔐 Variables de Entorno (`.env`)

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `SECRET_KEY` | Clave secreta criptográfica de Django | Generada automáticamente |
| `DEBUG` | Activa modo depuración (`True`/`False`) | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos separados por comas | `localhost,127.0.0.1,0.0.0.0` |
| `DB_NAME` | Nombre de la base de datos PostgreSQL | `combo_fgc_db` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `postgres` |
| `DB_HOST` | Host de PostgreSQL (`localhost` o `db` en docker) | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DATABASE_URL` | *(Opcional)* URL de conexión completa | `postgres://user:pass@host:5432/dbname` |

---

## ⚙️ Comandos Útiles de Django

- **Crear una nueva aplicación:**
  ```bash
  python manage.py startapp <nombre_de_app>
  ```
- **Crear nuevas migraciones tras modificar modelos:**
  ```bash
  python manage.py makemigrations
  ```
- **Aplicar migraciones pendientes:**
  ```bash
  python manage.py migrate
  ```
- **Recolectar archivos estáticos para producción:**
  ```bash
  python manage.py collectstatic
  ```
- **Ejecutar tests:**
  ```bash
  python manage.py test
  ```
