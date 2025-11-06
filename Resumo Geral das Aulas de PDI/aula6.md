# Aula 6 — Filtragem Espacial: Realce (Derivadas, Laplaciano, Unsharp)

Objetivos
- Realçar detalhes e bordas usando operadores de primeira e segunda ordem.

Conceitos
- Gradiente (Sobel/Prewitt): magnitude indica força da borda; direção indica orientação.
- Laplaciano: segunda derivada, isotrópico; sensível a ruído.
- Unsharp/High-boost: realce por realimentação de alta frequência.

Exemplo: magnitude do Sobel
```python
import numpy as np
from PIL import Image

def sobel(a):
    kx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    ky = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
    def conv(a,k):
        H,W=a.shape; p=k.shape[0]//2; ap=np.pad(a,p,mode='edge'); out=np.zeros_like(a,float)
        for i in range(H):
            for j in range(W):
                out[i,j]=np.sum(ap[i:i+2*p+1,j:j+2*p+1]*k)
        return out
    gx, gy = conv(a,kx), conv(a,ky)
    mag = np.hypot(gx, gy)
    return np.clip(mag,0,255).astype(np.uint8)

img = Image.open('Trabalho05/cln1.gif').convert('L')
a = np.array(img)
Image.fromarray(sobel(a)).save('sobel_mag.png')
```

Cuidados
- Aplique suavização leve antes de derivadas para reduzir ruído.

