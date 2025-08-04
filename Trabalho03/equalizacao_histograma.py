import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Função 1: Calcula o histograma manualmente
def calcular_histograma(imagem_array, L):
    histograma = np.zeros(L, dtype=int)
    for valor in imagem_array.flatten():
        histograma[valor] += 1
    return histograma

# Função 2: Equalização de histograma
def equalizar_histograma(imagem_array, L):
    histograma = calcular_histograma(imagem_array, L)
    cdf = np.cumsum(histograma)
    cdf_normalizada = np.floor((L - 1) * cdf / cdf[-1]).astype(np.uint8)
    return cdf_normalizada

# Função 3: Aplica o mapeamento na imagem
def aplicar_mapeamento(imagem_array, mapeamento):
    return mapeamento[imagem_array]

# Execução principal
if __name__ == "__main__":
    # 1. Carrega imagem em tons de cinza
    imagem = Image.open('imagem_exemplo2.png').convert('L')  # converte para escala de cinza
    imagem_array = np.array(imagem)

    # 2. Define número de níveis de cinza (L = 256 para 8 bits)
    L = 256

    # 3. Equaliza a imagem
    mapeamento = equalizar_histograma(imagem_array, L)
    imagem_equalizada_array = aplicar_mapeamento(imagem_array, mapeamento)
    imagem_equalizada = Image.fromarray(imagem_equalizada_array)

    # 4. Exibe imagem original e equalizada
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 2, 1)
    plt.imshow(imagem_array, cmap='gray')
    plt.title('Imagem Original')
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.hist(imagem_array.flatten(), bins=L, range=(0, L-1), color='gray')
    plt.title('Histograma Original')

    plt.subplot(2, 2, 3)
    plt.imshow(imagem_equalizada_array, cmap='gray')
    plt.title('Imagem Equalizada')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.hist(imagem_equalizada_array.flatten(), bins=L, range=(0, L-1), color='gray')
    plt.title('Histograma Equalizado')

    plt.tight_layout()
    plt.show()

    # 5. Salvar a imagem equalizada
    imagem_equalizada.save('imagem_equalizada2.png')

    # 6. Mostrar o mapeamento (para explicação)
    print("\nMapeamento de intensidades (original → equalizado):")
    for i, v in enumerate(mapeamento):
        print(f"{i} → {v}")