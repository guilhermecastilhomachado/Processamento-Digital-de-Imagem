# Aula 10 — Representação e Descrição de Regiões

Objetivos
- Representar objetos segmentados e extrair descritores para reconhecimento.

Representações
- Bordas/contornos: lista de pontos; cadeia de Freeman; polilinhas.
- Regiões: máscara binária; polígonos; bounding boxes.

Descritores clássicos
- Geométricos: área, perímetro, compacidade, circularidade, excentricidade.
- Momentos de Hu (invariantes a rotação/escala/traslação).
- Histogramas de orientação de gradientes (HOG), LBP (padrões locais binários).

Exemplo: medidas simples de uma região
- Dependência opcional: o snippet usa SciPy (ndimage). Para executar, instale antes:
  pip install scipy
```python
import numpy as np
from scipy import ndimage as ndi

# Suponha bin_img (0/1) com um único objeto
lbl, n = ndi.label(bin_img)
idx = (lbl==1)
area = np.sum(idx)
perimetro = np.sum(ndi.binary_dilation(idx) ^ idx)
# bounding box
coords = np.argwhere(idx)
(y0,x0),(y1,x1) = coords.min(0), coords.max(0)
altura, largura = (y1-y0+1), (x1-x0+1)
```

Dicas
- Normalizar descritores para comparação entre objetos de tamanhos distintos.
