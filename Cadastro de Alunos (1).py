import sqlite3
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect('alunos.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    nota REAL NOT NULL
)
''')


def nome_ja_existe(nome):
    cursor.execute('SELECT * FROM alunos WHERE nome = ?', (nome,))
    return cursor.fetchone() is not None


def nome_comeca_maiuscula(nome):
    return nome[0].isupper()

 
def cadastrar_aluno():
    nome = entry_nome.get().strip()  
    try:
        nota = float(entry_nota.get())
    except ValueError:
        messagebox.showerror("Erro", "A nota deve ser um número.")
        return

    if nome and nota:
    
        if not nome_comeca_maiuscula(nome):
            messagebox.showerror("Erro", "O nome deve começar com letra maiúscula.")
            return

        
        if nome_ja_existe(nome):
            messagebox.showerror("Erro", "Este nome já está cadastrado. Por favor, insira o sobrenome ou escolha outro nome.")
        else:
            cursor.execute('INSERT INTO alunos (nome, nota) VALUES (?, ?)', (nome, nota))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado com sucesso!")
            entry_nome.delete(0, tk.END)
            entry_nota.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Preencha todos os campos!")

def consultar_notas():
    cursor.execute('SELECT * FROM alunos')
    alunos = cursor.fetchall()

    text_resultado.delete(1.0, tk.END)  

    if alunos:
        text_resultado.insert(tk.END, "ID | Nome | Nota\n")
        text_resultado.insert(tk.END, "-" * 30 + "\n")
        for aluno in alunos:
            text_resultado.insert(tk.END, f"{aluno[0]} | {aluno[1]} | {aluno[2]}\n")
    else:
        text_resultado.insert(tk.END, "Nenhum aluno cadastrado.\n")


def buscar_aluno():
    nome = entry_nome_busca.get().strip()
    cursor.execute('SELECT * FROM alunos WHERE nome = ?', (nome,))
    aluno = cursor.fetchone()

    text_resultado.delete(1.0, tk.END)  

    if aluno:
        text_resultado.insert(tk.END, f"ID: {aluno[0]}\nNome: {aluno[1]}\nNota: {aluno[2]}\n")
    else:
        text_resultado.insert(tk.END, f"Aluno {nome} não encontrado.\n")


def apagar_aluno_especifico():
    aluno_id = entry_id_apagar.get().strip()
    if aluno_id:
        cursor.execute('SELECT * FROM alunos WHERE id = ?', (aluno_id,))
        aluno = cursor.fetchone()

        if aluno:
            resposta = messagebox.askyesno("Confirmação", f"Você tem certeza que deseja apagar o aluno {aluno[1]}?")
            if resposta:
                cursor.execute('DELETE FROM alunos WHERE id = ?', (aluno_id,))
                conn.commit()
                messagebox.showinfo("Sucesso", f"Aluno {aluno[1]} apagado com sucesso!")
                consultar_notas()  
        else:
            messagebox.showerror("Erro", f"Aluno com ID {aluno_id} não encontrado.")
    else:
        messagebox.showerror("Erro", "Por favor, insira um ID válido.")


def apagar_historico():
    resposta = messagebox.askyesno("Confirmação", "Você tem certeza que deseja apagar todo o histórico?")
    if resposta:  
        cursor.execute('DELETE FROM alunos') 
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="alunos"')  
        conn.commit()
        messagebox.showinfo("Sucesso", "Histórico de alunos apagado e IDs reiniciados com sucesso!")
        consultar_notas()  


root = tk.Tk()
root.title("Sistema de Cadastro de Notas de Alunos")
root.geometry("500x600")


bg_color = "#333333"  
fg_color = "#ffffff" 
button_bg = "#444444"  
button_fg = "#ffffff"  
entry_bg = "#555555"  
entry_fg = "#ffffff"   


root.configure(bg=bg_color)


frame_nome_nota = tk.Frame(root, bg=bg_color)
frame_nome_nota.pack(pady=10)


label_nome = tk.Label(frame_nome_nota, text="Nome do Aluno:", bg=bg_color, fg=fg_color)
label_nome.grid(row=0, column=0, padx=5)

entry_nome = tk.Entry(frame_nome_nota, bg=entry_bg, fg=entry_fg)
entry_nome.grid(row=0, column=1, padx=5)

label_nota = tk.Label(frame_nome_nota, text="Nota do Aluno:", bg=bg_color, fg=fg_color)
label_nota.grid(row=0, column=2, padx=5)

entry_nota = tk.Entry(frame_nome_nota, bg=entry_bg, fg=entry_fg)
entry_nota.grid(row=0, column=3, padx=5)


btn_cadastrar = tk.Button(root, text="Cadastrar Aluno", bg=button_bg, fg=button_fg, command=cadastrar_aluno)
btn_cadastrar.pack(pady=10)


label_nome_busca = tk.Label(root, text="Buscar Aluno por Nome:", bg=bg_color, fg=fg_color)
label_nome_busca.pack(pady=5)

entry_nome_busca = tk.Entry(root, bg=entry_bg, fg=entry_fg)
entry_nome_busca.pack(pady=5)


btn_buscar = tk.Button(root, text="Buscar Aluno", bg=button_bg, fg=button_fg, command=buscar_aluno)
btn_buscar.pack(pady=10)


btn_consultar = tk.Button(root, text="Consultar Todos os Alunos", bg=button_bg, fg=button_fg, command=consultar_notas)
btn_consultar.pack(pady=10)


text_resultado = tk.Text(root, height=10, width=40, bg=entry_bg, fg=entry_fg)
text_resultado.pack(pady=10)


label_id_apagar = tk.Label(root, text="Apagar Aluno por ID:", bg=bg_color, fg=fg_color)
label_id_apagar.pack(pady=5)

entry_id_apagar = tk.Entry(root, bg=entry_bg, fg=entry_fg)
entry_id_apagar.pack(pady=5)

btn_apagar_especifico = tk.Button(root, text="Apagar Aluno", bg=button_bg, fg=button_fg, command=apagar_aluno_especifico)
btn_apagar_especifico.pack(pady=10)


btn_apagar = tk.Button(root, text="Apagar Histórico", bg=button_bg, fg=button_fg, command=apagar_historico)
btn_apagar.pack(pady=20)


root.mainloop()


conn.close()
