from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

class PDFService:
    def generate_invoice(self, order):

        os.makedirs("storage/invoices", exist_ok=True)
        filename = f'storage/invoices/invoice_{order.id}.pdf'

        pdf = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        content = [
            Paragraph(f'Invoice #{order.id}', styles['Title']),
            Paragraph(f'Status: {order.status}', styles['Normal']),
            Paragraph(f'Total: ${order.total_price}', styles['Normal'])
        ]
        
        pdf.build(content)


        return filename

