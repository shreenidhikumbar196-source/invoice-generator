"""
utils/pdf_generator.py
Handles all PDF creation logic using ReportLab.
Kept separate from app.py to keep concerns clean.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from datetime import date
import os


# ──────────────────────────────────────────────
# Color palette — tweak these to rebrand quickly
# ──────────────────────────────────────────────
ACCENT      = colors.HexColor("#1A1A2E")   # dark navy
ACCENT_LITE = colors.HexColor("#16213E")   # slightly lighter navy
HIGHLIGHT   = colors.HexColor("#E94560")   # vivid red-pink accent
LIGHT_BG    = colors.HexColor("#F4F6FA")   # soft grey background
MID_GREY    = colors.HexColor("#8892A4")   # muted text
WHITE       = colors.white


def build_styles():
    """Return a dict of custom Paragraph styles."""
    base = getSampleStyleSheet()

    styles = {
        "company": ParagraphStyle(
            "company",
            fontName="Helvetica-Bold",
            fontSize=22,
            textColor=WHITE,
            leading=26,
        ),
        "tagline": ParagraphStyle(
            "tagline",
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.HexColor("#CBD5E1"),
            leading=14,
        ),
        "invoice_label": ParagraphStyle(
            "invoice_label",
            fontName="Helvetica-Bold",
            fontSize=28,
            textColor=WHITE,
            alignment=TA_RIGHT,
            leading=32,
        ),
        "invoice_sub": ParagraphStyle(
            "invoice_sub",
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.HexColor("#CBD5E1"),
            alignment=TA_RIGHT,
            leading=14,
        ),
        "section_header": ParagraphStyle(
            "section_header",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=HIGHLIGHT,
            spaceAfter=4,
            leading=12,
            letterSpacing=1.5,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=10,
            textColor=ACCENT,
            leading=16,
        ),
        "body_bold": ParagraphStyle(
            "body_bold",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=ACCENT,
            leading=16,
        ),
        "small_grey": ParagraphStyle(
            "small_grey",
            fontName="Helvetica",
            fontSize=8,
            textColor=MID_GREY,
            leading=12,
        ),
        "total_label": ParagraphStyle(
            "total_label",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=WHITE,
            alignment=TA_LEFT,
        ),
        "total_value": ParagraphStyle(
            "total_value",
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=WHITE,
            alignment=TA_RIGHT,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Helvetica",
            fontSize=8,
            textColor=MID_GREY,
            alignment=TA_CENTER,
            leading=12,
        ),
    }
    return styles


def generate_invoice_pdf(data: dict, output_dir: str) -> str:
    """
    Build a professional invoice PDF and save it to output_dir.

    Args:
        data: dict with keys — your_name, client_name, service,
              amount (float), invoice_number, notes
        output_dir: folder path where the PDF will be saved

    Returns:
        Full path to the generated PDF file.
    """
    today         = date.today()
    date_str      = today.strftime("%B %d, %Y")
    due_date_str  = date.today().replace(
        month=today.month % 12 + 1 if today.month < 12 else 1,
        year=today.year + (1 if today.month == 12 else 0)
    ).strftime("%B %d, %Y")

    filename  = f"Invoice_{data['invoice_number']}_{data['client_name'].replace(' ', '_')}.pdf"
    filepath  = os.path.join(output_dir, filename)

    # Page margins
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
    )

    W = A4[0] - 30*mm   # usable width
    styles = build_styles()
    story  = []         # ReportLab builds the PDF from this list of elements

    # ── HEADER BANNER ──────────────────────────────────────────────────────────
    header_data = [[
        Paragraph(data["your_name"], styles["company"]),
        Paragraph("INVOICE", styles["invoice_label"]),
    ]]
    header_table = Table(header_data, colWidths=[W * 0.55, W * 0.45])
    header_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), ACCENT),
        ("TOPPADDING",  (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING",(0,0), (-1, -1), 14),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",(0, 0), (-1, -1), 14),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(header_table)

    # Sub-header row: tagline + invoice meta
    sub_data = [[
        Paragraph("Professional Services", styles["tagline"]),
        Paragraph(
            f"Invoice No: <b>#{data['invoice_number']}</b><br/>"
            f"Date: {date_str}<br/>Due: {due_date_str}",
            styles["invoice_sub"]
        ),
    ]]
    sub_table = Table(sub_data, colWidths=[W * 0.55, W * 0.45])
    sub_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), ACCENT_LITE),
        ("TOPPADDING",  (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0,0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",(0, 0), (-1, -1), 14),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(sub_table)
    story.append(Spacer(1, 8*mm))

    # ── BILLED TO / FROM SECTION ──────────────────────────────────────────────
    billed_data = [[
        # Left: Billed To
        [
            Paragraph("BILLED TO", styles["section_header"]),
            Paragraph(data["client_name"], styles["body_bold"]),
            Paragraph("client@email.com", styles["small_grey"]),
        ],
        # Right: From
        [
            Paragraph("FROM", styles["section_header"]),
            Paragraph(data["your_name"], styles["body_bold"]),
            Paragraph("your@email.com", styles["small_grey"]),
        ],
    ]]

    billed_table = Table(billed_data, colWidths=[W * 0.5, W * 0.5])
    billed_table.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(billed_table)
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0")))
    story.append(Spacer(1, 6*mm))

    # ── LINE ITEMS TABLE ───────────────────────────────────────────────────────
    story.append(Paragraph("SERVICES", styles["section_header"]))
    story.append(Spacer(1, 2*mm))

    # Table headers
    items_header = [
        Paragraph("DESCRIPTION", styles["section_header"]),
        Paragraph("QTY", styles["section_header"]),
        Paragraph("RATE", styles["section_header"]),
        Paragraph("AMOUNT", styles["section_header"]),
    ]

    # Table row(s) — for now one service; easy to extend into multiple items
    amount = data["amount"]
    items_row = [
        Paragraph(data["service"], styles["body"]),
        Paragraph("1", styles["body"]),
        Paragraph(f"${amount:,.2f}", styles["body"]),
        Paragraph(f"${amount:,.2f}", styles["body"]),
    ]

    items_table = Table(
        [items_header, items_row],
        colWidths=[W * 0.50, W * 0.12, W * 0.18, W * 0.20],
    )
    items_table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND",    (0, 0), (-1, 0), LIGHT_BG),
        ("TOPPADDING",    (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        # Data rows
        ("TOPPADDING",    (0, 1), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 10),
        ("BACKGROUND",    (0, 1), (-1, -1), WHITE),
        # Borders
        ("LINEBELOW",     (0, 0), (-1, 0), 0.5, colors.HexColor("#E2E8F0")),
        ("LINEBELOW",     (0, 1), (-1, -1), 0.5, colors.HexColor("#F1F5F9")),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        # Right-align numeric columns
        ("ALIGN",         (1, 0), (-1, -1), "RIGHT"),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 4*mm))

    # ── TOTALS BOX ─────────────────────────────────────────────────────────────
    tax_rate  = 0.0        # set a % here if you want tax (e.g. 0.18 for 18%)
    tax_amt   = amount * tax_rate
    total     = amount + tax_amt

    totals_rows = []
    totals_rows.append([
        Paragraph("Subtotal", styles["small_grey"]),
        Paragraph(f"${amount:,.2f}", styles["small_grey"]),
    ])
    if tax_rate > 0:
        totals_rows.append([
            Paragraph(f"Tax ({int(tax_rate*100)}%)", styles["small_grey"]),
            Paragraph(f"${tax_amt:,.2f}", styles["small_grey"]),
        ])

    totals_table = Table(totals_rows, colWidths=[W * 0.78, W * 0.22])
    totals_table.setStyle(TableStyle([
        ("ALIGN",         (1, 0), (1, -1), "RIGHT"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(totals_table)

    # Total due — highlighted bar
    total_bar_data = [[
        Paragraph("TOTAL DUE", styles["total_label"]),
        Paragraph(f"${total:,.2f}", styles["total_value"]),
    ]]
    total_bar = Table(total_bar_data, colWidths=[W * 0.6, W * 0.4])
    total_bar.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), HIGHLIGHT),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(total_bar)
    story.append(Spacer(1, 8*mm))

    # ── NOTES SECTION ─────────────────────────────────────────────────────────
    if data.get("notes"):
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0")))
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph("NOTES", styles["section_header"]))
        story.append(Paragraph(data["notes"], styles["body"]))
        story.append(Spacer(1, 6*mm))

    # ── PAYMENT INFO ──────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0")))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("PAYMENT INFORMATION", styles["section_header"]))
    pay_info = [
        ["Bank / Payment Method:", "Add your bank or UPI / PayPal details here"],
        ["Account Name:",          data["your_name"]],
    ]
    pay_table = Table(pay_info, colWidths=[W * 0.3, W * 0.7])
    pay_table.setStyle(TableStyle([
        ("FONTNAME",      (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("TEXTCOLOR",     (0, 0), (-1, -1), ACCENT),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ]))
    story.append(pay_table)
    story.append(Spacer(1, 8*mm))

    # ── FOOTER ────────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0")))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        f"Thank you for your business, {data['client_name']}! · "
        "Payment is due within 30 days of invoice date.",
        styles["footer"]
    ))

    # Build and save the PDF
    doc.build(story)
    return filepath
