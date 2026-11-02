from fpdf import FPDF

METHOD_LABELS = {
    "especes": "Especes",
    "cheque": "Cheque",
    "virement": "Virement",
    "mobile_money": "Mobile Money",
}

class ReceiptPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "EduPaie - Recu de paiement", border=False, align="C")
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_receipt_pdf(receipt_data, output_path):
    pdf = ReceiptPDF()
    pdf.add_page()
    
    pdf.set_font("Helvetica", size=12)
    
    # Informations générales
    pdf.cell(0, 8, f"Numero de recu : {receipt_data['receipt_number']}", ln=True)
    pdf.cell(0, 8, f"Date du paiement : {receipt_data['payment_date']}", ln=True)
    pdf.cell(0, 8, f"Date d'emission : {receipt_data['issued_at'][:10]}", ln=True)
    pdf.ln(5)
    
    # Informations élève
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Informations de l'eleve", ln=True)
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 8, f"Nom et prenom : {receipt_data['student_full_name']}", ln=True)
    pdf.cell(0, 8, f"Classe : {receipt_data['student_class']}", ln=True)
    pdf.ln(5)
    
    # Détails du paiement
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Details du paiement", ln=True)
    pdf.set_font("Helvetica", size=12)
    
    # Formatage des montants
    amount_str = f"{receipt_data['amount']:,} FCFA".replace(",", " ")
    balance_str = f"{receipt_data['balance_after']:,} FCFA".replace(",", " ")
    method_str = METHOD_LABELS.get(receipt_data['payment_method'], receipt_data['payment_method'])
    
    pdf.cell(0, 8, f"Montant paye : {amount_str}", ln=True)
    pdf.cell(0, 8, f"Mode de paiement : {method_str}", ln=True)
    pdf.cell(0, 8, f"Solde restant apres paiement : {balance_str}", ln=True)
    
    pdf.ln(15)
    pdf.cell(0, 8, "Signature et cachet de l'etablissement", ln=True)
    
    pdf.output(output_path)