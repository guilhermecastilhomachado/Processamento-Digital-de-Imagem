# Aula 5 — Filtragem Espacial: Suavização (Média, Mediana, Gaussiano)

Índice
- [Objetivos](#objetivos)
- [Filtros comuns](#filtros-comuns)
- [Exemplo: convolução com média 3×3](#exemplo-convolução-com-média-33)
- [Dicas](#dicas)

Objetivos
- Entender filtros passa-baixa e seus efeitos em ruído e detalhes.

Filtros comuns
- Média: kernel com valores iguais (soma = 1). Suaviza, borra bordas.
- Mediana: substitui pelo valor mediano da vizinhança. Excelente contra ruído sal e pimenta.
- Gaussiano: pesos proporcionais à distância. Natural, controlado por σ.

Exemplo: convolução com média 3×3
```python
import numpy as np
from PIL import Image

def mean3(a):
    k = np.ones((3,3))/9
    H,W = a.shape
    p = 1
    ap = np.pad(a, p, mode='edge')
    out = np.zeros_like(a, dtype=float)
    for i in range(H):
        for j in range(W):
            out[i,j] = np.sum(ap[i:i+3, j:j+3]*k)
    return np.clip(out,0,255).astype(np.uint8)

img = Image.open('Trabalho04/ben2.png').convert('L')
a = np.array(img)
Image.fromarray(mean3(a)).save('ben2_mean3.png')
```

Dicas
- Para Gaussiano, tamanho ≈ 6σ+1 (ímpar) captura 99% da distribuição.
- Mediana é não-linear; não use convolução linear para implementá-la.
