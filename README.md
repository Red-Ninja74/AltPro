# AltPro – Alta de Proyectos

Aplicación web hecha con [Streamlit](https://streamlit.io/) para revisar y aprobar las **altas de proyecto** de los grupos estudiantiles. Lee el archivo Excel del alta, muestra su información para revisarla y, al aprobarla, la guarda en una hoja de **Google Sheets** que funciona como base de datos. Con esos datos la app muestra un calendario de eventos, estadísticas por grupo y un reporte en PDF.

---

## Contenido

1. [Funciones de la app](#funciones-de-la-app)
2. [Estructura del proyecto](#estructura-del-proyecto)
3. [Instalación y ejecución local](#instalación-y-ejecución-local)
4. [Configuración (`secrets.toml`)](#configuración-secretstoml)
5. [Base de datos: hoja EVENTOS](#base-de-datos-hoja-eventos)
6. [Cómo se lee el Excel del alta](#cómo-se-lee-el-excel-del-alta)
7. [IDs y giros de los grupos](#ids-y-giros-de-los-grupos)
8. [Caché y límite de Google Sheets](#caché-y-límite-de-google-sheets)
9. [Publicar en Streamlit Cloud](#publicar-en-streamlit-cloud)
10. [Pendientes conocidos](#pendientes-conocidos)

---

## Funciones de la app

### 🔐 Inicio de sesión
Al abrir la app se pide usuario y contraseña. Se validan contra la sección `[usuarios]` de `secrets.toml` (ver [Configuración](#configuración-secretstoml)). La sesión se guarda en `st.session_state` y se cierra con el botón **Cerrar Sesión** del menú lateral.

### 🧭 Menú lateral
- **Navegación:** 🏠 Inicio, 📂 AltPro y 📊 Estadísticas.
- **🔄 Actualizar datos:** borra la caché y vuelve a leer Google Sheets. Úsalo si alguien editó la hoja a mano y quieres ver el cambio de inmediato (ver [Caché](#caché-y-límite-de-google-sheets)).
- **Cerrar Sesión.**

### 🏠 Inicio – Calendario de eventos
Muestra un calendario mensual (en español, la semana empieza en lunes) con todos los eventos registrados en la hoja EVENTOS.
- Cada evento se pinta con el color del **giro** de su grupo (ver `COLORES_CATEGORIA` en `config.py`).
- Los textos largos se ven completos; los días crecen si tienen varios eventos.
- Al dar click en un evento aparece debajo un recuadro con su **título, grupo, lugar y fecha**.
- Hay vista de **Mes** y de **Lista**.
- Las filas con la fecha vacía o mal escrita no aparecen en el calendario.

### 📂 AltPro – Carga y aprobación de proyectos
1. Se sube el Excel del alta (`.xlsx` / `.xls`).
2. La app lo lee y muestra la información en cuatro pestañas:
   - **Información General:** grupo, nombre del proyecto, lugar, fechas y horas, además del **ID del grupo**, que se asigna automáticamente con `CATALOGO_IDS`. Si el grupo no está en el catálogo se usa `HID-DES-000`.
   - **Personas Involucradas.**
   - **Lugares Registrados:** valida cuántos lugares se pidieron y avisa si hay un error (ver [abajo](#cómo-se-lee-el-excel-del-alta)).
   - **Materiales de Bodega.**
3. El botón **✅ Aprobar y Guardar en Base de Datos** agrega una fila nueva a la hoja EVENTOS y limpia la caché para que el evento aparezca al instante en Inicio y Estadísticas.

### 📊 Estadísticas
- **Métricas:** total de proyectos registrados y el grupo con más eventos.
- **Gráfica "Eventos por Grupo"** (Plotly): barras de mayor a menor con degradado azul.
- **Configuración de Reporte:** opciones para un reporte general o personalizado (por giro, por grupo y por rango de fechas). *Las opciones todavía no cambian el contenido del PDF; ver [Pendientes](#pendientes-conocidos).* Esta sección está dentro de un `@st.fragment`, así que al mover sus opciones solo se vuelve a ejecutar esa parte de la página.
- **Descargar reporte:** descarga `Reporte_Gestion.pdf`.

### 📄 Reporte PDF
Lo genera `reporte_pdf.py` con **reportlab**, directamente en memoria (no se guarda ningún archivo en el servidor). Contiene:
1. **Grupos Estudiantiles:** todos los grupos del catálogo, agrupados por giro y acomodados en 3 columnas para que quepan en una página. Los nombres se escriben como "Leader Hub"; las siglas (definidas en `SIGLAS_GRUPOS`) se quedan en mayúsculas.
2. **Estadísticas → Resumen general:** la gráfica de eventos por grupo. Es una copia del diseño de la gráfica de la página, dibujada con reportlab (no usa Plotly, para no necesitar Chrome en el servidor). **Si cambias el diseño de una, cambia también la otra** (`grafica_eventos_por_grupo()` en `reporte_pdf.py`).
3. Secciones por giro (por ahora solo los títulos).

---

## Estructura del proyecto

```
AltPro/
├── README.md
├── .gitignore
├── .devcontainer/devcontainer.json   ← configuración para GitHub Codespaces
├── Archivo/leerArchivo.py            ← versión vieja del lector de Excel (ya no se usa)
└── main/
    ├── app.py              ← PUNTO DE ENTRADA: configuración de la página, login, menú lateral y navegación
    ├── config.py           ← catálogo de IDs, nombres de giros, siglas y colores
    ├── db_manager.py       ← clase BaseDatos_GE: leer y escribir en Google Sheets
    ├── consultas.py        ← cálculos sobre los datos (totales, ranking, eventos del calendario)
    ├── lector_excel.py     ← clase LectorProyectosExcel: lee el Excel del alta
    ├── reporte_pdf.py      ← genera el reporte PDF
    ├── requirements.txt    ← librerías necesarias
    ├── main.py             ← archivo de prueba, no lo usa la app
    └── paginas/
        ├── login.py        ← pantalla de inicio de sesión
        ├── inicio.py       ← bienvenida + calendario
        ├── altpro.py       ← carga y aprobación del Excel
        └── estadisticas.py ← métricas, gráfica y descarga del reporte
```

### Cómo se conectan las piezas

```
app.py
 ├─ paginas/login.py
 ├─ paginas/inicio.py ──────────► consultas.cargar_eventos() ─► db_manager (Google Sheets)
 │                                consultas.obtener_eventos_calendario(df)
 ├─ paginas/altpro.py ──────────► lector_excel.LectorProyectosExcel
 │                                db_manager.registrar_datos()
 └─ paginas/estadisticas.py ◄──── app.py lee la hoja UNA vez y calcula:
        │                         obtener_total_proyectos(df)
        │                         obtener_grupo_mas_eventos(df)
        │                         obtener_numero_eventos_grupos(df)
        └─► reporte_pdf.py (recibe los datos ya calculados)
```

Reglas que sigue el código:
- **Lógica de datos en `consultas.py`, interfaz en `paginas/`.** Si cambia el formato de la hoja, se toca `consultas.py`; si cambia el diseño, se tocan las páginas.
- **La hoja se lee una sola vez por página** con `cargar_eventos()`, y ese `df` se pasa a las funciones que lo necesitan. No llames `BaseDatos_GE(...).obtener_datos()` dentro de cada función: cada lectura cuenta contra el límite de Google.
- Datos fijos (catálogos, colores) van en `config.py`.

---

## Instalación y ejecución local

Requisitos: **Python 3.11 o superior**.

```bash
# 1. Clonar el repositorio
git clone https://github.com/Red-Ninja74/AltPro.git
cd AltPro

# 2. Instalar las librerías
pip install -r main/requirements.txt

# 3. Crear el archivo de configuración (ver la siguiente sección)
#    main/.streamlit/secrets.toml   o   .streamlit/secrets.toml

# 4. Ejecutar
streamlit run main/app.py
```

La app se abre en `http://localhost:8501`.

> **Windows:** si aparece un error de `pyarrow` del tipo *"An Application Control policy has blocked this file"*, Windows (Smart App Control o el antivirus) está bloqueando la librería. Sin ella fallan el calendario y las tablas. Prueba `pip install --force-reinstall pyarrow` o permite el archivo en Seguridad de Windows. En Streamlit Cloud no pasa.

---

## Configuración (`secrets.toml`)

La app necesita un archivo `secrets.toml` con dos secciones. **Nunca lo subas a GitHub** (ya está en `.gitignore`). En Streamlit Cloud el mismo contenido se pega en *App settings → Secrets*.

```toml
# Usuarios que pueden entrar a la app:  usuario = "contraseña"
[usuarios]
admin = "una-contraseña-segura"
otro_usuario = "otra-contraseña"

# Conexión a Google Sheets (cuenta de servicio de Google Cloud)
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/ID_DE_LA_HOJA/edit"
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "...@....iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

Los valores de `[connections.gsheets]` salen del archivo JSON de la cuenta de servicio en Google Cloud. La hoja de cálculo debe estar **compartida con el `client_email`** de esa cuenta con permiso de edición. Más detalles en la documentación de [st-gsheets-connection](https://github.com/streamlit/gsheets-connection).

---

## Base de datos: hoja EVENTOS

Todos los datos viven en la pestaña **EVENTOS** del Google Sheets. Cada fila es un evento aprobado. El código lee las columnas **por posición**, así que **no cambies el orden de las columnas**:

| Col. | Letra | Contenido | Ejemplo | Se usa en |
|---|---|---|---|---|
| 0 | A | ID del grupo (XXX-YYY-ZZZ) | `HID-ASE-ING` | Contar eventos por grupo, color del calendario |
| 1 | B | Nombre del grupo | `SEING` | Nombre en estadísticas y calendario |
| 2 | C | Nombre del evento | `Rally de Ingeniería` | Título en el calendario |
| 3 | D | Fecha | `18/9/2026` (día/mes/año) | Calendario |
| 4 | E | Lugar | `Auditorio` | Detalle del evento en el calendario |
| 5–8 | F–I | Personas, Huella de Carbono, Duración en horas, Link evidencias | | Todavía no se usan |

**¿Por qué se cuenta por ID y no por nombre?** El nombre puede venir con errores ("SEING" vs "SEiNG"); el ID no. Para mostrar el nombre de un grupo, la app toma el nombre que **más se repite** entre las filas de ese ID, así un error ocasional no afecta.

---

## Cómo se lee el Excel del alta

`lector_excel.py` busca estas pestañas (sin importar mayúsculas ni espacios extra al inicio/final):

| Pestaña | Qué se lee |
|---|---|
| **Alta de proyecto** | Grupo (E6), nombre del proyecto (E7), lugar (E8), fechas de inicio/término (C9, C10) y horas de inicio/término (G9, G10) |
| **PERSONAS** | Nombres en la columna A a partir de la fila 7, hasta la primera celda vacía |
| **LUGARES** | Materiales solicitados por lugar y materiales de Planta Física |
| **MATERIAL** | Materiales de bodega a partir de la fila 8: material, cantidad, observaciones y solicitados |

### Validación de lugares
Cada lugar del formato tiene un rango de filas. Si alguna celda de "solicitados/comentarios" (columnas I–J) de ese rango tiene datos, el lugar cuenta como solicitado:
- **Interior** (SADCO, Arte, Comedor Ejecutivo, Aulas, Terraza LiFE) suma **2**.
- **Exterior** (Explanada LiFE, Explanada CIT, Jardín CE frente, Jardín CE) suma **1**.

| Suma | Mensaje |
|---|---|
| 0 | No hay lugares registrados |
| 1 | Un lugar al aire libre ✅ |
| 2 | Un lugar en interior ✅ |
| 3 | Un interior y un exterior ✅ |
| otra | ⚠️ Error: más de dos lugares, revisar manualmente |

> Si cambia el formato del Excel (filas o columnas), hay que actualizar las posiciones en `lector_excel.py`.

---

## IDs y giros de los grupos

El ID tiene la forma `HID-GIRO-GRUPO`, por ejemplo `HID-ASE-ING`. La parte central es el **giro**:

| Código | Giro |
|---|---|
| ACE | Arte, Cultura y Entretenimiento |
| DYR | Deportivos y Recreativos |
| EMA | Ecología y Medio Ambiente |
| LID | Liderazgo |
| SYB | Salud y Bienestar |
| SHE | Sentido Humano y E. Social |
| VAC | Vinculación Académica |
| ASE | Asociaciones Estudiantiles |
| FTC | FETEC |

**Para agregar un grupo nuevo**, edita `main/config.py`:
1. Agrégalo a `CATALOGO_IDS` con su nombre **en mayúsculas**, tal como viene en el Excel del alta. Si el nombre lleva acentos, agrega también la versión sin acentos con el mismo ID.
2. Si su nombre son siglas, agrégalo a `SIGLAS_GRUPOS` para que en el reporte no se escriba como "Seing".

Con eso aparece automáticamente en el ID del alta, en el calendario (con el color de su giro) y en la lista del reporte PDF.

---

## Caché y límite de Google Sheets

Google permite **60 lecturas por minuto** por cuenta de servicio, **compartidas entre todos los usuarios** de la app. Streamlit vuelve a ejecutar todo el script cada vez que alguien toca un botón o una opción, así que sin cuidado ese límite se acaba rápido (error `429 RESOURCE_EXHAUSTED`).

Para evitarlo:
- **Caché de 5 minutos:** `obtener_datos()` reutiliza la última lectura durante `TTL_CACHE_SEGUNDOS = 300` segundos (en `db_manager.py`).
- **Una lectura por página:** `cargar_eventos()` lee una vez y los cálculos reciben ese `df`.
- **`@st.fragment`** en la configuración del reporte: mover sus opciones no vuelve a ejecutar toda la página.
- **Al guardar** (`registrar_datos`) se lee la hoja **sin caché**, para no borrar filas que otra persona haya agregado, y después se limpia la caché.

**Consecuencia:** si alguien edita la hoja **a mano** en Google Sheets, el cambio puede tardar hasta 5 minutos en verse. Para verlo al instante, usa **🔄 Actualizar datos** en el menú lateral.

---

## Publicar en Streamlit Cloud

1. Sube el código a GitHub (sin `secrets.toml`).
2. En [share.streamlit.io](https://share.streamlit.io) crea una app con:
   - **Repositorio:** `Red-Ninja74/AltPro`
   - **Branch:** `main`
   - **Main file path:** `main/app.py`
3. En *Advanced settings → Secrets* pega el contenido de tu `secrets.toml`.
4. Las librerías se instalan desde `main/requirements.txt`. Si agregas una librería nueva al código, **agrégala ahí**.

Si algo falla, los errores completos aparecen en *Manage app → logs*.

---

## Pendientes conocidos

- **Opciones del reporte personalizado:** los filtros por giro, grupo y fechas se muestran pero todavía no cambian el PDF. La lista de grupos del multiselect tiene valores de prueba (`1…10`).
- **Secciones por giro del PDF:** por ahora solo tienen el título.
- **Métrica "Promedio por Grupo":** dice "En desarrollo…".
- **Formato de la fecha al aprobar:** el botón de AltPro guarda la fecha como texto tal como la lee del Excel. Si la celda del Excel es una fecha real, se guarda como `2026-09-18 00:00:00` y **no aparecerá en el calendario**, que espera `18/9/2026`.
- **`use_container_width`:** Streamlit avisa que dejará de existir; hay que cambiarlo por `width="stretch"`.
- **Codespaces:** `.devcontainer/devcontainer.json` instala `requirements.txt` desde la raíz del repo, pero el archivo está en `main/requirements.txt`, así que en Codespaces las librerías no se instalan solas.
- **Archivos sin uso:** `Archivo/leerArchivo.py` y `main/main.py`.
- **`__pycache__`:** algunos archivos `.pyc` se subieron a git antes de crear el `.gitignore`. Para dejar de rastrearlos: `git rm -r --cached main/__pycache__ main/paginas/__pycache__`.
