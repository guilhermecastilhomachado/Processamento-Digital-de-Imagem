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
    imagem = Image.open('imagem_exemplo1.jpg').convert('L')  # converte para escala de cinza
    imagem_array = np.array(imagem) # Converte a imagem para um array NumPy

    # 2. Define número de níveis de cinza (L = 256 para 8 bits)
    L = 256

    # 3. Equaliza a imagem
    mapeamento = equalizar_histograma(imagem_array, L) # Calcula o mapeamento de intensidades
    imagem_equalizada_array = aplicar_mapeamento(imagem_array, mapeamento) # Aplica o mapeamento na imagem original
    imagem_equalizada = Image.fromarray(imagem_equalizada_array) # Converte o array de volta para uma imagem PIL

    # 4. Exibe imagem original e equalizada
    plt.figure(figsize=(12, 6)) # cria uma figura com tamanho 12x6 polegadas, com 2 linhas e 2 colunas
    # No caso usamos 4 subplots, de 2 linhas e 2 colunas para exibir a imagem original, o histograma original,
    # a imagem equalizada e o histograma equalizado

    plt.subplot(2, 2, 1) # esse primeiro subplot ocupa a posição 1 na grade 2x2 que e a imagem original
    plt.imshow(imagem_array, cmap='gray') # exibe a imagem original em tons de cinza
    plt.title('Imagem Original')
    plt.axis('off')

    plt.subplot(2, 2, 2) # esse segundo subplot ocupa a posição 2 na grade 2x2 que e o histograma original
    plt.hist(imagem_array.flatten(), bins=L, range=(0, L-1), color='gray') # exibe o histograma da imagem original
    plt.title('Histograma Original')

    plt.subplot(2, 2, 3) # esse terceiro subplot ocupa a posição 3 na grade 2x2 que e a imagem equalizada
    plt.imshow(imagem_equalizada_array, cmap='gray') # exibe a imagem equalizada em tons de cinza
    plt.title('Imagem Equalizada')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.hist(imagem_equalizada_array.flatten(), bins=L, range=(0, L-1), color='gray') # exibe o histograma da imagem
    plt.title('Histograma Equalizado') # equalizada

    plt.tight_layout() # Ajusta o layout para evitar sobreposição de subplots

    # a mudança começa aqui
    plt.show()  # Exibe os gráficos da primeira equalização

    # --- SEGUNDA EQUALIZAÇÃO SOBRE A IMAGEM JÁ EQUALIZADA ---
    # A parti daqui, vamos aplicar a equalização novamente na imagem já equalizada
    # para testar e ver o que acontece.
    # Para isso, vamos usar a mesma função de equalização que já foi definida anteriormente.
    # Para isso, vamos criar um novo mapeamento de intensidades e aplicar novamente a equalização.
    mapeamento2 = equalizar_histograma(imagem_equalizada_array, L) # Calcula o mapeamento de intensidades novamente
    imagem_equalizada2_array = aplicar_mapeamento(imagem_equalizada_array, mapeamento2) # Aplica o mapeamento na imagem
    # já equalizada
    imagem_equalizada2 = Image.fromarray(imagem_equalizada2_array) # Converte o array de volta para uma imagem PIL
    # Apos isso, vamos exibir a imagem equalizada pela segunda vez e seu histograma.

    # Exibe a imagem equalizada pela segunda vez e seu histograma
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 2, 1)
    plt.imshow(imagem_equalizada_array, cmap='gray')
    plt.title('Imagem Após 1ª Equalização')
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.hist(imagem_equalizada_array.flatten(), bins=L, range=(0, L - 1), color='gray')
    plt.title('Histograma Após 1ª Equalização')

    plt.subplot(2, 2, 3)
    plt.imshow(imagem_equalizada2_array, cmap='gray')
    plt.title('Imagem Após 2ª Equalização')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.hist(imagem_equalizada2_array.flatten(), bins=L, range=(0, L - 1), color='gray')
    plt.title('Histograma Após 2ª Equalização')

    plt.tight_layout()
    plt.show()

    # Apos aplicar novamente a equalização na imagem ja equalizada, percebemos que  após a primeira equalização,
    # a imagem já possui uma distribuição de intensidades mais uniforme, ou seja, o histograma já está "corrigido".
    # Portanto, aplicar novamente o mesmo algoritmo sobre uma imagem já equalizada não altera significativamente os
    # dados — o histograma permanece praticamente igual, e a imagem final também.

    # A função de equalização é idempotente neste caso — ou seja, reaplicá-la não muda mais o
    # resultado após a primeira aplicação.

    # 5. Salvar a imagem equalizada
    nome_arquivo = 'imagem_equalizada6.png'
    if os.path.exists(nome_arquivo): # Verifica se o arquivo já existe pela função os.path.exists
        print(f"A imagem '{nome_arquivo}' já existe. Nenhuma nova imagem foi salva.")
    else:
        imagem_equalizada.save(nome_arquivo) # Salva a imagem equalizada no arquivo especificado
        print(f"A imagem equalizada foi salva como '{nome_arquivo}'.")

    # 6. Mostrar o mapeamento (para explicação)
    print("\nMapeamento de intensidades (original → equalizado):") # Exibe o mapeamento de intensidades
    for i, v in enumerate(mapeamento): # Percorre o mapeamento
        print(f"{i} → {v}") # Exibe o valor original e o valor equalizado correspondente