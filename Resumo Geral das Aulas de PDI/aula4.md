# Aula 4 — Histogramas e Processamento Baseado em Histograma

Índice
- [Objetivos](#objetivos)
- [Conceitos](#conceitos)
- [Exemplo: equalização manual](#exemplo-equalização-manual)
- [Cuidados](#cuidados)

Objetivos
- Compreender histogramas, CDF e técnicas de realce como equalização.

Conceitos
- Histograma: contagem de pixels por intensidade (0–255).
- PDF e CDF: probabilidade por nível e soma acumulada.
- Equalização: mapeia intensidades para expandir contraste global.
- Especificação (matching): força uma distribuição alvo.

Exemplo: equalização manual
```python
import numpy as np
from PIL import Image

def equalize(a):
    L=256
    hist = np.bincount(a.ravel(), minlength=L)
    cdf = np.cumsum(hist) / a.size
    sk = np.rint((L-1)*cdf).astype(np.uint8)
    return sk[a]

img = Image.open('Trabalho03/imagem_exemplo6.png').convert('L')
a = np.array(img)
eq = equalize(a)
Image.fromarray(eq).save('eq.png')
```

Cuidados
- Pode superrealçar ruído em faixas estreitas.
- Em imagens coloridas, equalize por canal com cautela (melhor: equalização no espaço HSV/V).
