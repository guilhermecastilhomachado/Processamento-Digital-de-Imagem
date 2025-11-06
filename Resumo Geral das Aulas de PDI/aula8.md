# Aula 8 — Segmentação de Imagens

Índice
- [Objetivos](#objetivos)
- [Abordagens](#abordagens)
- [Exemplo: thresholding de Otsu (implementação simples)](#exemplo-thresholding-de-otsu-implementação-simples)
- [Dicas](#dicas)

Objetivos
- Separar objetos de interesse do fundo por thresholding, bordas e regiões.

Abordagens
- Thresholding global/adaptativo (Otsu, média local).
- Baseada em bordas (detecção e fechamento de contornos).
- Crescimento de regiões e watershed.

Exemplo: thresholding de Otsu (implementação simples)
```python
import numpy as np
from PIL import Image

def otsu(a):
    hist = np.bincount(a.ravel(), minlength=256)
    total = a.size
    sum_total = np.dot(np.arange(256), hist)
    sum_b = 0; w_b = 0; max_var=0; t=0
    for i in range(256):
        w_b += hist[i]
        if w_b==0: continue
        w_f = total - w_b
        if w_f==0: break
        sum_b += i*hist[i]
        m_b = sum_b / w_b
        m_f = (sum_total - sum_b) / w_f
        var_between = w_b*w_f*(m_b - m_f)**2
        if var_between > max_var:
            max_var = var_between
            t = i
    return (a > t).astype(np.uint8)

img = Image.open('Trabalho02/clc3.png').convert('L')
a = np.array(img)
bin_img = otsu(a)*255
Image.fromarray(bin_img).save('clc3_otsu.png')
```

Dicas
- Pré-processar com suavização reduz falsos contornos.
- Pós-processar com morfologia para limpar a segmentação.
