# Aula 7 — Morfologia Matemática

Objetivos
- Operações com elementos estruturantes em imagens binárias e em tons de cinza.

Conceitos
- Elemento estruturante (EE): forma que “varre” a imagem (quadrado, disco, cruz).
- Erosão: encolhe objetos (remove pixels nos contornos).
- Dilatação: expande objetos (adiciona pixels nos contornos).
- Abertura: erosão seguida de dilatação (remove ruído pequeno).
- Fechamento: dilatação seguida de erosão (fecha lacunas).

Exemplo (binário, EE 3×3 quadrado)
```python
import numpy as np

def dilatar(bin_img):
    H,W=bin_img.shape; p=1; ap=np.pad(bin_img,p)
    out=np.zeros_like(bin_img)
    for i in range(H):
        for j in range(W):
            out[i,j]=1 if np.any(ap[i:i+3,j:j+3]) else 0
    return out

def erodir(bin_img):
    H,W=bin_img.shape; p=1; ap=np.pad(bin_img,p)
    out=np.zeros_like(bin_img)
    for i in range(H):
        for j in range(W):
            out[i,j]=1 if np.all(ap[i:i+3,j:j+3]) else 0
    return out
```

Aplicações
- Limpeza de ruídos, fechamento de buracos, extração de esqueletos, medidas de forma.

