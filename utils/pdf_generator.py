from fpdf import FPDF

METHOD_LABELS = {
    "especes": "Espèces",
    "cheque": "Chèque",
    "virement": "Virement",
    "mobile_money": "Mobile Money",
}

class ReceiptPDF(FPDF):
    def __init__(self, school_name="COMPLEXE SCOLAIRE EDUPAIE", **kwargs):
        super().__init__(**kwargs)
        self.school_name = school_name

    def header(self):
        # Nom de l'école (Sans le sous-titre "Gestion des frais scolaires")
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 80, 158) # Bleu
        self.cell(0, 10, self.school_name, border=False, align="C")
        self.ln(15) # On garde un espacement pour aérer le haut du document

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Généré par EduPaie - Page {self.page_no()}", align="C")


def generate_receipt_pdf(receipt_data, output_path, school_name="COMPLEXE SCOLAIRE EDUPAIE"):
    pdf = ReceiptPDF(school_name=school_name)
    pdf.add_page()
    
    # Configuration globale : on enlève les traits épais
    pdf.set_line_width(0.3) 
    
    # Titre du reçu
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, "REÇU DE PAIEMENT", ln=True, align="C")
    pdf.ln(3)

    # Ligne fine de séparation
    pdf.set_draw_color(200, 200, 200) 
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)

    # Informations générales
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(40, 8, "N° de reçu :", border=0)
    pdf.set_font("Helvetica", "B", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 8, receipt_data['receipt_number'], border=0)
    
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(40, 8, "Date de paiement :", border=0)
    pdf.set_font("Helvetica", "B", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, receipt_data['payment_date'], border=0, ln=True)

    pdf.ln(10)

    # Bloc Élève
    pdf.set_fill_color(248, 249, 250)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 80, 158)
    pdf.cell(0, 8, "  INFORMATIONS DE L'ÉLÈVE", border=0, ln=True, fill=True)
    
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(40, 8, "Nom et prénom :", border=0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, receipt_data['student_full_name'], border=0, ln=True)
    
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(40, 8, "Classe :", border=0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, receipt_data['student_class'], border=0, ln=True)

    pdf.ln(10)

    # Bloc Détails du paiement
    pdf.set_fill_color(248, 249, 250)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 80, 158)
    pdf.cell(0, 8, "  DÉTAILS DU PAIEMENT", border=0, ln=True, fill=True)
    
    amount_str = f"{receipt_data['amount']:,} FCFA".replace(",", " ")
    balance_str = f"{receipt_data['balance_after']:,} FCFA".replace(",", " ")
    method_str = METHOD_LABELS.get(receipt_data['payment_method'], receipt_data['payment_method'])
    
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 10, "Montant payé :", border=0)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 128, 0) 
    pdf.cell(0, 10, amount_str, border=0, ln=True)
    
    pdf.set_text_color(80, 80, 80)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(60, 8, "Mode de paiement :", border=0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, method_str, border=0, ln=True)
    
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 8, "Solde restant :", border=0)
    pdf.set_font("Helvetica", "B", 10)
    
    if receipt_data['balance_after'] > 0:
        pdf.set_text_color(200, 0, 0) 
    else:
        pdf.set_text_color(0, 128, 0) 
        
    pdf.cell(0, 8, balance_str, border=0, ln=True)

    pdf.ln(25)
    
    # Signatures
    pdf.set_text_color(100, 100, 100)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(90, 10, "Signature de l'élève / Parent", align="C")
    pdf.cell(90, 10, "Signature et cachet de l'établissement", align="C", ln=True)

    pdf.output(output_path)