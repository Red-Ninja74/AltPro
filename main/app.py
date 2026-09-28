import streamlit as st

from consultas import (
    obtener_grupo_mas_eventos,
    obtener_numero_eventos_grupos,
    obtener_total_proyectos,
)
from paginas.altpro import mostrar_altpro
from paginas.estadisticas import mostrar_estadisticas
from paginas.inicio import mostrar_inicio
from paginas.login import mostrar_login

# ==========================================
# CONFIGURACIÓN DE PÁGINA STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Alta de Proyectos",
    layout="wide",
    initial_sidebar_state="expanded",
)


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
            mostrar_inicio()
        elif opcion == "📂 AltPro":
            mostrar_altpro()
        elif opcion == "📊 Estadísticas":
            total_proyectos = obtener_total_proyectos()
            grupo_mas_eventos = obtener_grupo_mas_eventos()
            eventos_por_grupo = obtener_numero_eventos_grupos()
            mostrar_estadisticas(total_proyectos, grupo_mas_eventos, eventos_por_grupo)

if __name__ == "__main__":
    main()
