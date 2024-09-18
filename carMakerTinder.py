import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from collections import defaultdict

# Lista de marcas disponíveis
marcas = [
    "AGRALE", "AUDI", "BMW", "CHERY", "CHEVROLET", "CITROEN", "DODGE", 
    "FIAT", "FORD", "HONDA", "HYUNDAI", "IVECO", "JAC", "JEEP", "KIA", 
    "LAND-ROVER", "MARCOPOLO", "MERCEDES-BENZ", "MITSUBISHI", "NISSAN", 
    "PEUGEOT", "RENAULT", "SCANIA", "SSANGYONG", "SUZUKI", "TOYOTA", 
    "TROLLER", "VOLVO", "VW"
]

# Função para carregar as imagens de um diretório específico
def carregar_imagens(diretorio):
    imagens = []
    for subdir, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo.endswith(('.png', '.jpg', '.jpeg')):
                imagens.append(os.path.join(subdir, arquivo))
    return imagens

# Função para criar pastas para marcas e "Não Identificável"
def criar_pastas(diretorio):
    for marca in marcas:
        pasta_marca = os.path.join(diretorio, marca)
        os.makedirs(pasta_marca, exist_ok=True)
    pasta_nao_identificavel = os.path.join(diretorio, "Nao_Identificavel")
    os.makedirs(pasta_nao_identificavel, exist_ok=True)

# Função para atualizar a imagem na interface
def atualizar_imagem():
    global img_index
    if img_index < len(imagens):
        img = Image.open(imagens[img_index])
        img = img.resize((400, 300), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        label_img.config(image=tk_img)
        label_img.image = tk_img
        label_info.config(text=f"Imagem {img_index + 1}/{len(imagens)}")
    else:
        messagebox.showinfo("Fim", "Todas as imagens foram verificadas!")
        gerar_estatisticas()
        gerar_relatorio_geral()
        remover_diretorios_vazios(diretorio)
        root.quit()

# Função para salvar a decisão e mover a imagem
def salvar_decisao(decisao):
    global img_index, erros_por_marca, acertos_por_marca, nao_identificavel_por_marca
    caminho_imagem = imagens[img_index]
    diretorio_atual = os.path.basename(os.path.dirname(caminho_imagem))
    
    if decisao == "errado":
        marca_corrigida = opcao_marca.get()
        if marca_corrigida == "Selecione a marca correta":
            messagebox.showwarning("Erro", "Por favor, selecione a marca correta.")
            return
        erros_por_marca[diretorio_atual].append(marca_corrigida)
        destino = os.path.join(diretorio, marca_corrigida)
    elif decisao == "nao_identificavel":
        nao_identificavel_por_marca[diretorio_atual] += 1
        destino = os.path.join(diretorio, "Nao_Identificavel")
    else:
        acertos_por_marca[diretorio_atual] += 1
        destino = os.path.join(diretorio, diretorio_atual)
    
    # Mover a imagem para o diretório apropriado
    shutil.move(caminho_imagem, destino)
    
    img_index += 1
    atualizar_imagem()

# Função para gerar estatísticas de erros, acertos e "Não é possível identificar"
def gerar_estatisticas():
    for marca in acertos_por_marca.keys():
        total_imagens = acertos_por_marca[marca] + len(erros_por_marca[marca]) + nao_identificavel_por_marca[marca]
        erros = len(erros_por_marca[marca])
        acertos = acertos_por_marca[marca]
        nao_identificaveis = nao_identificavel_por_marca[marca]
        
        # Contagem de erros por marca corrigida
        contagem_erros = defaultdict(int)
        for erro in erros_por_marca[marca]:
            contagem_erros[erro] += 1
        
        # Salvar os resultados em um arquivo resultados-marca.txt
        with open(f"{marca}/resultados-{marca}.txt", "w") as f:
            f.write(f"Total de imagens verificadas: {total_imagens}\n")
            f.write(f"Acertos: {acertos}\n")
            f.write(f"Erros: {erros}\n")
            f.write(f"Não é possível identificar: {nao_identificaveis}\n\n")
            f.write("Marcas que apareceram como erro:\n")
            for marca_erro, count in contagem_erros.items():
                f.write(f"{marca_erro}: {count} vezes\n")

# Função para gerar o relatório geral
def gerar_relatorio_geral():
    total_acertos = sum(acertos_por_marca.values())
    total_erros = sum(len(erros_por_marca[marca]) for marca in erros_por_marca)
    total_nao_identificaveis = sum(nao_identificavel_por_marca.values())
    
    with open(os.path.join(diretorio, "resultados-gerais.txt"), "w") as f:
        f.write(f"Total de imagens verificadas: {total_acertos + total_erros + total_nao_identificaveis}\n")
        f.write(f"Total de acertos: {total_acertos}\n")
        f.write(f"Total de erros: {total_erros}\n")
        f.write(f"Total de imagens não identificáveis: {total_nao_identificaveis}\n\n")
        
        f.write("Detalhes por marca:\n")
        for marca in marcas:
            acertos = acertos_por_marca[marca]
            erros = len(erros_por_marca[marca])
            nao_identificaveis = nao_identificavel_por_marca[marca]
            f.write(f"{marca}:\n")
            f.write(f"  Acertos: {acertos}\n")
            f.write(f"  Erros: {erros}\n")
            f.write(f"  Não é possível identificar: {nao_identificaveis}\n")
            f.write("\n")

# Função para remover diretórios vazios
def remover_diretorios_vazios(diretorio):
    for root, dirs, _ in os.walk(diretorio, topdown=False):
        for dir_ in dirs:
            caminho_dir = os.path.join(root, dir_)
            if not os.listdir(caminho_dir):
                os.rmdir(caminho_dir)

# Janela principal
root = tk.Tk()
root.title("Verificador de Imagens de Veículos")

# Dicionários para armazenar erros, acertos e "Não é possível identificar" por marca (diretório)
erros_por_marca = defaultdict(list)
acertos_por_marca = defaultdict(int)
nao_identificavel_por_marca = defaultdict(int)

# Carregar imagens
diretorio = filedialog.askdirectory(title="Selecione a pasta com as imagens")
criar_pastas(diretorio)
imagens = carregar_imagens(diretorio)
img_index = 0

# Layout da interface
label_img = tk.Label(root)
label_img.pack(pady=20)

label_info = tk.Label(root, text="Imagem 0/0")
label_info.pack()

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

btn_correto = tk.Button(frame_botoes, text="Correto", command=lambda: salvar_decisao("correto"))
btn_correto.grid(row=0, column=0, padx=10)

btn_errado = tk.Button(frame_botoes, text="Errado", command=lambda: salvar_decisao("errado"))
btn_errado.grid(row=0, column=1, padx=10)

btn_nao_identificavel = tk.Button(frame_botoes, text="Não é possível identificar", command=lambda: salvar_decisao("nao_identificavel"))
btn_nao_identificavel.grid(row=0, column=2, padx=10)

label_marca = tk.Label(root, text="Se errado, selecione a marca correta:")
label_marca.pack(pady=5)

# Menu suspenso (OptionMenu) com as 29 marcas
opcao_marca = tk.StringVar(root)
opcao_marca.set("Selecione a marca correta")  # Valor padrão
menu_marcas = tk.OptionMenu(root, opcao_marca, *marcas)
menu_marcas.pack(pady=5)

# Iniciar com a primeira imagem
atualizar_imagem()

root.mainloop()

