import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.pdfgen import canvas

class GerenciadorSupermercado:
    def __init__(self, root):
        self.root = root
        self.root.title("Baratão das Frutas")

        # Adicionando temas
        self.tema_claro = {
            'background': 'white',
            'foreground': 'black',
            'activeBackground': '#C0C0C0',
            'activeForeground': 'black'
        }

        self.tema_escuro = {
            'background': '#2E2E2E',
            'foreground': 'white',
            'activeBackground': '#404040',
            'activeForeground': 'white'
        }

        # Definindo tema padrão
        self.tema_atual = self.tema_claro

        # Aplicando cores iniciais
        self.root.tk_setPalette(background=self.tema_atual['background'],
                                foreground=self.tema_atual['foreground'],
                                activeBackground=self.tema_atual['activeBackground'],
                                activeForeground=self.tema_atual['activeForeground'])

        # Botões para escolher o tema
        self.botao_tema_claro = tk.Button(root, text="Tema Claro", command=self.aplicar_tema_claro)
        self.botao_tema_claro.pack(side="left")

        self.botao_tema_escuro = tk.Button(root, text="Tema Escuro", command=self.aplicar_tema_escuro)
        self.botao_tema_escuro.pack(side="right")


        # Variáveis para armazenar dados
        self.frutas = {"Maçã": 2.5, "Banana": 1.8, "Laranja": 1.0}
        self.clientes = {
            "Cliente1": {"Telefone": "123456789", "Cidade": "Cidade1"},
            "Cliente2": {"Telefone": "987654321", "Cidade": "Cidade2"}
        }
        self.compras = []
        self.cliente_selecionado = None

        # Interface
        self.label_cliente = tk.Label(root, text="Selecione o cliente:")
        self.label_cliente.pack()

        self.combobox_clientes = ttk.Combobox(root, values=list(self.clientes.keys()))
        self.combobox_clientes.pack()
        self.combobox_clientes.bind("<<ComboboxSelected>>", self.selecionar_cliente)

        self.label_pesquisa = tk.Label(root, text="Pesquisar por fruta:")
        self.label_pesquisa.pack()

        self.entry_pesquisa = tk.Entry(root)
        self.entry_pesquisa.pack()
        self.entry_pesquisa.bind("<Return>", lambda event: self.pesquisar_fruta())

        self.botao_pesquisar = tk.Button(root, text="Pesquisar", command=self.pesquisar_fruta)
        self.botao_pesquisar.pack()

        self.tree = ttk.Treeview(root, columns=("Fruta", "Quantidade", "Preço Unitário", "Preço Total"), show="headings", selectmode="browse")
        self.tree.heading("Fruta", text="Fruta")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Preço Unitário", text="Preço Unitário")
        self.tree.heading("Preço Total", text="Preço Total")
        self.tree.bind("<Double-1>", self.editar_preco)
        self.tree.pack()

        self.atualizar_tabela()

        self.label_quantidade = tk.Label(root, text="Quantidade:")
        self.label_quantidade.pack()

        self.entry_quantidade = tk.Entry(root)
        self.entry_quantidade.pack()

        self.botao_adicionar = tk.Button(root, text="Adicionar à nota fiscal", command=self.adicionar_compra)
        self.botao_adicionar.pack()

        self.botao_finalizar = tk.Button(root, text="Finalizar Compra", command=self.finalizar_compra)
        self.botao_finalizar.pack()

        self.botao_limpar = tk.Button(root, text="Limpar Tela", command=self.limpar_tela)
        self.botao_limpar.pack()

        self.botao_salvar_nota = tk.Button(root, text="Salvar Nota Fiscal", command=self.salvar_nota_fiscal)
        self.botao_salvar_nota.pack()

        self.nota_fiscal = tk.Text(root, height=10, width=40)
        self.nota_fiscal.pack()

    def aplicar_tema_claro(self):
        self.tema_atual = self.tema_claro
        self.atualizar_cores_tema()

    def aplicar_tema_escuro(self):
        self.tema_atual = self.tema_escuro
        self.atualizar_cores_tema()

    def atualizar_cores_tema(self):
        self.root.tk_setPalette(background=self.tema_atual['background'],
                                foreground=self.tema_atual['foreground'],
                                activeBackground=self.tema_atual['activeBackground'],
                                activeForeground=self.tema_atual['activeForeground'])

    def pesquisar_fruta(self):
        pesquisa = self.entry_pesquisa.get().capitalize()
        if pesquisa in self.frutas:
            messagebox.showinfo("Informação", f"{pesquisa} encontrada.")
        else:
            messagebox.showinfo("Aviso", f"{pesquisa} não encontrada. Tente novamente.")

    def adicionar_compra(self):
        if self.cliente_selecionado is None:
            messagebox.showinfo("Aviso", "Selecione um cliente antes de adicionar à nota fiscal.")
            return

        fruta = self.tree.item(self.tree.selection(), "values")[0]
        quantidade = int(self.entry_quantidade.get())
        preco_unitario = self.frutas[fruta]
        preco_total = quantidade * preco_unitario

        self.compras.append({
            "Fruta": fruta,
            "Quantidade": quantidade,
            "Preço Unitário": preco_unitario,
            "Preço Total": preco_total
        })

        self.atualizar_nota_fiscal()

    def finalizar_compra(self):
        total = sum(compra["Preço Total"] for compra in self.compras)
        self.nota_fiscal.insert(tk.END, f"\nTotal da compra: R${total:.2f}\n")

    def limpar_tela(self):
        self.entry_pesquisa.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.compras = []
        self.cliente_selecionado = None
        self.atualizar_nota_fiscal()

    def atualizar_nota_fiscal(self):
        self.nota_fiscal.delete("1.0", tk.END)

        if self.cliente_selecionado:
            self.nota_fiscal.insert(tk.END, f"Cliente: {self.cliente_selecionado}\n\n")

        self.nota_fiscal.insert(tk.END, "{:<15} {:<15} {:<20} {:<15}\n".format("Fruta", "Quantidade", "Preço Unitário", "Preço Total"))

        for compra in self.compras:
            self.nota_fiscal.insert(tk.END, "{:<15} {:<15} {:<20} {:<15}\n".format(compra['Fruta'],
                                                                                    compra['Quantidade'],
                                                                                    f"R${compra['Preço Unitário']:.2f}",
                                                                                    f"R${compra['Preço Total']:.2f}"))

    def atualizar_tabela(self):
        # Limpa a tabela antes de atualizar
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Preenche a tabela com frutas e preços
        for fruta, preco in self.frutas.items():
            self.tree.insert("", "end", values=(fruta, 0, f"R${preco:.2f}", 0))

    def editar_preco(self, event):
        item = self.tree.selection()[0]
        coluna = self.tree.identify_column(event.x)
        if coluna == "#3":  # Se a coluna clicada for a coluna "Preço Unitário"
            entrada = ttk.Entry(self.root, justify='center', validate='key')
            entrada.insert(0, self.tree.item(item, "values")[2][2:])  # Obtém o preço atual e remove o "R$"

            def confirmar_edicao():
                try:
                    novo_preco = float(entrada.get())
                    self.frutas[self.tree.item(item, "values")[0]] = novo_preco
                    self.atualizar_tabela()
                    entrada.destroy()
                    botao_confirmar.destroy()  # Destroi o botão de confirmação após a edição
                except ValueError:
                    messagebox.showinfo("Aviso", "Digite um valor numérico válido.")

            botao_confirmar = ttk.Button(self.root, text="Confirmar", command=confirmar_edicao)
            botao_confirmar.pack()

            entrada.bind("<Return>", lambda e: confirmar_edicao())
            entrada.bind("<FocusOut>", lambda e: confirmar_edicao())

            entrada.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Posiciona a entrada no centro da tela
            entrada.focus_set()

    def selecionar_cliente(self, event):
        cliente_selecionado = self.combobox_clientes.get()
        if cliente_selecionado in self.clientes:
            self.cliente_selecionado = cliente_selecionado
            messagebox.showinfo("Sucesso", f"Cliente {cliente_selecionado} selecionado.")
        else:
            messagebox.showinfo("Aviso", "Cliente não encontrado.")

    def salvar_nota_fiscal(self):
        if not self.compras:
            messagebox.showinfo("Aviso", "A nota fiscal está vazia. Não há nada para salvar.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivo PDF", "*.pdf")])

        if file_path:  # Verifica se o usuário escolheu um arquivo
            pdf = canvas.Canvas(file_path)
            pdf.drawString(100, 800, "Nota Fiscal")

            if self.cliente_selecionado:
                pdf.drawString(100, 780, f"Cliente: {self.cliente_selecionado}")

            pdf.drawString(100, 760, "{:<15} {:<15} {:<20} {:<15}".format("Fruta", "Quantidade", "Preço Unitário", "Preço Total"))

            for i, compra in enumerate(self.compras, start=1):
                pdf.drawString(100, 760 - i * 20, "{:<15} {:<15} {:<20} {:<15}".format(compra['Fruta'],
                                                                                        compra['Quantidade'],
                                                                                        f"R${compra['Preço Unitário']:.2f}",
                                                                                        f"R${compra['Preço Total']:.2f}"))

            total = sum(compra["Preço Total"] for compra in self.compras)
            pdf.drawString(100, 760 - (i + 1) * 20, f"Total da compra: R${total:.2f}")

            pdf.save()
            messagebox.showinfo("Sucesso", "Nota fiscal salva como PDF com sucesso.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorSupermercado(root)
    root.mainloop()
