"""
Modern PDF Report Generator with Charts and Graphics
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime, timedelta
import os
from pathlib import Path

class ModernPDFGenerator:
    """Generate modern, visually appealing PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Info text
        self.styles.add(ParagraphStyle(
            name='InfoText',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#475569'),
            spaceAfter=6
        ))
    
    def create_bar_chart(self, data, width=400, height=200):
        """Create a modern bar chart"""
        drawing = Drawing(width, height)
        
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = height - 80
        bc.width = width - 100
        bc.data = [data['values']]
        bc.categoryAxis.categoryNames = data['labels']
        
        # Styling
        bc.bars[0].fillColor = colors.HexColor('#3b82f6')
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max(data['values']) * 1.2 if data['values'] else 100
        bc.valueAxis.valueStep = max(data['values']) / 5 if data['values'] else 20
        
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 45
        bc.categoryAxis.labels.fontSize = 9
        
        bc.valueAxis.labels.fontSize = 9
        
        drawing.add(bc)
        return drawing
    
    def create_pie_chart(self, data, width=300, height=200):
        """Create a modern pie chart"""
        drawing = Drawing(width, height)
        
        pie = Pie()
        pie.x = 50
        pie.y = 50
        pie.width = 150
        pie.height = 150
        pie.data = data['values']
        pie.labels = data['labels']
        
        # Color scheme
        colors_list = [
            colors.HexColor('#3b82f6'),  # Blue
            colors.HexColor('#10b981'),  # Green
            colors.HexColor('#f59e0b'),  # Amber
            colors.HexColor('#ef4444'),  # Red
            colors.HexColor('#8b5cf6'),  # Purple
        ]
        
        for i, color in enumerate(colors_list[:len(data['values'])]):
            pie.slices[i].fillColor = color
        
        pie.slices.strokeWidth = 1
        pie.slices.strokeColor = colors.white
        
        drawing.add(pie)
        return drawing
    
    def create_stats_table(self, stats_data):
        """Create a styled statistics table"""
        data = [['Metrik', 'Değer']]
        
        for key, value in stats_data.items():
            data.append([key, str(value)])
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Body
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return table
    
    def create_sessions_table(self, sessions):
        """Create a detailed sessions table"""
        data = [['Kabin', 'Öğrenci', 'Başlangıç', 'Bitiş', 'Süre (dk)']]
        
        for session in sessions[:20]:  # Max 20 sessions
            start_time = session.get('start_time')
            end_time = session.get('end_time')
            duration = session.get('duration', 0)
            
            # Format times
            start_str = start_time.strftime('%d/%m %H:%M') if start_time else '-'
            end_str = end_time.strftime('%d/%m %H:%M') if end_time else '-'
            duration_min = round(duration / 60, 1)
            
            data.append([
                str(session.get('cabin_no', '-')),
                session.get('student_name', 'N/A'),
                start_str,
                end_str,
                str(duration_min)
            ])
        
        table = Table(data, colWidths=[0.8*inch, 1.5*inch, 1.3*inch, 1.3*inch, 1*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            
            # Body
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return table
    
    def generate_report(self, report_data, output_path):
        """
        Generate complete PDF report
        
        report_data = {
            'type': 'daily/weekly/monthly',
            'title': 'Report Title',
            'period': 'Date Range',
            'student_name': 'Student Name',
            'cabin_no': 1,
            'stats': {
                'Toplam Saat': '12.5',
                'Oturum Sayısı': '8',
                'Ortalama Oturum': '1.5 saat',
                'En Uzun Oturum': '3.2 saat'
            },
            'sessions': [...],  # List of session dicts
            'daily_breakdown': {
                'labels': ['Pts', 'Sal', 'Çar', ...],
                'values': [5, 8, 6, ...]
            }
        }
        """
        # Create reports directory if not exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Title
        title = Paragraph(report_data['title'], self.styles['CustomTitle'])
        elements.append(title)
        
        # Subtitle with period
        subtitle = Paragraph(f"<b>Dönem:</b> {report_data['period']}", self.styles['Subtitle'])
        elements.append(subtitle)
        
        # Student/Cabin info
        if report_data.get('student_name'):
            info_text = f"<b>Öğrenci:</b> {report_data['student_name']}"
            if report_data.get('cabin_no'):
                info_text += f" | <b>Kabin:</b> {report_data['cabin_no']}"
            info = Paragraph(info_text, self.styles['InfoText'])
            elements.append(info)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Statistics section
        elements.append(Paragraph("📊 İstatistikler", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.1*inch))
        
        stats_table = self.create_stats_table(report_data['stats'])
        elements.append(stats_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Daily breakdown chart
        if report_data.get('daily_breakdown'):
            elements.append(Paragraph("📈 Günlük Dağılım", self.styles['SectionHeader']))
            elements.append(Spacer(1, 0.1*inch))
            
            chart = self.create_bar_chart(report_data['daily_breakdown'])
            elements.append(chart)
            
            elements.append(Spacer(1, 0.3*inch))
        
        # Sessions table
        if report_data.get('sessions') and len(report_data['sessions']) > 0:
            elements.append(Paragraph("📝 Oturum Detayları", self.styles['SectionHeader']))
            elements.append(Spacer(1, 0.1*inch))
            
            sessions_table = self.create_sessions_table(report_data['sessions'])
            elements.append(sessions_table)
            
            if len(report_data['sessions']) > 20:
                note = Paragraph(
                    f"<i>Not: İlk 20 oturum gösterilmektedir. Toplam {len(report_data['sessions'])} oturum.</i>",
                    self.styles['InfoText']
                )
                elements.append(Spacer(1, 0.1*inch))
                elements.append(note)
        
        # Footer with generation time
        elements.append(Spacer(1, 0.5*inch))
        footer_text = f"<i>Rapor Oluşturma Zamanı: {datetime.now().strftime('%d/%m/%Y %H:%M')}</i>"
        footer = Paragraph(footer_text, self.styles['InfoText'])
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        return output_path


# Global generator instance
pdf_generator = ModernPDFGenerator()
