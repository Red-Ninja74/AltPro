import streamlit as st

from config import CATALOGO_IDS
from db_manager import BaseDatos_GE
from lector_excel import LectorProyectosExcel


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
