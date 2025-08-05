import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Função 1: Calcula o histograma manualmente
def calcular_histograma(imagem_array, L):
    histograma = np.zeros(L, dtype=int) # Inicializa o histograma com zeros com tamanho L que é 256 nivéis de cinza
    for valor in imagem_array.flatten(): # Percorre cada pixel da imagem, flatten transforma a matriz 2D em 1D
        histograma[valor] += 1 # Incrementa o contador do valor correspondente no histograma
    return histograma # Retorna o histograma como um array de contagens

# Função 2: Equalização de histograma
def equalizar_histograma(imagem_array, L):
    histograma = calcular_histograma(imagem_array, L) # Calcula o histograma da imagem com 256 níveis de cinza
    cdf = np.cumsum(histograma) # Calcula a função de distribuição acumulada (CDF) do histograma
    cdf_normalizada = np.floor((L - 1) * cdf / cdf[-1]).astype(np.uint8) # Normaliza a CDF para o intervalo [0, L-1]
    # e converte para uint8
    return cdf_normalizada # Retorna o mapeamento de intensidades

# Função 3: Aplica o mapeamento na imagem
def aplicar_mapeamento(imagem_array, mapeamento):
    return mapeamento[imagem_array] # Aplica o mapeamento de intensidades na imagem original

# Execução principal
if __name__ == "__main__":
    # 1. Carrega imagem em tons de cinza
    imagem = Image.open('imagem_exemplo3.png').convert('L')  # converte para escala de cinza
    imagem_array = np.array(imagem) # Converte a imagem para um array NumPy

    # 2. Define número de níveis de cinza (L = 256 para 8 bits)
    L = 256

    # 3. Equaliza a imagem
    mapeamento = equalizar_histograma(imagem_array, L) # Calcula o mapeamento de intensidades
    imagem_equalizada_array = aplicar_mapeamento(imagem_array, mapeamento) # Aplica o mapeamento na imagem original
    imagem_equalizada = Image.fromarray(imagem_equalizada_array) # Converte o array de volta para uma imagem PIL

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
    nome_arquivo = 'imagem_equalizada3.png'
    if os.path.exists(nome_arquivo):
        print(f"A imagem '{nome_arquivo}' já existe. Nenhuma nova imagem foi salva.")
    else:
        imagem_equalizada.save(nome_arquivo)
        print(f"A imagem equalizada foi salva como '{nome_arquivo}'.")

    # 6. Mostrar o mapeamento (para explicação)
    print("\nMapeamento de intensidades (original → equalizado):")
    for i, v in enumerate(mapeamento):
        print(f"{i} → {v}")