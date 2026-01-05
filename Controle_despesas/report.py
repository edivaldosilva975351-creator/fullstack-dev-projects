from fpdf import FPDF
import database
import matplotlib.pyplot as plt
import pandas as pd

def generate_pdf():
    transactions = database.get_transactions()
    
    if not transactions:
        return

    # Criar DataFrame para gráficos e relatório
    df = pd.DataFrame([t.__dict__ for t in transactions])
    
    # Total de saldo
    total = df.apply(lambda row: row['valor'] if row['tipo']=='receita' else -row['valor'], axis=1).sum()

    # GRAFICO DE PIZZA – Despesas por categoria
    df_despesas = df[df['tipo']=='despesa']
    if not df_despesas.empty:
        resumo = df_despesas.groupby('categoria')['valor'].sum()
        plt.figure(figsize=(6,6))
        cores = plt.cm.tab20.colors  # paleta bonita
        wedges, texts, autotexts = plt.pie(
            resumo,
            labels=resumo.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=cores
        )
        for text in texts + autotexts:
            text.set_fontsize(10)
        plt.title("Gastos por Categoria", fontsize=14)
        plt.tight_layout()
        plt.savefig("grafico_categoria.png")
        plt.close()

    # CRIAR PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório de Despesas Pessoais", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for t in transactions:
        pdf.cell(0, 8, f"{t.data} - {t.tipo.upper()} - {t.categoria} - Kz {t.valor:.2f}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Saldo Total: Kz {total:.2f}", ln=True)

    # Inserir gráfico se existir
    try:
        pdf.image("grafico_categoria.png", x=40, w=130)
    except:
        pass

    pdf.ln(5)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Autoria: Edivaldo Silva", ln=True, align="R")

    pdf.output("relatorio_despesas.pdf")
