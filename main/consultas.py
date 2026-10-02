import pandas as pd

from config import COLORES_CATEGORIA
from db_manager import BaseDatos_GE


def cargar_eventos():
    """Lee la hoja EVENTOS una sola vez; el resultado se pasa a las demás
    funciones para no repetir la lectura."""
    return BaseDatos_GE(nombre_hoja="EVENTOS").obtener_datos()


def obtener_total_proyectos(df):
    return len(df)  

def obtener_grupo_mas_eventos(df):
    if df.empty:
        return ("Sin datos", 0)
    conteo = df.iloc[:, 0].value_counts()
    matricula = conteo.idxmax()
    num_eventos = conteo.max()
    nombres = df[df.iloc[:, 0] == matricula].iloc[:, 1]
    nombre = nombres.value_counts().idxmax()
    return (nombre, num_eventos)

def obtener_numero_eventos_grupos(df):
    if df.empty:
        return pd.DataFrame(columns=["Grupo", "Eventos"])
    col_matricula = df.columns[0]
    col_nombre = df.columns[1]
    resumen = df.groupby(col_matricula).agg(
        Grupo=(col_nombre, lambda nombres: nombres.value_counts().idxmax()), Eventos=(col_nombre, "size"))
    return resumen.sort_values("Eventos", ascending=False).reset_index(drop=True)


def obtener_eventos_calendario(df):
    if df.empty:
        return []
    # Columna 3 (D): fechas en formato día/mes/año, p. ej. "18/9/2026"
    fechas = pd.to_datetime(df.iloc[:, 3], errors="coerce", format="%d/%m/%Y")
    eventos = []
    for i, fecha in enumerate(fechas):
        # Se omiten las filas con fecha vacía o con formato inválido
        if pd.isna(fecha):
            continue
        id_grupo = str(df.iloc[i, 0])
        lugar = df.iloc[i, 4]
        # La categoría es la parte central del ID, p. ej. "HID-ASE-ING" -> "ASE"
        partes_id = id_grupo.split("-")
        categoria = partes_id[1] if len(partes_id) == 3 else ""
        eventos.append({
            "title": str(df.iloc[i, 2]),
            "start": fecha.strftime("%Y-%m-%d"),
            "allDay": True,
            "color": COLORES_CATEGORIA.get(categoria, "#2563EB"),
            "extendedProps": {
                "grupo": str(df.iloc[i, 1]),
                "lugar": "Sin lugar registrado" if pd.isna(lugar) else str(lugar),
                "fecha": fecha.strftime("%d/%m/%Y"),
            },
        })
    return eventos
