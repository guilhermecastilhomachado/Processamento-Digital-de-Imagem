import cv2
import numpy as np
import matplotlib.pyplot as plt

# Exercicio 2 da tarefa 1 - Quantização de Imagem

# Utilize a imagem ctskull-256.tif e refaça a quantização de seus pixels
# utilizando de 7 a 1 bit(s) por pixel.

# Carrega a imagem em escala de cinza
imagem = cv2.imread('ctskull-256.tif', cv2.IMREAD_GRAYSCALE) # cv2.imread carrega a imagem do arquivo especificado
# cv2.IMREAD_GRAYSCALE garante que a imagem seja carregada em escala de cinza

# Função para quantizar a imagem para n bits
def quantizar_imagem(imagem, bits):
    # Calcula o número de níveis possíveis (2^bits)
    niveis = 2 ** bits # Calcula o número de níveis de cinza com base no número de bits

    # Normaliza os valores para os níveis desejados
    imagem_quantizada = np.floor(imagem / (256 / niveis)) * (255 / (niveis - 1))
    # A normalização é feita dividindo os valores da imagem pelo número de níveis possíveis
    # e multiplicando pelo valor máximo de intensidade (255) dividido pelo número de níveis menos 1.
    # np.floor arredonda para baixo os valores resultantes, garantindo que os valores quantizados sejam inteiros

    # Converte para uint8
    return imagem_quantizada.astype(np.uint8) # Converte a imagem quantizada para o tipo uint8
    # essa conversão é necessária para garantir que os valores da imagem estejam no intervalo correto de 0 a 255

# Exibir todas as quantizações de 7 a 1 bits
plt.figure(figsize=(12, 10))
for i, bits in enumerate(range(7, 0, -1), 1): # Cria um loop para quantizar a imagem de 7 a 1 bits
    img_q = quantizar_imagem(imagem, bits) # Chama a função para quantizar a imagem com o número de bits especificado

    # Mostrar na tela
    plt.subplot(3, 3, i) # o subplot dividir a tela em várias partes, neste caso 3 linhas e 3 colunas
    plt.imshow(img_q, cmap='gray') # imshow exibe a imagem, cmap='gray' indica que é uma imagem em escala de cinza
    plt.title(f'{bits} bit(s)') # título da imagem exibida
    plt.axis('off') # desativa os eixos para uma melhor visualização

plt.tight_layout() # ajusta o layout para evitar sobreposição de títulos
plt.show() # Exibe a imagem original