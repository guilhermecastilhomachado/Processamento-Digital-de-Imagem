import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

"""
Utilize a imagem relógio.tif e faça uma reamostragem de seus pixels para 
aproximadamente 300, 150 e 72 dpi. Sabe-se que a imagem original possui 1250 dpi.
"""

def gerar_reamostragem(imagem_original, nova_largura, nova_altura):
    # Dimensões da imagem original
    altura_original, largura_original = imagem_original.shape[:2]

    # Verifica se a imagem tem 3 canais (RGB) ou é em tons de cinza
    # Cria uma imagem vazia (preta) com as novas dimensões
    # O tipo de dado (dtype) deve ser o mesmo da imagem original
    if len(imagem_original.shape) == 3:
        canais = imagem_original.shape[2]
        imagem_reamostrada = np.zeros((nova_altura, nova_largura, canais), dtype=imagem_original.dtype)
    else:
        print("Imagem em tons de cinza detectada.")
        # Cria uma matriz para imagem reamostrada com nova_altura = linha (y) e nova_largura = coluna (x).
        imagem_reamostrada = np.zeros((nova_altura, nova_largura), dtype=imagem_original.dtype)


    # Fatores de escala: Divide o tamanho original pelo novo tamanho para saber a proporção entre eles
    fator_escala_x = largura_original / nova_largura
    fator_escala_y = altura_original / nova_altura
    
    # Itera sobre cada pixel da NOVA imagem
    for pixl_y_novo in range(nova_altura):
        for pixel_x_novo in range(nova_largura):
            # Encontra o pixel correspondente na imagem ORIGINAL
            # Multiplicamos a coordenada nova pelo fator de escala e arredondamos
            x_original = int(pixel_x_novo * fator_escala_x)
            y_original = int(pixl_y_novo * fator_escala_y)
            
            # Copia o valor do pixel da imagem original para a nova imagem
            imagem_reamostrada[pixl_y_novo, pixel_x_novo] = imagem_original[y_original, x_original]
            
    return imagem_reamostrada


def processar_imagem_relogio():

    DPI_ORIGINAL = 1250
    DPIS_ALVO = [300, 150, 72]
    PASTA = './Trabalho01'
   
    NOME_ARQUIVO = 'relogio.tif'

    diretorio_completo = 'relogio.tif' #f"{PASTA}/{NOME_ARQUIVO}"


    # Verifica se o arquivo de imagem existe
    if not os.path.exists(diretorio_completo):
        print(f"Erro: O arquivo '{NOME_ARQUIVO}' não foi encontrado.")
        print("Por favor, coloque a imagem na mesma pasta do script.")
        return

    # 1. Carregar a imagem original usando a biblioteca Pillow
    try:
        imagem_pil = Image.open(diretorio_completo)
    except Exception as e:
        print(f"Não foi possível abrir a imagem. Erro: {e}")
        return

    # Converter a imagem para um array (exemplo de matriz) para manipulação de pixels
    imagem_original_np = np.array(imagem_pil)
    
    # Obter dimensões originais
    altura_original, largura_original = imagem_original_np.shape[:2]
    
    print(f"Imagem original '{NOME_ARQUIVO}' carregada.")
    print(f"DPI Original: {DPI_ORIGINAL} dpi")
    print(f"Dimensões Originais: {largura_original}x{altura_original} pixels\n")

    # Exibir a imagem original
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    plt.imshow(imagem_original_np, cmap='gray')
    plt.title(f'Original ({DPI_ORIGINAL} dpi)\n{largura_original}x{altura_original} px')
    plt.axis('off')

    # 2. Loop para cada DPI alvo porque o index=1 já foi usado para a imagem original
    plot_index = 2
    for dpi_alvo in DPIS_ALVO:
        print(f"Processando para {dpi_alvo} dpi...")
        
        # Calcular o fator de reamostragem, ou seja, o novo tamanho da imagem
        # A fórmula é: nova dimensão = dimensão original * (DPI alvo / DPI original)
        fator_de_escala  = dpi_alvo / DPI_ORIGINAL
        
        # Calcular as novas dimensões em pixels (arredondando para o inteiro mais próximo)
        nova_largura = round(largura_original * fator_de_escala )
        nova_altura = round(altura_original * fator_de_escala )
        
        print(f"  - Novas dimensões calculadas: {nova_largura}x{nova_altura} pixels")
        
        # 3. Aplicar a reamostragem usando nossa função manual
        imagem_reamostrada = gerar_reamostragem(imagem_original_np, nova_largura, nova_altura)
        
        # 4. Exibir o resultado
        plt.subplot(2, 2, plot_index)
        plt.imshow(imagem_reamostrada, cmap='gray')
        plt.title(f'Reamostrada ({dpi_alvo} dpi)\n{nova_largura}x{nova_altura} px')
        plt.axis('off')
        plot_index += 1
        
    # Ajusta o layout para evitar sobreposição de títulos e exibe a janela
    plt.tight_layout()
    plt.suptitle('Reamostragem de Imagem - PDI', fontsize=16)
    plt.subplots_adjust(top=0.88)
    plt.show()

# Executa a função principal
if __name__ == "__main__":
    processar_imagem_relogio()
