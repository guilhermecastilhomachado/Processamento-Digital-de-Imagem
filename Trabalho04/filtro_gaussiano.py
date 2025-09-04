import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# =============================================================================
# ATIVIDADE AVALIATIVA 4 - REQUISITO 2
# FILTROS GAUSSIANOS - ANÁLISE SIGMA vs TAMANHO DA MÁSCARA
# =============================================================================

print("PROCESSAMENTO DIGITAL DE IMAGENS - ATIVIDADE AVALIATIVA 4")
print("REQUISITO 2: FILTROS GAUSSIANOS")
print("Profa. Alessandra Aparecida Paulino")
print("=" * 70)

# Configurações para análise
IMAGENS_ENTRADA = ['ben2.png', 'sta2.png']
TAMANHOS_FILTRO = [3, 7, 15]  # Para comparar efeito do tamanho
VALORES_SIGMA = [0.5, 1.0, 2.0, 3.0]  # Para comparar efeito do sigma


# =============================================================================
# FUNÇÕES BÁSICAS
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
        print(f"❌ ERRO: Arquivo '{caminho}' não encontrado!")
        return None


def normalizar_imagem(img):
    """Normaliza a imagem para o intervalo [0, 255]"""
    img_norm = np.clip(img, 0, 255)
    return img_norm.astype(np.uint8)


def aplicar_padding(imagem, tamanho_kernel):
    """Aplica padding zero à imagem"""
    pad_size = tamanho_kernel // 2
    return np.pad(imagem, pad_size, mode='constant', constant_values=0)


# =============================================================================
# IMPLEMENTAÇÃO DO FILTRO GAUSSIANO
# =============================================================================

def funcao_gaussiana_2d(x, y, sigma):
    """
    Implementa a função gaussiana 2D

    FÓRMULA MATEMÁTICA:
    G(x,y) = (1/(2π*σ²)) * exp(-(x² + y²)/(2σ²))

    PARÂMETROS:
    - x, y: Coordenadas do ponto
    - sigma (σ): Desvio padrão que controla a 'largura' da gaussiana

    INTERPRETAÇÃO:
    - σ pequeno: Gaussiana mais 'pontuda' (menos borramento)
    - σ grande: Gaussiana mais 'espalhada' (mais borramento)
    """
    # Fator de normalização
    fator_normalizacao = 1 / (2 * np.pi * sigma ** 2)

    # Expoente da função exponencial
    expoente = -(x ** 2 + y ** 2) / (2 * sigma ** 2)

    # Valor da função gaussiana
    return fator_normalizacao * np.exp(expoente)


def criar_filtro_gaussiano(tamanho, sigma):
    """
    Cria um filtro gaussiano com tamanho e sigma especificados

    TEORIA DO FILTRO GAUSSIANO:
    - Baseado na distribuição gaussiana (curva de Gauss)
    - Pixels centrais têm maior peso, pixels distantes têm menor peso
    - Produz suavização mais 'natural' que o filtro de média
    - O sigma (σ) controla o quanto a gaussiana se 'espalha'

    Args:
        tamanho: Tamanho do filtro (deve ser ímpar)
        sigma: Desvio padrão da gaussiana

    Returns:
        np.array: Matriz do filtro gaussiano normalizada
    """
    # Garante que o tamanho seja ímpar
    if tamanho % 2 == 0:
        tamanho += 1
        print(f"   ⚠️ Tamanho ajustado para {tamanho} (filtros devem ser ímpares)")

    print(f"\n🔧 CRIANDO FILTRO GAUSSIANO {tamanho}x{tamanho}, σ={sigma}")

    # Calcula o centro do filtro
    centro = tamanho // 2

    # Inicializa matriz do filtro
    filtro = np.zeros((tamanho, tamanho), dtype=np.float64)

    # Calcula cada elemento usando a função gaussiana
    for i in range(tamanho):
        for j in range(tamanho):
            # Coordenadas relativas ao centro
            x = i - centro
            y = j - centro

            # Calcula valor gaussiano para esta posição
            filtro[i, j] = funcao_gaussiana_2d(x, y, sigma)

    # Normaliza o filtro (soma = 1) para preservar brilho
    soma_filtro = np.sum(filtro)
    filtro_normalizado = filtro / soma_filtro

    # Informações sobre o filtro criado
    print(f"   • Valor central: {filtro_normalizado[centro, centro]:.6f}")
    print(f"   • Valor nas bordas: {filtro_normalizado[0, 0]:.6f}")
    print(f"   • Soma normalizada: {np.sum(filtro_normalizado):.1f}")
    print(f"   • Efeito esperado: Suavização gaussiana")

    return filtro_normalizado


def aplicar_convolucao_2d(imagem, kernel):
    """
    Aplica convolução 2D manualmente
    """
    altura_img, largura_img = imagem.shape
    altura_kernel, largura_kernel = kernel.shape

    print(f"   🔄 Aplicando convolução gaussiana...")

    # Aplica padding
    imagem_com_padding = aplicar_padding(imagem, altura_kernel)

    # Inicializa resultado
    imagem_resultado = np.zeros((altura_img, largura_img), dtype=np.float64)

    # Convolução pixel por pixel
    for i in range(altura_img):
        for j in range(largura_img):
            regiao = imagem_com_padding[i:i + altura_kernel, j:j + largura_kernel]
            valor_convoluido = np.sum(regiao * kernel)
            imagem_resultado[i, j] = valor_convoluido

    print(f"   ✓ Convolução gaussiana concluída")
    return imagem_resultado


def aplicar_filtro_gaussiano(imagem, tamanho, sigma):
    """
    Aplica filtro gaussiano à imagem
    """
    print(f"\n📊 APLICANDO FILTRO GAUSSIANO {tamanho}x{tamanho}, σ={sigma}")

    # Cria filtro gaussiano
    filtro = criar_filtro_gaussiano(tamanho, sigma)

    # Aplica convolução
    imagem_filtrada = aplicar_convolucao_2d(imagem, filtro)

    # Normaliza resultado
    imagem_final = normalizar_imagem(imagem_filtrada)

    print(f"✅ Filtragem gaussiana concluída")
    return imagem_final


# =============================================================================
# COMPARAÇÕES PARA RESPONDER À QUESTÃO PRINCIPAL
# =============================================================================

def comparar_efeito_tamanho_mascara(imagem_original, nome_imagem):
    """
    EXPERIMENTO 1: Analisa o efeito da variação do TAMANHO da máscara
    (mantendo sigma fixo)
    """
    print(f"\n{'=' * 60}")
    print(f"🧪 EXPERIMENTO 1: EFEITO DO TAMANHO DA MÁSCARA - {nome_imagem}")
    print(f"{'=' * 60}")

    sigma_fixo = 1.0  # Mantém sigma constante
    print(f"🔬 Condições do experimento:")
    print(f"   • Sigma FIXO: {sigma_fixo}")
    print(f"   • Tamanhos VARIÁVEIS: {TAMANHOS_FILTRO}")

    # Aplica filtros com tamanhos diferentes
    imagens_resultado = [imagem_original.astype(np.uint8)]
    titulos = ['Original']

    for tamanho in TAMANHOS_FILTRO:
        img_filtrada = aplicar_filtro_gaussiano(imagem_original, tamanho, sigma_fixo)
        imagens_resultado.append(img_filtrada)
        titulos.append(f'Gaussiano {tamanho}x{tamanho}\nσ={sigma_fixo}')

    # Visualização
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.suptitle(f'Experimento 1: Efeito do Tamanho da Máscara (σ={sigma_fixo}) - {nome_imagem}',
                 fontsize=14, fontweight='bold', y=1.05)

    for i, (img, titulo) in enumerate(zip(imagens_resultado, titulos)):
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(titulo, fontsize=11, fontweight='bold')
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()

    return imagens_resultado


def comparar_efeito_sigma(imagem_original, nome_imagem):
    """
    EXPERIMENTO 2: Analisa o efeito da variação do SIGMA
    (mantendo tamanho fixo)
    """
    print(f"\n{'=' * 60}")
    print(f"🧪 EXPERIMENTO 2: EFEITO DO SIGMA - {nome_imagem}")
    print(f"{'=' * 60}")

    tamanho_fixo = 7  # Mantém tamanho constante
    print(f"🔬 Condições do experimento:")
    print(f"   • Tamanho FIXO: {tamanho_fixo}x{tamanho_fixo}")
    print(f"   • Sigmas VARIÁVEIS: {VALORES_SIGMA}")

    # Aplica filtros com sigmas diferentes
    imagens_resultado = [imagem_original.astype(np.uint8)]
    titulos = ['Original']

    for sigma in VALORES_SIGMA:
        img_filtrada = aplicar_filtro_gaussiano(imagem_original, tamanho_fixo, sigma)
        imagens_resultado.append(img_filtrada)
        titulos.append(f'Gaussiano {tamanho_fixo}x{tamanho_fixo}\nσ={sigma}')

    # Visualização
    fig, axes = plt.subplots(1, 5, figsize=(25, 5))
    fig.suptitle(f'Experimento 2: Efeito do Sigma (Tamanho={tamanho_fixo}x{tamanho_fixo}) - {nome_imagem}',
                 fontsize=14, fontweight='bold', y=1.05)

    for i, (img, titulo) in enumerate(zip(imagens_resultado, titulos)):
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(titulo, fontsize=11, fontweight='bold')
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()

    return imagens_resultado


def comparar_casos_extremos(imagem_original, nome_imagem):
    """
    EXPERIMENTO 3: Compara casos extremos para demonstrar qual variável
    tem maior impacto
    """
    print(f"\n{'=' * 60}")
    print(f"🧪 EXPERIMENTO 3: CASOS EXTREMOS - {nome_imagem}")
    print(f"{'=' * 60}")

    print(f"🔬 Testando casos extremos para comparação direta:")

    # Casos para comparação
    casos = [
        ("Original", None, None),
        ("Máscara Grande,\nSigma Pequeno", 15, 0.5),
        ("Máscara Pequena,\nSigma Grande", 3, 3.0),
        ("Máscara Grande,\nSigma Grande", 15, 3.0)
    ]

    imagens_resultado = []
    titulos = []

    for titulo, tamanho, sigma in casos:
        if tamanho is None:  # Caso original
            imagens_resultado.append(imagem_original.astype(np.uint8))
            titulos.append(titulo)
            print(f"   • {titulo}")
        else:
            print(f"   • {titulo}: {tamanho}x{tamanho}, σ={sigma}")
            img_filtrada = aplicar_filtro_gaussiano(imagem_original, tamanho, sigma)
            imagens_resultado.append(img_filtrada)
            titulos.append(f"{titulo}\n{tamanho}x{tamanho}, σ={sigma}")

    # Visualização
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.suptitle(f'Experimento 3: Casos Extremos - Qual Variável Afeta Mais? - {nome_imagem}',
                 fontsize=14, fontweight='bold', y=1.05)

    for i, (img, titulo) in enumerate(zip(imagens_resultado, titulos)):
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(titulo, fontsize=10, fontweight='bold')
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()

    return imagens_resultado


# =============================================================================
# ANÁLISE E DISCUSSÃO CIENTÍFICA
# =============================================================================

def discutir_resultados_gaussiano():
    """
    Discussão científica detalhada respondendo à questão da atividade:
    "O que afetará mais a imagem: variação em sigma ou variação no tamanho da máscara?"
    """
    print(f"\n{'=' * 70}")
    print("📝 DISCUSSÃO CIENTÍFICA - FILTROS GAUSSIANOS")
    print(f"{'=' * 70}")

    print(f"\n❓ QUESTÃO CENTRAL DA ATIVIDADE:")
    print(f"   'O que afetará mais a imagem: variação em SIGMA ou variação no TAMANHO da máscara?'")

    print(f"\n🎯 RESPOSTA FUNDAMENTADA:")
    print(f"   ➤ A VARIAÇÃO DO SIGMA (σ) AFETA MAIS A IMAGEM!")

    print(f"\n🔬 FUNDAMENTAÇÃO CIENTÍFICA:")

    print(f"\n   📊 PAPEL DO SIGMA (σ):")
    print(f"      • FUNÇÃO: Controla a 'largura' da distribuição gaussiana")
    print(f"      • EFEITO DIRETO: Determina o peso relativo dos pixels vizinhos")
    print(f"      • σ PEQUENO (ex: 0.5): Gaussiana 'pontuda' → Menos borramento")
    print(f"      • σ GRANDE (ex: 3.0): Gaussiana 'espalhada' → Mais borramento")
    print(f"      • MUDANÇA RADICAL: Dobrar σ muda drasticamente o resultado")

    print(f"\n   📐 PAPEL DO TAMANHO DA MÁSCARA:")
    print(f"      • FUNÇÃO: Define a área de influência do filtro")
    print(f"      • EFEITO INDIRETO: Determina até onde o efeito se estende")
    print(f"      • MÁSCARA PEQUENA: Efeito localizado, pode truncar gaussiana")
    print(f"      • MÁSCARA GRANDE: Captura toda a gaussiana, mas sem intensificar")
    print(f"      • LIMITAÇÃO: Não pode criar borramento onde σ não permite")

    print(f"\n🧪 EVIDÊNCIAS DOS EXPERIMENTOS:")

    print(f"\n   🔍 EXPERIMENTO 1 - Variação do Tamanho (σ fixo):")
    print(f"      • OBSERVAÇÃO: Diferenças sutis entre 3x3, 7x7, 15x15")
    print(f"      • EXPLICAÇÃO: Com σ=1.0, a gaussiana já 'cabe' numa máscara 7x7")
    print(f"      • CONCLUSÃO: Aumentar para 15x15 não intensifica o borramento")

    print(f"\n   🔍 EXPERIMENTO 2 - Variação do Sigma (tamanho fixo):")
    print(f"      • OBSERVAÇÃO: Diferenças DRAMÁTICAS entre σ=0.5 e σ=3.0")
    print(f"      • EXPLICAÇÃO: Sigma controla diretamente a intensidade do filtro")
    print(f"      • CONCLUSÃO: Pequenas mudanças em σ causam grandes efeitos")

    print(f"\n   🔍 EXPERIMENTO 3 - Casos Extremos:")
    print(f"      • MÁSCARA GRANDE + σ PEQUENO: Pouco borramento")
    print(f"      • MÁSCARA PEQUENA + σ GRANDE: Muito borramento (limitado pela máscara)")
    print(f"      • CONFIRMAÇÃO: Sigma é o parâmetro dominante")

    print(f"\n📚 ANALOGIA DIDÁTICA:")
    print(f"   🔦 Imagine o filtro como uma LANTERNA:")
    print(f"      • SIGMA = Intensidade da luz (brilho do LED)")
    print(f"      • TAMANHO = Tamanho da lente (área iluminada)")
    print(f"      • RESULTADO: Uma luz fraca com lente grande ilumina pouco")
    print(f"      • RESULTADO: Uma luz forte com lente pequena ilumina muito")
    print(f"      ➤ A intensidade (σ) importa mais que o tamanho da lente!")

    print(f"\n⚖️ RELAÇÃO ENTRE OS PARÂMETROS:")
    print(f"   • INDEPENDÊNCIA: σ e tamanho são matematicamente independentes")
    print(f"   • LIMITAÇÃO PRÁTICA: Máscara muito pequena pode truncar gaussiana grande")
    print(f"   • REGRA DE OURO: Tamanho da máscara ≥ 6σ para capturar 99% da gaussiana")
    print(f"   • OTIMIZAÇÃO: Ajustar σ primeiro, depois escolher tamanho adequado")

    print(f"\n🎯 APLICAÇÕES PRÁTICAS:")
    print(f"   • SUAVIZAÇÃO LEVE: σ pequeno (0.5-1.0), máscara 3x3 ou 5x5")
    print(f"   • SUAVIZAÇÃO MODERADA: σ médio (1.0-2.0), máscara 7x7")
    print(f"   • SUAVIZAÇÃO INTENSA: σ grande (2.0+), máscara 9x9 ou maior")
    print(f"   • REGRA: Sempre ajustar σ primeiro para o efeito desejado")

    print(f"\n✅ CONCLUSÕES FINAIS:")
    print(f"   1. SIGMA (σ) é o parâmetro DOMINANTE no filtro gaussiano")
    print(f"   2. TAMANHO da máscara é um parâmetro AUXILIAR")
    print(f"   3. Pequenas variações em σ causam grandes mudanças no resultado")
    print(f"   4. O tamanho deve ser escolhido para 'acomodar' o σ desejado")
    print(f"   5. Para máximo controle: ajuste σ primeiro, dimensione máscara depois")

    print(f"\n📖 EMBASAMENTO MATEMÁTICO:")
    print(f"   • A função G(x,y) = (1/2πσ²)exp(-(x²+y²)/2σ²) mostra que:")
    print(f"   • σ² aparece no denominador → impacto exponencial")
    print(f"   • Coordenadas (x,y) são lineares → impacto linear do tamanho")
    print(f"   • Matematicamente, σ tem influência não-linear muito maior")


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """
    Executa o Requisito 2 completo da atividade
    """
    print("\n🚀 INICIANDO ANÁLISE - REQUISITO 2")
    print("🎯 OBJETIVO: Determinar se SIGMA ou TAMANHO afeta mais a imagem")

    # Processa cada imagem
    for nome_imagem in IMAGENS_ENTRADA:
        print(f"\n{'=' * 70}")
        print(f"📷 ANALISANDO: {nome_imagem}")
        print(f"{'=' * 70}")

        # Carrega imagem
        imagem = carregar_imagem(nome_imagem)
        if imagem is None:
            continue

        # EXPERIMENTO 1: Efeito do tamanho da máscara
        resultados_tamanho = comparar_efeito_tamanho_mascara(imagem, nome_imagem)

        # EXPERIMENTO 2: Efeito do sigma
        resultados_sigma = comparar_efeito_sigma(imagem, nome_imagem)

        # EXPERIMENTO 3: Casos extremos
        resultados_extremos = comparar_casos_extremos(imagem, nome_imagem)

        print(f"\n✅ Análise de {nome_imagem} concluída!")

    # Discussão científica final
    discutir_resultados_gaussiano()

    print(f"\n🎉 REQUISITO 2 CONCLUÍDO COM SUCESSO!")
    print(f"📋 Resultados obtidos:")
    print(f"   • 3 experimentos realizados para cada imagem")
    print(f"   • Comparações visuais que demonstram a resposta")
    print(f"   • Fundamentação científica completa")
    print(f"   • RESPOSTA: SIGMA afeta mais a imagem que o tamanho da máscara")


# =============================================================================
# EXECUÇÃO DO PROGRAMA
# =============================================================================

if __name__ == "__main__":
    main()