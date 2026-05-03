# ⚡ InvoiceGen — Flask Invoice Generator

A clean, professional invoice generator web app built with Flask + ReportLab.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open in browser
http://127.0.0.1:5000
```

## 📁 Project Structure

```
invoice_app/
├── app.py                  # Flask routes & entry point
├── requirements.txt        # Python dependencies
├── README.md
│
├── utils/
│   ├── __init__.py
│   └── pdf_generator.py    # ReportLab PDF logic (isolated here)
│
├── templates/
│   └── index.html          # The invoice form UI
│
├── static/
│   └── css/
│       └── style.css       # All styling
│
└── generated_invoices/     # PDFs saved here temporarily (auto-created)
```

## 🔧 Customisation Ideas (to make it sellable)

| Feature | How |
|---|---|
| Multi-line items | Add a JS "Add Item" button; send as JSON; loop in pdf_generator |
| Logo upload | `request.files`, save to disk, embed image in PDF with ReportLab |
| Currency selector | Dropdown → pass currency symbol to pdf_generator |
| Tax % field | Already stubbed in pdf_generator.py (`tax_rate`) |
| User accounts | Add Flask-Login + SQLite to save invoice history |
| Email invoice | Flask-Mail or SendGrid API |
| Recurring invoices | APScheduler or Celery + cron |
| Stripe payments | Add a "Pay Now" link using Stripe Payment Links |

## 🌐 Deploying (free tiers)

- **Railway** — `railway up` (easiest, no config)
- **Render** — connect GitHub repo, set start command to `python app.py`
- **PythonAnywhere** — good for Flask beginners

## 📄 License
MIT — free to use, modify, and sell.
