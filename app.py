"""
Invoice Generator - Flask Backend
Main entry point for the web application
"""

from flask import Flask, render_template, request, send_file
from utils.pdf_generator import generate_invoice_pdf
import os

app = Flask(__name__)

# Folder to temporarily store generated PDFs
INVOICES_DIR = "generated_invoices"
os.makedirs(INVOICES_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    """Render the main invoice form page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """
    Handle form submission, generate PDF, and send it to the user.
    POST fields: your_name, client_name, service_description, amount
    """
    # Collect form data
    data = {
        "your_name":    request.form.get("your_name", "").strip(),
        "client_name":  request.form.get("client_name", "").strip(),
        "service":      request.form.get("service_description", "").strip(),
        "amount":       request.form.get("amount", "0").strip(),
        "invoice_number": request.form.get("invoice_number", "001").strip(),
        "notes":        request.form.get("notes", "").strip(),
    }

    # Basic validation
    if not all([data["your_name"], data["client_name"], data["service"], data["amount"]]):
        return render_template("index.html", error="Please fill in all required fields.")

    try:
        amount = float(data["amount"])
    except ValueError:
        return render_template("index.html", error="Amount must be a valid number.")

    data["amount"] = amount

    # Generate the PDF and get the file path back
    pdf_path = generate_invoice_pdf(data, INVOICES_DIR)

    # Stream the file to the user as a download
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"Invoice_{data['invoice_number']}.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    # Debug mode ON for development; set debug=False in production
    app.run(debug=True)
