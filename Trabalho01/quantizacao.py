import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Carrega a imagem em escala de cinza
imagem = cv2.imread('ctskull-256.tif', cv2.IMREAD_GRAYSCALE)

# Cria uma pasta para salvar as imagens quantizadas (caso queira salvar)
os.makedirs("quantizadas", exist_ok=True)


# Função para quantizar a imagem para n bits
def quantizar_imagem(imagem, bits):
    # Calcula o número de níveis possíveis (2^bits)
    niveis = 2 ** bits

    # Normaliza os valores para os níveis desejados
    imagem_quantizada = np.floor(imagem / (256 / niveis)) * (255 / (niveis - 1))

    # Converte para uint8
    return imagem_quantizada.astype(np.uint8)


# Exibir todas as quantizações de 7 a 1 bits
plt.figure(figsize=(12, 10))
for i, bits in enumerate(range(7, 0, -1), 1):
    img_q = quantizar_imagem(imagem, bits)

    # Mostrar na tela
    plt.subplot(3, 3, i)
    plt.imshow(img_q, cmap='gray')
    plt.title(f'{bits} bit(s)')
    plt.axis('off')

plt.tight_layout()
plt.show()
