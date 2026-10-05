import plotly.express as px
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from config import CATALOGO_IDS, GIROS_GRUPOS
from reporte_pdf import reporte_pdf


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
    st.write("") 
    style_metric_cards(
        background_color="#F8FAFC",border_size_px=1,border_color="#E2E8F0",border_radius_px=12,border_left_color="#2563EB", box_shadow=True)
    
    
    with st.container(border=False):
        st.subheader("Eventos por Grupo")
        fig = px.bar(eventos_por_grupo, x="Grupo", y="Eventos", color="Eventos", color_continuous_scale=["#93C5FD", "#1E3A8A"])
        fig.update_traces(marker_pattern_shape="", cliponaxis=False)
        fig.update_layout(
        xaxis={"categoryorder": "total descending", "title": ""}, 
        yaxis_title="Cantidad de Eventos", 
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",     
        margin=dict(l=20, r=20, t=30, b=20), 
        font=dict(family="Inter, sans-serif", size=13, color="#64748B"), 
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
        coloraxis_showscale=False
    )
          
    
    st.plotly_chart(fig, use_container_width=True)
   
    seccion_reporte(eventos_por_grupo)


# Con @st.fragment, al cambiar las opciones del reporte solo se vuelve a
# ejecutar esta sección y no toda la app (no se vuelve a leer la hoja)
@st.fragment
def seccion_reporte(eventos_por_grupo):
    # El PDF se arma con los datos ya cargados en la página (tarda
    # centésimas de segundo) y el botón solo lo descarga
    
    st.subheader("Configuración de Reporte")
    tipo_reporte = st.radio('Tipo de Reporte:', ['General', 'Personalizado'])
    
    if tipo_reporte == "Personalizado":
        cola, colb, colc = st.columns(3)
        with cola:  
            giros_seleccionados = st.multiselect('Seleccione el/los Giro(s)', options=list(GIROS_GRUPOS.keys()))
        with colb:
            if giros_seleccionados:
                grupos_disponibles = []
                for giro in giros_seleccionados:
                    grupos_disponibles.extend(GIROS_GRUPOS.get(giro, []))
            else:
                grupos_disponibles = list(CATALOGO_IDS.keys())

            grupos_disponibles = sorted(list(set(grupos_disponibles)))
            
            grupos_seleccionados = []
            if st.radio('Grupos deseados:', ['Todos los grupos', 'Personalizado']) == "Personalizado":
                grupos_seleccionados = st.multiselect('Seleccione el/los Grupo(s)', options=grupos_disponibles)
            else:
                grupos_seleccionados = grupos_disponibles
            
            if st.radio('Grupos deseados:', ['Todos los grupos','Personalizado'])== "Personalizado":
                st.multiselect('Seleccione el/los Grupo(s)', [1,2,3,4,5,6,7,8,9,10])
        with colc:
            if st.radio('Rango personalizado de fechas:', ['No','Si'])== "Si":
                st.date_input('Fecha de Inicio', value=None, min_value=None, max_value=None, key=None)
                st.date_input('Fecha de Fin', value=None, min_value=None, max_value=None, key=None)
        ids_filtrados = [CATALOGO_IDS[grupo] for grupo in grupos_seleccionados if grupo in CATALOGO_IDS]
        st.info(f"📌 **IDs a filtrar en la base de datos:** {ids_filtrados}")
        st.write("")  
    
    try:
        pdf = reporte_pdf(eventos_por_grupo).crear_reporte()
    except Exception as e:
        st.error(f"No se pudo generar el reporte: {e}")
        return

    if st.download_button(
        "Descargar reporte",
        data=pdf,
        file_name="Reporte_Gestion.pdf",
        mime="application/pdf",
        use_container_width=True,):
        st.success("Reporte descargado con éxito!")
        st.balloons()

    