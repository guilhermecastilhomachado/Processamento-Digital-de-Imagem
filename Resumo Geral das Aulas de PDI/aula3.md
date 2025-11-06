# Aula 3 — Conectividade, Componentes e Rotulagem

Objetivos
- Definir conectividade 4 e 8, componentes conexos e como rotular objetos binários.

Conceitos
- Imagem binária: 1 = objeto, 0 = fundo.
- Vizinhos 4-conectados: N, S, W, E. Vizinhos 8-conectados: inclui diagonais.
- Componente conexo: conjunto de pixels 1 conectados sob a regra escolhida.

Algoritmos de rotulagem
- BFS/DFS: percorre os pixels marcando um rótulo até esgotar o componente.
- Duas passagens (algoritmo clássico): resolve equivalências de rótulos.

Exemplo (BFS 4-conectado)
```python
import numpy as np
from collections import deque

def rotular_bfs(bin_img):
    H,W = bin_img.shape
    labels = np.zeros((H,W), dtype=np.int32)
    label = 0
    neigh = [(-1,0),(1,0),(0,-1),(0,1)]
    for i in range(H):
        for j in range(W):
            if bin_img[i,j]==1 and labels[i,j]==0:
                label += 1
                q = deque([(i,j)])
                labels[i,j] = label
                while q:
                    y,x = q.popleft()
                    for dy,dx in neigh:
                        yy,xx = y+dy, x+dx
                        if 0<=yy<H and 0<=xx<W and bin_img[yy,xx]==1 and labels[yy,xx]==0:
                            labels[yy,xx] = label
                            q.append((yy,xx))
    return labels, label
```

Aplicações
- Contagem de objetos, medição de área/perímetro, filtragem por tamanho, segmentação.

Dicas
- Escolha a conectividade adequada ao problema (evitar “pontes” por diagonal indesejadas).
- Pré-filtragem pode reduzir ruído (remoção de pequenos componentes).

