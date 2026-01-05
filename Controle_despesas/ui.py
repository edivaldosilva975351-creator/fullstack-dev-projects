import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from models import Transaction
import database

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Despesas Pessoais")
        self.root.geometry("400x500")

        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        # Saldo
        self.saldo_label = tk.Label(self.root, text="Saldo Hoje: Kz 0", font=("Arial", 16))
        self.saldo_label.pack(pady=10)

        # Botões
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Adicionar Despesa", command=lambda: self.add_transaction("despesa")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Adicionar Receita", command=lambda: self.add_transaction("receita")).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Exportar PDF", command=self.export_pdf).grid(row=0, column=2, padx=5)

        # Lista de transações
        self.tree = ttk.Treeview(self.root, columns=("valor", "categoria", "data", "tipo"), show="headings")
        self.tree.heading("valor", text="Valor")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("data", text="Data")
        self.tree.heading("tipo", text="Tipo")
        self.tree.pack(fill="both", expand=True, pady=10)

    def refresh_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        transactions = database.get_transactions()
        saldo = 0
        for t in transactions:
            if t.tipo == "despesa":
                saldo -= t.valor
            else:
                saldo += t.valor
            self.tree.insert("", "end", values=(t.valor, t.categoria, t.data, t.tipo))

        self.saldo_label.config(text=f"Saldo Hoje: Kz {saldo:.2f}")

    def add_transaction(self, tipo):
        def salvar():
            try:
                valor = float(valor_entry.get())
                categoria = categoria_entry.get()
                data_atual = date.today().isoformat()
                t = Transaction(id=None, valor=valor, categoria=categoria, data=data_atual, tipo=tipo)
                database.add_transaction(t)
                top.destroy()
                self.refresh_list()
            except:
                messagebox.showerror("Erro", "Valor inválido!")

        top = tk.Toplevel(self.root)
        top.title("Adicionar")
        top.geometry("300x150")

        tk.Label(top, text="Valor:").pack(pady=5)
        valor_entry = tk.Entry(top)
        valor_entry.pack()

        tk.Label(top, text="Categoria:").pack(pady=5)
        categoria_entry = tk.Entry(top)
        categoria_entry.pack()

        tk.Button(top, text="Salvar", command=salvar).pack(pady=10)

    def export_pdf(self):
        import report
        report.generate_pdf()
        messagebox.showinfo("Sucesso", "Relatório PDF gerado!")

if __name__ == "__main__":
    database.init_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()