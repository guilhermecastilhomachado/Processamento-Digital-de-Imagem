import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import deque

plt.rcParams['font.family'] = 'Segoe UI Emoji'

# =============================================================================
# CONFIGURAÇÕES INICIAIS
# =============================================================================

# Configurações dos arquivos
NOME_ARQUIVO_ENTRADA = 'art8.png'
NOME_ARQUIVO_SAIDA_1 = 'art8lab1.png'  # Conforme especificado na atividade
NOME_ARQUIVO_SAIDA_2 = 'art8lab2.png'  # Conforme especificado na atividade
THRESHOLD_BINARIZACAO = 127  # Para converter escala de cinza em binário


# =============================================================================
# PASSO 1: CARREGAMENTO E PRÉ-PROCESSAMENTO DA IMAGEM
# =============================================================================

def carregar_e_preprocessar_imagem():
    """
    PASSO 1: Carrega a imagem art8.png e a prepara para rotulação

    Returns:
        tuple: (imagem_original_array, imagem_binaria) ou (None, None) se houver erro
    """
    print("=" * 60)
    print("PASSO 1: CARREGAMENTO E PRÉ-PROCESSAMENTO")
    print("=" * 60)

    try:
        # Carrega imagem e converte para escala de cinza
        imagem_original = Image.open(NOME_ARQUIVO_ENTRADA).convert('L')
        imagem_array = np.array(imagem_original)

        print(f"✓ Imagem '{NOME_ARQUIVO_ENTRADA}' carregada com sucesso!")
        print(f"✓ Dimensões: {imagem_array.shape[0]} x {imagem_array.shape[1]} pixels")
        print(f"✓ Valores de pixel: {np.min(imagem_array)} até {np.max(imagem_array)}")

        # Converte para binária (0s e 1s)
        # Pixels > threshold viram 1 (objeto), pixels <= threshold viram 0 (fundo)
        imagem_binaria = np.where(imagem_array > THRESHOLD_BINARIZACAO, 1, 0)

        # Estatísticas da binarização
        pixels_objeto = np.sum(imagem_binaria == 1)
        pixels_fundo = np.sum(imagem_binaria == 0)
        total_pixels = imagem_binaria.size

        print(f"\n✓ Binarização aplicada (threshold = {THRESHOLD_BINARIZACAO}):")
        print(f"  - Pixels de OBJETO (valor 1): {pixels_objeto} ({pixels_objeto / total_pixels * 100:.1f}%)")
        print(f"  - Pixels de FUNDO (valor 0): {pixels_fundo} ({pixels_fundo / total_pixels * 100:.1f}%)")

        return imagem_array, imagem_binaria

    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo '{NOME_ARQUIVO_ENTRADA}' não encontrado!")
        print("   Certifique-se de que o arquivo está na mesma pasta do código.")
        return None, None


def mostrar_imagem_binaria(imagem_binaria):
    """
    Mostra a imagem binária para verificação visual
    """
    print("\n✓ Exibindo imagem binária para verificação...")
    plt.figure(figsize=(8, 6))
    plt.imshow(imagem_binaria, cmap='gray')
    plt.title('Imagem Binária - art8.png\n(Preto = Fundo, Branco = Objeto)',
              fontsize=12, fontweight='bold')
    plt.axis('off')
    plt.show()


# =============================================================================
# PASSO 2: ALGORITMO DE ROTULAÇÃO 4-CONECTADA
# =============================================================================

def rotular_componente_bfs(imagem_binaria, matriz_rotulos, x_inicial, y_inicial, rotulo):
    """
    PASSO 2A: Rotula um componente específico usando BFS (Busca em Largura)

    Utiliza 4-conectividade: considera apenas vizinhos acima, abaixo, esquerda e direita

    Args:
        imagem_binaria: Imagem binarizada (0s e 1s)
        matriz_rotulos: Matriz onde serão armazenados os rótulos
        x_inicial, y_inicial: Coordenadas do pixel inicial do componente
        rotulo: Número do rótulo a ser atribuído

    Returns:
        int: Número de pixels do componente rotulado
    """
    altura, largura = imagem_binaria.shape

    # Inicializa fila para BFS (mais eficiente que recursão)
    fila = deque()
    fila.append((x_inicial, y_inicial))
    matriz_rotulos[x_inicial, y_inicial] = rotulo

    # Define os 4 vizinhos para conectividade (NÃO inclui diagonais)
    # Ordem: cima, baixo, esquerda, direita
    vizinhos_4conectados = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    pixels_rotulados = 1  # Conta pixels do componente atual

    # Algoritmo BFS
    while fila:
        x_atual, y_atual = fila.popleft()

        # Verifica todos os 4 vizinhos do pixel atual
        for deslocamento_x, deslocamento_y in vizinhos_4conectados:
            x_vizinho = x_atual + deslocamento_x
            y_vizinho = y_atual + deslocamento_y

            # Verifica se o vizinho está dentro dos limites da imagem
            if (0 <= x_vizinho < altura) and (0 <= y_vizinho < largura):
                # Verifica se é pixel de objeto (1) e ainda não foi rotulado (0)
                if (imagem_binaria[x_vizinho, y_vizinho] == 1 and
                        matriz_rotulos[x_vizinho, y_vizinho] == 0):
                    # Rotula o vizinho e adiciona à fila
                    matriz_rotulos[x_vizinho, y_vizinho] = rotulo
                    fila.append((x_vizinho, y_vizinho))
                    pixels_rotulados += 1

    return pixels_rotulados


def executar_rotulacao_completa(imagem_binaria):
    """
    PASSO 2B: Executa a rotulação completa de todos os componentes

    Returns:
        tuple: (matriz_rotulos, numero_componentes, tamanhos_componentes)
    """
    print("\n" + "=" * 60)
    print("PASSO 2: ROTULAÇÃO DE COMPONENTES 4-CONECTADOS")
    print("=" * 60)

    altura, largura = imagem_binaria.shape
    matriz_rotulos = np.zeros((altura, largura), dtype=int)  # 0 = não visitado
    rotulo_atual = 1  # Começa rotulando a partir de 1
    tamanhos_componentes = []

    print("🔍 Percorrendo imagem pixel por pixel...")

    # Percorre toda a imagem procurando componentes não rotulados
    for linha in range(altura):
        for coluna in range(largura):
            # Se encontrou um pixel de objeto ainda não rotulado
            if imagem_binaria[linha, coluna] == 1 and matriz_rotulos[linha, coluna] == 0:
                print(f"✓ Componente {rotulo_atual} encontrado na posição ({linha}, {coluna})", end=" ")

                # Rotula todo o componente conectado usando BFS
                tamanho_componente = rotular_componente_bfs(
                    imagem_binaria, matriz_rotulos, linha, coluna, rotulo_atual
                )

                tamanhos_componentes.append(tamanho_componente)
                print(f"→ Tamanho: {tamanho_componente} pixels")

                rotulo_atual += 1

    numero_total_componentes = rotulo_atual - 1

    # Estatísticas finais
    print(f"\n🎯 ROTULAÇÃO CONCLUÍDA!")
    print(f"✓ Total de componentes encontrados: {numero_total_componentes}")
    if tamanhos_componentes:
        print(f"✓ Maior componente: {max(tamanhos_componentes)} pixels")
        print(f"✓ Menor componente: {min(tamanhos_componentes)} pixels")
        print(f"✓ Tamanho médio dos componentes: {np.mean(tamanhos_componentes):.1f} pixels")

    return matriz_rotulos, numero_total_componentes, tamanhos_componentes


# =============================================================================
# PASSO 3: VISUALIZAÇÃO E SALVAMENTO DOS RESULTADOS
# =============================================================================

def criar_visualizacao_comparativa(imagem_original, imagem_binaria, matriz_rotulos):
    """
    PASSO 3A: Cria visualização comparativa dos resultados

    EXPLICAÇÃO DOS 3 GRÁFICOS:
    1. IMAGEM ORIGINAL: Como a imagem foi carregada (escala de cinza)
    2. IMAGEM BINÁRIA: Após binarização (apenas 0s e 1s - preto e branco)
    3. COMPONENTES ROTULADOS: Cada componente conexo com uma cor diferente
    """
    print("\n" + "=" * 60)
    print("PASSO 3: VISUALIZAÇÃO DOS RESULTADOS")
    print("=" * 60)
    print("📊 Criando 3 visualizações para comparação:")
    print("   1️⃣ ORIGINAL: Imagem como foi carregada")
    print("   2️⃣ BINÁRIA: Após aplicar threshold (preto/branco)")
    print("   3️⃣ ROTULADA: Cada componente com cor diferente")

    # Configura subplot com 3 imagens lado a lado
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # GRÁFICO 1: Imagem Original em escala de cinza
    axes[0].imshow(imagem_original, cmap='gray')
    axes[0].set_title('1️⃣ IMAGEM ORIGINAL\n(Escala de Cinza)\n' +
                      f'Valores: {np.min(imagem_original)} - {np.max(imagem_original)}',
                      fontsize=11, fontweight='bold')
    axes[0].axis('off')

    # GRÁFICO 2: Imagem Binária
    pixels_objeto = np.sum(imagem_binaria == 1)
    pixels_fundo = np.sum(imagem_binaria == 0)
    axes[1].imshow(imagem_binaria, cmap='gray')
    axes[1].set_title('2️⃣ IMAGEM BINÁRIA\n(Após Threshold)\n' +
                      f'Objetos: {pixels_objeto} pixels',
                      fontsize=11, fontweight='bold')
    axes[1].axis('off')

    # GRÁFICO 3: Componentes rotulados com cores
    num_componentes = len(np.unique(matriz_rotulos)) - 1  # -1 para excluir o fundo (0)
    if np.max(matriz_rotulos) > 0:
        matriz_normalizada = matriz_rotulos / np.max(matriz_rotulos)
    else:
        matriz_normalizada = matriz_rotulos

    im = axes[2].imshow(matriz_normalizada, cmap='nipy_spectral')
    axes[2].set_title('3️⃣ COMPONENTES ROTULADOS\n(Cada Cor = 1 Componente)\n' +
                      f'Total: {num_componentes} componentes',
                      fontsize=11, fontweight='bold')
    axes[2].axis('off')

    # Adiciona barra de cores para a imagem rotulada
    cbar = plt.colorbar(im, ax=axes[2], fraction=0.046, pad=0.04)
    cbar.set_label('Rótulo do Componente', rotation=270, labelpad=15)

    plt.tight_layout()
    plt.show()

    print("\n🎨 INTERPRETAÇÃO DOS GRÁFICOS:")
    print("   • GRÁFICO 1: Mostra a imagem como você a vê normalmente")
    print("   • GRÁFICO 2: Mostra apenas objetos (branco) e fundo (preto)")
    print("   • GRÁFICO 3: Cada 'ilha' de pixels conectados tem uma cor única")
    print("   ✓ Compare: pixels brancos do gráfico 2 viram cores diferentes no gráfico 3")


def salvar_resultados(matriz_rotulos, numero_componentes):
    """
    PASSO 3B: Salva os resultados conforme especificado na atividade
    """
    print(f"\n🗄️ SALVANDO RESULTADOS...")

    # Verifica se há componentes para salvar
    if numero_componentes == 0:
        print("⚠️  Nenhum componente encontrado. Não há nada para salvar.")
        return

    # SAÍDA 1: art8lab1.png - Imagem em escala de cinza com rótulos
    # Normaliza rótulos para o intervalo 0-255
    rotulos_normalizados = (matriz_rotulos * 255 // numero_componentes).astype(np.uint8)

    if not os.path.exists(NOME_ARQUIVO_SAIDA_1):
        imagem_cinza = Image.fromarray(rotulos_normalizados, 'L')
        imagem_cinza.save(NOME_ARQUIVO_SAIDA_1)
        print(f"✓ '{NOME_ARQUIVO_SAIDA_1}' salvo com sucesso!")
    else:
        print(f"⚠️  '{NOME_ARQUIVO_SAIDA_1}' já existe. Arquivo não foi sobrescrito.")

    # SAÍDA 2: art8lab2.png - Imagem colorida com rótulos
    # Converte rótulos normalizados para imagem colorida usando colormap
    matriz_normalizada = matriz_rotulos / np.max(matriz_rotulos) if np.max(matriz_rotulos) > 0 else matriz_rotulos

    # Aplica colormap e converte para RGB (CORREÇÃO do warning do Matplotlib)
    import matplotlib.pyplot as plt
    colormap = plt.colormaps.get_cmap('nipy_spectral')  # Método atualizado
    imagem_colorida_array = colormap(matriz_normalizada)
    imagem_colorida_rgb = (imagem_colorida_array[:, :, :3] * 255).astype(np.uint8)

    if not os.path.exists(NOME_ARQUIVO_SAIDA_2):
        imagem_colorida = Image.fromarray(imagem_colorida_rgb, 'RGB')
        imagem_colorida.save(NOME_ARQUIVO_SAIDA_2)
        print(f"✓ '{NOME_ARQUIVO_SAIDA_2}' salvo com sucesso!")
    else:
        print(f"⚠️  '{NOME_ARQUIVO_SAIDA_2}' já existe. Arquivo não foi sobrescrito.")


# =============================================================================
# FUNÇÃO PRINCIPAL - EXECUTA TODOS OS PASSOS
# =============================================================================

def main():
    """
    FUNÇÃO PRINCIPAL: Executa todos os passos da rotulação em sequência
    """
    print("PROCESSAMENTO DIGITAL DE IMAGENS - ATIVIDADE AVALIATIVA 2")
    print("REQUISITO 1: ROTULAÇÃO DE COMPONENTES CONEXOS")
    print("Profa. Alessandra Aparecida Paulino")

    # PASSO 1: Carregamento e pré-processamento
    imagem_original, imagem_binaria = carregar_e_preprocessar_imagem()
    if imagem_binaria is None:
        return None

    # Mostra imagem binária para verificação
    mostrar_imagem_binaria(imagem_binaria)

    # PASSO 2: Rotulação de componentes
    matriz_rotulos, numero_componentes, tamanhos = executar_rotulacao_completa(imagem_binaria)

    # PASSO 3: Visualização e salvamento
    criar_visualizacao_comparativa(imagem_original, imagem_binaria, matriz_rotulos)
    salvar_resultados(matriz_rotulos, numero_componentes)

    # RESULTADO FINAL
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    print(f"🎯 NÚMERO TOTAL DE COMPONENTES: {numero_componentes}")
    print(f"📁 Arquivos de saída gerados: '{NOME_ARQUIVO_SAIDA_1}' e '{NOME_ARQUIVO_SAIDA_2}'")
    print("✅ Rotulação concluída com sucesso!")

    return numero_componentes


# =============================================================================
# EXECUÇÃO DO PROGRAMA
# =============================================================================

if __name__ == "__main__":
    resultado = main()