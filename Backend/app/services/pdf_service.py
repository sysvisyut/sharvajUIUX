from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from io import BytesIO
from datetime import datetime
import os

class PDFService:
    """Service for generating PDF reports"""
    
    @staticmethod
    def generate_credit_report(user_data, financial_data, score_data):
        """Generate comprehensive credit score report PDF"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build the document
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=HexColor('#2E86C1'),
                alignment=1  # Center alignment
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=HexColor('#1B4F72'),
                borderWidth=1,
                borderColor=HexColor('#2E86C1'),
                borderPadding=5,
                backColor=HexColor('#EBF5FB')
            )
            
            # Title and Header
            story.append(Paragraph("Credit Score Analysis Report", title_style))
            story.append(Spacer(1, 20))
            
            # Report metadata
            report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
            story.append(Paragraph(f"Generated on: {report_date}", styles['Normal']))
            story.append(Spacer(1, 30))
            
            # Credit Score Summary Section
            story.append(Paragraph("Credit Score Summary", heading_style))
            
            credit_score = score_data.get('credit_score', 0)
            score_color = PDFService._get_score_color(credit_score)
            
            score_table_data = [
                ['Credit Score', f"<font color='{score_color}'><b>{credit_score}</b></font>"],
                ['Score Range', PDFService._get_score_range(credit_score)],
                ['Loan Approval Status', 'Approved' if score_data.get('loan_approved') else 'Not Approved'],
                ['Best Achievable Score', str(score_data.get('best_achievable_score', 850))],
                ['Last Updated', score_data.get('calculated_at', '')[:10] if score_data.get('calculated_at') else 'N/A']
            ]
            
            score_table = Table(score_table_data, colWidths=[3*inch, 2*inch])
            score_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E86C1')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9FA')),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#BDC3C7'))
            ]))
            
            story.append(score_table)
            story.append(Spacer(1, 20))
            
            # Score Factors Section
            if score_data.get('score_factors'):
                story.append(Paragraph("Credit Score Factors", heading_style))
                
                factors_data = [['Factor', 'Weight', 'Status']]
                for factor in score_data['score_factors']:
                    status_color = '#27AE60' if factor['status'] == 'good' else '#E74C3C' if factor['status'] == 'poor' else '#F39C12'
                    factors_data.append([
                        factor['factor'],
                        f"{factor['weight']}%",
                        f"<font color='{status_color}'><b>{factor['status'].upper()}</b></font>"
                    ])
                
                factors_table = Table(factors_data, colWidths=[2.5*inch, 1*inch, 1.5*inch])
                factors_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E86C1')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9FA')),
                    ('GRID', (0, 0), (-1, -1), 1, HexColor('#BDC3C7'))
                ]))
                
                story.append(factors_table)
                story.append(Spacer(1, 20))
            
            # Personal Information Section
            story.append(Paragraph("Personal Information", heading_style))
            
            personal_info = financial_data.get('personal_info', {})
            personal_data = [
                ['Age', str(personal_info.get('age', 'N/A'))],
                ['State', personal_info.get('state', 'N/A')],
                ['Education Level', personal_info.get('education_level', 'N/A')]
            ]
            
            personal_table = Table(personal_data, colWidths=[2*inch, 3*inch])
            personal_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), HexColor('#E8F6F3')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#BDC3C7'))
            ]))
            
            story.append(personal_table)
            story.append(Spacer(1, 15))
            
            # Employment & Income Section
            employment_info = financial_data.get('employment_income', {})
            story.append(Paragraph("Employment & Income", heading_style))
            
            employment_data = [
                ['Employment Type', employment_info.get('employment_type', 'N/A')],
                ['Annual Income', f"${employment_info.get('annual_income', 0):,}"],
                ['Job Duration', employment_info.get('job_duration', 'N/A')]
            ]
            
            employment_table = Table(employment_data, colWidths=[2*inch, 3*inch])
            employment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), HexColor('#E8F6F3')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#BDC3C7'))
            ]))
            
            story.append(employment_table)
            story.append(Spacer(1, 20))
            
            # Financial Insights Section
            if score_data.get('insights'):
                story.append(Paragraph("Financial Insights & Recommendations", heading_style))
                
                for insight in score_data['insights']:
                    icon = PDFService._get_insight_icon(insight['type'])
                    insight_text = f"{icon} <b>{insight['title']}</b>: {insight['message']}"
                    story.append(Paragraph(insight_text, styles['Normal']))
                    story.append(Spacer(1, 10))
                
                story.append(Spacer(1, 20))
            
            # Disclaimer
            story.append(Paragraph("Important Information", heading_style))
            disclaimer = """This credit score analysis is generated by our proprietary algorithm and is for informational purposes only. 
            This score may differ from scores provided by other credit bureaus or lenders. The recommendations provided are general 
            financial guidance and should not be considered as personalized financial advice. Please consult with a qualified 
            financial advisor for specific guidance regarding your financial situation."""
            
            story.append(Paragraph(disclaimer, styles['Normal']))
            
            # Build the PDF
            doc.build(story)
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            raise Exception(f"PDF generation error: {str(e)}")
    
    @staticmethod
    def _get_score_color(score):
        """Get color based on credit score"""
        if score >= 750:
            return '#27AE60'  # Green
        elif score >= 700:
            return '#F39C12'  # Orange
        elif score >= 650:
            return '#E67E22'  # Dark Orange
        else:
            return '#E74C3C'  # Red
    
    @staticmethod
    def _get_score_range(score):
        """Get score range description"""
        if score >= 800:
            return 'Exceptional (800-850)'
        elif score >= 750:
            return 'Excellent (750-799)'
        elif score >= 700:
            return 'Good (700-749)'
        elif score >= 650:
            return 'Fair (650-699)'
        elif score >= 600:
            return 'Poor (600-649)'
        else:
            return 'Very Poor (300-599)'
    
    @staticmethod
    def _get_insight_icon(insight_type):
        """Get emoji icon for insight type"""
        icons = {
            'positive': '✅',
            'warning': '⚠️',
            'tip': '💡',
            'info': 'ℹ️'
        }
        return icons.get(insight_type, '•')
