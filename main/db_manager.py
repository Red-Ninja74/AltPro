import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection


class BaseDatos_GE:

    def __init__(self, nombre_hoja: str = "EVENTOS"):
        self.nombre_hoja = nombre_hoja
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def obtener_datos(self) -> pd.DataFrame:
        try:
            df = self.conn.read(worksheet=self.nombre_hoja, ttl=0)
            return df
        except Exception as e:
            st.error(f"Error al obtener los datos de la hoja '{self.nombre_hoja}': {e}")
            return pd.DataFrame()

    def registrar_datos(self, datos_evento: dict) -> bool:
        try:
            df_existente = self.obtener_datos()

            df_nuevo = pd.DataFrame([datos_evento])

            if not df_existente.empty:
                df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
            else:
                df_final = df_nuevo

            self.conn.update(worksheet=self.nombre_hoja, data=df_final)
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