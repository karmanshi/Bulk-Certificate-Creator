from pathlib import Path 
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas 

def generate_certificate(recipient_name, output_path):
    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        str(output_path),
        pagesize=(page_width,page_height)

    )

    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
        page_width/2,
        page_height - 120,
        "CERTIFICATE OF PARTICIPATION"
    )

    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        page_width/2,
        page_height - 250,
        recipient_name
    )

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(
        page_width/2,
        100,
        "Thank you for your participation"
    )
    pdf.save()

output_path = Path("media/certificates/test_certificate.pdf")















