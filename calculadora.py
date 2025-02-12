import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("Dark")  # Modo Dark (ou "Light" para modo claro)
ctk.set_default_color_theme("blue")  # Tema azul (ou "green", "dark-blue")

# Funções para cálculo de IMC
def calcular_imc():
    try:
        peso = float(entry_peso.get())
        altura_cm = float(entry_altura.get())
        altura = altura_cm / 100
        imc = peso / (altura ** 2)
        classificacao = interpretar_imc(imc)
        resultado = f"Seu IMC é: {imc:.2f}\nClassificação: {classificacao}"
        mostrar_grafico_imc(imc)  # Mostra gráfico visual do IMC
        messagebox.showinfo("Resultado", resultado)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para peso e altura.")

def interpretar_imc(imc):
    if imc < 18.5:
        return "Magro"
    elif imc < 25:
        return "Normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obeso"

def mostrar_grafico_imc(imc):
    fig, ax = plt.subplots(figsize=(4, 3))
    categorias = ["Magro", "Normal", "Sobrepeso", "Obeso"]
    valores = [18.5, 24.9, 29.9, 40]
    ax.bar(categorias, valores, color=["blue", "green", "orange", "red"])
    ax.axhline(imc, color="black", linestyle="--", label=f"Seu IMC: {imc:.2f}")
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=frame_imc)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, pady=10)

# Funções para cálculo gestacional
def calcular_gestacional():
    try:
        dum_str = entry_dum.get()
        dum = datetime.strptime(dum_str, "%d/%m/%Y")
        dpp = dum + timedelta(days=280)  # 280 dias = 40 semanas
        hoje = datetime.today()
        idade_gestacional = (hoje - dum).days // 7  # Idade gestacional em semanas
        resultado = (
            f"Data da Última Menstruação (DUM): {dum.strftime('%d/%m/%Y')}\n"
            f"Data Provável do Parto (DPP): {dpp.strftime('%d/%m/%Y')}\n"
            f"Idade Gestacional: {idade_gestacional} semanas"
        )
        messagebox.showinfo("Resultado", resultado)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira a data no formato DD/MM/AAAA.")

# Funções para cálculo de período fértil
def calcular_periodo_fertil():
    try:
        ciclo = int(entry_ciclo.get())
        ultima_menstruacao_str = entry_ultima_menstruacao.get()
        ultima_menstruacao = datetime.strptime(ultima_menstruacao_str, "%d/%m/%Y")
        ovulacao = ultima_menstruacao + timedelta(days=ciclo - 14)  # Ovulação ocorre 14 dias antes do próximo ciclo
        inicio_fertil = ovulacao - timedelta(days=5)  # 5 dias antes da ovulação
        fim_fertil = ovulacao + timedelta(days=1)  # 1 dia após a ovulação
        resultado = (
            f"Última Menstruação: {ultima_menstruacao.strftime('%d/%m/%Y')}\n"
            f"Período Fértil: {inicio_fertil.strftime('%d/%m/%Y')} até {fim_fertil.strftime('%d/%m/%Y')}\n"
            f"Dia de Ovulação: {ovulacao.strftime('%d/%m/%Y')}"
        )
        messagebox.showinfo("Resultado", resultado)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.\nData no formato DD/MM/AAAA e ciclo como número inteiro.")

# Função para trocar o tema
def mudar_tema(novo_tema):
    ctk.set_appearance_mode(novo_tema)

# Configuração da janela principal
root = ctk.CTk()
root.title("Calculadoras de Saúde")
root.geometry("600x400")
root.resizable(False, False)

# Menu suspenso para trocar o tema
menu_tema = ctk.CTkOptionMenu(root, values=["Light", "Dark"], command=mudar_tema)
menu_tema.set("Dark")  # Define o tema inicial como Dark
menu_tema.pack(pady=10)

# Criar abas
notebook = ctk.CTkTabview(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Aba 1: Calculadora de IMC
frame_imc = notebook.add("IMC")

ctk.CTkLabel(frame_imc, text="Peso (kg):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_peso = ctk.CTkEntry(frame_imc)
entry_peso.grid(row=0, column=1, padx=10, pady=10)

ctk.CTkLabel(frame_imc, text="Altura (cm):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_altura = ctk.CTkEntry(frame_imc)
entry_altura.grid(row=1, column=1, padx=10, pady=10)

btn_calcular_imc = ctk.CTkButton(frame_imc, text="Calcular IMC", command=calcular_imc)
btn_calcular_imc.grid(row=2, column=0, columnspan=2, pady=20)

# Aba 2: Calculadora Gestacional
frame_gestacional = notebook.add("Gestacional")

ctk.CTkLabel(frame_gestacional, text="Data da Última Menstruação (DD/MM/AAAA):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_dum = ctk.CTkEntry(frame_gestacional)
entry_dum.grid(row=0, column=1, padx=10, pady=10)

btn_calcular_gestacional = ctk.CTkButton(frame_gestacional, text="Calcular", command=calcular_gestacional)
btn_calcular_gestacional.grid(row=1, column=0, columnspan=2, pady=20)

# Aba 3: Calculadora de Período Fértil
frame_fertil = notebook.add("Período Fértil")

ctk.CTkLabel(frame_fertil, text="Duração do Ciclo Menstrual (dias):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_ciclo = ctk.CTkEntry(frame_fertil)
entry_ciclo.grid(row=0, column=1, padx=10, pady=10)

ctk.CTkLabel(frame_fertil, text="Data da Última Menstruação (DD/MM/AAAA):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_ultima_menstruacao = ctk.CTkEntry(frame_fertil)
entry_ultima_menstruacao.grid(row=1, column=1, padx=10, pady=10)

btn_calcular_fertil = ctk.CTkButton(frame_fertil, text="Calcular", command=calcular_periodo_fertil)
btn_calcular_fertil.grid(row=2, column=0, columnspan=2, pady=20)

# Executar a aplicação
root.mainloop()