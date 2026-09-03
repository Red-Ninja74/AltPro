from Archivo import leerArchivo

archivo = leerArchivo.leerArchivo()
alt = archivo.leer_Alta_de_Proyecto()
per = archivo.leer_Personas()
lug = archivo.leer_Lugares()
mat = archivo.leer_Materiales()
archivo.mostrar_datos(alt, per, lug, mat)