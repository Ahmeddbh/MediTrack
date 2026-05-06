from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class NumeredCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_graphic_state = None

    def showPage(self):
        self._add_page_number()
        canvas.Canvas.showPage(self)

    def _add_page_number(self):
        self.setFont("Helvetica", 9)
        self.drawString(19.5 * cm, 1 * cm, f"Página {self.getPageNumber()}")

def generar_pdf_profesional(nombre_archivo, doc, texto_informe):
    """
    Genera un PDF profesional con estructura de informe hospitalario
    """
    # Generar el informe de texto con IA
    pdf = SimpleDocTemplate(
        nombre_archivo, 
        pagesize=A4,
        leftMargin=1.5*cm, 
        rightMargin=1.5*cm,
        topMargin=2*cm, 
        bottomMargin=1.5*cm,
        canvasmaker=NumeredCanvas
    )
    
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=6,
        alignment=1,  # Centro
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        spaceAfter=12,
        alignment=1,
        fontName='Helvetica'
    )
    
    seccion_style = ParagraphStyle(
        'Seccion',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderColor=colors.HexColor('#1f77b4'),
        borderWidth=2,
        borderPadding=6,
        backColor=colors.HexColor('#f0f5fa')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    contenido = []
    
    # ============ ENCABEZADO ============
    encabezado_data = [
        [
            Paragraph("<b>MEDITRACK</b><br/>Sistema de Gestión de Ingresos Hospitalarios", 
                     ParagraphStyle('Header', parent=styles['Normal'], fontSize=14, 
                                   textColor=colors.HexColor('#1f77b4'), 
                                   fontName='Helvetica-Bold', alignment=0)),
            Paragraph(f"<b>INFORME CLÍNICO</b><br/>Nº: {str(doc.get('_id'))[:8]}", 
                     ParagraphStyle('HeaderRight', parent=styles['Normal'], fontSize=12, 
                                   textColor=colors.HexColor('#1f77b4'), 
                                   fontName='Helvetica-Bold', alignment=2))
        ]
    ]
    
    tabla_encabezado = Table(encabezado_data, colWidths=[10*cm, 8*cm])
    tabla_encabezado.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, -1), 2, colors.HexColor('#1f77b4')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    contenido.append(tabla_encabezado)
    contenido.append(Spacer(1, 0.3*cm))
    
    # ============ INFORMACIÓN DEL HOSPITAL Y PACIENTE ============
    info_data = [
        [
            Paragraph(f"<b>Hospital:</b> {doc.get('hospital', 'N/A')}", normal_style),
            Paragraph(f"<b>Médico:</b> {doc.get('doctor', 'N/A')}", normal_style)
        ],
        [
            Paragraph(f"<b>Fecha de Ingreso:</b> {doc.get('date_of_admission', 'N/A')}", normal_style),
            Paragraph(f"<b>Fecha de Alta:</b> {doc.get('discharge_date', 'N/A')}", normal_style)
        ]
    ]
    
    tabla_info = Table(info_data, colWidths=[9.5*cm, 9.5*cm])
    tabla_info.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    contenido.append(tabla_info)
    contenido.append(Spacer(1, 0.4*cm))
    
    # ============ DATOS DEL PACIENTE ============
    contenido.append(Paragraph("DATOS DEL PACIENTE", seccion_style))
    
    paciente_data = [
        [
            Paragraph(f"<b>Nombre:</b> {doc.get('name', 'N/A')}", normal_style),
            Paragraph(f"<b>Edad:</b> {doc.get('age', 'N/A')} años", normal_style)
        ],
        [
            Paragraph(f"<b>Género:</b> {doc.get('gender', 'N/A')}", normal_style),
            Paragraph(f"<b>Grupo Sanguíneo:</b> {doc.get('blood_type', 'N/A')}", normal_style)
        ],
        [
            Paragraph(f"<b>Aseguradora:</b> {doc.get('insurance_provider', 'N/A')}", normal_style),
            Paragraph(f"<b>Habitación:</b> {doc.get('room_number', 'N/A')}", normal_style)
        ]
    ]
    
    tabla_paciente = Table(paciente_data, colWidths=[9.5*cm, 9.5*cm])
    tabla_paciente.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
    ]))
    contenido.append(tabla_paciente)
    contenido.append(Spacer(1, 0.4*cm))
    
    # ============ INFORMACIÓN CLÍNICA ============
    contenido.append(Paragraph("INFORMACIÓN CLÍNICA", seccion_style))
    
    clinica_data = [
        [
            Paragraph(f"<b>Diagnóstico:</b><br/>{doc.get('medical_condition', 'N/A')}", normal_style),
            Paragraph(f"<b>Tipo de Ingreso:</b><br/>{doc.get('admission_type', 'N/A')}", normal_style)
        ],
        [
            Paragraph(f"<b>Resultado de Pruebas:</b><br/>{doc.get('test_results', 'N/A')}", normal_style),
            Paragraph(f"<b>Días de Estancia:</b><br/>{doc.get('stay_days', 'N/A')} días", normal_style)
        ]
    ]
    
    tabla_clinica = Table(clinica_data, colWidths=[9.5*cm, 9.5*cm])
    tabla_clinica.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
    ]))
    contenido.append(tabla_clinica)
    contenido.append(Spacer(1, 0.4*cm))
    
    # ============ INFORMACIÓN ADICIONAL ============
    if doc.get('antecedentes'):
        contenido.append(Paragraph("ANTECEDENTES / MOTIVO DE CONSULTA", seccion_style))
        contenido.append(Paragraph(doc.get('antecedentes'), normal_style))
        contenido.append(Spacer(1, 0.3*cm))
    
    # ============ INFORME CLÍNICO GENERADO POR IA ============
    contenido.append(Paragraph("INFORME CLÍNICO DETALLADO", seccion_style))
    
    # Parsear el informe de texto para mejor formato
    lineas = texto_informe.split('\n')
    for linea in lineas:
        linea = linea.strip()
        if linea:
            # Detectar títulos de secciones (líneas que terminan con :)
            if linea.endswith(':') and len(linea) < 100:
                estilo_titulo = ParagraphStyle(
                    'TituloSeccion',
                    parent=styles['Normal'],
                    fontSize=11,
                    fontName='Helvetica-Bold',
                    textColor=colors.HexColor('#1f77b4'),
                    spaceAfter=4,
                    spaceBefore=8
                )
                contenido.append(Paragraph(linea, estilo_titulo))
            else:
                contenido.append(Paragraph(linea, normal_style))
    
    contenido.append(Spacer(1, 0.4*cm))
    
    # ============ INFORMACIÓN DE MEDICACIÓN ============
    fda_info = doc.get('fda_info') or {}
    if fda_info:
        contenido.append(Paragraph("INFORMACIÓN FARMACOLÓGICA", seccion_style))
        
        med_data = [
            [Paragraph("<b>Medicamento:</b>", normal_style), 
             Paragraph(doc.get('medication', 'N/A'), normal_style)],
            [Paragraph("<b>Dosis / Frecuencia:</b>", normal_style), 
             Paragraph(doc.get('dosage', 'No especificada'), normal_style)],
            [Paragraph("<b>Nombre Comercial:</b>", normal_style), 
             Paragraph(fda_info.get('brand_name', 'No disponible'), normal_style)],
            [Paragraph("<b>Nombre Genérico:</b>", normal_style), 
             Paragraph(fda_info.get('generic_name', 'No disponible'), normal_style)],
        ]
        
        tabla_med = Table(med_data, colWidths=[4*cm, 15*cm])
        tabla_med.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f5fa')),
        ]))
        contenido.append(tabla_med)
        contenido.append(Spacer(1, 0.3*cm))
    
    # ============ COMENTARIOS DEL MÉDICO ============
    if doc.get('comentarios'):
        contenido.append(Paragraph("COMENTARIOS DEL MÉDICO", seccion_style))
        contenido.append(Paragraph(doc.get('comentarios'), normal_style))
        contenido.append(Spacer(1, 0.3*cm))
    
    # ============ INFORMACIÓN FINANCIERA ============
    contenido.append(Paragraph("INFORMACIÓN ADMINISTRATIVA", seccion_style))
    
    admin_data = [
        [Paragraph(f"<b>Importe Facturado:</b> ${doc.get('billing_amount', 0):.2f} USD", normal_style)]
    ]
    
    tabla_admin = Table(admin_data, colWidths=[19*cm])
    tabla_admin.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    contenido.append(tabla_admin)
    
    # ============ PIE DE PÁGINA ============
    contenido.append(Spacer(1, 0.5*cm))
    pie_style = ParagraphStyle(
        'Pie',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#999999'),
        alignment=1
    )
    contenido.append(Paragraph(
        f"Documento generado automáticamente por MediTrack el {datetime.now().strftime('%d/%m/%Y a las %H:%M')} | "
        "Sistema de Gestión de Ingresos Hospitalarios - Bases de Datos Avanzadas 2025/2026",
        pie_style
    ))
    
    # Construir PDF
    pdf.build(contenido)
