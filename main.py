import os
import re
from tkinter import Tk, filedialog, simpledialog

# ==== UTILITÁRIOS DE INTERFACE ====

def escolher_diretorio(titulo):
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory(title=titulo)

def escolher_arquivo(titulo, tipo):
    root = Tk()
    root.withdraw()
    return filedialog.asksaveasfilename(
        title=titulo,
        defaultextension=tipo,
        filetypes=[(f"Arquivos {tipo}", f"*{tipo}")]
    )

def escolher_arquivo_estrutura():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Selecione o arquivo structure.txt",
        filetypes=[("Arquivos de texto", "*.txt")]
    )

# ==== PARSER FLEXÍVEL DE ESTRUTURA VISUAL ====

def contar_nivel_indice(linha):
    """
    Detecta quantos níveis existem com base em blocos de 4 espaços ou '│   ', '    ' etc.
    Remove conectores como '├──', '└──' e retorna o nome limpo.
    """
    padrao_indentacao = re.compile(r'^(│   |    |\t)+')
    padrao_conector = re.compile(r'^[├└]──\s+')

    match = padrao_indentacao.match(linha)
    nivel = 0
    if match:
        unidades = match.group(0)
        nivel = len(unidades) // 4  # considerando 4 espaços/tab

    linha = padrao_indentacao.sub('', linha)
    linha = padrao_conector.sub('', linha).strip()

    return nivel, linha

def converter_para_caminhos(arquivo):
    caminhos = []
    pilha = []

    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.rstrip('\n')

            # Ignora linhas vazias ou decorativas
            if not linha.strip() or re.fullmatch(r'[│├└─\s]+', linha):
                continue

            # Remove comentário após o conteúdo
            comentario_index = linha.find('#')
            if comentario_index != -1:
                linha = linha[:comentario_index].rstrip()

            # Conta nível de indentação
            nivel = 0
            while linha.startswith(('│   ', '    ', '\t')):
                nivel += 1
                linha = linha[4:] if linha.startswith(('│   ', '    ')) else linha[1:]

            # Remove conectores ├── ou └──
            linha = re.sub(r'^[├└]──\s*', '', linha).strip()
            if not linha:
                continue

            # Detecta se é diretório
            is_dir = linha.endswith('/')

            # Atualiza pilha até o nível
            pilha = pilha[:nivel]
            pilha.append(linha.rstrip('/'))  # Remove a / apenas para criar o caminho corretamente

            # Monta o caminho
            caminho = os.path.join(*pilha)
            if is_dir:
                caminho += '/'

            caminhos.append(caminho)

            # Só mantemos na pilha se for diretório
            if not is_dir:
                pilha.pop()

    return caminhos

# ==== CONSTRUÇÃO ====

def criar_estrutura(destino, caminhos):
    for caminho in caminhos:
        destino_abs = os.path.join(destino, caminho)
        if caminho.endswith('/'):
            os.makedirs(destino_abs, exist_ok=True)
            print(f"[DIR]  {destino_abs}")
        else:
            os.makedirs(os.path.dirname(destino_abs), exist_ok=True)
            if not os.path.exists(destino_abs):
                with open(destino_abs, 'w', encoding='utf-8') as f:
                    f.write("")
                print(f"[FILE] {destino_abs}")
            else:
                print(f"[SKIP] {destino_abs}")

# ==== ANÁLISE ====

def gerar_estrutura_aninhada(caminho, prefixo="", estrutura=None):
    if estrutura is None:
        estrutura = []
    itens = sorted(os.listdir(caminho))
    for i, nome in enumerate(itens):
        caminho_completo = os.path.join(caminho, nome)
        is_last = i == len(itens) - 1
        conector = "└── " if is_last else "├── "
        novo_prefixo = prefixo + ("    " if is_last else "│   ")

        if os.path.isdir(caminho_completo):
            estrutura.append(f"{prefixo}{conector}{nome}/")
            gerar_estrutura_aninhada(caminho_completo, novo_prefixo, estrutura)
        else:
            estrutura.append(f"{prefixo}{conector}{nome}")
    return estrutura

def gerar_estrutura_plana(caminho):
    estrutura = []
    for raiz, dirs, arquivos in os.walk(caminho):
        rel_raiz = os.path.relpath(raiz, caminho)
        if rel_raiz == '.':
            rel_raiz = ''
        for d in dirs:
            estrutura.append(os.path.join(rel_raiz, d).replace('\\', '/') + '/')
        for a in arquivos:
            estrutura.append(os.path.join(rel_raiz, a).replace('\\', '/'))
    return estrutura

# ==== MODOS ====

def modo_criar():
    estrutura_txt = escolher_arquivo_estrutura()
    if not estrutura_txt or not os.path.isfile(estrutura_txt):
        print("Nenhum arquivo válido selecionado.")
        return

    destino = escolher_diretorio("Escolha a pasta de destino")
    if not destino:
        print("Nenhum diretório selecionado.")
        return

    caminhos = converter_para_caminhos(estrutura_txt)
    criar_estrutura(destino, caminhos)
    print("✅ Estrutura criada com sucesso!")

def modo_analisar():
    origem = escolher_diretorio("Selecione a pasta para análise")
    if not origem:
        print("Nenhuma pasta selecionada.")
        return

    salvar_tree = escolher_arquivo("Salvar como estrutura em árvore", ".txt")
    salvar_flat = escolher_arquivo("Salvar como estrutura plana", ".txt")

    if not salvar_tree or not salvar_flat:
        print("Operação cancelada.")
        return

    estrutura_aninhada = gerar_estrutura_aninhada(origem)
    with open(salvar_tree, 'w', encoding='utf-8') as f:
        f.write('\n'.join(estrutura_aninhada))

    estrutura_plana = gerar_estrutura_plana(origem)
    with open(salvar_flat, 'w', encoding='utf-8') as f:
        f.write('\n'.join(estrutura_plana))

    print(f"""
✅ Análise concluída!
- Estrutura em árvore salva em: {salvar_tree}
- Estrutura plana salva em: {salvar_flat}
""")

# ==== MAIN ====

def main():
    root = Tk()
    root.withdraw()
    opcao = simpledialog.askstring(
        "Modo de operação",
        "Escolha o modo:\n1 - Criar estrutura\n2 - Analisar pasta",
        initialvalue="1"
    )

    if opcao == '1':
        modo_criar()
    elif opcao == '2':
        modo_analisar()
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
