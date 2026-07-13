from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class PDFService:
    def generate_invoice(self, order):

        filename = f'storage/invoices/invoice_{order}.pdf'

        pdf = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        content = [
            Paragraph(f'Invoice #{order.id}', styles['Title']),
            Paragraph(f'Status: {order.status}', styles['Normal']),
            Paragraph(f'Total: ${order.total_price}', styles['Normal'])
        ]
        
        pdf.build(content)


        return filename

