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
    style_metric_cards(background_color="#F8FAFC",border_size_px=1,border_color="#E2E8F0",border_radius_px=12,border_left_color="#2563EB", box_shadow=True)
    st.title("Eventos por grupo", text_alignment="center")
    with st.container(border=False):
        st.subheader("General")
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
    st.plotly_chart(fig, use_container_width=True, key="grafica_general")
    
    with st.container(border=False):
        st.subheader("Arte y Cultura")
        df_ayc = eventos_por_grupo[eventos_por_grupo["Giro"] == "ACE"]
        if df_ayc.empty:
            st.info("Todavía no hay eventos registrados de Arte y Cultura.")
        fig_ayc = px.bar(df_ayc, x="Grupo", y="Eventos", color="Eventos", color_continuous_scale=["#DB6193", "#DB2777"])
        fig_ayc.update_traces(marker_pattern_shape="", cliponaxis=False)
        fig_ayc.update_layout(
        xaxis={"categoryorder": "total descending", "title": ""}, 
        yaxis_title="Cantidad de Eventos", 
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",     
        margin=dict(l=20, r=20, t=30, b=20), 
        font=dict(family="Inter, sans-serif", size=13, color="#64748B"), 
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
        coloraxis_showscale=False)
        st.plotly_chart(fig_ayc, use_container_width=True, key="grafica_ayc")
    
    with st.container(border=False):
        st.subheader("Deportivos y Recreativos")
        df_dyr = eventos_por_grupo[eventos_por_grupo["Giro"] == "DYR"]
        if df_dyr.empty:
            st.info("Todavía no hay eventos registrados de Deportivos y Recreativos.")
        else:
            fig_dyr = px.bar(df_dyr, x="Grupo", y="Eventos", color="Eventos", color_continuous_scale=["#EA9265", "#EA580C"])
        fig_dyr.update_traces(marker_pattern_shape="", cliponaxis=False)
        fig_dyr.update_layout(
        xaxis={"categoryorder": "total descending", "title": ""}, 
        yaxis_title="Cantidad de Eventos", 
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",     
        margin=dict(l=20, r=20, t=30, b=20), 
        font=dict(family="Inter, sans-serif", size=13, color="#64748B"), 
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
        coloraxis_showscale=False)
        st.plotly_chart(fig_dyr, use_container_width=True, key="grafica_dyr")
    
    with st.container(border=False):
        st.subheader("Liderazgo")
        df_lid = eventos_por_grupo[eventos_por_grupo["Giro"] == "LID"]
        if df_lid.empty:
            st.info("Todavía no hay eventos registrados de Liderazgo.")
        else:
            fig_lid = px.bar(df_lid, x="Grupo", y="Eventos", color="Eventos", color_continuous_scale=["#B799E7", "#7C3AED"])
        fig_lid.update_traces(marker_pattern_shape="", cliponaxis=False)
        fig_lid.update_layout(
        xaxis={"categoryorder": "total descending", "title": ""}, 
        yaxis_title="Cantidad de Eventos", 
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",     
        margin=dict(l=20, r=20, t=30, b=20), 
        font=dict(family="Inter, sans-serif", size=13, color="#64748B"), 
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
        coloraxis_showscale=False)
        st.plotly_chart(fig_lid, use_container_width=True, key="grafica_lid")
    
    with st.container(border=False):
        st.subheader("Salud y Bienestar")
        df_syb = eventos_por_grupo[eventos_por_grupo["Giro"] == "SYB"]
        if df_syb.empty:
            st.info("Todavía no hay eventos registrados de Salud y Bienestar.")
        else:
            fig_syb = px.bar(df_syb, x="Grupo", y="Eventos", color="Eventos", color_continuous_scale=["#4D948E", "#0D9488"])
        fig_syb.update_traces(marker_pattern_shape="", cliponaxis=False)
        fig_syb.update_layout(
        xaxis={"categoryorder": "total descending", "title": ""}, 
        yaxis_title="Cantidad de Eventos", 
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",     
        margin=dict(l=20, r=20, t=30, b=20), 
        font=dict(family="Inter, sans-serif", size=13, color="#64748B"), 
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
        coloraxis_showscale=False)
        st.plotly_chart(fig_syb, use_container_width=True, key="grafica_syb")
    
    with st.container(border=False):
        st.subheader("Sentido Humano y E. Social")
        df_she = eventos_por_grupo[eventos_por_grupo["Giro"] == "SHE"]
        if df_she.empty:
            st.info("Todavía no hay eventos registrados de Sentido Humano y E. Social.")
        else:
            fig_she = px.bar(df_she, x="Grupo", y="Eventos", color="Eventos", color_continuous_scale=["#DC7E7E", "#DC2626"])
        fig_she.update_traces(marker_pattern_shape="", cliponaxis=False)
        fig_she.update_layout(
        xaxis={"categoryorder": "total descending", "title": ""}, 
        yaxis_title="Cantidad de Eventos", 
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",     
        margin=dict(l=20, r=20, t=30, b=20), 
        font=dict(family="Inter, sans-serif", size=13, color="#64748B"), 
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
        coloraxis_showscale=False)
        st.plotly_chart(fig_she, use_container_width=True, key="grafica_she")
        
    with st.container(border=False):
        st.subheader("Vinculación Académica")
        df_vac = eventos_por_grupo[eventos_por_grupo["Giro"] == "VAC"]
        if df_vac.empty:
            st.info("Todavía no hay eventos registrados de Vinculación Académica.")
        else:
            fig_vac = px.bar(df_vac, x="Grupo", y="Eventos", color="Eventos", color_continuous_scale=["#95ADED", "#2563EB"])
        fig_vac.update_traces(marker_pattern_shape="", cliponaxis=False)
        fig_vac.update_layout(
        xaxis={"categoryorder": "total descending", "title": ""}, 
        yaxis_title="Cantidad de Eventos", 
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",     
        margin=dict(l=20, r=20, t=30, b=20), 
        font=dict(family="Inter, sans-serif", size=13, color="#64748B"), 
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
        coloraxis_showscale=False)
        st.plotly_chart(fig_vac, use_container_width=True, key="grafica_vac")
        
    with st.container(border=False):
            st.subheader("Asociaciones Estudiantiles")
            df_ase = eventos_por_grupo[eventos_por_grupo["Giro"] == "ASE"]
            if df_ase.empty:
                st.info("Todavía no hay eventos registrados de Asociaciones Estudiantiles.")
            else:
                fig_ase = px.bar(df_ase, x="Grupo", y="Eventos", color="Eventos", color_continuous_scale=["#CAB174", "#CA8A04"])
            fig_ase.update_traces(marker_pattern_shape="", cliponaxis=False)
            fig_ase.update_layout(
            xaxis={"categoryorder": "total descending", "title": ""}, 
            yaxis_title="Cantidad de Eventos", 
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)",     
            margin=dict(l=20, r=20, t=30, b=20), 
            font=dict(family="Inter, sans-serif", size=13, color="#64748B"), 
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
            coloraxis_showscale=False)
            st.plotly_chart(fig_ase, use_container_width=True, key="grafica_ase")
   
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

    