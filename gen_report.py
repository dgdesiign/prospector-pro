from fpdf import FPDF
import sqlite3
from datetime import datetime

class RevOpsReport(FPDF):
    def header(self):
        self.set_fill_color(15, 15, 15)
        self.rect(0, 0, 210, 40, 'F')
        self.set_font('helvetica', 'B', 22)
        self.set_text_color(212, 175, 55) # Gold
        self.cell(0, 20, 'PROSPECTOR PRO - ELITE INTELLIGENCE', ln=True, align='C')
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 5, f'Relatório de Auditoria RevOps - Gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")}', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()} - Documento Confidencial RevOps', align='C')

def generate_pdf():
    pdf = RevOpsReport()
    pdf.add_page()
    
    # Cabeçalho da Tabela
    pdf.set_fill_color(212, 175, 55) # Gold
    pdf.set_text_color(0)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(70, 10, 'EMPRESA', 1, 0, 'C', True)
    pdf.cell(50, 10, 'FATURAMENTO EST. (Anual)', 1, 0, 'C', True)
    pdf.cell(30, 10, 'RISCO JUR.', 1, 0, 'C', True)
    pdf.cell(20, 10, 'SCORE', 1, 0, 'C', True)
    pdf.cell(20, 10, 'TIER', 1, 1, 'C', True)

    # Dados do Banco
    conn = sqlite3.connect("data/prospector.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, capital_social, risco_juridico, score, tier FROM leads ORDER BY capital_social DESC LIMIT 10")
    
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(50)
    
    for nome, capital, risco, score, tier in cursor.fetchall():
        faturamento = capital * 5 # Lógica de projeção
        pdf.cell(70, 10, f' {nome[:35]}', 1)
        pdf.cell(50, 10, f' R$ {faturamento:,.2f}', 1, 0, 'R')
        pdf.cell(30, 10, f' {risco}', 1, 0, 'C')
        pdf.cell(20, 10, f' {score} pts', 1, 0, 'C')
        pdf.cell(20, 10, f' {tier}', 1, 1, 'C')
    
    conn.close()
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, 'ANÁLISE ESTRATÉGICA DO DIRETOR:', ln=True)
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 7, 'O pipeline atual apresenta uma concentração saudável em contas Enterprise (Tier 1M+). '
                         'Recomenda-se que os SDRs foquem na qualificação das contas com Score > 90 para '
                         'garantir a meta do trimestre. O risco jurídico identificado nas contas de varejo '
                         'deve ser usado como alavanca de fechamento SPICED.')

    pdf.output("Relatorio_Elite_RevOps.pdf")
    print("✅ Relatório Relatorio_Elite_RevOps.pdf gerado com sucesso.")

if __name__ == "__main__":
    generate_pdf()
