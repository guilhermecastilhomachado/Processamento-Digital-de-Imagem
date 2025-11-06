# Aula 9 — Modelos de Cor

Índice
- [Objetivos](#objetivos)
- [Por que vários espaços de cor?](#por-que-vários-espaços-de-cor)
- [Principais modelos](#principais-modelos)
  - [RGB (aditivo)](#rgb-aditivo)
  - [HSV/HSI (perceptual)](#hsvhsi-perceptual)
  - [YCbCr (luminância+croma)](#ycbcr-luminânciacroma)
  - [CMYK (subtrativo)](#cmyk-subtrativo)
- [Conversões úteis](#conversões-úteis)
  - [RGB → HSV (exemplo)](#rgb--hsv-exemplo)
  - [RGB → YCbCr (exemplo simples)](#rgb--ycbcr-exemplo-simples)
- [Aplicações e dicas](#aplicações-e-dicas)

Objetivos
- Entender espaços de cor comuns, quando utilizá-los e como converter entre eles.
- Separar luminância de crominância quando desejado (ex.: segmentação por cor, compressão).

Por que vários espaços de cor?
- RGB é ótimo para exibição, mas nem sempre é conveniente para análise. Em HSV, a tonalidade (H) separa a cor do brilho; em YCbCr, Y carrega a luminância isolada.

Principais modelos

### RGB (aditivo)
- Combinação de luzes Vermelho, Verde e Azul (monitores e sensores).
- Intervalos típicos: 0–255 por canal (8 bits) ou [0,1] em ponto flutuante.
- Não separa brilho de cor (dificulta limiarização por cor com iluminação variável).

### HSV/HSI (perceptual)
- HSV: Hue (tonalidade, 0–360°), Saturation (0–1) e Value/Brightness (0–1).
- Vantagem: trabalhar em H (ou S) para segmentar cores, ignorando variações de brilho.
- Observação: conversões podem ter descontinuidades (H indefinido quando S≈0).

### YCbCr (luminância+croma)
- Y: luminância; Cb/Cr: crominâncias (azul-verde, vermelho-verde).
- Usado em vídeo/TV e compressão (JPEG/MPEG). Permite subamostragem de cromas (4:2:0) com pouco impacto visual.

### CMYK (subtrativo)
- Ciano, Magenta, Amarelo, Preto (key). Processo de impressão. Não costuma ser usado em análise direta com Python padrão.

Conversões úteis

#### RGB → HSV (exemplo)
```python
import numpy as np
from PIL import Image

img = Image.open('Trabalho03/imagem_exemplo4.jpg').convert('RGB')
arr = np.array(img).astype(np.float32) / 255.0
R,G,B = arr[...,0], arr[...,1], arr[...,2]
Cmax = np.max(arr, axis=2)
Cmin = np.min(arr, axis=2)
delta = Cmax - Cmin

# Hue (em graus)
H = np.zeros_like(Cmax)
mask = delta > 1e-6
H[mask & (Cmax==R)] = (60 * ((G - B)/delta % 6))[mask & (Cmax==R)]
H[mask & (Cmax==G)] = (60 * ((B - R)/delta + 2))[mask & (Cmax==G)]
H[mask & (Cmax==B)] = (60 * ((R - G)/delta + 4))[mask & (Cmax==B)]

# Saturation e Value
S = np.where(Cmax==0, 0, delta / Cmax)
V = Cmax

print('H range:', H.min(), H.max())
print('S,V range:', S.min(), S.max(), V.min(), V.max())
```

#### RGB → YCbCr (exemplo simples)
- Uma aproximação usada em JPEG (escala 0–255) é:
  - Y  =  0.299 R + 0.587 G + 0.114 B
  - Cb = -0.168736 R - 0.331264 G + 0.5 B + 128
  - Cr =  0.5 R - 0.418688 G - 0.081312 B + 128
```python
import numpy as np
from PIL import Image

a = np.array(Image.open('Trabalho03/imagem_exemplo2.png').convert('RGB')).astype(np.float32)
R,G,B = a[...,0], a[...,1], a[...,2]
Y  =  0.299*R + 0.587*G + 0.114*B
Cb = -0.168736*R - 0.331264*G + 0.5*B + 128
Cr =  0.5*R - 0.418688*G - 0.081312*B + 128

# Exemplos de usos: equalizar Y; threshold em H (se convertesse a HSV)
Y8  = np.clip(Y,  0, 255).astype(np.uint8)
Cb8 = np.clip(Cb, 0, 255).astype(np.uint8)
Cr8 = np.clip(Cr, 0, 255).astype(np.uint8)

Image.fromarray(Y8,  mode='L').save('aula9_Y.png')
Image.fromarray(Cb8, mode='L').save('aula9_Cb.png')
Image.fromarray(Cr8, mode='L').save('aula9_Cr.png')
```

Aplicações e dicas
- Segmentação por cor: trabalhe em HSV e limiarize H/S (ex.: frutas, semáforos).
- Realce/normalização de iluminação: processe apenas Y (em YCbCr) para equalização.
- Compressão: subamostrar Cb/Cr (4:2:0) para reduzir dados mantendo detalhes de luminância.
- Atenção a faixas: verifique se os arrays estão em [0,1] ou [0,255] antes de converter.

