import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import deque

# ================================================
# 1. Carregar a imagem art8.png em modo binário
# ================================================

# Abre a imagem e converte para tons de cinza
imagem_original = Image.open('art8.png').convert('L')
imagem_array = np.array(imagem_original)

# Verifica se a imagem já é binária (apenas 0s e 255s) e converte para 0s e 1s
imagem_binaria = np.where(imagem_array > 127, 1, 0)

# Exibe a imagem binária para verificação
plt.imshow(imagem_binaria, cmap='gray')
plt.title('Imagem Binária art8.png')
plt.axis('off')
plt.show()

# ================================================
# 2. Função de rotulagem 4-conectada com BFS
# ================================================

def rotular_bfs(imagem, visitado, x_inicial, y_inicial, rotulo):
    """
    Marca todos os pixels conectados 4-conectadamente a partir de (x_inicial, y_inicial)
    usando busca em largura (BFS) e atribui o rótulo informado.
    """
    altura, largura = imagem.shape
    fila = deque()
    fila.append((x_inicial, y_inicial))
    visitado[x_inicial, y_inicial] = rotulo

    # Vizinhos 4-conectados: cima, baixo, esquerda, direita
    vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while fila:
        x, y = fila.popleft()

        for dx, dy in vizinhos:
            nx, ny = x + dx, y + dy

            if 0 <= nx < altura and 0 <= ny < largura:
                if imagem[nx, ny] == 1 and visitado[nx, ny] == 0:
                    visitado[nx, ny] = rotulo
                    fila.append((nx, ny))

# ================================================
# 3. Aplicar a rotulagem na imagem binária
# ================================================

altura, largura = imagem_binaria.shape
visitado = np.zeros((altura, largura), dtype=int)  # matriz de rótulos (0 = não visitado)
rotulo = 1  # começa a rotular a partir de 1

# Percorre todos os pixels da imagem
for i in range(altura):
    for j in range(largura):
        if imagem_binaria[i, j] == 1 and visitado[i, j] == 0:
            rotular_bfs(imagem_binaria, visitado, i, j, rotulo)
            rotulo += 1

# Total de componentes encontrados
num_componentes = rotulo - 1
print(f"Número total de componentes conectados: {num_componentes}")

# ================================================
# 4. Criar imagem colorida com os rótulos
# ================================================

# Normaliza os rótulos para o intervalo [0, 1] e aplica colormap
imagem_normalizada = visitado / np.max(visitado)
plt.imshow(imagem_normalizada, cmap='nipy_spectral')
plt.title('Imagem Rotulada (cores diferentes por componente)')
plt.axis('off')
plt.show()

# ================================================
# 5. Salvar a imagem rotulada
# ================================================

# Converter para imagem 8-bit colorida
imagem_colorida = (imagem_normalizada * 255).astype(np.uint8)
imagem_colorida_pil = Image.fromarray(imagem_colorida)
imagem_colorida_pil.save('art8_rotulada.png')
# agora criar condição para que a imagem nao seja salva se ja existir
if os.path.exists('art8_rotulada.png'):
    print("A imagem 'art8_rotulada.png' já existe. Não foi possível salvar.")
else:
    imagem_colorida_pil.save('art8_rotulada.png')
print("Imagem rotulada salva como art8_rotulada.png")