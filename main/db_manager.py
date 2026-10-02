import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Segundos que se reutilizan los datos leídos antes de volver a pedirlos a
# Google Sheets (el límite de Google es de 60 lecturas por minuto)
TTL_CACHE_SEGUNDOS = 300


class BaseDatos_GE:

    def __init__(self, nombre_hoja: str = "EVENTOS"):
        self.nombre_hoja = nombre_hoja
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def obtener_datos(self, ttl: int = TTL_CACHE_SEGUNDOS) -> pd.DataFrame:
        """Lee la hoja. Durante `ttl` segundos se reutiliza la última lectura
        en lugar de volver a pedirla a Google (ttl=0 fuerza leer de nuevo)."""
        try:
            df = self.conn.read(worksheet=self.nombre_hoja, ttl=ttl)
            return df
        except Exception as e:
            st.error(f"Error al obtener los datos de la hoja '{self.nombre_hoja}': {e}")
            return pd.DataFrame()

    def registrar_datos(self, datos_evento: dict) -> bool:
        try:
            # Sin caché: hay que partir de lo que hay en la hoja en este
            # momento para no borrar filas que alguien más haya agregado
            df_existente = self.obtener_datos(ttl=0)

            df_nuevo = pd.DataFrame([datos_evento])

            if not df_existente.empty:
                df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
            else:
                df_final = df_nuevo

            self.conn.update(worksheet=self.nombre_hoja, data=df_final)
            # Se borra la caché para que el evento nuevo aparezca de inmediato
            # en el calendario y en las estadísticas
            st.cache_data.clear()
            return True
        except Exception as e:
            st.error(f"Error al registrar el evento: {e}")
            return False

    def buscar_datos(self, id_grupo: str) -> pd.DataFrame:
        df = self.obtener_datos()
        col_id = "ID del grupo (XXX-YYY-ZZZ)"
        if not df.empty and col_id in df.columns:
            return df[df[col_id].astype(str) == str(id_grupo)]
        return pd.DataFrame()