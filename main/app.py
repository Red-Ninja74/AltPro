import streamlit as st
import pandas as pd

# ==========================================
# CONFIGURACIÓN DE PÁGINA STREAMLIT
# ==========================================
st.set_page_config(page_title="Alta de Proyectos", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# CLASE DE LECTURA 
# ==========================================
class LectorProyectosExcel:
    def __init__(self, archivo_subido):
        self.archivo = archivo_subido
    
    def _leer_pestana(self, nombre_pestana):
        return pd.read_excel(self.archivo, sheet_name=nombre_pestana, header=None)

    def leer_Alta_de_Proyecto(self):
        df = self._leer_pestana("Alta de proyecto")
        alta = {
            "Grupo Estudiantil": df.iloc[5, 4], 
            "Nombre de Proyecto": df.iloc[6, 4],
            "Lugar": df.iloc[7, 4],
            "Fecha de inicio": df.iloc[8, 2],
            "Fecha de termino": df.iloc[9, 2],
            "Hora de inicio": df.iloc[8, 6],
            "Hora de termino": df.iloc[9, 6]
        }
        return alta
    
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
        materiales_planta, observaciones_planta, lugar_planta, solicitados_planta, comentarios_planta = [], [], [], [], []
                
        def procesar_lugar(rango_inicio, rango_fin):
            for fila in range(rango_inicio, rango_fin):
                materiales_lugar.append(df.iloc[fila, 0] if pd.notna(df.iloc[fila, 0]) else "")
                solicitados_lugar.append(df.iloc[fila, 8] if pd.notna(df.iloc[fila, 8]) else "")
                comentarios_lugar.append(df.iloc[fila, 9] if pd.notna(df.iloc[fila, 9]) else "")

        if df.loc[9:18, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all(): SADCO = 0
        else:
            SADCO = 2
            procesar_lugar(9, 18)
        
        if df.loc[25:34, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all(): ARTE = 0
        else:
            ARTE = 2
            procesar_lugar(25, 34)

        if df.loc[41:47, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all(): Comedor_Ejecutivo = 0
        else:
            Comedor_Ejecutivo = 2
            procesar_lugar(41, 47)

        if df.loc[54:57, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all(): Aulas = 0
        else:
            Aulas = 2
            procesar_lugar(54, 57)

        if df.loc[64:67, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all(): Explanada_LiFE = 0
        else:
            Explanada_LiFE = 1
            procesar_lugar(64, 67)

        if df.loc[73:76, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all(): Explanada_CIT = 0
        else:
            Explanada_CIT = 1
            procesar_lugar(73, 76)

        if df.loc[82:87, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all(): Jardin_CE_frente = 0
        else:
            Jardin_CE_frente = 1
            procesar_lugar(82, 87)

        if df.loc[93:97, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all(): Jardin_CE = 0
        else:
            Jardin_CE = 1
            procesar_lugar(93, 97)

        if df.loc[103:106, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all(): Terraza_LiFE = 0
        else:
            Terraza_LiFE = 2
            procesar_lugar(103, 106)
        
        for fila in range(9, 31):
            materiales_planta.append(df.iloc[fila, 11] if pd.notna(df.iloc[fila, 11]) else "")
            observaciones_planta.append(df.iloc[fila, 18] if pd.notna(df.iloc[fila, 18]) else "")
            lugar_planta.append(df.iloc[fila, 19] if pd.notna(df.iloc[fila, 19]) else "")
            solicitados_planta.append(df.iloc[fila, 20] if pd.notna(df.iloc[fila, 20]) else "")
            comentarios_planta.append(df.iloc[fila, 21] if pd.notna(df.iloc[fila, 21]) else "")
            
        z = sum([SADCO, ARTE, Comedor_Ejecutivo, Aulas, Explanada_LiFE, Explanada_CIT, Jardin_CE_frente, Jardin_CE, Terraza_LiFE])
        
        df_lugares = pd.DataFrame({"Materiales/Equipo": materiales_lugar, "Solicitados": solicitados_lugar, "Comentarios": comentarios_lugar})
        df_planta = pd.DataFrame({"Materiales/Equipo": materiales_planta, "Observaciones": observaciones_planta, "Lugar Solicitado": lugar_planta, "Solicitados": solicitados_planta, "Comentarios": comentarios_planta})

        df_lugares = df_lugares[df_lugares["Solicitados"].astype(str).str.strip() != ""]
        df_planta = df_planta[(df_planta["Lugar Solicitado"].astype(str).str.strip() != "") & (df_planta["Solicitados"].astype(str).str.strip() != "")]

        return {"Lugares registrados": z, "df_lugares": df_lugares, "df_planta": df_planta}

    def leer_Materiales(self):
        df = self._leer_pestana("MATERIAL ")
        mat, cant, obs, sol = [], [], [], []
        fila = 6
            
        while fila < len(df):
            material = df.iloc[fila, 0]
            if (pd.isna(material) or str(material).strip() == ""):
                break
            
            mat.append(material)
            cant.append(df.iloc[fila, 3])
            obs.append(df.iloc[fila, 4])
            sol.append(df.iloc[fila, 7])
            fila += 1
        
        df_mat = pd.DataFrame({"Materiales/Equipo": mat, "Cantidad": cant, "Observaciones": obs, "Solicitados": sol})
        return df_mat.dropna(subset=["Materiales/Equipo"]).reset_index(drop=True)

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
            # Validar credenciales desde st.secrets
            if "usuarios" in st.secrets:
                diccionario_usuarios = st.secrets["usuarios"]
                
                # Verificar si el usuario existe y si la contraseña coincide
                if usuario in diccionario_usuarios and password == diccionario_usuarios[usuario]:
                    st.session_state["logeado"] = True
                    st.session_state["usuario_actual"] = usuario
                    st.success(f"¡Bienvenido, {usuario}!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
            else:
                st.error("⚠️ No se encontró la configuración de usuarios ('secrets.toml'). Por favor configúrala.")

def mostrar_altpro():
    st.title("AltPro - Carga de Proyectos")
    st.markdown("Sube el archivo **Excel (.xlsx)** del proyecto para leerlo y aprobarlo.")

    archivo_subido = st.file_uploader("Arrastra aquí el archivo Excel", type=["xlsx", "xls"])

    if archivo_subido is not None:
        st.success("Archivo cargado correctamente. Procesando datos...")
        
        try:
            lector = LectorProyectosExcel(archivo_subido)
            
            alt = lector.leer_Alta_de_Proyecto()
            df_personas = lector.leer_Personas()
            lugares_data = lector.leer_Lugares()
            df_materiales = lector.leer_Materiales()

            tab1, tab2, tab3, tab4 = st.tabs(["Información General", "Personas Involucradas", "Lugares Registrados", "Materiales de Bodega"])

            with tab1:
                st.subheader("Datos del Proyecto")
                col1, col2 = st.columns(2)
                for i, (clave, valor) in enumerate(alt.items()):
                    if i % 2 == 0:
                        col1.metric(label=clave, value=str(valor))
                    else:
                        col2.metric(label=clave, value=str(valor))

            with tab2:
                st.subheader("Personas Involucradas")
                st.dataframe(df_personas, use_container_width=True)

            with tab3:
                st.subheader("Estado de Lugares")
                z = lugares_data["Lugares registrados"]
                
                if z == 0: st.info("No hay materiales registrados en ninguno de los lugares del Alta.")
                elif z == 1: st.success("Hay un lugar registrado al aire libre. No hay errores en el alta.")
                elif z == 2: st.success("Hay un lugar registrado en interior. No hay errores en el alta.")
                elif z == 3: st.success("Hay un lugar registrado en interior y un en exterior. No hay errores en el alta.")
                else: st.error("⚠️ Hay un error en el alta. Hay más de dos lugares registrados. Revisar manualmente.")

                st.markdown("### Materiales por Lugar")
                st.dataframe(lugares_data["df_lugares"], use_container_width=True)

                st.markdown("### Materiales de Planta Física")
                st.dataframe(lugares_data["df_planta"], use_container_width=True)

            with tab4:
                st.subheader("Materiales y Equipos")
                st.dataframe(df_materiales, use_container_width=True)
                
            st.divider()
            st.markdown("¿La información es correcta?")
            if st.button("Aprobar y Guardar en Base de Datos", use_container_width=True):
                st.success("¡Datos aprobados! (Aquí conectaremos más adelante a Google Sheets para guardar esto).")
                st.balloons()

        except Exception as e:
            st.error(f"Error al leer el documento: {e}")
            st.info("Asegúrate de que el archivo tenga el formato y las pestañas correctas.")


def mostrar_estadisticas():
    st.title("Página en desarrollo...")

# ==========================================
# FLUJO PRINCIPAL DE LA APP
# ==========================================
def main():
    if "logeado" not in st.session_state:
        st.session_state["logeado"] = False

    if not st.session_state["logeado"]:
        mostrar_login()
    else:
        st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1055/1055664.png", width=100)
        st.sidebar.title("Menú Principal")
        st.sidebar.write(f"**Usuario:** {st.session_state.get('usuario_actual', '')}")
        st.sidebar.divider()
        
        opcion = st.sidebar.radio("Navegación:", ["Inicio", "AltPro","Estadísticas"])
        
        st.sidebar.divider()
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state["logeado"] = False
            st.session_state["usuario_actual"] = None
            st.rerun()

        if opcion == "🏠 Inicio":
            st.title("Bienvenido al Sistema")
            st.write(f"Hola **{st.session_state.get('usuario_actual', '')}**. Selecciona **AltPro** en el menú de la izquierda para comenzar a subir proyectos.")
        
        elif opcion == "📂 AltPro":
            mostrar_altpro()
            
        elif opcion == "📊 Estadísticas":
            mostrar_estadisticas()

if __name__ == "__main__":
    main()