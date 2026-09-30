from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from consultas import obtener_numero_eventos_grupos


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
        header_table_style = ParagraphStyle(
            "HeaderTable",
            parent=body_style,
            fontName="Helvetica-Bold",
            textColor=colors.white,
            alignment=1,
        )
        estilo_tabla = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A365D")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#F7FAFC")],
                ),
            ]
        )

        matriz_grupos = [
            [
                Paragraph("Grupos Estudiantiles", header_table_style),
                Paragraph("", header_table_style),
                Paragraph("", header_table_style),
            ],
            [
                Paragraph("Art at Tec", body_style),
                Paragraph("Bloom Craft", body_style),
                Paragraph("Court Club", body_style),
            ],
            [
                Paragraph("Cinephoria", body_style),
                Paragraph("SEING", body_style),
                Paragraph("SEAAD", body_style),
            ],
            [
                Paragraph("SENEG", body_style),
                Paragraph("SELAET", body_style),
                Paragraph("SEPREPA", body_style),
            ],
        ]
        tabla_grupos = Table(matriz_grupos, colWidths=[80, 80, 80])
        tabla_grupos.setStyle(estilo_tabla)
        tabla_grupos.setStyle([("SPAN", (0, 0), (2, 0))])  # Unifica el encabezado

        # Tabla con el número de eventos de cada grupo (datos de la hoja)
        if datos_grupos.empty:
            tabla_eventos = Paragraph(
                "No hay eventos registrados en la base de datos.", body_style
            )
        else:
            matriz_datos = [[
                Paragraph("Grupo Estudiantil", header_table_style),
                Paragraph("Eventos", header_table_style),
            ]]
            for grupo, eventos in zip(datos_grupos["Grupo"], datos_grupos["Eventos"]):
                matriz_datos.append([
                    # escape() evita que un "<" o "&" en la hoja rompa el PDF
                    Paragraph(escape(str(grupo)), body_style),
                    Paragraph(str(eventos), body_style),
                ])
            tabla_eventos = Table(
                matriz_datos, colWidths=[300, 80], repeatRows=1
            )
            tabla_eventos.setStyle(estilo_tabla)

        story.append(Paragraph("Reporte de Gestión", title_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Grupos Estudiantiles", h2_style))
        story.append(tabla_grupos)
        story.append(Spacer(1, 8))
        story.append(tabla_eventos)
        story.append(Spacer(1, 12))
        story.append(Paragraph("Estadísticas por Giro", title_style))
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
