
# Explicação do Código - Equalização de Histograma (Questão 1)

Este arquivo `.md` documenta passo a passo o funcionamento do código da **Questão 1** da atividade avaliativa 3, 
que realiza a equalização de histograma **manualmente**, sem utilizar funções prontas de bibliotecas como OpenCV.

---

## 🎯 Objetivo

- Ler uma imagem em escala de cinza.
- Calcular o histograma da imagem original.
- Calcular a função de distribuição acumulada (CDF).
- Gerar uma nova imagem equalizada com base na CDF.
- Salvar a imagem equalizada.
- (Opcional) Exibir histogramas antes e depois da equalização.

---

## 📦 Bibliotecas Utilizadas

- `os`: manipulação de arquivos e diretórios.
- `numpy`: manipulação de arrays e operações matemáticas.
- `PIL.Image`: carregamento e salvamento de imagens.
- `matplotlib.pyplot`: visualização de histogramas (opcional).

---

## 🔍 Etapas do Código

### 1. Carregar a imagem e converter para escala de cinza

```python
imagem = Image.open('nome_da_imagem.png').convert('L')
imagem_array = np.array(imagem)
```

- Converte a imagem para escala de cinza.
- Transforma a imagem em um array NumPy para facilitar os cálculos.

---

### 2. Calcular o histograma manualmente

```python
histograma = np.zeros(256, dtype=int)
for i in range(imagem_array.shape[0]):
    for j in range(imagem_array.shape[1]):
        intensidade = imagem_array[i, j]
        histograma[intensidade] += 1
```

- Contabiliza quantos pixels possuem cada nível de cinza (0 a 255).

---

### 3. Calcular a função de distribuição acumulada (CDF)

```python
cdf = np.cumsum(histograma)
cdf_min = cdf[np.nonzero(cdf)].min()
```
- A `cdf` indica quantos pixels têm valor menor ou igual a um certo nível.
- A `cdf_min` é usada para normalizar e evitar valores muito baixos.

---

### 4. Normalizar a CDF para obter os novos tons

```python
cdf_normalizada = ((cdf - cdf_min) / (cdf[-1] - cdf_min)) * 255
cdf_normalizada = cdf_normalizada.astype(np.uint8)
```

- Transforma a CDF em uma escala de 0 a 255 (níveis de cinza).

---

### 5. Aplicar a equalização

```python
imagem_equalizada = cdf_normalizada[imagem_array]
```

- Cada pixel da imagem original é substituído por seu valor mapeado na `cdf_normalizada`.

---

### 6. Salvar a imagem equalizada

```python
nome_arquivo = 'imagem_equalizada3.png'
if os.path.exists(nome_arquivo): # Verifica se o arquivo já existe
    print(f"A imagem '{nome_arquivo}' já existe. Nenhuma nova imagem foi salva.")
else:
    imagem_equalizada.save(nome_arquivo) # Salva a imagem equalizada
    print(f"A imagem equalizada foi salva como '{nome_arquivo}'.")
```

---

## ✅ Resultado

- Uma nova imagem com contraste melhorado é gerada.
- O histograma final tende a ser mais "espalhado", cobrindo mais níveis de cinza.

---

## 📌 Observações

- Nenhuma função de equalização pronta é usada (como `cv2.equalizeHist()`).
- Todo o processo é implementado manualmente conforme solicitado na atividade.

---

## 🧪 Recomendações de Teste

- Utilize imagens com contraste fraco (ex: "imagem antiga", "imagem com névoa", etc).
- Teste com imagens diferentes e observe como o histograma muda.

---

## 👨‍🏫 Finalidade Didática

Esse exercício ajuda a compreender:
- A importância do histograma.
- Como o contraste pode ser ajustado.
- O funcionamento da transformação de intensidades.

---

_Fim do documento._
