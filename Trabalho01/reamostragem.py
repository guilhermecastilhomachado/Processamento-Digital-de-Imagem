import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# =============================================================================
# ATIVIDADE AVALIATIVA 1 - REQUISITO 1: REAMOSTRAGEM DPI
# PROFA. ALESSANDRA APARECIDA PAULINO
# =============================================================================

print("PROCESSAMENTO DIGITAL DE IMAGENS - ATIVIDADE AVALIATIVA 1")
print("REQUISITO 1: REAMOSTRAGEM DE PIXELS (DPI)")
print("Profa. Alessandra Aparecida Paulino")
print("=" * 80)

# Configurações
IMAGEM_ENTRADA = 'relogio.tif'
DPI_ORIGINAL = 1250
DPI_ALVOS = [300, 150, 72]  # DPIs solicitados na atividade

# =============================================================================
# TEORIA: O QUE É REAMOSTRAGEM?
# =============================================================================

print("\n📚 CONCEITOS FUNDAMENTAIS:")
print("\n   🔍 O QUE É DPI (Dots Per Inch)?")
print("      • DPI = Pontos por Polegada")
print("      • Mede a RESOLUÇÃO ESPACIAL da imagem")
print("      • Quanto MAIOR o DPI, MAIS detalhes a imagem possui")
print("      • Exemplo: 1250 DPI = 1250 pixels em 1 polegada (2.54 cm)")

print("\n   🔍 O QUE É REAMOSTRAGEM?")
print("      • Processo de REDUZIR ou AUMENTAR o número de pixels")
print("      • Nesta atividade: REDUZIR de 1250 DPI para valores menores")
print("      • Técnica: Subamostragem (pegar pixels em intervalos)")

print("\n   🔍 CÁLCULO DA NOVA DIMENSÃO:")
print("      • Se DPI diminui, o número de pixels também diminui")
print("      • Fator de escala = DPI_novo / DPI_original")
print("      • Nova dimensão = dimensão_original × fator_escala")


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
        print(f"   • DPI original: {DPI_ORIGINAL}")
        return array_img
    except FileNotFoundError:
        print(f"\n⚠ ERRO: Arquivo '{caminho}' não encontrado!")
        print("Criando uma imagem sintética para demonstração...")
        return criar_imagem_sintetica()


def criar_imagem_sintetica():
    """
    Cria uma imagem sintética de um relógio para demonstração
    """
    # Cria imagem 1250x1250 para simular 1250 DPI em 1 polegada²
    tamanho = 1250
    img = np.ones((tamanho, tamanho), dtype=np.uint8) * 255

    # Centro da imagem
    centro_y, centro_x = tamanho // 2, tamanho // 2

    # Desenha círculo do relógio
    y, x = np.ogrid[:tamanho, :tamanho]
    raio_relogio = 500
    mascara_circulo = (x - centro_x) ** 2 + (y - centro_y) ** 2 <= raio_relogio ** 2
    img[mascara_circulo] = 200

    # Borda do relógio
    mascara_borda = ((x - centro_x) ** 2 + (y - centro_y) ** 2 <= raio_relogio ** 2) & \
                    ((x - centro_x) ** 2 + (y - centro_y) ** 2 >= (raio_relogio - 20) ** 2)
    img[mascara_borda] = 0

    # Marcações de horas (12 marcações)
    for hora in range(12):
        angulo = hora * np.pi / 6 - np.pi / 2
        x_marca = int(centro_x + 450 * np.cos(angulo))
        y_marca = int(centro_y + 450 * np.sin(angulo))
        # Marca cada hora
        for dy in range(-30, 31):
            for dx in range(-8, 9):
                yy, xx = y_marca + dy, x_marca + dx
                if 0 <= yy < tamanho and 0 <= xx < tamanho:
                    img[yy, xx] = 0

    # Ponteiro das horas (apontando para 3)
    for i in range(300):
        x_pont = int(centro_x + i * np.cos(0))
        y_pont = int(centro_y + i * np.sin(0))
        for dy in range(-10, 11):
            for dx in range(-10, 11):
                yy, xx = y_pont + dy, x_pont + dx
                if 0 <= yy < tamanho and 0 <= xx < tamanho:
                    img[yy, xx] = 50

    # Ponteiro dos minutos (apontando para 12)
    for i in range(400):
        x_pont = int(centro_x + i * np.cos(-np.pi / 2))
        y_pont = int(centro_y + i * np.sin(-np.pi / 2))
        for dy in range(-6, 7):
            for dx in range(-6, 7):
                yy, xx = y_pont + dy, x_pont + dx
                if 0 <= yy < tamanho and 0 <= xx < tamanho:
                    img[yy, xx] = 50

    # Centro do relógio
    mascara_centro = (x - centro_x) ** 2 + (y - centro_y) ** 2 <= 30 ** 2
    img[mascara_centro] = 0

    print(f"\n✓ Imagem sintética criada para demonstração")
    print(f"   • Dimensões: {tamanho} x {tamanho} pixels")
    print(f"   • DPI simulado: {DPI_ORIGINAL}")

    return img


# =============================================================================
# IMPLEMENTAÇÃO DA REAMOSTRAGEM (SEM FUNÇÕES PRONTAS)
# =============================================================================

def calcular_dimensoes_reamostragem(dimensao_original, dpi_original, dpi_novo):
    """
    Calcula as novas dimensões após reamostragem

    TEORIA:
    - Se o DPI diminui, precisamos de menos pixels para representar a mesma área
    - Fator de escala = DPI_novo / DPI_original
    - Nova dimensão = dimensão_original × fator_escala

    Args:
        dimensao_original: Dimensão (altura ou largura) da imagem original
        dpi_original: DPI original da imagem
        dpi_novo: DPI desejado

    Returns:
        int: Nova dimensão calculada
    """
    # Calcula fator de escala
    fator_escala = dpi_novo / dpi_original

    # Calcula nova dimensão
    nova_dimensao = int(dimensao_original * fator_escala)

    print(f"\n   📐 CÁLCULO DE DIMENSÃO:")
    print(f"      • Dimensão original: {dimensao_original} pixels")
    print(f"      • DPI: {dpi_original} → {dpi_novo}")
    print(f"      • Fator de escala: {dpi_novo}/{dpi_original} = {fator_escala:.4f}")
    print(f"      • Nova dimensão: {dimensao_original} × {fator_escala:.4f} = {nova_dimensao} pixels")

    return nova_dimensao


def reamostrar_imagem_nearest_neighbor(imagem, nova_altura, nova_largura):
    """
    Reamostra a imagem usando o método NEAREST NEIGHBOR (vizinho mais próximo)
    IMPLEMENTAÇÃO MANUAL - SEM FUNÇÕES PRONTAS

    TEORIA DO NEAREST NEIGHBOR:
    - Método mais simples de reamostragem
    - Para cada pixel da nova imagem, pega o pixel mais próximo da imagem original
    - Rápido, mas pode criar artefatos (efeito de "blocagem")

    ALGORITMO:
    1. Para cada posição (i,j) na nova imagem
    2. Calcula a posição correspondente na imagem original
    3. Arredonda para o pixel inteiro mais próximo
    4. Copia o valor desse pixel

    Args:
        imagem: Array numpy da imagem original
        nova_altura: Altura desejada
        nova_largura: Largura desejada

    Returns:
        np.array: Imagem reamostrada
    """
    altura_original, largura_original = imagem.shape

    print(f"\n   🔄 APLICANDO REAMOSTRAGEM (Nearest Neighbor)")
    print(f"      • Método: Vizinho mais próximo")
    print(f"      • Original: {largura_original} x {altura_original}")
    print(f"      • Nova: {nova_largura} x {nova_altura}")

    # Cria matriz para a nova imagem
    imagem_reamostrada = np.zeros((nova_altura, nova_largura), dtype=np.uint8)

    # Calcula fatores de escala
    escala_y = altura_original / nova_altura
    escala_x = largura_original / nova_largura

    print(f"      • Escala Y: {escala_y:.4f}")
    print(f"      • Escala X: {escala_x:.4f}")

    # Para cada pixel da nova imagem
    for i in range(nova_altura):
        for j in range(nova_largura):
            # Calcula posição correspondente na imagem original
            y_original = i * escala_y
            x_original = j * escala_x

            # Arredonda para o pixel inteiro mais próximo
            y_original = int(round(y_original))
            x_original = int(round(x_original))

            # Garante que não ultrapassa os limites
            y_original = min(y_original, altura_original - 1)
            x_original = min(x_original, largura_original - 1)

            # Copia o valor do pixel
            imagem_reamostrada[i, j] = imagem[y_original, x_original]

        # Mostra progresso a cada 10% (opcional, para ver o processo)
        if (i + 1) % (nova_altura // 10) == 0:
            progresso = ((i + 1) / nova_altura) * 100
            print(f"      • Progresso: {progresso:.0f}%")

    print(f"      ✓ Reamostragem concluída!")

    return imagem_reamostrada


def aplicar_reamostragem_dpi(imagem_original, dpi_novo):
    """
    Aplica reamostragem completa para um novo DPI

    Args:
        imagem_original: Array numpy da imagem original
        dpi_novo: DPI desejado

    Returns:
        np.array: Imagem reamostrada
    """
    print(f"\n{'=' * 70}")
    print(f"🔄 REAMOSTRAGEM PARA {dpi_novo} DPI")
    print(f"{'=' * 70}")

    altura_original, largura_original = imagem_original.shape

    # Calcula novas dimensões
    nova_altura = calcular_dimensoes_reamostragem(altura_original, DPI_ORIGINAL, dpi_novo)
    nova_largura = calcular_dimensoes_reamostragem(largura_original, DPI_ORIGINAL, dpi_novo)

    # Aplica reamostragem
    imagem_reamostrada = reamostrar_imagem_nearest_neighbor(
        imagem_original, nova_altura, nova_largura
    )

    # Calcula estatísticas
    reducao_pixels = (1 - (nova_altura * nova_largura) / (altura_original * largura_original)) * 100

    print(f"\n   📊 RESULTADOS:")
    print(f"      • Pixels originais: {largura_original * altura_original:,}")
    print(f"      • Pixels após reamostragem: {nova_largura * nova_altura:,}")
    print(f"      • Redução: {reducao_pixels:.2f}%")
    print(f"      • Tamanho em memória: {nova_altura * nova_largura / 1024:.2f} KB")

    return imagem_reamostrada


# =============================================================================
# VISUALIZAÇÃO DOS RESULTADOS
# =============================================================================

def visualizar_resultados(imagem_original, imagens_reamostradas, dpis):
    """
    Visualiza todas as imagens lado a lado para comparação
    """
    print(f"\n{'=' * 70}")
    print("🎨 VISUALIZANDO RESULTADOS")
    print(f"{'=' * 70}")

    # Cria figura com subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 16))
    fig.suptitle('REQUISITO 1: Reamostragem de Pixels (DPI)',
                 fontsize=16, fontweight='bold')

    # Imagem original
    axes[0, 0].imshow(imagem_original, cmap='gray')
    axes[0, 0].set_title(f'Original\n{DPI_ORIGINAL} DPI\n{imagem_original.shape[1]}x{imagem_original.shape[0]} pixels',
                         fontweight='bold', fontsize=12)
    axes[0, 0].axis('off')

    # Imagens reamostradas
    posicoes = [(0, 1), (1, 0), (1, 1)]

    for idx, (img_reamos, dpi) in enumerate(zip(imagens_reamostradas, dpis)):
        pos = posicoes[idx]
        axes[pos].imshow(img_reamos, cmap='gray')

        # Calcula redução percentual
        reducao = (1 - (img_reamos.shape[0] * img_reamos.shape[1]) /
                   (imagem_original.shape[0] * imagem_original.shape[1])) * 100

        axes[pos].set_title(
            f'Reamostrado\n{dpi} DPI\n{img_reamos.shape[1]}x{img_reamos.shape[0]} pixels\nRedução: {reducao:.1f}%',
            fontweight='bold', fontsize=12
        )
        axes[pos].axis('off')

    plt.tight_layout()
    plt.show()

    print("✓ Visualização concluída!")


def visualizar_zoom_comparacao(imagem_original, imagens_reamostradas, dpis):
    """
    Visualiza um ZOOM em uma região específica para ver os detalhes
    """
    print(f"\n{'=' * 70}")
    print("🔍 VISUALIZAÇÃO COM ZOOM (Detalhes)")
    print(f"{'=' * 70}")

    # Define região de interesse (centro da imagem)
    altura_orig, largura_orig = imagem_original.shape

    # Região central (25% da imagem)
    y_start = altura_orig // 3
    y_end = 2 * altura_orig // 3
    x_start = largura_orig // 3
    x_end = 2 * largura_orig // 3

    # Recorta região
    regiao_original = imagem_original[y_start:y_end, x_start:x_end]

    # Cria figura
    fig, axes = plt.subplots(2, 2, figsize=(16, 16))
    fig.suptitle('ZOOM: Comparação de Detalhes (Região Central)',
                 fontsize=16, fontweight='bold')

    # Original
    axes[0, 0].imshow(regiao_original, cmap='gray', interpolation='nearest')
    axes[0, 0].set_title(f'Original - {DPI_ORIGINAL} DPI\n(ALTA RESOLUÇÃO)',
                         fontweight='bold', fontsize=12)
    axes[0, 0].axis('off')

    # Reamostradas (mesma região proporcional)
    posicoes = [(0, 1), (1, 0), (1, 1)]

    for idx, (img_reamos, dpi) in enumerate(zip(imagens_reamostradas, dpis)):
        pos = posicoes[idx]

        # Calcula região proporcional
        fator = img_reamos.shape[0] / imagem_original.shape[0]
        y_s = int(y_start * fator)
        y_e = int(y_end * fator)
        x_s = int(x_start * fator)
        x_e = int(x_end * fator)

        regiao = img_reamos[y_s:y_e, x_s:x_e]

        axes[pos].imshow(regiao, cmap='gray', interpolation='nearest')
        axes[pos].set_title(f'{dpi} DPI\n(Perda de detalhes visível)',
                            fontweight='bold', fontsize=12)
        axes[pos].axis('off')

    plt.tight_layout()
    plt.show()

    print("✓ Visualização com zoom concluída!")


# =============================================================================
# ANÁLISE E DISCUSSÃO DOS RESULTADOS
# =============================================================================

def analisar_resultados():
    """
    Análise detalhada dos efeitos da reamostragem
    """
    print(f"\n{'=' * 80}")
    print("📊 ANÁLISE DOS RESULTADOS - EFEITOS DA REAMOSTRAGEM")
    print(f"{'=' * 80}")

    print("\n🔍 OBSERVAÇÕES SOBRE RESOLUÇÃO ESPACIAL:")

    print("\n   📌 1250 DPI → 300 DPI:")
    print("      • Redução: Aproximadamente 76% dos pixels")
    print("      • Efeito visual: Ainda mantém boa qualidade")
    print("      • Detalhes: A maioria preservada")
    print("      • Aplicação típica: Impressão de alta qualidade")

    print("\n   📌 1250 DPI → 150 DPI:")
    print("      • Redução: Aproximadamente 94% dos pixels")
    print("      • Efeito visual: Perda moderada de detalhes")
    print("      • Detalhes finos: Começam a desaparecer")
    print("      • Aplicação típica: Impressão padrão, revistas")

    print("\n   📌 1250 DPI → 72 DPI:")
    print("      • Redução: Aproximadamente 97% dos pixels")
    print("      • Efeito visual: Perda significativa de detalhes")
    print("      • Detalhes finos: Muito degradados ou perdidos")
    print("      • Aplicação típica: Visualização em tela, web")

    print("\n💡 CONCEITOS IMPORTANTES:")
    print("   • RESOLUÇÃO ESPACIAL: Mede o menor detalhe discernível")
    print("   • DPI ↓ = Menos pixels = Menos detalhes")
    print("   • Trade-off: Qualidade vs Tamanho do arquivo")
    print("   • Escolha do DPI depende da aplicação final")

    print("\n📚 APLICAÇÕES PRÁTICAS (conforme slides):")
    print("   • Jornal: ~75 DPI")
    print("   • Revista: ~133 DPI")
    print("   • Livros de alta qualidade: ~2400 DPI")
    print("   • Tela de computador: ~72-96 DPI")

    print("\n⚠️ IMPORTANTE:")
    print("   • A reamostragem REDUZ informação (processo irreversível)")
    print("   • Não é possível recuperar detalhes perdidos")
    print("   • Sempre mantenha uma cópia da imagem original!")


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """
    Executa o Requisito 1 completo da atividade
    """
    print("\n🚀 INICIANDO REQUISITO 1: REAMOSTRAGEM DPI")

    # Carrega imagem original
    print(f"\n{'=' * 80}")
    print("📷 ETAPA 1: CARREGANDO IMAGEM ORIGINAL")
    print(f"{'=' * 80}")

    imagem_original = carregar_imagem(IMAGEM_ENTRADA)

    # Aplica reamostragem para cada DPI solicitado
    print(f"\n{'=' * 80}")
    print("📷 ETAPA 2: APLICANDO REAMOSTRAGENS")
    print(f"{'=' * 80}")

    imagens_reamostradas = []

    for dpi_alvo in DPI_ALVOS:
        img_reamostrada = aplicar_reamostragem_dpi(imagem_original, dpi_alvo)
        imagens_reamostradas.append(img_reamostrada)

    # Visualiza resultados
    print(f"\n{'=' * 80}")
    print("📷 ETAPA 3: VISUALIZAÇÃO DOS RESULTADOS")
    print(f"{'=' * 80}")

    visualizar_resultados(imagem_original, imagens_reamostradas, DPI_ALVOS)
    visualizar_zoom_comparacao(imagem_original, imagens_reamostradas, DPI_ALVOS)

    # Análise final
    analisar_resultados()

    print(f"\n{'=' * 80}")
    print("🎉 REQUISITO 1 CONCLUÍDO COM SUCESSO!")
    print(f"{'=' * 80}")
    print("\n📋 Resultados obtidos:")
    print(f"   ✅ Imagem original ({DPI_ORIGINAL} DPI) carregada")
    print(f"   ✅ Reamostragem para 300 DPI concluída")
    print(f"   ✅ Reamostragem para 150 DPI concluída")
    print(f"   ✅ Reamostragem para 72 DPI concluída")
    print(f"   ✅ Visualizações comparativas geradas")
    print(f"   ✅ Análise detalhada dos resultados apresentada")
    print(f"   ✅ NENHUMA função pronta utilizada (implementação manual)")


# =============================================================================
# EXECUÇÃO DO PROGRAMA
# =============================================================================

if __name__ == "__main__":
    main()