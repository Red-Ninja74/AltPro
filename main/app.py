import pandas as pd
import plotly.express as px
import streamlit as st
from db_manager import BaseDatos_GE
from streamlit_extras.metric_cards import style_metric_cards

# ==========================================
# CATÁLOGO DE IDs POR GRUPO ESTUDIANTIL
# ==========================================
CATALOGO_IDS = {
    # 🎨 Arte, Cultura y Entretenimiento
    "ART AT TEC": "HID-ACE-AAT",
    "BLOOM CRAFT STUDIO": "HID-ACE-BCS",
    "CINEPHORIA": "HID-ACE-CNP",

    # 🏃 Deportivos y Recreativos
    "COURT CLUB": "HID-DYR-CCL",
    "MONKLIMB": "HID-DYR-MKL",

    # 🌱 Ecología y Medio Ambiente
    "GREEN CREW": "HID-EMA-GCR",

    # 🚀 Liderazgo
    "ALMA": "HID-LID-ALM",
    "CARNERO": "HID-LID-CRN",
    "KREI": "HID-LID-KRE",
    "LASOS": "HID-LID-LAS",
    "LEADER HUB": "HID-LID-LHB",
    "NOVA": "HID-LID-NOV",
    "REVO": "HID-LID-RVO",
    "START A NEW LIFE": "HID-LID-SNL",

    # 🧘 Salud y Bienestar
    "BECOMING": "HID-SYB-BCM",
    "CLOUD": "HID-SYB-CLD",
    "ZENIT": "HID-SYB-ZNT",

    # ❤️ Sentido Humano y E. Social
    "CLICKED": "HID-SHE-CLK",
    "CORAZÓN EN ACCIÓN": "HID-SHE-CEA",
    "CORAZON EN ACCION": "HID-SHE-CEA",
    "ORIX": "HID-SHE-ORX",
    "VOLUNTAD COMPARTIDA": "HID-SHE-VCO",

    # 🎓 Vinculación Académica
    "BEETRONIX": "HID-VAC-BTX",
    "KEYBOT": "HID-VAC-KBT",
    "NÉBULA": "HID-VAC-NEB",
    "NEBULA": "HID-VAC-NEB",
    "NEHS": "HID-VAC-NHS",
    "STEAM": "HID-VAC-STM",
    "TOASTMASTERS": "HID-VAC-TMS",
    "TEC RACING": "HID-VAC-TRA",
    "VOICES": "HID-VAC-VOC",

    # 🏛️ Asociaciones Estudiantiles
    "SEAAD": "HID-ASE-AAD",
    "SEART": "HID-ASE-ART",
    "SECSG": "HID-ASE-CSG",
    "SEING": "HID-ASE-ING",
    "SELAET": "HID-ASE-LAE",
    "SELCPF": "HID-ASE-CPF",
    "SENEG": "HID-ASE-NEG",

    # 🔵 FETEC
    "CVIG": "HID-FTC-VIG",
    "CRS": "HID-FTC-CRS",
    "CPE": "HID-FTC-CPE",
    "SEPREPA": "HID-FTC-PRE",
    "TRIBUNAL": "HID-FTC-TRB",
    "COMITÉ EJECUTIVO": "HID-FTC-CEJ",
    "COMITE EJECUTIVO": "HID-FTC-CEJ",
}

# ==========================================
# CONFIGURACIÓN DE PÁGINA STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Alta de Proyectos",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# CLASE DE LECTURA DE EXCEL
# ==========================================
class LectorProyectosExcel:

    def __init__(self, archivo_subido):
        self.archivo = archivo_subido
        self.xls = pd.ExcelFile(archivo_subido)

    def _leer_pestana(self, nombre_pestana):
        # Normaliza búsquedas ignorando espacios extra y mayúsculas
        nombres_reales = self.xls.sheet_names
        coincidencia = next(
            (
                n
                for n in nombres_reales
                if n.strip().lower() == nombre_pestana.strip().lower()
            ),
            None,
        )
        if coincidencia:
            # Corrección: parsear usando el objeto ExcelFile ya abierto
            return self.xls.parse(sheet_name=coincidencia, header=None)
        raise ValueError(
            f"No se encontró la pestaña '{nombre_pestana}' en el archivo."
        )

    def leer_Alta_de_Proyecto(self):
        df = self._leer_pestana("Alta de proyecto")

        def safe_get(r, c):
            try:
                val = df.iloc[r, c]
                return "" if pd.isna(val) else str(val).strip()
            except IndexError:
                return ""

        return {
            "Grupo Estudiantil": safe_get(5, 4),
            "Nombre de Proyecto": safe_get(6, 4),
            "Lugar": safe_get(7, 4),
            "Fecha de inicio": safe_get(8, 2),
            "Fecha de termino": safe_get(9, 2),
            "Hora de inicio": safe_get(8, 6),
            "Hora de termino": safe_get(9, 6),
        }

    def leer_Personas(self):
        df = self._leer_pestana("PERSONAS")
        nombres = []
        fila = 6

        while fila < len(df):
            val = df.iloc[fila, 0]
            if pd.isna(val) or str(val).strip() == "":
                break
            nombres.append(val)
            fila += 1

        return pd.DataFrame({"Nombre": nombres})

    def leer_Lugares(self):
        df = self._leer_pestana("LUGARES")

        materiales_lugar, solicitados_lugar, comentarios_lugar = [], [], []
        (
            materiales_planta,
            observaciones_planta,
            lugar_planta,
            solicitados_planta,
            comentarios_planta,
        ) = ([], [], [], [], [])

        def safe_val(r, c):
            try:
                val = df.iloc[r, c]
                return val if pd.notna(val) else ""
            except IndexError:
                return ""

        def procesar_lugar(rango_inicio, rango_fin):
            for fila in range(rango_inicio, rango_fin):
                materiales_lugar.append(safe_val(fila, 0))
                solicitados_lugar.append(safe_val(fila, 8))
                comentarios_lugar.append(safe_val(fila, 9))

        def check_rango(r1, r2, c1, c2):
            try:
                sub = df.iloc[r1:r2, c1:c2].replace(r"^\s*$", pd.NA, regex=True)
                return not sub.isna().all().all()
            except Exception:
                return False

        SADCO = 2 if check_rango(9, 18, 8, 10) else 0
        if SADCO:
            procesar_lugar(9, 18)

        ARTE = 2 if check_rango(25, 34, 8, 10) else 0
        if ARTE:
            procesar_lugar(25, 34)

        Comedor_Ejecutivo = 2 if check_rango(41, 47, 8, 10) else 0
        if Comedor_Ejecutivo:
            procesar_lugar(41, 47)

        Aulas = 2 if check_rango(54, 57, 8, 10) else 0
        if Aulas:
            procesar_lugar(54, 57)

        Explanada_LiFE = 1 if check_rango(64, 67, 8, 10) else 0
        if Explanada_LiFE:
            procesar_lugar(64, 67)

        Explanada_CIT = 1 if check_rango(73, 76, 8, 10) else 0
        if Explanada_CIT:
            procesar_lugar(73, 76)

        Jardin_CE_frente = 1 if check_rango(82, 87, 8, 10) else 0
        if Jardin_CE_frente:
            procesar_lugar(82, 87)

        Jardin_CE = 1 if check_rango(93, 97, 8, 10) else 0
        if Jardin_CE:
            procesar_lugar(93, 97)

        Terraza_LiFE = 2 if check_rango(103, 106, 8, 10) else 0
        if Terraza_LiFE:
            procesar_lugar(103, 106)

        for fila in range(9, min(31, len(df))):
            materiales_planta.append(safe_val(fila, 11))
            observaciones_planta.append(safe_val(fila, 18))
            lugar_planta.append(safe_val(fila, 19))
            solicitados_planta.append(safe_val(fila, 20))
            comentarios_planta.append(safe_val(fila, 21))

        z = sum([
            SADCO,
            ARTE,
            Comedor_Ejecutivo,
            Aulas,
            Explanada_LiFE,
            Explanada_CIT,
            Jardin_CE_frente,
            Jardin_CE,
            Terraza_LiFE,
        ])

        df_lugares = pd.DataFrame({
            "Materiales/Equipo": materiales_lugar,
            "Solicitados": solicitados_lugar,
            "Comentarios": comentarios_lugar,
        })
        df_planta = pd.DataFrame({
            "Materiales/Equipo": materiales_planta,
            "Observaciones": observaciones_planta,
            "Lugar Solicitado": lugar_planta,
            "Solicitados": solicitados_planta,
            "Comentarios": comentarios_planta,
        })

        if not df_lugares.empty and "Solicitados" in df_lugares:
            df_lugares = df_lugares[
                df_lugares["Solicitados"].astype(str).str.strip() != ""
            ]
        if not df_planta.empty and "Lugar Solicitado" in df_planta:
            df_planta = df_planta[
                (df_planta["Lugar Solicitado"].astype(str).str.strip() != "")
                & (df_planta["Solicitados"].astype(str).str.strip() != "")
            ]

        return {
            "Lugares registrados": z,
            "df_lugares": df_lugares,
            "df_planta": df_planta,
        }

    def leer_Materiales(self):
        df = self._leer_pestana("MATERIAL")
        mat, cant, obs, sol = [], [], [], []
        fila = 7

        def safe_val(r, c):
            try:
                val = df.iloc[r, c]
                return val if pd.notna(val) else ""
            except IndexError:
                return ""

        while fila < len(df):
            material = safe_val(fila, 0)
            if str(material).strip() == "":
                break

            mat.append(material)
            cant.append(safe_val(fila, 3))
            obs.append(safe_val(fila, 4))
            sol.append(safe_val(fila, 7))
            fila += 1

        df_mat = pd.DataFrame({
            "Materiales/Equipo": mat,
            "Cantidad": cant,
            "Observaciones": obs,
            "Solicitados": sol,
        })
        return df_mat.dropna(subset=["Materiales/Equipo"]).reset_index(
            drop=True
        )


def obtener_total_proyectos():
    db = BaseDatos_GE(nombre_hoja="EVENTOS")
    df = db.obtener_datos()
    return len(df)  

def obtener_grupo_mas_eventos():
    db = BaseDatos_GE(nombre_hoja="EVENTOS")
    df = db.obtener_datos()
    if df.empty:
        return ("Sin datos", 0)
    conteo = df.iloc[:, 0].value_counts()
    matricula = conteo.idxmax()
    num_eventos = conteo.max()
    nombres = df[df.iloc[:, 0] == matricula].iloc[:, 1]
    nombre = nombres.value_counts().idxmax()
    return (nombre, num_eventos)

def obtener_numero_eventos_grupos():
    db = BaseDatos_GE(nombre_hoja="EVENTOS")
    df = db.obtener_datos()
    if df.empty:
        return pd.DataFrame(columns=["Grupo", "Eventos"])
    col_matricula = df.columns[0]
    col_nombre = df.columns[1]
    resumen = df.groupby(col_matricula).agg(
        Grupo=(col_nombre, lambda nombres: nombres.value_counts().idxmax()),
        Eventos=(col_nombre, "size"),
    )
    return resumen.sort_values("Eventos", ascending=False).reset_index(drop=True)

# ==========================================
# FUNCIONES DE INTERFAZ
# ==========================================
def mostrar_login():
    st.title("Iniciar Sesión")
    st.markdown("Por favor, ingresa tus credenciales para acceder al sistema.")

    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            if "usuarios" in st.secrets:
                diccionario_usuarios = st.secrets["usuarios"]
                if (
                    usuario in diccionario_usuarios
                    and password == diccionario_usuarios[usuario]
                ):
                    st.session_state["logeado"] = True
                    st.session_state["usuario_actual"] = usuario
                    st.success(f"¡Bienvenido, {usuario}!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
            else:
                st.error(
                    "⚠️ No se encontró la configuración de usuarios"
                    " ('secrets.toml'). Por favor configúrala."
                )


def mostrar_altpro():
    st.title("AltPro - Carga de Proyectos")
    st.markdown(
        "Sube el archivo **Excel (.xlsx)** del proyecto para leerlo y"
        " aprobarlo."
    )

    archivo_subido = st.file_uploader(
        "Arrastra aquí el archivo Excel", type=["xlsx", "xls"]
    )

    if archivo_subido is None:
        st.info("👆 Por favor sube un archivo Excel para mostrar los datos.")
        return

    st.success("Archivo cargado correctamente. Procesando datos...")

    try:
        lector = LectorProyectosExcel(archivo_subido)

        alt = lector.leer_Alta_de_Proyecto()
        df_personas = lector.leer_Personas()
        lugares_data = lector.leer_Lugares()
        df_materiales = lector.leer_Materiales()

        # Asignación automática del ID a partir del grupo
        nombre_grupo = alt.get("Grupo Estudiantil", "").strip()
        id_grupo = CATALOGO_IDS.get(nombre_grupo.upper(), "HID-DES-000")

        tab1, tab2, tab3, tab4 = st.tabs([
            "Información General",
            "Personas Involucradas",
            "Lugares Registrados",
            "Materiales de Bodega",
        ])

        with tab1:
            st.subheader("Datos del Proyecto")
            col1, col2 = st.columns(2)

            # Mostrar el ID asignado en pantalla
            col1.metric(label="ID del Grupo", value=id_grupo)

            for i, (clave, valor) in enumerate(alt.items()):
                if i % 2 == 0:
                    col2.metric(label=clave, value=str(valor))
                else:
                    col1.metric(label=clave, value=str(valor))

        with tab2:
            st.subheader("Personas Involucradas")
            st.dataframe(df_personas, use_container_width=True)

        with tab3:
            st.subheader("Estado de Lugares")
            z = lugares_data["Lugares registrados"]

            if z == 0:
                st.info(
                    "No hay materiales registrados en ninguno de los lugares"
                    " del Alta."
                )
            elif z == 1:
                st.success(
                    "Hay un lugar registrado al aire libre. No hay errores en"
                    " el alta."
                )
            elif z == 2:
                st.success(
                    "Hay un lugar registrado en interior. No hay errores en el"
                    " alta."
                )
            elif z == 3:
                st.success(
                    "Hay un lugar registrado en interior y uno en exterior. No"
                    " hay errores en el alta."
                )
            else:
                st.error(
                    "⚠️ Hay un error en el alta. Hay más de dos lugares"
                    " registrados. Revisar manualmente."
                )

            st.markdown("### Materiales por Lugar")
            st.dataframe(lugares_data["df_lugares"], use_container_width=True)

            st.markdown("### Materiales de Planta Física")
            st.dataframe(lugares_data["df_planta"], use_container_width=True)

        with tab4:
            st.subheader("Materiales y Equipos")
            st.dataframe(df_materiales, use_container_width=True)

        st.divider()
        st.markdown("### ¿La información es correcta?")

        if st.button(
            "✅ Aprobar y Guardar en Base de Datos", use_container_width=True
        ):
            with st.spinner("Guardando en Google Sheets..."):
                datos_evento = {
                    "ID del grupo (XXX-YYY-ZZZ)": id_grupo,
                    "Nombre del Grupo": alt.get("Grupo Estudiantil", ""),
                    "Nombre del Evento": alt.get("Nombre de Proyecto", ""),
                    "Fecha": str(alt.get("Fecha de inicio", "")),
                    "Lugar": alt.get("Lugar", ""),
                    "Personas": "",
                    "Huella de Carbono": "",
                    "Duración en horas": "",
                    "Link evidencias": "",
                }

                db = BaseDatos_GE(nombre_hoja="EVENTOS")
                exito = db.registrar_datos(datos_evento)

                if exito:
                    st.success("¡Datos aprobados y guardados con éxito en la Base de Datos!")
                    st.balloons()

    except Exception as e:
        st.error(f"Error al leer el documento: {e}")


import streamlit as st
import plotly.express as px


def mostrar_estadisticas(total_proyectos, grupo_mas_eventos, eventos_por_grupo):
    st.title("Estadísticas")
    
    # 1. MÉTRICAS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total de Proyectos Registrados", value=total_proyectos)

    with col2:
        st.metric(
            label="Grupo con más eventos", 
            value=str(grupo_mas_eventos[0]), 
            delta=f"{grupo_mas_eventos[1]} eventos",
            delta_color="normal"
        )
    with col3:
        st.metric(
            label="Promedio por Grupo", 
            value="En desarrollo...", 
            delta="Proyectos activos"
        )

    style_metric_cards(
        background_color="#F8FAFC",  
        border_size_px=1,            
        border_color="#E2E8F0",      
        border_radius_px=12,         
        border_left_color="#2563EB", 
        box_shadow=True
    )

    st.write("") # Espaciador visual

    # 2. GRÁFICA ESTILIZADA EN UN CONTENEDOR
    with st.container(border=True):
        st.subheader("📊 Eventos por Grupo")
        
        # Generar gráfico base
        fig = px.bar(
            eventos_por_grupo, 
            x="Grupo", 
            y="Eventos", 
            text="Eventos"
        )
        
        # Estilo de las barras (color azul a juego con las métricas y esquinas redondeadas)
        fig.update_traces(
            marker_color="#2563EB",            # Azul moderno matching con border_left_color
            marker_pattern_shape="",           # Sin patrones interrumpiendo el color
            textposition="outside",            # Muestra el número sobre la barra
            textfont=dict(size=13, weight="bold"),
            cliponaxis=False                   # Evita que el texto superior se corte
        )
        
        # Estilo del layout general (sin rejillas molestas, fondo transparente)
        fig.update_layout(
            xaxis={"categoryorder": "total descending", "title": ""}, # Ordenar y quitar etiqueta sobrante
            yaxis_title="Cantidad de Eventos",
            plot_bgcolor="rgba(0,0,0,0)",      # Fondo transparente
            paper_bgcolor="rgba(0,0,0,0)",     # Fondo de papel transparente
            margin=dict(l=20, r=20, t=30, b=20), # Márgenes limpios
            font=dict(family="Inter, sans-serif", size=13, color="#64748B"), # Tipografía limpia
            yaxis=dict(
                showgrid=True, 
                gridcolor="#F1F5F9",            # Líneas de guía muy suaves
                zeroline=False
            )
        )
        
        # Renderizar en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    st.write("") # Espaciador visual

    # 3. BOTÓN DE DESCARGA
    if st.button("Descargar reporte", use_container_width=True):
        st.success("Reporte descargado con éxito!")
        st.balloons()

# ==========================================
# FLUJO PRINCIPAL DE LA APP
# ==========================================
def main():
    if "logeado" not in st.session_state:
        st.session_state["logeado"] = False

    if not st.session_state["logeado"]:
        mostrar_login()
    else:
        st.sidebar.image(
            "https://cdn-icons-png.flaticon.com/512/1055/1055664.png", width=100
        )
        st.sidebar.title("Menú Principal")
        st.sidebar.write(
            f"**Usuario:** {st.session_state.get('usuario_actual', '')}"
        )
        st.sidebar.divider()

        opcion = st.sidebar.radio(
            "Navegación:", ["🏠 Inicio", "📂 AltPro", "📊 Estadísticas"]
        )

        st.sidebar.divider()
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state["logeado"] = False
            st.session_state["usuario_actual"] = None
            st.rerun()

        if opcion == "🏠 Inicio":
            st.title("Bienvenido al Sistema")
            st.write(
                f"Hola **{st.session_state.get('usuario_actual', '')}**."
                " Selecciona **AltPro** en el menú de la izquierda para"
                " comenzar."
            )
        elif opcion == "📂 AltPro":
            mostrar_altpro()
        elif opcion == "📊 Estadísticas":
            total_proyectos = obtener_total_proyectos()
            grupo_mas_eventos = obtener_grupo_mas_eventos()
            eventos_por_grupo = obtener_numero_eventos_grupos()
            mostrar_estadisticas(total_proyectos, grupo_mas_eventos, eventos_por_grupo)

if __name__ == "__main__":
    main()