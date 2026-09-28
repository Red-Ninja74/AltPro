import pandas as pd


# ==========================================
# CLASE DE LECTURA DE EXCEL
# ==========================================
class LectorProyectosExcel:

    def __init__(self, archivo_subido):
        self.archivo = archivo_subido
        self.xls = pd.ExcelFile(archivo_subido)

    def _leer_pestana(self, nombre_pestana):
        # Normaliza búsquedas ignorando espacios extra y mayúsculas
        nombres_reales = self.xls.sheet_names
        coincidencia = next(
            (
                n
                for n in nombres_reales
                if n.strip().lower() == nombre_pestana.strip().lower()
            ),
            None,
        )
        if coincidencia:
            # Corrección: parsear usando el objeto ExcelFile ya abierto
            return self.xls.parse(sheet_name=coincidencia, header=None)
        raise ValueError(
            f"No se encontró la pestaña '{nombre_pestana}' en el archivo."
        )

    def leer_Alta_de_Proyecto(self):
        df = self._leer_pestana("Alta de proyecto")

        def safe_get(r, c):
            try:
                val = df.iloc[r, c]
                return "" if pd.isna(val) else str(val).strip()
            except IndexError:
                return ""

        return {
            "Grupo Estudiantil": safe_get(5, 4),
            "Nombre de Proyecto": safe_get(6, 4),
            "Lugar": safe_get(7, 4),
            "Fecha de inicio": safe_get(8, 2),
            "Fecha de termino": safe_get(9, 2),
            "Hora de inicio": safe_get(8, 6),
            "Hora de termino": safe_get(9, 6),
        }

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
        (
            materiales_planta,
            observaciones_planta,
            lugar_planta,
            solicitados_planta,
            comentarios_planta,
        ) = ([], [], [], [], [])

        def safe_val(r, c):
            try:
                val = df.iloc[r, c]
                return val if pd.notna(val) else ""
            except IndexError:
                return ""

        def procesar_lugar(rango_inicio, rango_fin):
            for fila in range(rango_inicio, rango_fin):
                materiales_lugar.append(safe_val(fila, 0))
                solicitados_lugar.append(safe_val(fila, 8))
                comentarios_lugar.append(safe_val(fila, 9))

        def check_rango(r1, r2, c1, c2):
            try:
                sub = df.iloc[r1:r2, c1:c2].replace(r"^\s*$", pd.NA, regex=True)
                return not sub.isna().all().all()
            except Exception:
                return False

        SADCO = 2 if check_rango(9, 18, 8, 10) else 0
        if SADCO:
            procesar_lugar(9, 18)

        ARTE = 2 if check_rango(25, 34, 8, 10) else 0
        if ARTE:
            procesar_lugar(25, 34)

        Comedor_Ejecutivo = 2 if check_rango(41, 47, 8, 10) else 0
        if Comedor_Ejecutivo:
            procesar_lugar(41, 47)

        Aulas = 2 if check_rango(54, 57, 8, 10) else 0
        if Aulas:
            procesar_lugar(54, 57)

        Explanada_LiFE = 1 if check_rango(64, 67, 8, 10) else 0
        if Explanada_LiFE:
            procesar_lugar(64, 67)

        Explanada_CIT = 1 if check_rango(73, 76, 8, 10) else 0
        if Explanada_CIT:
            procesar_lugar(73, 76)

        Jardin_CE_frente = 1 if check_rango(82, 87, 8, 10) else 0
        if Jardin_CE_frente:
            procesar_lugar(82, 87)

        Jardin_CE = 1 if check_rango(93, 97, 8, 10) else 0
        if Jardin_CE:
            procesar_lugar(93, 97)

        Terraza_LiFE = 2 if check_rango(103, 106, 8, 10) else 0
        if Terraza_LiFE:
            procesar_lugar(103, 106)

        for fila in range(9, min(31, len(df))):
            materiales_planta.append(safe_val(fila, 11))
            observaciones_planta.append(safe_val(fila, 18))
            lugar_planta.append(safe_val(fila, 19))
            solicitados_planta.append(safe_val(fila, 20))
            comentarios_planta.append(safe_val(fila, 21))

        z = sum([
            SADCO,
            ARTE,
            Comedor_Ejecutivo,
            Aulas,
            Explanada_LiFE,
            Explanada_CIT,
            Jardin_CE_frente,
            Jardin_CE,
            Terraza_LiFE,
        ])

        df_lugares = pd.DataFrame({
            "Materiales/Equipo": materiales_lugar,
            "Solicitados": solicitados_lugar,
            "Comentarios": comentarios_lugar,
        })
        df_planta = pd.DataFrame({
            "Materiales/Equipo": materiales_planta,
            "Observaciones": observaciones_planta,
            "Lugar Solicitado": lugar_planta,
            "Solicitados": solicitados_planta,
            "Comentarios": comentarios_planta,
        })

        if not df_lugares.empty and "Solicitados" in df_lugares:
            df_lugares = df_lugares[
                df_lugares["Solicitados"].astype(str).str.strip() != ""
            ]
        if not df_planta.empty and "Lugar Solicitado" in df_planta:
            df_planta = df_planta[
                (df_planta["Lugar Solicitado"].astype(str).str.strip() != "")
                & (df_planta["Solicitados"].astype(str).str.strip() != "")
            ]

        return {
            "Lugares registrados": z,
            "df_lugares": df_lugares,
            "df_planta": df_planta,
        }

    def leer_Materiales(self):
        df = self._leer_pestana("MATERIAL")
        mat, cant, obs, sol = [], [], [], []
        fila = 7

        def safe_val(r, c):
            try:
                val = df.iloc[r, c]
                return val if pd.notna(val) else ""
            except IndexError:
                return ""

        while fila < len(df):
            material = safe_val(fila, 0)
            if str(material).strip() == "":
                break

            mat.append(material)
            cant.append(safe_val(fila, 3))
            obs.append(safe_val(fila, 4))
            sol.append(safe_val(fila, 7))
            fila += 1

        df_mat = pd.DataFrame({
            "Materiales/Equipo": mat,
            "Cantidad": cant,
            "Observaciones": obs,
            "Solicitados": sol,
        })
        return df_mat.dropna(subset=["Materiales/Equipo"]).reset_index(
            drop=True
        )
