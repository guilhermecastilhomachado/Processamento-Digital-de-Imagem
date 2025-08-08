import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def equalizar_histograma(imagem_np, L=256):
    """Calcula o mapeamento de equalização de histograma para uma imagem."""
    if imagem_np.ndim != 2: # Verifica se a imagem é 2D (tons de cinza), o 2 significa que é uma matriz 2D
        raise ValueError("A imagem de entrada deve estar em tons de cinza (array 2D).")
    nk = [0] * L # Inicializa a lista de frequências com zeros, onde L é o número de níveis de intensidade
    for pixel_value in np.nditer(imagem_np): # Itera sobre cada pixel da imagem usando nditer
        nk[int(pixel_value)] += 1 # Incrementa a frequência do valor do pixel correspondente
    total_pixels = imagem_np.size # Obtém o número total de pixels na imagem
    pr_rk = [freq / total_pixels for freq in nk] # Calcula a probabilidade de cada nível de intensidade
    cdf = [0.0] * L # Inicializa a lista da função de distribuição acumulada (CDF) com zeros
    cdf[0] = pr_rk[0] # A CDF do primeiro nível é igual à sua probabilidade
    for i in range(1, L): # Calcula a CDF acumulando as probabilidades
        cdf[i] = cdf[i-1] + pr_rk[i] # A CDF do nível i é a soma da CDF do nível i-1 e a probabilidade do nível i
    sk = [round((L - 1) * c) for c in cdf] # Normaliza a CDF para o intervalo [0, L-1] e arredonda para o inteiro mais próximo
    return sk # Retorna o mapeamento de intensidades sk, que é uma lista onde cada índice representa o nível de intensidade original

""" Em suma, essa função de equalizar_histograma recebe uma imagem em tons de cinza (array 2D) e calcula o 
mapeamento de intensidades"""


def aplicar_mapeamento(imagem_np, mapa_sk):
    """Aplica um mapeamento de intensidade a uma imagem."""
    imagem_equalizada_np = np.copy(imagem_np) # Cria uma cópia da imagem original para evitar modificações diretas

    for rk in range(len(mapa_sk)): # Itera sobre cada nível de intensidade original
        imagem_equalizada_np[imagem_np == rk] = mapa_sk[rk] # Substitui os valores da imagem original pelo mapeamento correspondente
    return imagem_equalizada_np # Retorna a imagem com o mapeamento aplicado, que agora está equalizada

""" Em resumo, essa função de aplicar_mapeamento recebe uma imagem em tons de cinza (array 2D) e um mapeamento"""


def calcular_histograma_simples(imagem_np, L=256):
    """Calcula a frequência (histograma) de uma imagem.
        No geral, irá contar quantos pixels existem para cada nível de intensidade (0 a L-1).
    """
    hist = [0] * L
    for pixel_value in np.nditer(imagem_np):
        hist[int(pixel_value)] += 1
    return hist

""" Em resumo, essa função de calcular_histograma_simples recebe uma imagem em tons de cinza (array 2D) e calcula o histograma,"""


if __name__ == "__main__":
    # --- Configuração dos argumentos da linha de comando ---
    
    caminho_imagem = "imagem_exemplo6.png"  # Caminho padrão da imagem
    num_passes = 2 # Número de vezes que a equalização será aplicada
    L_intensidades = 256

    try:
        # --- Listas para armazenar os resultados de cada passo ---
        lista_imagens = []
        lista_histogramas = []

        # --- Carregamento e Armazenamento da Imagem Original (Passo 0) ---
        print(f"Carregando a imagem: {caminho_imagem}")
        img_pil = Image.open(caminho_imagem).convert('L')
        imagem_atual = np.array(img_pil)
        
        lista_imagens.append(imagem_atual)
        lista_histogramas.append(calcular_histograma_simples(imagem_atual, L_intensidades))

        # --- Laço FOR para aplicar a equalização N vezes ---
        for i in range(num_passes):
            print(f"Executando a {i+1}ª passagem da equalização...")
            
            # Pega a imagem do último passo para processar
            imagem_anterior = lista_imagens[-1]
            
            # Calcula e aplica a equalização
            mapeamento = equalizar_histograma(imagem_anterior, L=L_intensidades)
            imagem_nova = aplicar_mapeamento(imagem_anterior, mapeamento)
            
            lista_imagens.append(imagem_nova)
            lista_histogramas.append(calcular_histograma_simples(imagem_nova, L_intensidades))

        # --- Exibição Dinâmica dos Resultados ---
        print("Exibindo os resultados para comparação...")

        num_linhas_plot = num_passes + 1
        fig, axes = plt.subplots(num_linhas_plot, 2, figsize=(14, 7 * num_linhas_plot))
        fig.suptitle(f'Comparação da Equalização Aplicada {num_passes} Vezes', fontsize=16)

        if num_linhas_plot == 1:
            axes = np.array([axes])

        for i in range(num_linhas_plot):
            imagem = lista_imagens[i]
            histograma = lista_histogramas[i]
            
            # Define o título da linha
            if i == 0:
                titulo_passo = "Original"
            else:
                titulo_passo = f"Após {i}ª Equalização"

            # Plot da imagem
            axes[i, 0].imshow(imagem, cmap='gray', vmin=0, vmax=255)
            axes[i, 0].set_title(f"Imagem {titulo_passo}")
            axes[i, 0].axis('off')

            # Plot do histograma
            axes[i, 1].bar(range(L_intensidades), histograma, color='gray')
            #axes[i, 1].set_title(f"Histograma {titulo_passo}")
            axes[i, 1].set_xlim([0, L_intensidades-1])
            axes[i, 1].set_xlabel("Intensidade")
            axes[i, 1].set_ylabel("Frequência")

        plt.tight_layout(rect=[0, 0, 1, 0.97])
        plt.show()

    except FileNotFoundError:
        print(f"ERRO: O arquivo '{caminho_imagem}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")