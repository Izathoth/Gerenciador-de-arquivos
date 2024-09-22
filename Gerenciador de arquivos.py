import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Frame, Button, Label, Menu, StringVar, Entry
import os
import re

class GerenciadorArquivos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Arquivos")
        self.geometry("800x600")
        self.configure(bg="#f7f9fc")

        self.current_file = None
        self.recent_files = []

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Frame da barra lateral
        sidebar = Frame(self, width=200, bg="#007BFF")
        sidebar.pack(side="left", fill="y")

        # Título da aplicação
        title_label = Label(sidebar, text="Menu", bg="#007BFF", fg="white", font=("Helvetica", 18))
        title_label.pack(pady=20)

        # Botões na barra lateral
        buttons = [
            ("Novo", self.novo_arquivo),
            ("Abrir", self.abrir_arquivo),
            ("Salvar", self.salvar_arquivo),
            ("Contar Palavras", self.contar_palavras),
            ("Creditos", self.mostrar_creditos),
            ("Sair", self.quit)
        ]
        
        for (text, command) in buttons:
            btn = Button(sidebar, text=text, command=command, bg="#0056b3", fg="white", font=("Helvetica", 12), 
                         relief=tk.FLAT, padx=10, pady=5)
            btn.pack(fill="x", padx=10, pady=5)
            btn.bind("<Enter>", lambda e: btn.config(bg="#004494"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#0056b3"))

        # Barra de busca
        search_frame = Frame(self, bg="#f7f9fc")
        search_frame.pack(fill="x", padx=20, pady=10)

        Label(search_frame, text="Buscar:", bg="#f7f9fc", font=("Helvetica", 12)).pack(side="left")
        self.search_var = StringVar()
        Entry(search_frame, textvariable=self.search_var, font=("Helvetica", 12), width=30).pack(side="left", padx=5)
        Button(search_frame, text="Buscar", command=self.buscar_palavras, bg="#007BFF", fg="white").pack(side="left", padx=5)

        # Área de texto
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg="#ffffff", fg="#333333",
                                                    font=("Helvetica", 12), borderwidth=2, relief="groove")
        self.text_area.pack(expand=True, fill='both', padx=20, pady=10)

        # Label de status
        self.status_label = Label(self, text="Pronto", bg="#f7f9fc", anchor="w", font=("Helvetica", 10))
        self.status_label.pack(side="bottom", fill="x", padx=20, pady=5)

        # Efeitos visuais
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def create_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        arquivo_menu = Menu(menu)
        menu.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Recentes", command=self.exibir_recent_files)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.quit)

        ajuda_menu = Menu(menu)
        menu.add_cascade(label="Ajuda", menu=ajuda_menu)
        ajuda_menu.add_command(label="Sobre", command=self.sobre)

    def novo_arquivo(self):
        if self.text_area.get("1.0", tk.END).strip():
            if messagebox.askyesno("Confirmação", "Deseja salvar o arquivo atual?"):
                self.salvar_como()
        self.text_area.delete("1.0", tk.END)
        self.current_file = None
        self.status_label.config(text="Novo arquivo criado.")

    def abrir_arquivo(self):
        file_path = filedialog.askopenfilename(defaultextension=".*",
                                                filetypes=[("Todos os Arquivos", "*.*")])
        if file_path:
            self.text_area.delete("1.0", tk.END)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text_area.insert(tk.END, file.read())
                self.current_file = file_path
                self.recent_files.append(file_path)
                self.status_label.config(text=f"Abrindo: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir o arquivo: {e}")

    def salvar_arquivo(self):
        if self.current_file:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get("1.0", tk.END))
            messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")
            self.status_label.config(text=f"Arquivo salvo: {os.path.basename(self.current_file)}")
        else:
            self.salvar_como()

    def salvar_como(self):
        self.current_file = filedialog.asksaveasfilename(defaultextension=".txt",
                                                          filetypes=[("Todos os Arquivos", "*.*")])
        if self.current_file:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get("1.0", tk.END))
            messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")
            self.status_label.config(text=f"Arquivo salvo: {os.path.basename(self.current_file)}")

    def contar_palavras(self):
        texto = self.text_area.get("1.0", tk.END)
        palavras = re.findall(r'\w+', texto)
        num_palavras = len(palavras)
        messagebox.showinfo("Contagem de Palavras", f"Número de palavras: {num_palavras}")
        self.status_label.config(text="Contagem de palavras realizada.")

    def buscar_palavras(self):
        termo = self.search_var.get()
        texto = self.text_area.get("1.0", tk.END)
        ocorrencias = re.findall(re.escape(termo), texto, re.IGNORECASE)
        num_ocorrencias = len(ocorrencias)
        messagebox.showinfo("Resultados da Busca", f"Número de ocorrências de '{termo}': {num_ocorrencias}")

    def exibir_recent_files(self):
        recent_files = "\n".join([os.path.basename(f) for f in self.recent_files]) or "Nenhum arquivo recente."
        messagebox.showinfo("Arquivos Recentes", recent_files)

    def mostrar_creditos(self):
        messagebox.showinfo("Creditos", "Desenvolvedor: Soradevs\nLink do GitHub: https://github.com/soradevs\n\n"
                                          "Intuito do projeto: Fácil de usar, útil e para aprendizagem própria do criador(a).")

    def sobre(self):
        messagebox.showinfo("Sobre", "Gerenciador de Arquivos\nVersão 1.0\nDesenvolvido por Isaque")

    def on_focus_in(self, event):
        self.configure(bg="#e1e5ea")

    def on_focus_out(self, event):
        self.configure(bg="#f7f9fc")

if __name__ == "__main__":
    app = GerenciadorArquivos()
    app.mainloop()