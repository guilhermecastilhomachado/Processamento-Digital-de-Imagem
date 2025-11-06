# Aula 1 — Introdução ao Processamento Digital de Imagens (PDI)

Objetivos
- Entender o que é PDI, onde é aplicado e o pipeline básico.
- Conhecer os pilares: amostragem (resolução espacial), quantização (profundidade de bits) e representação.

Aplicações típicas
- Médicas (radiologia, TC/RM), indústria (inspeção), segurança (biometria), satélites, fotografia e arte.

Conceitos-chave
- Imagem digital: matriz de pixels. Cada pixel armazena intensidade (tons de cinza) ou cor (RGB).
- Resolução espacial: número de pixels (largura × altura). Mais pixels → mais detalhes.
- DPI/PPI: densidade de pontos/pixels por polegada. Importante para impressão e digitalização.
- Profundidade de bits: número de bits por pixel. 8 bits → 256 níveis (0–255). 1 bit → binária.
- Canal de cor: RGB (vermelho, verde, azul). Imagens coloridas combinam três matrizes.

Pipeline típico de PDI
1) Aquisição (câmera, scanner)
2) Pré-processamento (suavização, realce)
3) Segmentação (separar objeto/fundo)
4) Representação e descrição (características)
5) Reconhecimento/decisão

Exemplo rápido (Python)
- Requisitos: numpy, pillow, matplotlib

```python
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Carrega imagem e converte para tons de cinza
img = Image.open('Trabalho03/imagem_exemplo6.png').convert('L')
arr = np.array(img)

print('Dimensões (HxW):', arr.shape)
print('Valor mínimo/máximo:', arr.min(), arr.max())

fig, ax = plt.subplots(1, 2, figsize=(10,4))
ax[0].imshow(arr, cmap='gray', vmin=0, vmax=255)
ax[0].set_title('Imagem em tons de cinza')
ax[0].axis('off')
ax[1].hist(arr.ravel(), bins=256, range=(0,256), color='gray')
ax[1].set_title('Histograma (0–255)')
plt.tight_layout(); plt.show()
```

Dicas
- Trabalhe sempre com cópias (evite sobrescrever original).
- Verifique faixas de valores (0–255) após operações.

Exercício rápido
- Troque a imagem por outra do projeto e compare histogramas.

Referências
- Gonzalez & Woods, Digital Image Processing.

