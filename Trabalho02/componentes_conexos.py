import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import deque

# 1. Carregar a imagem em escala de cinza
# ---------------------------------------------------
# OBS: Certifique-se de que clc3.png está na mesma pasta do código!
imagem_original = Image.open('clc3.png').convert('L')  # L = grayscale
imagem_array = np.array(imagem_original)

# Exibir imagem original (opcional, para entendimento)
plt.imshow(imagem_array, cmap='gray')
plt.title('Imagem Original em Tons de Cinza')
plt.axis('off')
plt.show()

# 2. Binarizar a imagem com threshold 67
# ---------------------------------------------------
# Regra: valores <= 67 → 1 (branco - objeto), valores > 67 → 0 (preto - fundo)
threshold = 67
imagem_binaria = np.where(imagem_array <= threshold, 1, 0)

# 3. Função auxiliar para rotulagem usando busca em largura (BFS)
# ---------------------------------------------------
def rotular_componente(imagem, visitado, x_inicial, y_inicial, rotulo):
    """
    Rotula todos os pixels conectados 4-conectadamente ao ponto (x_inicial, y_inicial)
    usando BFS (fila) para evitar recursão profunda.
    """
    altura, largura = imagem.shape
    fila = deque()
    fila.append((x_inicial, y_inicial))
    visitado[x_inicial, y_inicial] = rotulo

    # Vizinhos 4-conectados (cima, baixo, esquerda, direita)
    vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while fila:
        x, y = fila.popleft()

        for dx, dy in vizinhos:
            nx, ny = x + dx, y + dy

            # Verifica se está dentro dos limites e é parte do objeto (valor 1)
            if (0 <= nx < altura) and (0 <= ny < largura):
                if imagem[nx, ny] == 1 and visitado[nx, ny] == 0:
                    visitado[nx, ny] = rotulo
                    fila.append((nx, ny))

# 4. Aplicar a rotulagem manual na imagem binária
# ---------------------------------------------------
altura, largura = imagem_binaria.shape
visitado = np.zeros((altura, largura), dtype=int)
rotulo_atual = 1

for i in range(altura):
    for j in range(largura):
        # Se for pixel do objeto (1) e ainda não foi visitado
        if imagem_binaria[i, j] == 1 and visitado[i, j] == 0:
            rotular_componente(imagem_binaria, visitado, i, j, rotulo_atual)
            rotulo_atual += 1

# 5. Exibir número total de objetos encontrados
# ---------------------------------------------------
numero_de_objetos = rotulo_atual - 1
print(f"Número de objetos (componentes 4-conectados): {numero_de_objetos}")

# 6. (Opcional) Exibir imagem rotulada com cores diferentes por rótulo
# ---------------------------------------------------
# Normalizar para visualizar cada componente com cor diferente
maximo = np.max(visitado)
if maximo == 0:
    imagem_colorida = visitado
else:
    imagem_colorida = visitado / maximo
plt.imshow(imagem_colorida, cmap='nipy_spectral')
plt.title('Componentes Rotulados (cada cor = um objeto)')
plt.axis('off')
plt.show()