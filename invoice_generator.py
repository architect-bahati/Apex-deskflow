import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_invoice(client_name, items, invoice_number="INV-1001"):
    """
    Generates a professional PDF invoice.
    items: List of tuples -> [("Item/Service Name", Quantity, Unit Price KES), ...]
    """
    pdf_filename = f"Invoice_{invoice_number}_{client_name.replace(' ', '_')}.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=colors.HexColor('#0d1117'),
        alignment=0,
        spaceAfter=5
    )
    
    sub_style = ParagraphStyle(
        'SubStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#57606a'),
        spaceAfter=15
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#24292e'),
        spaceAfter=4
    )

    elements = []

    # Business Header
    elements.append(Paragraph("APEX SOFTWARE HUB", title_style))
    elements.append(Paragraph("Software Development & Digital Solutions | Kenya", sub_style))
    elements.append(Spacer(1, 10))

    # Invoice Details Table
    today_str = datetime.now().strftime("%Y-%m-%d")
    info_data = [
        [f"<b>Billed To:</b> {client_name}", f"<b>Invoice No:</b> {invoice_number}"],
        [f"<b>Payment Status:</b> Pending / Paid", f"<b>Date:</b> {today_str}"]
    ]
    info_table = Table(info_data, colWidths=[260, 240])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#24292e')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Items Breakdown
    table_data = [["Description", "Qty", "Unit Price (KES)", "Total (KES)"]]
    
    subtotal = 0
    for desc, qty, price in items:
        item_total = qty * price
        subtotal += item_total
        table_data.append([desc, str(qty), f"{price:,.2f}", f"{item_total:,.2f}"])

    table_data.append(["", "", "Grand Total:", f"KES {subtotal:,.2f}"])

    item_table = Table(table_data, colWidths=[240, 50, 110, 100])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f6beb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.HexColor('#d0d7de')),
        ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (2, -1), (-1, -1), colors.HexColor('#f6f8fa')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(item_table)
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("<b>Payment Info:</b> M-Pesa / Bank Transfer accepted.", normal_style))
    elements.append(Paragraph("Thank you for your business!", sub_style))

    doc.build(elements)
    print(f"✅ Generated Invoice: {pdf_filename}")

# Quick Test
if __name__ == "__main__":
    sample_items = [
        ("Web Development (Apex Hub)", 1, 15000),
        ("Python Desktop Automation Setup", 1, 8000),
    ]
    create_invoice("Client Enterprise", sample_items, "INV-1002")