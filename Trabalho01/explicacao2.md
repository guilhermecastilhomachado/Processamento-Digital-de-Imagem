# Atividade Avaliativa 1 – Tarefa 2
## Tema: Quantização de imagem em diferentes profundidades de bits (7 a 1 bit por pixel)

---
## 🎯 Objetivo

Reduzir a profundidade de bits (quantização) da imagem `ctskull-256.tif`, simulando diferentes níveis de compressão. A ideia é representar a imagem com menos informações, ou seja, com menos níveis de cinza, indo de 7 bits até 1 bit por pixel.

---

## 📂 Estrutura do Código

### 1. **Importação das bibliotecas**
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
```
cv2: É a biblioteca OpenCV (Open Source Computer Vision).
Ela é usada para ler, manipular e salvar imagens.
Aqui, ela serve para abrir a imagem original e salvar as imagens modificadas.

numpy (np): Biblioteca para operações matemáticas e com arrays.
Muito usada para fazer cálculos nos pixels das imagens.

matplotlib.pyplot (plt): Biblioteca para exibir imagens em gráficos.
Usamos para mostrar as imagens quantizadas lado a lado.

---
### 2. **Carregamento da Imagem**
```python
imagem_original = cv2.imread('ctskull-256.tif', cv2.IMREAD_GRAYSCALE)
```
A imagem é carregada em escala de cinza com 256 níveis de tons (8 bits por pixel).

--- 
### 3. **Função de Quantização**
```python
def quantizar_imagem(imagem, bits):
    # Calcula o número de níveis de cinza
    niveis = 2 ** bits
    
    # Aplica a quantização
    imagem_quantizada = np.floor(imagem / (256 / niveis)) * (255 / (niveis - 1))
    
    return imagem_quantizada.astype(np.uint8)
```
niveis = 2 ** bits: calcula o número de níveis possíveis para os bits informados.

* Ex: 2³ = 8 níveis para 3 bits.

imagem / (256 / niveis): normaliza os valores da imagem para o novo número de níveis.

* Ex: se são 8 níveis, os tons serão divididos por 32 (256/8).

np.floor(...): arredonda os valores para baixo, garantindo que o nível seja inteiro.

(255 / (niveis - 1)): retorna os valores à faixa de 0 a 255 para visualização correta.

* Como estamos em escala de cinza, mantemos o intervalo 0–255 mesmo com menos níveis.

astype(np.uint8): converte para o formato correto de imagem (inteiro de 8 bits).

--- 

### 4. **Loop de Quantização e visualização**'
```python
plt.figure(figsize=(12, 10))
for i, bits in enumerate(range(7, 0, -1), 1):
    img_q = quantizar_imagem(imagem, bits)
    cv2.imwrite(f'quantizadas/ctskull_{bits}bits.tif', img_q)
    
    plt.subplot(3, 3, i)
    plt.imshow(img_q, cmap='gray')
    plt.title(f'{bits} bit(s)')
    plt.axis('off')
```
range(7, 0, -1): cria uma sequência de bits de 7 até 1.

enumerate(..., 1): gera o índice i para posicionar os gráficos no subplot.

quantizar_imagem(imagem, bits): quantiza a imagem com o número de bits atual.

cv2.imwrite(...): salva a imagem quantizada na pasta quantizadas/ com nome claro.

plt.subplot(...): organiza a visualização das imagens lado a lado, 3 por linha.

plt.imshow(..., cmap='gray'): mostra a imagem em tons de cinza.

plt.title(...): exibe o número de bits usado.

plt.axis('off'): remove eixos da imagem para visualização mais limpa.

---

### 5. **Ajuste e exibição final**
```python
plt.tight_layout()
plt.show()
```
Garante que os gráficos fiquem bem distribuídos e exibidos corretamente na tela.