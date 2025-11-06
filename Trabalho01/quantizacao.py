import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# =============================================================================
# ATIVIDADE AVALIATIVA 1 - REQUISITO 2: QUANTIZAÇÃO
# PROFA. ALESSANDRA APARECIDA PAULINO
# =============================================================================

print("PROCESSAMENTO DIGITAL DE IMAGENS - ATIVIDADE AVALIATIVA 1")
print("REQUISITO 2: QUANTIZAÇÃO DE PIXELS (BITS POR PIXEL)")
print("Profa. Alessandra Aparecida Paulino")
print("=" * 80)

# Configurações
IMAGEM_ENTRADA = 'ctskull-256.tif'
BITS_ORIGINAL = 8  # Imagem original tem 8 bits (256 níveis)
BITS_ALVOS = [7, 6, 5, 4, 3, 2, 1]  # Bits solicitados na atividade

# =============================================================================
# TEORIA: O QUE É QUANTIZAÇÃO?
# =============================================================================

print("\n📚 CONCEITOS FUNDAMENTAIS:")
print("\n   🔍 O QUE É QUANTIZAÇÃO?")
print("      • Processo de REDUZIR o número de níveis de intensidade")
print("      • Cada pixel passa a ter MENOS bits para representar sua cor/intensidade")
print("      • Imagem fica com MENOS tons de cinza")

print("\n   🔍 BITS POR PIXEL:")
print("      • Determina quantos níveis de cinza existem")
print("      • Fórmula: L = 2^k (onde k = número de bits)")
print("      • 8 bits → 2^8 = 256 níveis (0 a 255)")
print("      • 7 bits → 2^7 = 128 níveis")
print("      • 1 bit  → 2^1 = 2 níveis (preto e branco)")

print("\n   🔍 EFEITOS DA QUANTIZAÇÃO:")
print("      • Reduz o número de cores/tons")
print("      • Cria efeito de 'posterização' ou 'contorno falso'")
print("      • Diminui o tamanho do arquivo")
print("      • Pode causar perda de detalhes sutis")


# =============================================================================
# FUNÇÕES BÁSICAS
# =============================================================================

def carregar_imagem(caminho):
    """
    Carrega uma imagem e converte para escala de cinza
    """
    try:
        img = Image.open(caminho).convert('L')
        array_img = np.array(img, dtype=np.uint8)
        print(f"\n✓ Imagem '{caminho}' carregada com sucesso!")
        print(f"   • Dimensões: {array_img.shape[1]} x {array_img.shape[0]} pixels")
        print(f"   • Bits por pixel: {BITS_ORIGINAL}")
        print(f"   • Níveis de cinza: {2 ** BITS_ORIGINAL}")
        print(f"   • Faixa de valores: 0 a {2 ** BITS_ORIGINAL - 1}")
        return array_img
    except FileNotFoundError:
        print(f"\n⚠ ERRO: Arquivo '{caminho}' não encontrado!")
        print("Criando uma imagem sintética para demonstração...")
        return criar_imagem_sintetica()


def criar_imagem_sintetica():
    """
    Cria uma imagem sintética de um crânio (CT scan simulado)
    """
    tamanho = 256
    img = np.zeros((tamanho, tamanho), dtype=np.uint8)

    # Cria círculo (crânio)
    y, x = np.ogrid[:tamanho, :tamanho]
    centro_y, centro_x = tamanho // 2, tamanho // 2

    # Crânio externo
    raio_externo = 100
    mascara_cranio = (x - centro_x) ** 2 + (y - centro_y) ** 2 <= raio_externo ** 2
    img[mascara_cranio] = 180

    # Borda do crânio
    raio_borda = 95
    mascara_borda = ((x - centro_x) ** 2 + (y - centro_y) ** 2 <= raio_externo ** 2) & \
                    ((x - centro_x) ** 2 + (y - centro_y) ** 2 >= raio_borda ** 2)
    img[mascara_borda] = 255

    # Cérebro (interior)
    raio_cerebro = 85
    mascara_cerebro = (x - centro_x) ** 2 + (y - centro_y) ** 2 <= raio_cerebro ** 2
    img[mascara_cerebro] = 120

    # Detalhes internos (ventículos, etc)
    mascara_ventriculo1 = ((x - centro_x + 20) ** 2 + (y - centro_y) ** 2 <= 15 ** 2)
    mascara_ventriculo2 = ((x - centro_x - 20) ** 2 + (y - centro_y) ** 2 <= 15 ** 2)
    img[mascara_ventriculo1] = 60
    img[mascara_ventriculo2] = 60

    # Sulcos cerebrais (linhas)
    for i in range(-80, 81, 20):
        if centro_y + i >= 0 and centro_y + i < tamanho:
            for j in range(-60, 61):
                if centro_x + j >= 0 and centro_x + j < tamanho:
                    if mascara_cerebro[centro_y + i, centro_x + j]:
                        img[centro_y + i, centro_x + j] = 90

    # Adiciona ruído sutil para simular textura de CT
    ruido = np.random.normal(0, 5, img.shape)
    img = np.clip(img + ruido, 0, 255).astype(np.uint8)

    print(f"\n✓ Imagem sintética (CT scan simulado) criada")
    print(f"   • Dimensões: {tamanho} x {tamanho} pixels")
    print(f"   • Bits por pixel: {BITS_ORIGINAL}")

    return img


# =============================================================================
# IMPLEMENTAÇÃO DA QUANTIZAÇÃO (SEM FUNÇÕES PRONTAS)
# =============================================================================

def calcular_niveis_quantizacao(bits):
    """
    Calcula o número de níveis de cinza para um dado número de bits

    FÓRMULA: L = 2^k
    onde:
    - L = número de níveis
    - k = número de bits

    Args:
        bits: Número de bits por pixel

    Returns:
        int: Número de níveis de cinza
    """
    niveis = 2 ** bits
    print(f"\n   📐 CÁLCULO DE NÍVEIS:")
    print(f"      • Bits: {bits}")
    print(f"      • Fórmula: L = 2^{bits}")
    print(f"      • Níveis de cinza: {niveis}")

    return niveis


def quantizar_imagem(imagem, bits_alvo):
    """
    Quantiza a imagem para um número específico de bits
    IMPLEMENTAÇÃO MANUAL - SEM FUNÇÕES PRONTAS

    TEORIA DA QUANTIZAÇÃO:
    - Imagem original tem 256 níveis (8 bits)
    - Queremos reduzir para 2^bits_alvo níveis
    - Precisamos "agrupar" os níveis originais em menos grupos

    ALGORITMO:
    1. Calcula quantos níveis teremos (2^bits_alvo)
    2. Calcula o "passo" entre cada nível
    3. Para cada pixel:
       a) Divide o valor pelo passo (determina em qual grupo está)
       b) Multiplica de volta pelo passo (obtém o valor representativo do grupo)

    EXEMPLO:
    - Original: 256 níveis (0-255)
    - Alvo: 4 bits → 16 níveis
    - Passo: 256/16 = 16
    - Valor 127 → 127/16 = 7 → 7*16 = 112 (novo valor)

    Args:
        imagem: Array numpy da imagem original
        bits_alvo: Número de bits desejado

    Returns:
        np.array: Imagem quantizada
    """
    print(f"\n{'=' * 70}")
    print(f"🔄 QUANTIZAÇÃO PARA {bits_alvo} BIT(S)")
    print(f"{'=' * 70}")

    # Calcula número de níveis
    niveis_alvo = calcular_niveis_quantizacao(bits_alvo)
    niveis_original = 2 ** BITS_ORIGINAL

    # Calcula o "passo" entre níveis
    passo = niveis_original / niveis_alvo

    print(f"\n   🔄 PROCESSO DE QUANTIZAÇÃO:")
    print(f"      • Níveis originais: {niveis_original} (8 bits)")
    print(f"      • Níveis alvo: {niveis_alvo} ({bits_alvo} bit(s))")
    print(f"      • Passo de quantização: {niveis_original}/{niveis_alvo} = {passo:.2f}")

    # Cria imagem quantizada
    altura, largura = imagem.shape
    imagem_quantizada = np.zeros((altura, largura), dtype=np.uint8)

    print(f"      • Processando {altura * largura:,} pixels...")

    # QUANTIZAÇÃO PIXEL POR PIXEL (implementação manual)
    for i in range(altura):
        for j in range(largura):
            # Pega valor original do pixel
            valor_original = imagem[i, j]

            # ETAPA 1: Divide pelo passo para determinar o grupo
            grupo = int(valor_original / passo)

            # ETAPA 2: Multiplica de volta para obter o valor representativo
            valor_quantizado = int(grupo * passo)

            # Garante que não ultrapassa 255
            valor_quantizado = min(valor_quantizado, 255)

            # Atribui o novo valor
            imagem_quantizada[i, j] = valor_quantizado

        # Mostra progresso a cada 10%
        if (i + 1) % (altura // 10) == 0:
            progresso = ((i + 1) / altura) * 100
            print(f"      • Progresso: {progresso:.0f}%")

    print(f"      ✓ Quantização concluída!")

    # Calcula estatísticas
    valores_unicos_original = len(np.unique(imagem))
    valores_unicos_quantizada = len(np.unique(imagem_quantizada))

    print(f"\n   📊 ESTATÍSTICAS:")
    print(f"      • Valores únicos (original): {valores_unicos_original}")
    print(f"      • Valores únicos (quantizada): {valores_unicos_quantizada}")
    print(f"      • Redução de informação: {(1 - bits_alvo / BITS_ORIGINAL) * 100:.1f}%")
    print(f"      • Compressão teórica: {BITS_ORIGINAL / bits_alvo:.2f}x")

    return imagem_quantizada


def aplicar_quantizacao_detalhada(imagem, bits_alvo):
    """
    Aplica quantização com explicação detalhada do processo
    """
    print(f"\n   💡 EXEMPLO NUMÉRICO DA QUANTIZAÇÃO:")

    # Pega alguns pixels de exemplo
    pixel_exemplo = imagem[128, 128]  # Pixel central

    niveis_alvo = 2 ** bits_alvo
    passo = 256 / niveis_alvo

    grupo = int(pixel_exemplo / passo)
    valor_quantizado = int(grupo * passo)

    print(f"      • Pixel exemplo (128, 128):")
    print(f"        - Valor original: {pixel_exemplo}")
    print(f"        - Grupo: {pixel_exemplo}/{passo:.2f} = {grupo}")
    print(f"        - Valor quantizado: {grupo} × {passo:.2f} = {valor_quantizado}")
    print(f"        - Diferença: {abs(pixel_exemplo - valor_quantizado)}")

    # Aplica quantização
    return quantizar_imagem(imagem, bits_alvo)


# =============================================================================
# VISUALIZAÇÃO DOS RESULTADOS
# =============================================================================

def visualizar_resultados(imagem_original, imagens_quantizadas, bits):
    """
    Visualiza todas as imagens lado a lado para comparação
    """
    print(f"\n{'=' * 70}")
    print("🎨 VISUALIZANDO RESULTADOS")
    print(f"{'=' * 70}")

    # Cria figura com 4x2 subplots (original + 7 quantizadas)
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('REQUISITO 2: Quantização de Pixels (Redução de Bits)',
                 fontsize=16, fontweight='bold')

    # Flatten axes para facilitar iteração
    axes = axes.flatten()

    # Imagem original
    axes[0].imshow(imagem_original, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title(f'Original\n8 bits\n256 níveis',
                      fontweight='bold', fontsize=11)
    axes[0].axis('off')

    # Imagens quantizadas
    for idx, (img_quant, bits_val) in enumerate(zip(imagens_quantizadas, bits)):
        axes[idx + 1].imshow(img_quant, cmap='gray', vmin=0, vmax=255)
        niveis = 2 ** bits_val
        axes[idx + 1].set_title(f'{bits_val} bit(s)\n{niveis} níveis',
                                fontweight='bold', fontsize=11)
        axes[idx + 1].axis('off')

    plt.tight_layout()
    plt.show()

    print("✓ Visualização principal concluída!")


def visualizar_histogramas(imagem_original, imagens_quantizadas, bits):
    """
    Visualiza histogramas para mostrar a distribuição de intensidades
    """
    print(f"\n{'=' * 70}")
    print("📊 VISUALIZANDO HISTOGRAMAS")
    print(f"{'=' * 70}")

    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('Histogramas: Distribuição de Níveis de Intensidade',
                 fontsize=16, fontweight='bold')

    axes = axes.flatten()

    # Histograma original
    axes[0].hist(imagem_original.ravel(), bins=256, range=(0, 256),
                 color='gray', alpha=0.7)
    axes[0].set_title(f'Original (8 bits)\n256 níveis possíveis', fontweight='bold')
    axes[0].set_xlabel('Intensidade')
    axes[0].set_ylabel('Frequência')
    axes[0].grid(True, alpha=0.3)

    # Histogramas quantizados
    for idx, (img_quant, bits_val) in enumerate(zip(imagens_quantizadas, bits)):
        niveis = 2 ** bits_val
        axes[idx + 1].hist(img_quant.ravel(), bins=niveis, range=(0, 256),
                           color='gray', alpha=0.7)
        axes[idx + 1].set_title(f'{bits_val} bit(s)\n{niveis} níveis',
                                fontweight='bold')
        axes[idx + 1].set_xlabel('Intensidade')
        axes[idx + 1].set_ylabel('Frequência')
        axes[idx + 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    print("✓ Histogramas gerados!")


def visualizar_zoom_comparacao(imagem_original, imagens_quantizadas, bits):
    """
    Visualiza ZOOM em uma região para ver o efeito de posterização
    """
    print(f"\n{'=' * 70}")
    print("🔍 VISUALIZAÇÃO COM ZOOM (Efeito de Posterização)")
    print(f"{'=' * 70}")

    # Define região de interesse (centro)
    altura, largura = imagem_original.shape
    y_start = altura // 3
    y_end = 2 * altura // 3
    x_start = largura // 3
    x_end = 2 * largura // 3

    # Cria figura
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('ZOOM: Efeito de Posterização (Contornos Falsos)',
                 fontsize=16, fontweight='bold')

    axes = axes.flatten()

    # Original
    regiao_orig = imagem_original[y_start:y_end, x_start:x_end]
    axes[0].imshow(regiao_orig, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
    axes[0].set_title('Original (8 bits)\nTransições suaves', fontweight='bold')
    axes[0].axis('off')

    # Quantizadas
    for idx, (img_quant, bits_val) in enumerate(zip(imagens_quantizadas, bits)):
        regiao = img_quant[y_start:y_end, x_start:x_end]
        axes[idx + 1].imshow(regiao, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
        axes[idx + 1].set_title(f'{bits_val} bit(s)\nContornos visíveis', fontweight='bold')
        axes[idx + 1].axis('off')

    plt.tight_layout()
    plt.show()

    print("✓ Visualização com zoom concluída!")


# =============================================================================
# ANÁLISE E DISCUSSÃO DOS RESULTADOS
# =============================================================================

def analisar_resultados(imagem_original, imagens_quantizadas, bits):
    """
    Análise detalhada dos efeitos da quantização
    """
    print(f"\n{'=' * 80}")
    print("📊 ANÁLISE DOS RESULTADOS - EFEITOS DA QUANTIZAÇÃO")
    print(f"{'=' * 80}")

    print("\n🔍 OBSERVAÇÕES SOBRE RESOLUÇÃO DE INTENSIDADE:")

    for img_quant, bits_val in zip(imagens_quantizadas, bits):
        niveis = 2 ** bits_val
        valores_unicos = len(np.unique(img_quant))

        print(f"\n   📌 {bits_val} BIT(S) ({niveis} NÍVEIS):")
        print(f"      • Níveis teóricos: {niveis}")
        print(f"      • Valores únicos na imagem: {valores_unicos}")

        if bits_val >= 5:
            print(f"      • Efeito visual: Quase imperceptível ao olho humano")
            print(f"      • Qualidade: Excelente para a maioria das aplicações")
        elif bits_val >= 3:
            print(f"      • Efeito visual: Posterização visível em zonas suaves")
            print(f"      • Qualidade: Aceitável para algumas aplicações")
        else:
            print(f"      • Efeito visual: Posterização severa, contornos falsos")
            print(f"      • Qualidade: Perda significativa de informação")

    print("\n💡 CONCEITOS IMPORTANTES:")
    print("   • RESOLUÇÃO DE INTENSIDADE: Menor alteração discernível nos níveis")
    print("   • POSTERIZAÇÃO: Efeito de 'bandas' ou 'contornos falsos'")
    print("   • Ocorre quando há poucos níveis para representar transições suaves")
    print("   • Bits ↓ = Níveis ↓ = Mais posterização")

    print("\n📚 OBSERVAÇÃO CIENTÍFICA:")
    print("   • O olho humano distingue aproximadamente 100-200 níveis de cinza")
    print("   • 8 bits (256 níveis) é geralmente suficiente")
    print("   • 6 bits (64 níveis) ainda é aceitável em muitos casos")
    print("   • Abaixo de 5 bits a qualidade deteriora rapidamente")

    print("\n⚖️ TRADE-OFF: QUALIDADE vs ARMAZENAMENTO")
    print("   • 8 bits → 1 byte por pixel (padrão)")
    print("   • 4 bits → 0.5 byte por pixel (50% de economia)")
    print("   • 1 bit  → 0.125 byte por pixel (87.5% de economia)")
    print("   • Mas com perda progressiva de qualidade!")

    print("\n🎯 APLICAÇÕES PRÁTICAS:")
    print("   • IMAGENS MÉDICAS: 12-16 bits (alta precisão)")
    print("   • FOTOS COMUNS: 8 bits (suficiente)")
    print("   • FAX, DOCUMENTOS: 1 bit (preto e branco)")
    print("   • COMPRESSÃO: Pode usar menos bits em regiões homogêneas")


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """
    Executa o Requisito 2 completo da atividade
    """
    print("\n🚀 INICIANDO REQUISITO 2: QUANTIZAÇÃO")

    # Carrega imagem original
    print(f"\n{'=' * 80}")
    print("📷 ETAPA 1: CARREGANDO IMAGEM ORIGINAL")
    print(f"{'=' * 80}")

    imagem_original = carregar_imagem(IMAGEM_ENTRADA)

    # Aplica quantização para cada nível de bits
    print(f"\n{'=' * 80}")
    print("📷 ETAPA 2: APLICANDO QUANTIZAÇÕES")
    print(f"{'=' * 80}")

    imagens_quantizadas = []

    for bits in BITS_ALVOS:
        img_quantizada = aplicar_quantizacao_detalhada(imagem_original, bits)
        imagens_quantizadas.append(img_quantizada)

    # Visualiza resultados
    print(f"\n{'=' * 80}")
    print("📷 ETAPA 3: VISUALIZAÇÃO DOS RESULTADOS")
    print(f"{'=' * 80}")

    visualizar_resultados(imagem_original, imagens_quantizadas, BITS_ALVOS)
    visualizar_histogramas(imagem_original, imagens_quantizadas, BITS_ALVOS)
    visualizar_zoom_comparacao(imagem_original, imagens_quantizadas, BITS_ALVOS)

    # Análise final
    analisar_resultados(imagem_original, imagens_quantizadas, BITS_ALVOS)

    print(f"\n{'=' * 80}")
    print("🎉 REQUISITO 2 CONCLUÍDO COM SUCESSO!")
    print(f"{'=' * 80}")
    print("\n📋 Resultados obtidos:")
    print(f"   ✅ Imagem original (8 bits) carregada")
    print(f"   ✅ Quantização para 7 bits concluída")
    print(f"   ✅ Quantização para 6 bits concluída")
    print(f"   ✅ Quantização para 5 bits concluída")
    print(f"   ✅ Quantização para 4 bits concluída")
    print(f"   ✅ Quantização para 3 bits concluída")
    print(f"   ✅ Quantização para 2 bits concluída")
    print(f"   ✅ Quantização para 1 bit concluída")
    print(f"   ✅ Visualizações comparativas geradas (imagens, histogramas, zoom)")
    print(f"   ✅ Análise detalhada dos efeitos apresentada")
    print(f"   ✅ NENHUMA função pronta utilizada (implementação manual)")


# =============================================================================
# EXECUÇÃO DO PROGRAMA
# =============================================================================

if __name__ == "__main__":
    main()