import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

class BaseDatos_GE:
    def __init__(self, nombre_hoja: str = "EVENTOS"):
        self.nombre_hoja = nombre_hoja
        self.conn = st.connection("gsheets", type=GSheetsConnection)
    def obtener_datos(self) -> pd.DataFrame:
        try:
            df = self.conn.read(self.nombre_hoja, ttl=0)
            return df
        except Exception as e:
            st.error(f"Error al obtener los datos: {e}")
            return pd.DataFrame() 
    def registrar_datos(self, datos_evento: dict) -> bool:
        try:
            df_evento = pd.DataFrame([datos_evento])
            self.conn.update(self.nombre_hoja, df_evento)
            return True
        except Exception as e:
            st.error(f"Error al registrar el evento: {e}")
            return False
    def buscar_datos(self, id_grupo: str) -> pd.DataFrame:
        df = self.obtener_datos()
        if not df.empty and "ID del grupo (XXX-YYY-ZZZ)" in df.columns:
            return df[df["ID del grupo (XXX-YYY-ZZZ)"] == id_grupo]
        return pd.DataFrame()