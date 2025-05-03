
from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import io
from datetime import datetime
import os

app = Flask(__name__)
INVOICE_COUNTER_FILE = "invoice_counter.txt"

def get_next_invoice_number():
    if not os.path.exists(INVOICE_COUNTER_FILE):
        with open(INVOICE_COUNTER_FILE, "w") as f:
            f.write("1")
            return 1
    with open(INVOICE_COUNTER_FILE, "r+") as f:
        num = int(f.read().strip()) + 1
        f.seek(0)
        f.write(str(num))
        f.truncate()
        return num

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    client_name = request.form['client_name']
    amount_per_container = int(request.form['amount_per_container'])
    containers = request.form['containers'].splitlines()
    total_amount = amount_per_container * len(containers)
    invoice_number = get_next_invoice_number()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "INVOICE", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    pdf.multi_cell(0, 10, "PICKLOAD MOVERS LIMITED\nP. O. Box 41069 - 80100 CHANGAMWE MSA KE\nNairobi - Kenya\nTel: 0796 497 074, 0729 211 882")

    pdf.ln(5)
    pdf.cell(0, 10, f"Invoice Number: INV-{invoice_number:04}", ln=True)
    pdf.cell(0, 10, f"Invoice Date: {datetime.today().strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(0, 10, f"Client Name: {client_name}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, f"Number of Containers: {len(containers)}", ln=True)
    pdf.cell(0, 10, f"Amount per Container: KES {amount_per_container:,}", ln=True)
    pdf.cell(0, 10, f"Total Amount: KES {total_amount:,}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, "Container Numbers:", ln=True)
    for container in containers:
        pdf.cell(0, 10, f"- {container.strip()}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Payment Instructions", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Bank: ABSA Bank", ln=True)
    pdf.cell(0, 10, "Account Name: Pickload Movers Limited", ln=True)
    pdf.cell(0, 10, "Account Number: 2053231554", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Terms & Conditions", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, "1. Payment is due within 10 days of invoice date.\n2. All bank charges are to be borne by the payer.\n3. Please include the invoice number as reference when making payment.")

    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    return send_file(output, download_name=f'invoice_INV-{invoice_number:04}.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
