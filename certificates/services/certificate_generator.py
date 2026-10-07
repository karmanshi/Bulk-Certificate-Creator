from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


def generate_certificate(recipient_name, output_path):

    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        str(output_path),
        pagesize=(page_width, page_height)
    )

    # --------------------------------------------------
    # Background
    # --------------------------------------------------

    pdf.setFillColor(colors.white)

    pdf.rect(
        0,
        0,
        page_width,
        page_height,
        fill=1,
        stroke=0
    )

    # --------------------------------------------------
    # Outer Border
    # --------------------------------------------------

    pdf.setStrokeColor(colors.HexColor("#1E3A8A"))
    pdf.setLineWidth(4)

    pdf.rect(
        25,
        25,
        page_width - 50,
        page_height - 50,
        fill=0,
        stroke=1
    )

    # Inner Border

    pdf.setStrokeColor(colors.HexColor("#C9A227"))
    pdf.setLineWidth(2)

    pdf.rect(
        35,
        35,
        page_width - 70,
        page_height - 70,
        fill=0,
        stroke=1
    )

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    pdf.setFillColor(colors.HexColor("#1E3A8A"))

    pdf.setFont(
        "Helvetica-Bold",
        32
    )

    pdf.drawCentredString(
        page_width / 2,
        page_height - 110,
        "CERTIFICATE"
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.setFillColor(
        colors.HexColor("#C9A227")
    )

    pdf.drawCentredString(
        page_width / 2,
        page_height - 145,
        "OF PARTICIPATION"
    )

    # --------------------------------------------------
    # Decorative Line
    # --------------------------------------------------

    pdf.setStrokeColor(
        colors.HexColor("#C9A227")
    )

    pdf.setLineWidth(2)

    pdf.line(
        page_width / 2 - 130,
        page_height - 165,
        page_width / 2 + 130,
        page_height - 165
    )

    # --------------------------------------------------
    # Body
    # --------------------------------------------------

    pdf.setFillColor(
        colors.HexColor("#333333")
    )

    pdf.setFont(
        "Helvetica",
        16
    )

    pdf.drawCentredString(
        page_width / 2,
        page_height - 215,
        "This certificate is proudly presented to"
    )

    # --------------------------------------------------
    # Recipient Name
    # --------------------------------------------------

    pdf.setFillColor(
        colors.HexColor("#1E3A8A")
    )

    pdf.setFont(
        "Helvetica-Bold",
        30
    )

    pdf.drawCentredString(
        page_width / 2,
        page_height - 265,
        recipient_name
    )

    # --------------------------------------------------
    # Description
    # --------------------------------------------------

    pdf.setFillColor(
        colors.HexColor("#444444")
    )

    pdf.setFont(
        "Helvetica",
        14
    )

    pdf.drawCentredString(
        page_width / 2,
        page_height - 310,
        "for successfully participating in the program."
    )

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.setFillColor(
        colors.HexColor("#555555")
    )

    pdf.drawCentredString(
        page_width / 2,
        90,
        "Bulk Certificate Generator"
    )

    # --------------------------------------------------
    # Signature
    # --------------------------------------------------

    pdf.setStrokeColor(
        colors.HexColor("#333333")
    )

    pdf.setLineWidth(1)

    signature_y = 120

    pdf.line(
        page_width / 2 - 80,
        signature_y,
        page_width / 2 + 80,
        signature_y
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawCentredString(
        page_width / 2,
        signature_y - 18,
        "Authorized Signature"
    )

    # --------------------------------------------------
    # Save PDF
    # --------------------------------------------------

    pdf.save()

output_path = Path("media/certificates/test_certificate.pdf")















