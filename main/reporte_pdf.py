from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from config import CATALOGO_IDS, NOMBRES_GIRO, SIGLAS_GRUPOS
from consultas import obtener_numero_eventos_grupos

# Palabras que van en minúscula dentro de un nombre (excepto al inicio)
PALABRAS_MENORES = {"A", "AT", "DE", "EN", "Y"}


def formatear_nombre(nombre):
    """ "LEADER HUB" -> "Leader Hub"; las siglas como "SEING" se quedan igual."""
    if nombre in SIGLAS_GRUPOS:
        return nombre
    palabras = []
    for i, palabra in enumerate(nombre.split()):
        if i > 0 and palabra in PALABRAS_MENORES:
            palabras.append(palabra.lower())
        else:
            palabras.append(palabra.capitalize())
    return " ".join(palabras)


def grafica_eventos_por_grupo(datos_grupos, ancho=528, alto=260):
    """Gráfica de barras con el mismo estilo que la de Estadísticas."""
    datos = datos_grupos.sort_values("Eventos", ascending=False)
    grupos = [str(g) for g in datos["Grupo"]]
    eventos = [int(e) for e in datos["Eventos"]]

    dibujo = Drawing(ancho, alto)
    grafica = VerticalBarChart()
    grafica.x = 40
    grafica.y = 90  # espacio abajo para los nombres inclinados
    grafica.width = ancho - 50
    grafica.height = alto - 110
    grafica.data = [eventos]
    grafica.barSpacing = 2
    grafica.groupSpacing = 6
    grafica.bars.strokeColor = None

    # Degradado de azul claro (menos eventos) a azul marino (más eventos)
    claro = colors.HexColor("#93C5FD")
    oscuro = colors.HexColor("#1E3A8A")
    minimo, maximo = min(eventos), max(eventos)
    for i, valor in enumerate(eventos):
        t = 0 if maximo == minimo else (valor - minimo) / (maximo - minimo)
        grafica.bars[(0, i)].fillColor = colors.linearlyInterpolatedColor(
            claro, oscuro, 0, 1, t
        )

    gris = colors.HexColor("#64748B")
    grafica.categoryAxis.categoryNames = grupos
    grafica.categoryAxis.labels.angle = 45
    grafica.categoryAxis.labels.boxAnchor = "ne"
    grafica.categoryAxis.labels.fontName = "Helvetica"
    grafica.categoryAxis.labels.fontSize = 7
    grafica.categoryAxis.labels.fillColor = gris
    grafica.categoryAxis.strokeColor = colors.HexColor("#CBD5E0")

    grafica.valueAxis.valueMin = 0
    grafica.valueAxis.valueStep = max(1, -(-maximo // 5))  # ~5 líneas guía
    grafica.valueAxis.labels.fontName = "Helvetica"
    grafica.valueAxis.labels.fontSize = 8
    grafica.valueAxis.labels.fillColor = gris
    grafica.valueAxis.strokeColor = None
    grafica.valueAxis.visibleGrid = True
    grafica.valueAxis.gridStrokeColor = colors.HexColor("#E2E8F0")
    grafica.valueAxis.gridStrokeWidth = 0.5

    # Número de eventos encima de cada barra
    grafica.barLabelFormat = "%d"
    grafica.barLabels.fontName = "Helvetica"
    grafica.barLabels.fontSize = 7
    grafica.barLabels.fillColor = gris
    grafica.barLabels.nudge = 6

    dibujo.add(grafica)
    return dibujo


def lista_grupos_por_giro(giro_style, body_style, ancho=528, num_columnas=3):
    """Lista de grupos por giro acomodada en columnas para ocupar poco espacio."""
    grupos_por_giro = {}
    for nombre, id_grupo in CATALOGO_IDS.items():
        giro = id_grupo.split("-")[1]
        grupos = grupos_por_giro.setdefault(giro, {})
        # Algunos grupos aparecen dos veces (con y sin acento); se deja
        # solo el primer nombre de cada ID
        grupos.setdefault(id_grupo, nombre)

    # Se reparten los giros en columnas, en orden, con un número parecido de
    # renglones en cada una (cada giro cuenta su título + sus grupos)
    total_renglones = sum(len(g) + 1 for g in grupos_por_giro.values())
    limite = total_renglones / num_columnas * 1.1
    columnas = [[]]
    renglones = 0
    for giro, grupos in grupos_por_giro.items():
        tamano = len(grupos) + 1
        if renglones + tamano > limite and columnas[-1] and len(columnas) < num_columnas:
            columnas.append([])
            renglones = 0
        renglones += tamano
        columnas[-1].append(
            Paragraph(escape(NOMBRES_GIRO.get(giro, giro)), giro_style)
        )
        columnas[-1].append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(escape(formatear_nombre(n)), body_style),
                        leftIndent=12,
                    )
                    for n in grupos.values()
                ],
                bulletType="bullet",
                start="•",
                bulletFontSize=9,
                bulletColor=colors.HexColor("#2B6CB0"),
                leftIndent=12,
            )
        )
    while len(columnas) < num_columnas:
        columnas.append([])

    # Tabla sin bordes: solo sirve para acomodar las columnas lado a lado
    tabla = Table([columnas], colWidths=[ancho / num_columnas] * num_columnas)
    tabla.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tabla


class reporte_pdf:

    def __init__(self, data=None):
        self.data = data

    def crear_reporte(self):
        """Genera el PDF en memoria y regresa sus bytes.

        No se guarda ningún archivo en el servidor: los bytes se pueden pasar
        directo a st.download_button(data=...).
        """
        # Si ya se pasaron los datos al crear el reporte, no se vuelve a
        # consultar la base de datos
        if self.data is not None:
            datos_grupos = self.data
        else:
            datos_grupos = obtener_numero_eventos_grupos()

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )
        # Ancho disponible dentro de los márgenes (el marco deja 6 pt por lado)
        ancho_util = doc.width - 12
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            alignment=1,
            leading=24,
            textColor=colors.HexColor("#1A365D"),
            spaceAfter=10,
        )
        h2_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#2B6CB0"),
            spaceBefore=10,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#2D3748"),
        )
        giro_style = ParagraphStyle(
            "GiroLista",
            parent=body_style,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#1A365D"),
            spaceBefore=6,
            spaceAfter=2,
        )

        story.append(Paragraph("Reporte de Gestión", title_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Grupos Estudiantiles", h2_style))
        story.append(lista_grupos_por_giro(giro_style, body_style, ancho=ancho_util))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Estadísticas", title_style))
        if datos_grupos.empty:
            contenido_resumen = Paragraph(
                "No hay eventos registrados en la base de datos.", body_style
            )
        else:
            contenido_resumen = grafica_eventos_por_grupo(datos_grupos, ancho=ancho_util)
        # El subtítulo y la gráfica siempre quedan en la misma página
        story.append(KeepTogether([
            Paragraph("Resumen general", h2_style),
            contenido_resumen,
        ]))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Arte, Cultura y Entretenimiento", h2_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Deportivos y Recreativos", h2_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Ecología y Medio Ambiente", h2_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Liderazgo", h2_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Salud y Bienestar", h2_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Sentido Humano y E. Social", h2_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Vinculación Académica", h2_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Asociaciones Estudiantiles", h2_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("FETEC", h2_style))
        story.append(Spacer(1, 12))

        doc.build(story)
        return buffer.getvalue()
