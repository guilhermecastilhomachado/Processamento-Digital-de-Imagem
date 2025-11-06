# Aula 2 — Representação de Imagem Digital

Índice
- [Objetivos](#objetivos)
- [Amostragem (resolução espacial)](#amostragem-resolução-espacial)
- [Quantização (resolução de intensidade)](#quantização-resolução-de-intensidade)
- [Formatos de arquivo](#formatos-de-arquivo)
- [Exemplos de reamostragem e quantização](#exemplos-de-reamostragem-e-quantização)
- [Dicas](#dicas)

Objetivos
- Entender como imagens são representadas no computador: amostragem, quantização e formatos.

Amostragem (resolução espacial)
- Número de amostras no plano 2D → pixels. Mais amostras → melhor representação espacial.
- Efeito de reamostragem: reduzir resolução cria pixelização; aumentar sem informação gera interpolação.

Quantização (resolução de intensidade)
- Número de níveis por pixel. 8 bits → 256 níveis. 4 bits → 16 níveis → posterização.

Formatos de arquivo
- PNG (sem perdas, suporta 8/16 bits), JPEG (com perdas), GIF (paleta), TIFF (flexível, científico).

Exemplos de reamostragem e quantização
- Reamostragem (vizinho mais próximo):
```python
import numpy as np
from PIL import Image

img = Image.open('Trabalho01/relogio.tif').convert('L')
arr = np.array(img)

# reduzir para metade (aprox.)
new_h = arr.shape[0]//2
new_w = arr.shape[1]//2
out = np.zeros((new_h, new_w), dtype=arr.dtype)
sy = arr.shape[0]/new_h
sx = arr.shape[1]/new_w
for i in range(new_h):
    for j in range(new_w):
        y = min(int(round(i*sy)), arr.shape[0]-1)
        x = min(int(round(j*sx)), arr.shape[1]-1)
        out[i,j] = arr[y,x]
Image.fromarray(out).save('reamostrada.png')
```
- Quantização manual (4 bits):
```python
import numpy as np
from PIL import Image
img = Image.open('Trabalho01/ctskull-256.tif').convert('L')
a = np.array(img)
L = 16
step = 256//L
q = (a//step)*step
Image.fromarray(q.astype(np.uint8)).save('quantizada_4bits.png')
```

Dicas
- Para Gaussiano, use tamanho de máscara ímpar e compatível com σ (≈ 6σ).
- Sempre normalizar kernels (soma = 1) para preservar brilho.
