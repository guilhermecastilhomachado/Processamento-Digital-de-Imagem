import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import deque

# =============================================================================
# CONFIGURAÇÕES INICIAIS
# =============================================================================

# Configurações do threshold (conforme especificado na atividade)
THRESHOLD = 167  # Valor correto conforme a atividade
NOME_ARQUIVO = 'clc3.png'
NOME_ARQUIVO_SAIDA = 'clc3thr1.png'


# =============================================================================
# PASSO 1: CARREGAMENTO DA IMAGEM
# =============================================================================

def carregar_imagem_original():
    """
    PASSO 1: Carrega a imagem original em escala de cinza

    Returns:
        tuple: (imagem_pil, imagem_array) - objeto PIL e array numpy
    """
    print("=" * 60)
    print("PASSO 1: CARREGANDO A IMAGEM ORIGINAL")
    print("=" * 60)

    try:
        # Carrega imagem e converte para escala de cinza
        imagem_original = Image.open(NOME_ARQUIVO).convert('L')
        imagem_array = np.array(imagem_original)

        print(f"✓ Imagem '{NOME_ARQUIVO}' carregada com sucesso!")
        print(f"✓ Dimensões: {imagem_array.shape[0]} x {imagem_array.shape[1]} pixels")
        print(f"✓ Valores de pixel: {np.min(imagem_array)} até {np.max(imagem_array)}")
        print(f"✓ Valor médio dos pixels: {np.mean(imagem_array):.1f}")

        return imagem_original, imagem_array

    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo '{NOME_ARQUIVO}' não encontrado!")
        print("   Certifique-se de que o arquivo está na mesma pasta do código.")
        return None, None


# =============================================================================
# PASSO 2: BINARIZAÇÃO COM THRESHOLD
# =============================================================================

def aplicar_threshold(imagem_array, threshold=THRESHOLD):
    """
    PASSO 2: Aplica threshold para binarizar a imagem

    REGRA ESPECÍFICA DA ATIVIDADE:
    - Pixels com valor <= threshold recebem valor 1 (OBJETO - branco)
    - Pixels com valor > threshold recebem valor 0 (FUNDO - preto)

    Args:
        imagem_array: Array numpy da imagem original
        threshold: Valor do threshold (padrão: 67)

    Returns:
        np.array: Imagem binarizada (valores 0 e 1)
    """
    print("\n" + "=" * 60)
    print("PASSO 2: APLICANDO THRESHOLD PARA BINARIZAÇÃO")
    print("=" * 60)

    # Aplica a regra específica da atividade
    imagem_binaria = np.where(imagem_array <= threshold, 1, 0)

    # Estatísticas da binarização
    pixels_objeto = np.sum(imagem_binaria == 1)
    pixels_fundo = np.sum(imagem_binaria == 0)
    total_pixels = imagem_binaria.size

    print(f"✓ Threshold aplicado: {threshold}")
    print(f"✓ Regra: pixels ≤ {threshold} → 1 (objeto), pixels > {threshold} → 0 (fundo)")
    print(f"✓ Pixels de OBJETO (valor 1): {pixels_objeto} ({pixels_objeto / total_pixels * 100:.1f}%)")
    print(f"✓ Pixels de FUNDO (valor 0): {pixels_fundo} ({pixels_fundo / total_pixels * 100:.1f}%)")

    return imagem_binaria


def salvar_imagem_binaria(imagem_binaria, nome_arquivo=NOME_ARQUIVO_SAIDA):
    """
    Salva a imagem binarizada conforme especificado na atividade
    """
    # Converte para 0-255 para salvamento (0→0, 1→255)
    imagem_para_salvar = (imagem_binaria * 255).astype(np.uint8)
    imagem_pil = Image.fromarray(imagem_para_salvar, 'L')
    imagem_pil.save(nome_arquivo)
    print(f"✓ Imagem binarizada salva como: '{nome_arquivo}'")


# =============================================================================
# PASSO 3: ROTULAÇÃO DE COMPONENTES CONEXOS
# =============================================================================

def rotular_componente_bfs(imagem_binaria, matriz_rotulos, x_inicial, y_inicial, rotulo):
    """
    PASSO 3A: Rotula um componente específico usando BFS (Busca em Largura)

    Usa 4-conectividade: considera apenas vizinhos acima, abaixo, esquerda e direita

    Args:
        imagem_binaria: Imagem binarizada (0s e 1s)
        matriz_rotulos: Matriz onde serão armazenados os rótulos
        x_inicial, y_inicial: Coordenadas do pixel inicial do componente
        rotulo: Número do rótulo a ser atribuído
    """
    altura, largura = imagem_binaria.shape

    # Fila para BFS (mais eficiente que recursão para imagens grandes)
    fila = deque()
    fila.append((x_inicial, y_inicial))
    matriz_rotulos[x_inicial, y_inicial] = rotulo

    # Definição dos 4 vizinhos (4-conectividade)
    # Ordem: cima, baixo, esquerda, direita
    vizinhos_4conectados = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    pixels_no_componente = 1  # Conta pixels do componente atual

    while fila:
        x_atual, y_atual = fila.popleft()

        # Verifica todos os 4 vizinhos
        for dx, dy in vizinhos_4conectados:
            x_vizinho = x_atual + dx
            y_vizinho = y_atual + dy

            # Verifica se o vizinho está dentro dos limites da imagem
            if (0 <= x_vizinho < altura) and (0 <= y_vizinho < largura):
                # Verifica se é pixel de objeto (1) e ainda não foi rotulado
                if (imagem_binaria[x_vizinho, y_vizinho] == 1 and
                        matriz_rotulos[x_vizinho, y_vizinho] == 0):
                    matriz_rotulos[x_vizinho, y_vizinho] = rotulo
                    fila.append((x_vizinho, y_vizinho))
                    pixels_no_componente += 1

    return pixels_no_componente


def encontrar_todos_componentes(imagem_binaria):
    """
    PASSO 3B: Encontra e rotula todos os componentes 4-conectados

    Returns:
        tuple: (matriz_rotulos, numero_componentes, tamanhos_componentes)
    """
    print("\n" + "=" * 60)
    print("PASSO 3: ENCONTRANDO COMPONENTES 4-CONECTADOS")
    print("=" * 60)

    altura, largura = imagem_binaria.shape
    matriz_rotulos = np.zeros((altura, largura), dtype=int)
    rotulo_atual = 1
    tamanhos_componentes = []

    # Percorre toda a imagem pixel por pixel
    for i in range(altura):
        for j in range(largura):
            # Se encontrou um pixel de objeto ainda não rotulado
            if imagem_binaria[i, j] == 1 and matriz_rotulos[i, j] == 0:
                print(f"✓ Componente {rotulo_atual} encontrado na posição ({i}, {j})", end=" ")

                # Rotula todo o componente conectado
                tamanho = rotular_componente_bfs(imagem_binaria, matriz_rotulos,
                                                 i, j, rotulo_atual)
                tamanhos_componentes.append(tamanho)
                print(f"- Tamanho: {tamanho} pixels")

                rotulo_atual += 1

    numero_componentes = rotulo_atual - 1

    print(f"\n✓ TOTAL DE COMPONENTES ENCONTRADOS: {numero_componentes}")
    print(f"✓ Maior componente: {max(tamanhos_componentes) if tamanhos_componentes else 0} pixels")
    print(f"✓ Menor componente: {min(tamanhos_componentes) if tamanhos_componentes else 0} pixels")
    print(f"✓ Tamanho médio: {np.mean(tamanhos_componentes):.1f} pixels")

    return matriz_rotulos, numero_componentes, tamanhos_componentes


# =============================================================================
# PASSO 4: VISUALIZAÇÃO DOS RESULTADOS
# =============================================================================

def mostrar_resultados_visuais(imagem_original, imagem_binaria, matriz_rotulos):
    """
    PASSO 4: Cria visualizações comparativas dos resultados
    """
    print("\n" + "=" * 60)
    print("PASSO 4: CRIANDO VISUALIZAÇÕES")
    print("=" * 60)

    # Configura a figura com 3 subplots lado a lado
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Subplot 1: Imagem Original
    axes[0].imshow(imagem_original, cmap='gray')
    axes[0].set_title('Imagem Original\n(Escala de Cinza)', fontsize=12, fontweight='bold')
    axes[0].axis('off')

    # Subplot 2: Imagem Binarizada
    axes[1].imshow(imagem_binaria, cmap='gray')
    axes[1].set_title(f'Imagem Binarizada\n(Threshold = {THRESHOLD})', fontsize=12, fontweight='bold')
    axes[1].axis('off')

    # Subplot 3: Componentes Rotulados
    # Normaliza os rótulos para visualização colorida
    if np.max(matriz_rotulos) > 0:
        matriz_normalizada = matriz_rotulos / np.max(matriz_rotulos)
    else:
        matriz_normalizada = matriz_rotulos

    im = axes[2].imshow(matriz_normalizada, cmap='nipy_spectral')
    axes[2].set_title('Componentes Rotulados\n(Cada cor = 1 objeto)', fontsize=12, fontweight='bold')
    axes[2].axis('off')

    # Ajusta layout e mostra
    plt.tight_layout()
    plt.show()

    print("✓ Visualizações criadas com sucesso!")


# =============================================================================
# FUNÇÃO PRINCIPAL - EXECUTA TODOS OS PASSOS
# =============================================================================

def main():
    """
    FUNÇÃO PRINCIPAL: Executa todos os passos da atividade em sequência
    """
    print("PROCESSAMENTO DIGITAL DE IMAGENS - ATIVIDADE AVALIATIVA 2")
    print("REQUISITO 2: CONTAGEM DE OBJETOS COM THRESHOLD")
    print("Profa. Alessandra Aparecida Paulino")

    # PASSO 1: Carregar imagem
    imagem_pil, imagem_array = carregar_imagem_original()
    if imagem_array is None:
        return None

    # PASSO 2: Binarizar com threshold
    imagem_binaria = aplicar_threshold(imagem_array, THRESHOLD)
    salvar_imagem_binaria(imagem_binaria)

    # PASSO 3: Encontrar componentes conexos
    matriz_rotulos, numero_objetos, tamanhos = encontrar_todos_componentes(imagem_binaria)

    # PASSO 4: Mostrar resultados visuais
    mostrar_resultados_visuais(imagem_array, imagem_binaria, matriz_rotulos)

    # RESULTADO FINAL
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    print(f"🎯 NÚMERO DE OBJETOS ENCONTRADOS: {numero_objetos}")
    print(f"📊 Arquivo de saída gerado: '{NOME_ARQUIVO_SAIDA}'")
    print("✅ Processamento concluído com sucesso!")

    return numero_objetos


# =============================================================================
# EXECUÇÃO DO PROGRAMA
# =============================================================================

if __name__ == "__main__":
    resultado = main()