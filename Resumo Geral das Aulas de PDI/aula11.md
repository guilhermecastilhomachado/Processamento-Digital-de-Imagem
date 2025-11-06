# Aula 11 — Representação e Descrição (Parte 2): Textura e Formas Avançadas

Objetivos
- Explorar descritores avançados: textura, formas e contornos robustos.

Textura
- Matriz de coocorrência (GLCM): contrasta, homogeneidade, energia, correlação.
- Filtros de Gabor: resposta a frequências e orientações específicas.

Formas
- Fourier descriptors: descrevem contornos no domínio da frequência.
- Skeletonization: eixo medial; útil para análise topológica.

Exemplo: métricas GLCM (usando skimage)
- Dependência opcional: instale scikit-image antes de executar o snippet:
  pip install scikit-image
```python
import numpy as np
from skimage.feature import graycomatrix, graycoprops
from PIL import Image

img = Image.open('Trabalho03/imagem_exemplo2.png').convert('L')
a = np.array(img)
# Reduz níveis para GLCM modesta
b = (a/8).astype(np.uint8)  # 32 níveis
P = graycomatrix(b, distances=[1], angles=[0], levels=32, symmetric=True, normed=True)
contraste = graycoprops(P, 'contrast')[0,0]
homog = graycoprops(P, 'homogeneity')[0,0]
energia = graycoprops(P, 'energy')[0,0]
correl = graycoprops(P, 'correlation')[0,0]
print(contraste, homog, energia, correl)
```

Dicas
- Padronize recortes e parâmetros para comparar texturas entre imagens.
