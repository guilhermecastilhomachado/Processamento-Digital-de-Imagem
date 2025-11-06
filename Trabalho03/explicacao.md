# README / explicacao.md — Trabalho 03: Histograma e Equalização Manual

Este documento explica o(s) script(s) da Atividade Avaliativa 3 para cálculo de histograma e equalização manual de histograma, cobrindo objetivos, bibliotecas, conceitos, etapas do código e como executar em qualquer máquina.

Arquivos deste trabalho:
- `histograma.py` — implementa equalização manual e permite aplicar o processo múltiplas vezes, com visualização comparativa.
- Imagens de exemplo: `imagem_exemplo1.jpg`, `imagem_exemplo2.png`, ..., `imagem_exemplo6.png` (uma delas é usada por padrão).
- Saídas geradas (exemplos): `imagem_equalizada.png`, `imagem_equalizada2.png`, etc.

---
## 🎯 Objetivos
- Calcular manualmente o histograma (frequência de intensidades) de uma imagem em tons de cinza.
- Calcular a função de distribuição acumulada (CDF) e construir o mapeamento de equalização.
- Aplicar a equalização (uma ou mais vezes) e comparar efeitos nos histogramas e na imagem.

---
## 📦 Bibliotecas Utilizadas
- `numpy`: manipulação de arrays e contagens; operações matemáticas.
- `PIL.Image`: carregamento de imagens e conversão para escala de cinza.
- `matplotlib.pyplot`: geração de gráficos (imagens e histogramas lado a lado).

---
## 🧠 Conceitos Principais
- Histograma: distribuição de frequências dos níveis de cinza (0 a 255).
- Probabilidade por nível: `p_r(r_k) = n_k / (M*N)`, onde `n_k` é a contagem de pixels com nível k.
- CDF (distribuição acumulada): soma cumulativa das probabilidades até o nível k.
- Equalização de histograma: novo nível `s_k = round((L-1) * CDF(r_k))`, espalhando intensidades para melhorar contraste global.
- Aplicações múltiplas: reaplicar equalização pode gerar resultados que tendem a estabilizar (nem sempre melhora após a primeira vez).

---
## 🔍 Explicação do Código (`histograma.py`)

### 1) Função `equalizar_histograma(imagem_np, L=256)`
- Garante que a entrada seja 2D (tons de cinza).
- Calcula `nk` (frequência por nível) percorrendo os pixels.
- Converte em probabilidades `pr_rk = nk / total_pixels`.
- Calcula CDF acumulando `pr_rk`.
- Gera o mapeamento `sk = round((L-1) * CDF)` para cada nível 0..L-1.
- Retorna a lista `sk` com o novo valor para cada nível original.

### 2) Função `aplicar_mapeamento(imagem_np, mapa_sk)`
- Cria cópia da imagem e, para cada nível `rk`, substitui por `mapa_sk[rk]`.
- Retorna a imagem com as intensidades re-mapeadas (equalizada).

### 3) Função `calcular_histograma_simples(imagem_np, L=256)`
- Percorre a imagem somando frequências por nível.
- Retorna vetor com 256 contadores (para L=256).

### 4) Bloco principal (`if __name__ == '__main__':`)
- Define imagem padrão `caminho_imagem = 'imagem_exemplo6.png'`, número de passagens `num_passes = 2` e L=256.
- Carrega a imagem, armazena imagem original e histograma.
- Aplica equalização N vezes:
  - Calcula mapeamento via `equalizar_histograma`.
  - Aplica mapeamento em `aplicar_mapeamento`.
  - Salva em listas para visualização cumulativa.
- Visualiza comparações em subplot com duas colunas: imagem e histograma para cada passo (0 = original; i = após i-ésima equalização).

---
## ✅ Resultados Esperados
- A primeira equalização tende a melhorar contraste em imagens com histograma concentrado.
- Histograma resultante aproxima-se de uma distribuição mais uniforme (nem sempre perfeitamente homogênea).
- Aplicar uma segunda vez pode ter efeito sutil; nem sempre melhora — documente observações ao testar.

---
## 🚀 Passo a Passo de Execução
Pré-requisitos:
- Python 3.8+ instalado.
- Pacotes: `numpy`, `pillow`, `matplotlib`.

### Windows (CMD)
```cmd
cd "C:\Users\SEU_USUARIO\OneDrive\Área de Trabalho\Processamento Digital de Imagem"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt   (ou: pip install numpy pillow matplotlib)
cd Trabalho03
python histograma.py
```

### Linux / macOS
```bash
cd /caminho/para/Processamento\ Digital\ de\ Imagem
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd Trabalho03
python3 histograma.py
```

### Dicas
- Para usar outra imagem, ajuste `caminho_imagem` no topo do script.
- Ajuste `num_passes` para testar equalização repetida (ex.: 1, 2, 3).
- Se preferir salvar figuras: dentro do script, troque `plt.show()` por `plt.savefig('saida.png')`.

---
## 🧪 Testes Recomendados
- Use imagens de baixo contraste (neblina, iluminação ruim).
- Compare histograma antes/depois e observe se há ganho perceptível de contraste.
- Aplique equalização repetida e avalie quando deixa de trazer benefício.

---
## ⚠️ Observações
- Implementação é manual, sem `cv2.equalizeHist()`.
- Trabalha apenas com tons de cinza (2D). Para RGB, equalize por canal com cuidado.
- Equalização pode aumentar ruído em áreas escuras ou claras; avalie caso a caso.

---
_Fim do documento — Trabalho 03._
