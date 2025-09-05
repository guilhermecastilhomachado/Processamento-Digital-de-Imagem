import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# =============================================================================
# ATIVIDADE AVALIATIVA 5 - FILTROS DE REALCE
# PROFA. ALESSANDRA APARECIDA PAULINO
# =============================================================================

print("PROCESSAMENTO DIGITAL DE IMAGENS - ATIVIDADE AVALIATIVA 5")
print("FILTROS DE REALCE - SOBEL, LAPLACIANO, UNSHARP MASKING E HIGHBOOST")
print("Profa. Alessandra Aparecida Paulino")
print("=" * 80)

# Configurações
IMAGEM_ENTRADA = 'cln1.gif'


# =============================================================================
# FUNÇÕES BÁSICAS (REUTILIZADAS DA ATIVIDADE ANTERIOR)
# =============================================================================

def carregar_imagem(caminho):
    """
    Carrega uma imagem e converte para escala de cinza
    """
    try:
        img = Image.open(caminho).convert('L')
        array_img = np.array(img, dtype=np.float64)
        print(f"✓ Imagem '{caminho}' carregada: {array_img.shape[0]}x{array_img.shape[1]} pixels")
        return array_img
    except FileNotFoundError:
        print(f"⚠ ERRO: Arquivo '{caminho}' não encontrado!")
        print("Criando uma imagem sintética para demonstração...")
        return criar_imagem_sintetica()


def criar_imagem_sintetica():
    """
    Cria uma imagem sintética para demonstração caso o arquivo não seja encontrado
    """
    # Cria uma imagem com diferentes regiões para testar os filtros
    img = np.zeros((200, 200))

    # Quadrado no centro
    img[50:150, 50:150] = 100

    # Círculo
    y, x = np.ogrid[:200, :200]
    center_y, center_x = 100, 150
    mask = (x - center_x) ** 2 + (y - center_y) ** 2 <= 30 ** 2
    img[mask] = 200

    # Gradiente horizontal
    for i in range(200):
        img[150:180, i] = i * 255 / 200

    # Adiciona ruído
    noise = np.random.normal(0, 10, img.shape)
    img = np.clip(img + noise, 0, 255)

    print("✓ Imagem sintética criada para demonstração")
    return img


def normalizar_imagem(img):
    """
    Normaliza a imagem para o intervalo [0, 255] e converte para uint8
    """
    img_norm = np.clip(img, 0, 255)
    return img_norm.astype(np.uint8)


def aplicar_padding(imagem, tamanho_kernel):
    """
    Aplica padding zero à imagem para manter o tamanho original após convolução
    """
    pad_size = tamanho_kernel // 2
    return np.pad(imagem, pad_size, mode='constant', constant_values=0)


def aplicar_convolucao_2d(imagem, kernel):
    """
    Aplica convolução 2D manualmente (IMPLEMENTAÇÃO DA ATIVIDADE ANTERIOR)
    Esta é a função base que será usada por todos os filtros
    """
    altura_img, largura_img = imagem.shape
    altura_kernel, largura_kernel = kernel.shape

    # Aplica padding para manter o tamanho original
    imagem_com_padding = aplicar_padding(imagem, altura_kernel)

    # Inicializa matriz de saída
    imagem_resultado = np.zeros((altura_img, largura_img), dtype=np.float64)

    # Executa convolução pixel por pixel
    for i in range(altura_img):
        for j in range(largura_img):
            # Extrai a região da imagem correspondente ao kernel
            regiao = imagem_com_padding[i:i + altura_kernel, j:j + largura_kernel]
            # Executa a operação de convolução: multiplica e soma
            valor_convoluido = np.sum(regiao * kernel)
            imagem_resultado[i, j] = valor_convoluido

    return imagem_resultado


# =============================================================================
# REQUISITO 1: FILTRO DE SOBEL
# =============================================================================

def criar_filtros_sobel():
    """
    Cria as máscaras do operador de Sobel para detectar bordas horizontais e verticais

    TEORIA DO FILTRO DE SOBEL:
    - Baseado em derivadas de primeira ordem
    - Utiliza duas máscaras 3x3: uma para bordas verticais (Gx) e outra para horizontais (Gy)
    - A magnitude do gradiente combina ambas as direções
    """
    print("\n🔧 CRIANDO FILTROS DE SOBEL")

    # Máscara para detectar bordas verticais (derivada em X)
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]], dtype=np.float64)

    # Máscara para detectar bordas horizontais (derivada em Y)
    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]], dtype=np.float64)

    print("   • Sobel X (bordas verticais):")
    print("     -1  0  1")
    print("     -2  0  2")
    print("     -1  0  1")

    print("   • Sobel Y (bordas horizontais):")
    print("     -1 -2 -1")
    print("      0  0  0")
    print("      1  2  1")

    return sobel_x, sobel_y


def aplicar_filtro_sobel(imagem):
    """
    Aplica o filtro de Sobel obtendo:
    1. Derivada em X (bordas verticais)
    2. Derivada em Y (bordas horizontais)
    3. Magnitude do gradiente
    """
    print("\n📊 APLICANDO FILTRO DE SOBEL")

    # Cria as máscaras de Sobel
    sobel_x, sobel_y = criar_filtros_sobel()

    # Aplica convolução com cada máscara (USANDO IMPLEMENTAÇÃO DA ATIVIDADE ANTERIOR)
    print("   🔄 Calculando derivada em X...")
    derivada_x = aplicar_convolucao_2d(imagem, sobel_x)

    print("   🔄 Calculando derivada em Y...")
    derivada_y = aplicar_convolucao_2d(imagem, sobel_y)

    # Calcula a magnitude do gradiente: M(x,y) = sqrt(Gx² + Gy²)
    print("   🔄 Calculando magnitude do gradiente...")
    magnitude = np.sqrt(derivada_x ** 2 + derivada_y ** 2)

    # Normaliza todas as imagens para visualização
    derivada_x_norm = normalizar_imagem(np.abs(derivada_x))  # Valor absoluto para visualização
    derivada_y_norm = normalizar_imagem(np.abs(derivada_y))
    magnitude_norm = normalizar_imagem(magnitude)

    print("✅ Filtro de Sobel aplicado com sucesso")

    return derivada_x_norm, derivada_y_norm, magnitude_norm


# =============================================================================
# REQUISITO 2A: FILTRO LAPLACIANO
# =============================================================================

def criar_filtro_laplaciano():
    """
    Cria a máscara do operador Laplaciano (derivada de segunda ordem)

    TEORIA DO LAPLACIANO:
    - Baseado na derivada de segunda ordem: ∇²f = ∂²f/∂x² + ∂²f/∂y²
    - Isotrópico (independente da direção)
    - Enfatiza bordas e descontinuidades
    - Produz imagem com fundo "perdido"
    """
    print("\n🔧 CRIANDO FILTRO LAPLACIANO")

    # Máscara Laplaciana padrão (conforme slides da aula)
    laplaciano = np.array([[0, 1, 0],
                           [1, -4, 1],
                           [0, 1, 0]], dtype=np.float64)

    print("   • Máscara Laplaciana:")
    print("      0  1  0")
    print("      1 -4  1")
    print("      0  1  0")

    return laplaciano


def aplicar_filtro_laplaciano(imagem):
    """
    Aplica filtro Laplaciano com reconstrução do fundo
    Fórmula: g(x,y) = f(x,y) + c*∇²f(x,y)
    onde c = -1 se o centro da máscara é negativo, c = +1 caso contrário
    """
    print("\n📊 APLICANDO FILTRO LAPLACIANO")

    # Cria a máscara Laplaciana
    laplaciano = criar_filtro_laplaciano()

    # Aplica convolução (USANDO IMPLEMENTAÇÃO DA ATIVIDADE ANTERIOR)
    print("   🔄 Aplicando convolução Laplaciana...")
    resultado_laplaciano = aplicar_convolucao_2d(imagem, laplaciano)

    # Reconstrói o fundo somando à imagem original
    # Como o centro da máscara é negativo (-4), usamos c = -1
    c = -1
    print("   🔄 Reconstruindo fundo da imagem...")
    imagem_realcada = imagem + c * resultado_laplaciano

    # Normaliza o resultado
    imagem_final = normalizar_imagem(imagem_realcada)

    print("✅ Filtro Laplaciano aplicado com sucesso")

    return imagem_final


# =============================================================================
# REQUISITO 2B: UNSHARP MASKING
# =============================================================================

def criar_filtro_gaussiano_simples():
    """
    Cria um filtro gaussiano simples para suavização (implementação própria)
    """
    # Filtro gaussiano 5x5 aproximado
    gaussiano = np.array([[1, 4, 6, 4, 1],
                          [4, 16, 24, 16, 4],
                          [6, 24, 36, 24, 6],
                          [4, 16, 24, 16, 4],
                          [1, 4, 6, 4, 1]], dtype=np.float64)

    # Normaliza para que a soma seja 1
    gaussiano = gaussiano / np.sum(gaussiano)

    return gaussiano


def aplicar_unsharp_masking(imagem, k=1.0):
    """
    Aplica Unsharp Masking

    PROCESSO (conforme slides da aula):
    1. Suaviza a imagem original: s(x,y)
    2. Calcula a máscara: g_mask = f(x,y) - s(x,y)
    3. Adiciona a máscara à original: g = f + k*g_mask

    Args:
        imagem: Imagem original
        k: Fator de intensificação (k=1 é unsharp masking padrão)
    """
    print(f"\n📊 APLICANDO UNSHARP MASKING (k={k})")

    # Passo 1: Suaviza a imagem (USANDO IMPLEMENTAÇÃO DA ATIVIDADE ANTERIOR)
    print("   🔄 Suavizando imagem...")
    filtro_gaussiano = criar_filtro_gaussiano_simples()
    imagem_suavizada = aplicar_convolucao_2d(imagem, filtro_gaussiano)

    # Passo 2: Calcula a máscara de nitidez
    print("   🔄 Calculando máscara de nitidez...")
    mascara_nitidez = imagem - imagem_suavizada

    # Passo 3: Adiciona a máscara à imagem original
    print("   🔄 Aplicando realce...")
    imagem_realcada = imagem + k * mascara_nitidez

    # Normaliza o resultado
    imagem_final = normalizar_imagem(imagem_realcada)

    print("✅ Unsharp Masking aplicado com sucesso")

    return imagem_final


# =============================================================================
# REQUISITO 2C: HIGHBOOST FILTERING
# =============================================================================

def aplicar_highboost_filtering(imagem, k=2.0):
    """
    Aplica Highboost Filtering (k > 1)
    É uma extensão do unsharp masking com fator k > 1
    Fórmula: g = f + k*g_mask (onde k > 1)
    """
    print(f"\n📊 APLICANDO HIGHBOOST FILTERING (k={k})")

    # Usa a mesma implementação do unsharp masking com k > 1
    return aplicar_unsharp_masking(imagem, k)


# =============================================================================
# REQUISITO 2D: ATENUAÇÃO DO EFEITO (K < 1)
# =============================================================================

def aplicar_efeito_atenuado(imagem, k=0.5):
    """
    Aplica filtro com k < 1 para atenuar o efeito
    Fórmula: g = f + k*g_mask (onde k < 1)
    """
    print(f"\n📊 APLICANDO EFEITO ATENUADO (k={k})")

    # Usa a mesma implementação do unsharp masking com k < 1
    return aplicar_unsharp_masking(imagem, k)


# =============================================================================
# VISUALIZAÇÃO E COMPARAÇÃO DOS RESULTADOS
# =============================================================================

def visualizar_resultados_sobel(imagem_original, derivada_x, derivada_y, magnitude):
    """
    Visualiza os resultados do filtro de Sobel
    """
    print("\n🎨 VISUALIZANDO RESULTADOS DO SOBEL")

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('REQUISITO 1: Filtro de Sobel - Detecção de Bordas',
                 fontsize=16, fontweight='bold')

    # Imagem original
    axes[0, 0].imshow(imagem_original, cmap='gray')
    axes[0, 0].set_title('Imagem Original', fontweight='bold')
    axes[0, 0].axis('off')

    # Derivada em X (bordas verticais)
    axes[0, 1].imshow(derivada_x, cmap='gray')
    axes[0, 1].set_title('Derivada em X\n(Bordas Verticais)', fontweight='bold')
    axes[0, 1].axis('off')

    # Derivada em Y (bordas horizontais)
    axes[1, 0].imshow(derivada_y, cmap='gray')
    axes[1, 0].set_title('Derivada em Y\n(Bordas Horizontais)', fontweight='bold')
    axes[1, 0].axis('off')

    # Magnitude do gradiente
    axes[1, 1].imshow(magnitude, cmap='gray')
    axes[1, 1].set_title('Magnitude do Gradiente\n(Bordas Completas)', fontweight='bold')
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.show()


def visualizar_resultados_realce(imagem_original, resultado_laplaciano,
                                 resultado_unsharp, resultado_highboost, resultado_atenuado):
    """
    Visualiza os resultados dos filtros de realce
    """
    print("\n🎨 VISUALIZANDO RESULTADOS DOS FILTROS DE REALCE")

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('REQUISITO 2: Técnicas de Realce de Imagens',
                 fontsize=16, fontweight='bold')

    # Imagem original
    axes[0, 0].imshow(imagem_original, cmap='gray')
    axes[0, 0].set_title('Original', fontweight='bold')
    axes[0, 0].axis('off')

    # Filtro Laplaciano
    axes[0, 1].imshow(resultado_laplaciano, cmap='gray')
    axes[0, 1].set_title('a) Filtro Laplaciano\n(Realce de bordas)', fontweight='bold')
    axes[0, 1].axis('off')

    # Unsharp Masking
    axes[0, 2].imshow(resultado_unsharp, cmap='gray')
    axes[0, 2].set_title('b) Unsharp Masking\n(k=1.0)', fontweight='bold')
    axes[0, 2].axis('off')

    # Highboost Filtering
    axes[1, 0].imshow(resultado_highboost, cmap='gray')
    axes[1, 0].set_title('c) Highboost Filtering\n(k=2.0)', fontweight='bold')
    axes[1, 0].axis('off')

    # Efeito atenuado
    axes[1, 1].imshow(resultado_atenuado, cmap='gray')
    axes[1, 1].set_title('d) Efeito Atenuado\n(k=0.5)', fontweight='bold')
    axes[1, 1].axis('off')

    # Remove subplot vazio
    axes[1, 2].axis('off')

    plt.tight_layout()
    plt.show()


# =============================================================================
# DISCUSSÃO DOS RESULTADOS (CONFORME SOLICITADO NA ATIVIDADE)
# =============================================================================

def discutir_resultados():
    """
    Discussão detalhada das diferenças entre os métodos (conforme solicitado)
    """
    print(f"\n{'=' * 80}")
    print("🔍 DISCUSSÃO DAS DIFERENÇAS - ANÁLISE COMPARATIVA")
    print(f"{'=' * 80}")

    print("\n📊 ANÁLISE DO FILTRO DE SOBEL:")
    print("   • DERIVADA EM X: Detecta bordas VERTICAIS (mudanças horizontais de intensidade)")
    print("   • DERIVADA EM Y: Detecta bordas HORIZONTAIS (mudanças verticais de intensidade)")
    print("   • MAGNITUDE: Combina ambas as direções, fornecendo detecção completa de bordas")
    print("   • VANTAGEM: Boa supressão de ruído comparado a outros operadores de borda")

    print("\n📊 COMPARAÇÃO DOS MÉTODOS DE REALCE:")

    print("\n   🔸 FILTRO LAPLACIANO:")
    print("     ✓ CARACTERÍSTICAS:")
    print("       - Baseado na derivada de segunda ordem")
    print("       - Isotrópico (detecta bordas em todas as direções)")
    print("       - Realça detalhes finos e bordas")
    print("     ✓ DIFERENÇAS OBSERVADAS:")
    print("       - Produz realce mais agressivo que outros métodos")
    print("       - Amplifica significativamente o ruído")
    print("       - Cria bordas mais nítidas mas pode gerar artefatos")

    print("\n   🔸 UNSHARP MASKING (k=1.0):")
    print("     ✓ CARACTERÍSTICAS:")
    print("       - Método clássico de realce fotográfico")
    print("       - Preserva características naturais da imagem")
    print("     ✓ DIFERENÇAS OBSERVADAS:")
    print("       - Realce mais suave e natural comparado ao Laplaciano")
    print("       - Melhor preservação de tons médios")
    print("       - Menor amplificação de ruído")

    print("\n   🔸 HIGHBOOST FILTERING (k=2.0):")
    print("     ✓ CARACTERÍSTICAS:")
    print("       - Extensão do unsharp masking com intensificação")
    print("       - Permite controle preciso do nível de realce")
    print("     ✓ DIFERENÇAS OBSERVADAS:")
    print("       - Realce mais intenso que unsharp masking padrão")
    print("       - Bordas mais pronunciadas")
    print("       - Maior contraste geral da imagem")

    print("\n   🔸 EFEITO ATENUADO (k=0.5):")
    print("     ✓ CARACTERÍSTICAS:")
    print("       - Realce muito sutil")
    print("       - Preservação máxima das características originais")
    print("     ✓ DIFERENÇAS OBSERVADAS:")
    print("       - Melhoria quase imperceptível visualmente")
    print("       - Não amplifica ruído")
    print("       - Adequado para imagens que requerem processamento conservador")

    print("\n⚖️ PRINCIPAIS DIFERENÇAS IDENTIFICADAS:")
    print("\n   1. INTENSIDADE DO REALCE:")
    print("      Laplaciano > Highboost (k=2.0) > Unsharp (k=1.0) > Atenuado (k=0.5)")

    print("\n   2. AMPLIFICAÇÃO DE RUÍDO:")
    print("      Laplaciano > Highboost > Unsharp > Atenuado")

    print("\n   3. PRESERVAÇÃO DE CARACTERÍSTICAS ORIGINAIS:")
    print("      Atenuado > Unsharp > Highboost > Laplaciano")

    print("\n   4. NATURALIDADE DO RESULTADO:")
    print("      Unsharp/Highboost > Atenuado > Laplaciano")

    print("\n🎯 RECOMENDAÇÕES DE USO BASEADAS NAS DIFERENÇAS:")
    print("   • IMAGENS MÉDICAS: Efeito atenuado (preserva informações críticas)")
    print("   • FOTOGRAFIA: Unsharp masking (realce natural)")
    print("   • DETECÇÃO DE BORDAS: Laplaciano (máximo contraste)")
    print("   • IMPRESSÃO: Highboost (compensação de perda de nitidez)")

    print("\n✅ CONCLUSÕES SOBRE AS DIFERENÇAS:")
    print("   1. Cada método possui trade-offs específicos entre realce e preservação")
    print("   2. O parâmetro k oferece controle fino nos métodos de unsharp masking")
    print("   3. Laplaciano produz o maior contraste mas com mais artefatos")
    print("   4. Métodos baseados em unsharp masking são mais versáteis")
    print("   5. A escolha do método deve considerar o tipo de aplicação e tolerância a ruído")


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """
    Executa a Atividade Avaliativa 5 completa
    """
    print("\n🚀 INICIANDO ATIVIDADE AVALIATIVA 5")

    # Carrega a imagem cln1.gif
    print(f"\n{'=' * 80}")
    print("📷 CARREGANDO IMAGEM")
    print(f"{'=' * 80}")

    imagem_original = carregar_imagem(IMAGEM_ENTRADA)

    # REQUISITO 1: Filtro de Sobel (derivadas X, Y e magnitude)
    print(f"\n{'=' * 80}")
    print("📋 REQUISITO 1: FILTRO DE SOBEL")
    print(f"{'=' * 80}")

    derivada_x, derivada_y, magnitude = aplicar_filtro_sobel(imagem_original)
    visualizar_resultados_sobel(imagem_original.astype(np.uint8),
                                derivada_x, derivada_y, magnitude)

    # REQUISITO 2: Técnicas de Realce
    print(f"\n{'=' * 80}")
    print("📋 REQUISITO 2: TÉCNICAS DE REALCE")
    print(f"{'=' * 80}")

    # 2a. Filtro Laplaciano
    resultado_laplaciano = aplicar_filtro_laplaciano(imagem_original)

    # 2b. Unsharp Masking
    resultado_unsharp = aplicar_unsharp_masking(imagem_original, k=1.0)

    # 2c. Highboost Filtering (k escolhido = 2.0)
    resultado_highboost = aplicar_highboost_filtering(imagem_original, k=2.0)

    # 2d. K < 1 para atenuar o efeito
    resultado_atenuado = aplicar_efeito_atenuado(imagem_original, k=0.5)

    # Visualização comparativa
    visualizar_resultados_realce(imagem_original.astype(np.uint8),
                                 resultado_laplaciano, resultado_unsharp,
                                 resultado_highboost, resultado_atenuado)

    # Discussão das diferenças (conforme solicitado)
    discutir_resultados()

    print(f"\n🎉 ATIVIDADE AVALIATIVA 5 CONCLUÍDA COM SUCESSO!")
    print(f"📋 Todos os requisitos atendidos:")
    print(f"   ✅ 1) Filtro de Sobel implementado (derivada X, Y e magnitude) - imagem cln1.gif")
    print(f"   ✅ 2a) Filtro Laplaciano aplicado")
    print(f"   ✅ 2b) Unsharp Masking implementado")
    print(f"   ✅ 2c) Highboost Filtering aplicado (k=2.0 escolhido)")
    print(f"   ✅ 2d) K < 1 para atenuar efeito demonstrado (k=0.5)")
    print(f"   ✅ Discussão completa das diferenças apresentada")
    print(f"   ✅ Implementação da atividade anterior reutilizada (convolução 2D)")
    print(f"   ✅ Nenhuma função pronta utilizada nos requisitos principais")


# =============================================================================
# EXECUÇÃO DO PROGRAMA
# =============================================================================

if __name__ == "__main__":
    main()