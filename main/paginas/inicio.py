import streamlit as st
from streamlit_calendar import calendar

from consultas import obtener_eventos_calendario


CSS_CALENDARIO = """
    .fc-event {
        border: none;
        border-radius: 6px;
        padding: 3px 6px;
        margin: 2px 3px;
        cursor: pointer;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
    }
    .fc-event:hover {
        filter: brightness(1.1);
    }
    /* El texto largo se parte en varias líneas en vez de cortarse */
    .fc-daygrid-event,
    .fc-event-main,
    .fc-event-title {
        white-space: normal !important;
        overflow: visible !important;
        word-break: break-word;
    }
    .fc-event-title {
        font-size: 0.8rem;
        font-weight: 600;
        line-height: 1.25;
    }
    .fc-toolbar-title {
        font-size: 1.3rem;
        text-transform: capitalize;
    }
    .fc-day-today {
        background: #EFF6FF !important;
    }
"""


def mostrar_calendario(eventos):
    with st.container(border=True):
        st.subheader("Calendario de Eventos")
        resultado = calendar(
            events=eventos,
            options={
                "initialView": "dayGridMonth",
                "locale": "es",
                "firstDay": 1,
                "headerToolbar": {
                    "left": "prev,next today",
                    "center": "title",
                    "right": "dayGridMonth,listMonth",
                },
                "buttonText": {"today": "Hoy", "month": "Mes", "list": "Lista"},
                "eventDisplay": "block",
                # Los días crecen para mostrar todos sus eventos
                "dayMaxEvents": False,
                "contentHeight": "auto",
            },
            custom_css=CSS_CALENDARIO,
            callbacks=["eventClick"],
            key="calendario_inicio",
        )

        # Detalle del evento al que se le dio click
        if resultado and resultado.get("callback") == "eventClick":
            evento = resultado["eventClick"]["event"]
            datos = evento.get("extendedProps", {})
            with st.container(border=True):
                st.markdown(f"### {evento['title']}")
                col1, col2, col3 = st.columns(3)
                col1.markdown(f"**👥 Grupo**  \n{datos.get('grupo', '')}")
                col2.markdown(f"**📍 Lugar**  \n{datos.get('lugar', '')}")
                col3.markdown(f"**📅 Fecha**  \n{datos.get('fecha', '')}")
        else:
            st.caption("Da click en un evento para ver sus detalles.")


def mostrar_inicio():
    st.title("Bienvenido al Sistema")
    st.write(
        f"Hola **{st.session_state.get('usuario_actual', '')}**."
        " Selecciona **AltPro** en el menú de la izquierda para"
        " comenzar."
    )
    mostrar_calendario(obtener_eventos_calendario())
