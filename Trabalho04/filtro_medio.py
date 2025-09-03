import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# =============================================================================
# ATIVIDADE AVALIATIVA 4 - REQUISITO 1
# FILTROS DE MÉDIA COM TAMANHOS 3x3, 7x7 E 15x15
# =============================================================================

print("PROCESSAMENTO DIGITAL DE IMAGENS - ATIVIDADE AVALIATIVA 4")
print("REQUISITO 1: FILTROS DE MÉDIA")
print("Profa. Alessandra Aparecida Paulino")
print("=" * 70)

# Configurações
IMAGENS_ENTRADA = ['ben2.png', 'sta2.png']
TAMANHOS_FILTRO = [3, 7, 15]  # Tamanhos solicitados na atividade


# =============================================================================
# FUNÇÕES BÁSICAS
# =============================================================================

def carregar_imagem(caminho):
    """
    Carrega uma imagem e converte para escala de cinza

    Args:
        caminho: Caminho para o arquivo de imagem

    Returns:
        np.array: Array numpy da imagem em escala de cinza
    """
    try:
        img = Image.open(caminho).convert('L')
        array_img = np.array(img, dtype=np.float64)  # Usa float64 para evitar overflow
        print(f"✓ Imagem '{caminho}' carregada: {array_img.shape[0]}x{array_img.shape[1]} pixels")
        return array_img
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo '{caminho}' não encontrado!")
        return None


def normalizar_imagem(img):
    """
    Normaliza a imagem para o intervalo [0, 255] e converte para uint8
    """
    img_norm = np.clip(img, 0, 255)
    return img_norm.astype(np.uint8)


def aplicar_padding(imagem, tamanho_kernel):
    """
    Aplica padding zero à imagem para manter o tamanho original após convolução

    EXPLICAÇÃO: O padding adiciona bordas de zeros na imagem para que,
    após a convolução, a imagem resultante tenha o mesmo tamanho da original.

    Args:
        imagem: Array numpy da imagem
        tamanho_kernel: Tamanho do kernel (assumindo kernel quadrado)

    Returns:
        np.array: Imagem com padding aplicado
    """
    pad_size = tamanho_kernel // 2  # Metade do tamanho do kernel
    return np.pad(imagem, pad_size, mode='constant', constant_values=0)


# =============================================================================
# IMPLEMENTAÇÃO DO FILTRO DE MÉDIA
# =============================================================================

def criar_filtro_media(tamanho):
    """
    Cria um filtro de média (passa-baixa) do tamanho especificado

    TEORIA DO FILTRO DE MÉDIA:
    - É um filtro passa-baixa que realiza suavização
    - Todos os coeficientes são iguais
    - A soma de todos os coeficientes deve ser 1 para preservar o brilho
    - Quanto maior o filtro, maior o efeito de borramento

    Args:
        tamanho: Tamanho do filtro (ex: 3 para filtro 3x3)

    Returns:
        np.array: Matriz do filtro de média normalizada
    """
    print(f"\n🔧 CRIANDO FILTRO DE MÉDIA {tamanho}x{tamanho}")

    # Cria matriz com todos os valores iguais a 1
    filtro = np.ones((tamanho, tamanho), dtype=np.float64)

    # Normaliza dividindo pelo número total de elementos
    # Isso garante que a soma seja 1, preservando o brilho médio
    num_elementos = tamanho * tamanho
    filtro = filtro / num_elementos

    # Informações do filtro criado
    print(f"   • Cada coeficiente: {1 / num_elementos:.6f}")
    print(f"   • Soma total: {np.sum(filtro):.1f}")
    print(f"   • Efeito esperado: Suavização com borramento")
    print(filtro) # Mostra o filtro criado diretamente

    return filtro


def aplicar_convolucao_2d(imagem, kernel):
    """
    Aplica convolução 2D manualmente (implementação do zero)

    PROCESSO DE CONVOLUÇÃO:
    1. Posiciona o kernel sobre cada pixel da imagem
    2. Multiplica cada coeficiente do kernel pelo pixel correspondente
    3. Soma todos os produtos para obter o novo valor do pixel
    4. Move o kernel para a próxima posição

    Args:
        imagem: Array numpy da imagem original
        kernel: Array numpy do kernel/filtro

    Returns:
        np.array: Imagem após convolução
    """
    altura_img, largura_img = imagem.shape
    altura_kernel, largura_kernel = kernel.shape

    print(f"   🔄 Aplicando convolução...")
    print(f"      Imagem: {altura_img}x{largura_img}")
    print(f"      Kernel: {altura_kernel}x{largura_kernel}")

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

    print(f"   ✓ Convolução concluída")
    return imagem_resultado


def aplicar_filtro_media(imagem, tamanho):
    """
    Aplica filtro de média à imagem completa

    Args:
        imagem: Array numpy da imagem original
        tamanho: Tamanho do filtro

    Returns:
        np.array: Imagem suavizada
    """
    print(f"\n📊 APLICANDO FILTRO DE MÉDIA {tamanho}x{tamanho}")

    # Cria o filtro de média
    filtro = criar_filtro_media(tamanho)

    # Aplica convolução
    imagem_filtrada = aplicar_convolucao_2d(imagem, filtro)

    # Normaliza para o intervalo [0, 255]
    imagem_final = normalizar_imagem(imagem_filtrada)

    print(f"✅ Filtragem {tamanho}x{tamanho} concluída com sucesso")

    return imagem_final


# =============================================================================
# VISUALIZAÇÃO E COMPARAÇÃO DOS RESULTADOS
# =============================================================================

def comparar_filtros_media(imagem_original, nome_imagem):
    """
    Aplica todos os filtros de média e mostra comparação lado a lado

    Args:
        imagem_original: Array numpy da imagem original
        nome_imagem: Nome da imagem para títulos

    Returns:
        list: Lista com todas as imagens (original + filtradas)
    """
    print(f"\n{'=' * 50}")
    print(f"🔍 COMPARAÇÃO DE FILTROS - {nome_imagem}")
    print(f"{'=' * 50}")

    # Lista para armazenar resultados
    todas_imagens = [imagem_original.astype(np.uint8)]  # Inclui original
    titulos = ['Original']

    # Aplica cada filtro
    for tamanho in TAMANHOS_FILTRO:
        img_filtrada = aplicar_filtro_media(imagem_original, tamanho)
        todas_imagens.append(img_filtrada)
        titulos.append(f'Média {tamanho}x{tamanho}')

    # Cria visualização comparativa
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.suptitle(f'Comparação Filtros de Média - {nome_imagem}',
                 fontsize=16, fontweight='bold', y=1.02)

    for i, (img, titulo) in enumerate(zip(todas_imagens, titulos)):
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(titulo, fontsize=12, fontweight='bold')
        axes[i].axis('off')

        # Adiciona informação de borramento
        if i > 0:  # Não adiciona para a original
            nivel_borramento = ['Leve', 'Moderado', 'Intenso'][i - 1]
            axes[i].text(0.5, -0.1, f'Borramento: {nivel_borramento}',
                         ha='center', va='top', transform=axes[i].transAxes,
                         fontsize=10, style='italic')

    plt.tight_layout()
    plt.show()

    return todas_imagens


# =============================================================================
# ANÁLISE E DISCUSSÃO DOS RESULTADOS
# =============================================================================

def discutir_resultados_filtros_media():
    """
    Gera discussão detalhada sobre os resultados dos filtros de média
    """
    print(f"\n{'=' * 70}")
    print("📝 DISCUSSÃO DOS RESULTADOS - FILTROS DE MÉDIA")
    print(f"{'=' * 70}")

    print("\n🔍 ANÁLISE COMPARATIVA DOS TAMANHOS:")

    print("\n   📐 FILTRO 3x3:")
    print("      • EFEITO: Suavização leve")
    print("      • CARACTERÍSTICAS: Preserva a maioria dos detalhes")
    print("      • USO: Redução de ruído sutil, pré-processamento")
    print("      • VANTAGEM: Mantém bordas relativamente nítidas")

    print("\n   📐 FILTRO 7x7:")
    print("      • EFEITO: Suavização moderada")
    print("      • CARACTERÍSTICAS: Equilibrio entre suavização e preservação")
    print("      • USO: Redução de ruído moderada, preparação para segmentação")
    print("      • VANTAGEM: Bom compromisso entre eficiência e qualidade")

    print("\n   📐 FILTRO 15x15:")
    print("      • EFEITO: Suavização intensa")
    print("      • CARACTERÍSTICAS: Forte borramento, perda significativa de detalhes")
    print("      • USO: Remoção de texturas, criação de fundos homogêneos")
    print("      • DESVANTAGEM: Pode eliminar informações importantes")

    print("\n⚖️ RELAÇÃO TAMANHO vs EFEITO:")
    print("   • REGRA GERAL: Quanto maior o filtro, maior o borramento")
    print("   • CAUSA: Mais pixels contribuem para o cálculo da média")
    print("   • CONSEQUÊNCIA: Detalhes finos são 'diluídos' em áreas maiores")
    print("   • TRADE-OFF: Redução de ruído vs Perda de detalhes")

    print("\n💡 APLICAÇÕES PRÁTICAS:")
    print("   • IMAGENS COM MUITO RUÍDO: Filtros maiores (7x7, 15x15)")
    print("   • IMAGENS DETALHADAS: Filtros menores (3x3)")
    print("   • PRÉ-PROCESSAMENTO: Geralmente 3x3 ou 5x5")
    print("   • EFEITOS ARTÍSTICOS: Filtros grandes (15x15+)")

    print("\n🎯 CONCLUSÕES:")
    print("   1. Filtros de média são eficazes para suavização")
    print("   2. O tamanho do filtro controla diretamente o nível de borramento")
    print("   3. Existe um trade-off entre remoção de ruído e preservação de detalhes")
    print("   4. A escolha do tamanho deve considerar o objetivo da aplicação")


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """
    Executa o Requisito 1 completo da atividade
    """
    print("\n🚀 INICIANDO PROCESSAMENTO - REQUISITO 1")

    # Processa cada imagem solicitada
    for nome_imagem in IMAGENS_ENTRADA:
        print(f"\n{'=' * 70}")
        print(f"📷 PROCESSANDO: {nome_imagem}")
        print(f"{'=' * 70}")

        # Carrega a imagem
        imagem = carregar_imagem(nome_imagem)
        if imagem is None:
            continue

        # Aplica filtros e gera comparação
        resultados = comparar_filtros_media(imagem, nome_imagem)

        print(f"\n✅ Processamento de {nome_imagem} concluído!")
        print(f"   • {len(resultados)} imagens geradas (original + 3 filtros)")

    # Discussão teórica dos resultados
    discutir_resultados_filtros_media()

    print(f"\n🎉 REQUISITO 1 CONCLUÍDO COM SUCESSO!")
    print(f"📋 Resultados obtidos:")
    print(f"   • Filtros 3x3, 7x7 e 15x15 implementados e aplicados")
    print(f"   • Comparações visuais geradas para ambas as imagens")
    print(f"   • Discussão detalhada dos resultados apresentada")


# =============================================================================
# EXECUÇÃO DO PROGRAMA
# =============================================================================

if __name__ == "__main__":
    main()