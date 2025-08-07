import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def equalizar_histograma(imagem_np, L=256):
    """Calcula o mapeamento de equalização de histograma para uma imagem."""
    if imagem_np.ndim != 2:
        raise ValueError("A imagem de entrada deve estar em tons de cinza (array 2D).")
    nk = [0] * L
    for pixel_value in np.nditer(imagem_np):
        nk[int(pixel_value)] += 1
    total_pixels = imagem_np.size
    pr_rk = [freq / total_pixels for freq in nk]
    cdf = [0.0] * L
    cdf[0] = pr_rk[0]
    for i in range(1, L):
        cdf[i] = cdf[i-1] + pr_rk[i]
    sk = [round((L - 1) * c) for c in cdf]
    return sk

def aplicar_mapeamento(imagem_np, mapa_sk):
    """Aplica um mapeamento de intensidade a uma imagem."""
    imagem_equalizada_np = np.copy(imagem_np)

    for rk in range(len(mapa_sk)):
        imagem_equalizada_np[imagem_np == rk] = mapa_sk[rk]
    return imagem_equalizada_np

def calcular_histograma_simples(imagem_np, L=256):
    """Calcula a frequência (histograma) de uma imagem.
        No geral, irá contar quantos pixels existem para cada nível de intensidade (0 a L-1).
    """
    hist = [0] * L
    for pixel_value in np.nditer(imagem_np):
        hist[int(pixel_value)] += 1
    return hist


if __name__ == "__main__":
    # --- Configuração dos argumentos da linha de comando ---
    
    caminho_imagem = "./trabalho03/imagem_exemplo6.png"  # Caminho padrão da imagem
    num_passes = 2
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