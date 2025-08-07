import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# FUNÇÃO PRINCIPAL DO EXERCÍCIO
# --------------------------------------------------------------------------
def equalizar_histograma(imagem_np, L=256):
    """
    Calcula o mapeamento de equalização de histograma para uma imagem.
    """
    # Validação para garantir que a imagem está em tons de cinza
    if imagem_np.ndim != 2:
        raise ValueError("A imagem de entrada deve estar em tons de cinza (array 2D).")

    # Passo 1: Calcular a frequência de cada intensidade (nk)
    # np.histogram é eficiente, mas vamos fazer manualmente para seguir o espírito.
    nk = [0] * L
    for pixel_value in np.nditer(imagem_np):
        nk[int(pixel_value)] += 1

    # Obter o número total de pixels
    total_pixels = imagem_np.size

    # Passo 2: Calcular a probabilidade de cada intensidade (Pr(rk))
    pr_rk = [freq / total_pixels for freq in nk]

    # Passo 3: Calcular a Função de Distribuição Cumulativa (CDF)
    cdf = [0.0] * L
    cdf[0] = pr_rk[0]
    for i in range(1, L):
        cdf[i] = cdf[i-1] + pr_rk[i]

    # Passo 4: Calcular o mapeamento de transformação (sk)
    # sk = (L - 1) * CDF(rk)
    sk = [round((L - 1) * c) for c in cdf]

    return sk


def aplicar_mapeamento(imagem_np, mapa_sk):
    """Aplica um mapeamento de intensidade a uma imagem."""
    # Cria uma cópia da imagem para não alterar a original
    imagem_equalizada_np = np.copy(imagem_np)
    # Itera sobre cada valor de pixel possível (0-255)
    for rk in range(len(mapa_sk)):
        # Encontra todos os pixels com o valor rk e os substitui pelo valor sk
        imagem_equalizada_np[imagem_np == rk] = mapa_sk[rk]
    return imagem_equalizada_np

def calcular_histograma_simples(imagem_np, L=256):
    """Calcula a frequência (histograma) de uma imagem."""
    hist = [0] * L
    for pixel_value in np.nditer(imagem_np):
        hist[int(pixel_value)] += 1
    return hist

if __name__ == "__main__":
    # --- Configuração ---
    # COLOQUE O CAMINHO PARA SUA IMAGEM AQUI
    caminho_imagem = './Trabalho03/imagem_exemplo1.jpg'
    L_intensidades = 256

    try:
        # --- Carregamento e Preparação da Imagem ---
        print(f"Carregando a imagem: {caminho_imagem}")
        # Abre a imagem e a converte para tons de cinza ('L' mode)
        img_pil = Image.open(caminho_imagem).convert('L')
        # Converte a imagem PIL para um array NumPy para processamento
        imagem_original_np = np.array(img_pil)

        # --- Processamento ---
        # 1. Chamar a função principal para obter o mapeamento
        print("Calculando o mapeamento de equalização...")
        mapeamento_sk = equalizar_histograma(imagem_original_np, L=L_intensidades)

        # 2. Aplicar o mapeamento para criar a imagem equalizada
        print("Aplicando o mapeamento para gerar a nova imagem...")
        imagem_equalizada_np = aplicar_mapeamento(imagem_original_np, mapeamento_sk)

        # 3. Calcular os histogramas para exibição
        print("Calculando os histogramas...")
        hist_original = calcular_histograma_simples(imagem_original_np, L=L_intensidades)
        hist_equalizado = calcular_histograma_simples(imagem_equalizada_np, L=L_intensidades)

        # --- Exibição dos Resultados ---
        print("Exibindo os resultados...")
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Imagem Original
        axes[0, 0].imshow(imagem_original_np, cmap='gray', vmin=0, vmax=255)
        axes[0, 0].set_title("1. Imagem Original")
        axes[0, 0].axis('off')

        # Histograma Original
        axes[0, 1].bar(range(L_intensidades), hist_original, color='gray')
        axes[0, 1].set_title("2. Histograma Original")
        axes[0, 1].set_xlabel("Intensidade (rk)")
        axes[0, 1].set_ylabel("Frequência Pr(rk)")
        axes[0, 1].set_xlim([0, L_intensidades-1])

        # Imagem Equalizada
        axes[1, 0].imshow(imagem_equalizada_np, cmap='gray', vmin=0, vmax=255)
        axes[1, 0].set_title("3. Imagem Equalizada")
        axes[1, 0].axis('off')

        # Histograma Equalizado
        axes[1, 1].bar(range(L_intensidades), hist_equalizado, color='gray')
        axes[1, 1].set_title("4. Histograma Equalizado")
        axes[1, 1].set_xlabel("Intensidade (sk)")
        axes[1, 1].set_ylabel("Frequência (Ps(sk)")
        axes[1, 1].set_xlim([0, L_intensidades-1])

        plt.tight_layout(pad=3.0)
        plt.show()

    except FileNotFoundError:
        print(f"ERRO: O arquivo '{caminho_imagem}' não foi encontrado.")
        print("Por favor, verifique se o nome do arquivo está correto e no mesmo diretório do script.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")