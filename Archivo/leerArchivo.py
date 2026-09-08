import pandas as pd


class LeerArchivo:
    def __init__(self, archivo="Alta de Proyectos.xlsx"):
        self.archivo = archivo
        self.excel = pd.ExcelFile(archivo)
    
    def leer_Alta_de_Proyecto(self, pestana="Alta de proyecto"):
        df = pd.read_excel(self.excel, sheet_name=pestana, header=None)
        alta = {
            "Grupo Estudiantil": df.iloc[5, 4], 
            "Nombre de Proyecto": df.iloc[6, 4],
            "Lugar": df.iloc[7, 4],
            "Fecha de inicio": df.iloc[8, 2],
            "Fecha de termino": df.iloc[9, 2],
            "Hora de inicio": df.iloc[8, 6],
            "Hora de termino": df.iloc[9, 6]
        }
        return alta
    
    def leer_Personas(self, pestana="PERSONAS"):
        df = pd.read_excel(self.excel, sheet_name=pestana, header=None)

        nombres = []
        fila = 6

        while fila < len(df):
            val = df.iloc[fila, 0]
            if pd.isna(val) or str(val).strip() == "":
                break
            nombres.append(val)
            fila += 1

        return {"Nombre": nombres}
            
    
    
    def leer_Lugares(self, pestana="LUGARES"):
        df = pd.read_excel(self.excel, sheet_name=pestana, header=None)
        materiales_lugar = []
        solicitados_lugar = []
        comentarios_lugar = []
        
        materiales_planta_fisica = []
        solicitados_planta_fisica  = []
        comentarios_planta_fisica  = []
        observaciones_planta_fisica  = []
        lugar_solicitado_planta_fisica = []
                
        if df.loc[9:18, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all():
            SADCO = 0
        else:
            SADCO = 2
        
            for fila in range(9, 18):
                val = df.iloc[fila, 0]
                if pd.notna(val):
                    materiales_lugar.append(val)
        
            for fila in range(9, 18):
                val = df.iloc[fila, 8]
                if pd.notna(val):
                    solicitados_lugar.append(val)
                    
            for fila in range(9, 18):
                val = df.iloc[fila, 9]
                if pd.notna(val):
                    comentarios_lugar.append(val)
        
        if df.loc[25:34, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all():
            ARTE = 0
        else:
            ARTE = 2
            for fila in range(25, 34):
                val = df.iloc[fila, 0]
                if pd.notna(val):
                    materiales_lugar.append(val)
        
            for fila in range(25, 34):
                val = df.iloc[fila, 8]
                if pd.notna(val):
                    solicitados_lugar.append(val)
                    
            for fila in range(25, 34):
                val = df.iloc[fila, 9]
                if pd.notna(val):
                    comentarios_lugar.append(val)

        if df.loc[41:47, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all():
            Comedor_Ejecutivo = 0
        else:
            Comedor_Ejecutivo = 2
            for fila in range(41, 47):
                val = df.iloc[fila, 0]
                if pd.notna(val):
                    materiales_lugar.append(val)
        
            for fila in range(41, 47):
                val = df.iloc[fila, 8]
                if pd.notna(val):
                    solicitados_lugar.append(val)
                    
            for fila in range(41, 47):
                val = df.iloc[fila, 9]
                if pd.notna(val):
                    comentarios_lugar.append(val)

        if df.loc[54:57, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all():
            Aulas = 0
        else:
            Aulas = 2
            for fila in range(54, 57):
                val = df.iloc[fila, 0]
                if pd.notna(val):
                    materiales_lugar.append(val)
        
            for fila in range(54, 57):
                val = df.iloc[fila, 8]
                if pd.notna(val):
                    solicitados_lugar.append(val)
                    
            for fila in range(54, 57):
                val = df.iloc[fila, 9]
                if pd.notna(val):
                    comentarios_lugar.append(val)

        if df.loc[64:67, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all():
            Explanada_LiFE = 0
        else:
            Explanada_LiFE = 1
            for fila in range(64, 67):
                val = df.iloc[fila, 0]
                if pd.notna(val):
                    materiales_lugar.append(val)
        
            for fila in range(64, 67):
                val = df.iloc[fila, 8]
                if pd.notna(val):
                    solicitados_lugar.append(val)
                    
            for fila in range(64, 67):
                val = df.iloc[fila, 9]
                if pd.notna(val):
                    comentarios_lugar.append(val)

        if df.loc[73:76, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all():
            Explanada_CIT = 0
        else:
            Explanada_CIT = 1
            for fila in range(73, 76):
                val = df.iloc[fila, 0]
                if pd.notna(val):
                    materiales_lugar.append(val)
        
            for fila in range(73, 76):
                val = df.iloc[fila, 8]
                if pd.notna(val):
                    solicitados_lugar.append(val)
                    
            for fila in range(73, 76):
                val = df.iloc[fila, 9]
                if pd.notna(val):
                    comentarios_lugar.append(val)

        if df.loc[82:87, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all():
            Jardin_CE_frente = 0
        else:
            Jardin_CE_frente = 1
            for fila in range(82, 86):
                val = df.iloc[fila, 0]
                if pd.notna(val):
                    materiales_lugar.append(val)
        
            for fila in range(82, 87):
                val = df.iloc[fila, 8]
                if pd.notna(val):
                    solicitados_lugar.append(val)
                    
            for fila in range(82, 87):
                val = df.iloc[fila, 9]
                if pd.notna(val):
                    comentarios_lugar.append(val)

        if df.loc[93:97, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all():
            Jardin_CE = 0
        else:
            Jardin_CE = 1
            for fila in range(93, 97):
                val = df.iloc[fila, 0]
                if pd.notna(val):
                    materiales_lugar.append(val)
        
            for fila in range(93, 97):
                val = df.iloc[fila, 8]
                if pd.notna(val):
                    solicitados_lugar.append(val)
                    
            for fila in range(93, 97):
                val = df.iloc[fila, 9]
                if pd.notna(val):
                    comentarios_lugar.append(val)

        if df.loc[103:106, 8:10].replace(r'^\s*$', pd.NA, regex=True).isna().all().all():
            Terraza_LiFE = 0
        else:
            Terraza_LiFE = 2
            for fila in range(103, 105):
                val = df.iloc[fila, 0]
                if pd.notna(val):
                    materiales_lugar.append(val)
        
            for fila in range(103, 105):
                val = df.iloc[fila, 8]
                if pd.notna(val):
                    solicitados_lugar.append(val)
                    
            for fila in range(103, 105):
                val = df.iloc[fila, 9]
                if pd.notna(val):
                    comentarios_lugar.append(val)
        
        for fila in range(9, 31):
                val = df.iloc[fila, 11]
                if pd.notna(val):
                    materiales_planta_fisica.append(val)
                else:
                    materiales_planta_fisica.append("")
                    
        for fila in range(9, 31):
                val = df.iloc[fila, 18]
                if pd.notna(val):
                    observaciones_planta_fisica.append(val)
                else:
                    observaciones_planta_fisica.append("")
        
        for fila in range(9, 31):
                val = df.iloc[fila, 19]
                if pd.notna(val):
                    lugar_solicitado_planta_fisica.append(val)
                else:
                    lugar_solicitado_planta_fisica.append("")
        
        for fila in range(9, 31):
                val = df.iloc[fila, 20]
                if pd.notna(val):
                    solicitados_planta_fisica.append(val)
                else:
                    solicitados_planta_fisica.append("")
        
        for fila in range(9, 31):
                val = df.iloc[fila, 21]
                if pd.notna(val):
                    comentarios_planta_fisica.append(val)
                else:
                    comentarios_planta_fisica.append("")
        
            
        z = sum([SADCO, ARTE, Comedor_Ejecutivo, Aulas, Explanada_LiFE, Explanada_CIT, Jardin_CE_frente, Jardin_CE, Terraza_LiFE])
        return {"Lugares":{"Materiales/Equipo": materiales_lugar, "Solicitados": solicitados_lugar, "Comentarios": comentarios_lugar, "Lugares registrados": z}, "Planta Fisica":{"Materiales/Equipo": materiales_planta_fisica , "Observaciones": observaciones_planta_fisica , "Lugar Solicitado": lugar_solicitado_planta_fisica, "Solicitados": solicitados_planta_fisica , "Comentarios": comentarios_planta_fisica}}

    def leer_Materiales(self, pestana="MATERIAL "):
        df = pd.read_excel(self.excel, sheet_name=pestana, header=None)
        materiales_bodega = []
        cantidad_bodega = []
        observaciones_bodega = []
        solicitados_bodega = []
        fila = 6
            
        while fila < len(df):

            material = df.iloc[fila, 0]
            cantidad = df.iloc[fila, 3]
            observacion = df.iloc[fila, 4]
            solicitado = df.iloc[fila, 7]

            if (pd.isna(material) or str(material).strip() == ""):
                break

            materiales_bodega.append(material)
            cantidad_bodega.append(cantidad)
            observaciones_bodega.append(observacion)
            solicitados_bodega.append(solicitado)

            fila += 1
        
        return {"Materiales/Equipo": materiales_bodega, "Cantidad": cantidad_bodega, "Observaciones": observaciones_bodega, "Solicitados": solicitados_bodega}

    def mostrar_datos(self, datos: dict, personas: dict, lugares: dict, materiales: dict):
        print("\033[1;34m\n--- INFORMACIÓN GENERAL ---\033[0m")
        for clave, valor in datos.items():
            print(f"\033[1m{clave}\033[0m: {valor}")

        print("\033[1;33m\n--- PERSONAS INVOLUCRADAS ---\033[0m")
        for clave, valores in personas.items():
            for valor in valores:
                print(f"{valor}")

        print("\033[1;35m\n--- LUGARES REGISTRADOS ---\033[0m")
        z = lugares["Lugares"]["Lugares registrados"]
        match z:
            case 0:
                print("No hay materiales registrados ninguno de los lugares del Alta")
            case 1:
                print("Hay un lugar registrado al aire libre\nNo hay errores en el alta")
            case 2:
                print("Hay un lugar registrado en interior\nNo hay errores en el alta")
            case 3:
                print("Hay un lugar registrado en interior y un en exterior\nNo hay errores en el alta")
            case _:
                print("Hay un error en el alta\nHay más de dos lugares registrados\nRevisar manualemnte")

        mats = lugares["Lugares"].get("Materiales/Equipo", [])
        sols = lugares["Lugares"].get("Solicitados", [])
        coms = lugares["Lugares"].get("Comentarios", [])

        print("")
        header = f"\033[1;36m{'Materiales/Equipo':<45} | {'Solicitados':<15} | {'Comentarios':<40}\033[0m"
        print(header)
        print("-" * 90) 

        limite = max(len(mats), len(sols), len(coms))
        for i in range(limite):
            mat = str(mats[i]) if i < len(mats) else ""
            sol = str(sols[i]) if i < len(sols) else ""
            com = str(coms[i]) if i < len(coms) else ""
            
            if sol.strip() == "":
                continue
            
            print(f"{mat:<45} | {sol:<15} | {com:<40}")
        
        print("\033[1;35m\n--- MATERALES DE PLANTA FISICA ---\033[0m")
        header2 = f"\033[1;36m{'Materiales/Equipo':<45} | {'Observaciones':<30} | {'Lugar Solicitado':<40}| {'Solicitados':<15} | {'Comentarios':<40}\033[0m"
        print(header2)
        print("-" * 150)
        
        mat2 = lugares["Planta Fisica"].get("Materiales/Equipo", [])
        sol2= lugares["Planta Fisica"].get("Solicitados", [])
        com2 = lugares["Planta Fisica"].get("Comentarios", [])
        
        limite2 = max(len(lugares["Planta Fisica"].get("Materiales/Equipo", [])), len(lugares["Planta Fisica"].get("Observaciones", [])), len(lugares["Planta Fisica"].get("Lugar Solicitado", [])), len(lugares["Planta Fisica"].get("Solicitados", [])), len(lugares["Planta Fisica"].get("Comentarios", [])))
        
        
        for i in range(limite2):
            mat2 = str(lugares["Planta Fisica"].get("Materiales/Equipo", [])[i]) if i < len(lugares["Planta Fisica"].get("Materiales/Equipo", [])) else ""
            obs2 = str(lugares["Planta Fisica"].get("Observaciones", [])[i]) if i < len(lugares["Planta Fisica"].get("Observaciones", [])) else ""
            lug2 = str(lugares["Planta Fisica"].get("Lugar Solicitado", [])[i]) if i < len(lugares["Planta Fisica"].get("Lugar Solicitado", [])) else ""
            sol2 = str(lugares["Planta Fisica"].get("Solicitados", [])[i]) if i < len(lugares["Planta Fisica"].get("Solicitados", [])) else ""
            com2 = str(lugares["Planta Fisica"].get("Comentarios", [])[i]) if i < len(lugares["Planta Fisica"].get("Comentarios", [])) else ""
            
            if lug2.strip() == "" or sol2.strip() == "":
                continue
            print(f"{mat2:<45} | {obs2:<30} | {lug2:<40} | {sol2:<15} | {com2:<40}")
            
            
        print("\033[1;35m\n--- MATERALES DE BODEGA ---\033[0m")
        header3 = f"\033[1;36m{'Materiales/Equipo':<45} | {'Cantidad':<15} | {'Observaciones':<40}| {'Solicitados':<15}\033[0m"
        print(header3)
        print("-" * 120)
        
        mat3 = materiales.get("Materiales/Equipo", [])
        can3 = materiales.get("Cantidad", [])
        obs3= materiales.get("Observaciones", [])
        sol3 = materiales.get("Solicitados", [])
        
        limite3 = max(len(materiales.get("Materiales/Equipo", [])), len(materiales.get("Cantidad", [])), len(materiales.get("Solicitados", [])), len(materiales.get("Comentarios", [])))
        
        
        for i in range(limite3):
            mat3 = str(materiales.get("Materiales/Equipo", [])[i]) if i < len(materiales.get("Materiales/Equipo", [])) and not pd.isna(materiales.get("Materiales/Equipo", [])[i]) else ""
            can3 = str(materiales.get("Cantidad", [])[i]) if i < len(materiales.get("Cantidad", [])) and not pd.isna(materiales.get("Cantidad", [])[i]) else ""
            obs3 = str(materiales.get("Observaciones", [])[i]) if i < len(materiales.get("Observaciones", [])) and not pd.isna(materiales.get("Observaciones", [])[i]) else ""
            sol3 = str(materiales.get("Solicitados", [])[i]) if i < len(materiales.get("Solicitados", [])) and not pd.isna(materiales.get("Solicitados", [])[i]) else ""
            
            if mat3.strip() == "" or can3.strip() == "" and sol3.strip() == "":
                continue
            
            print(f"{mat3:<45} | {can3:<15} | {obs3:<40} | {sol3:<40}")
        
archivo = LeerArchivo()
alt = archivo.leer_Alta_de_Proyecto()
per = archivo.leer_Personas()
lug = archivo.leer_Lugares()
mat = archivo.leer_Materiales()
archivo.mostrar_datos(alt, per, lug, mat)

