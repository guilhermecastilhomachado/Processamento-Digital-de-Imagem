# README / explicacao.md — Trabalho 02: Rotulação de Componentes e Contagem de Objetos

Este documento explica detalhadamente os dois requisitos da Atividade Avaliativa 2:
1. Rotulação de Componentes Conexos (4-conectividade) — `rotulacao_comp_conexos.py`
2. Contagem de Objetos com Threshold + Rotulação — `contagem_obj_Threshold.py`

Inclui objetivos, conceitos principais, bibliotecas usadas, explicação das etapas e funções, passos de execução, observações e sugestões de extensão.

---
## 🎯 Objetivos
- Transformar imagens em binárias por thresholding manual.
- Rotular componentes conectados (objetos) usando Busca em Largura (BFS) com 4-conectividade.
- Contar, visualizar e salvar resultados (incluindo imagens rotuladas em escala de cinza e coloridas).

---
## 📁 Arquivos
- `rotulacao_comp_conexos.py`: Implementa rotulação completa da imagem `art8.png`, gerando `art8lab1.png` e `art8lab2.png`.
- `contagem_obj_Threshold.py`: Aplica threshold específico na imagem `clc3.png`, salva binarizada (`clc3thr1.png`) e conta componentes.
- Imagens auxiliares: `art8.png`, `clc3.png`.

---
## 🧪 Conceitos Principais
### Thresholding
- Processo de converter imagem escala de cinza em binária (0 = fundo, 1 = objeto).
- Critério: comparar intensidade do pixel com um valor limite (threshold).
- Diferentes regras possíveis: `pixel <= T` como objeto ou `pixel > T` como objeto — definido pela atividade.

### Componentes Conexos
- Conjunto de pixels de objeto conectados entre si.
- 4-conectividade: vizinhos em cima, baixo, esquerda e direita (não inclui diagonais).
- Rotulação atribui identificadores inteiros a cada componente (1, 2, 3...).

### BFS (Busca em Largura)
- Estrutura de fila (queue) para explorar vizinhos gradualmente.
- Evita recursão profunda e stack overflow em imagens grandes.

### Visualização
- Conversão de rótulos para cores facilita distinção entre objetos próximos.
- Normalização para 0–1 antes de aplicar colormap.

---
## 📦 Bibliotecas Utilizadas
- `numpy`: manipulação de arrays, operações lógicas e contagem.
- `PIL.Image`: carregamento e salvamento de imagens (escala de cinza / RGB).
- `matplotlib.pyplot`: visualizações lado a lado e colormap.
- `collections.deque`: fila eficiente para BFS.
- `os`: verificação de existência de arquivos antes de salvar (evita sobrescrita).

---
## 🔍 Detalhamento — rotulacao_comp_conexos.py
### Fluxo
1. Carregar imagem `art8.png` e converter para escala de cinza.
2. Aplicar binarização (`imagem_binaria = np.where(imagem_array > THRESHOLD, 1, 0)`).
3. Percorrer todos os pixels:
   - Para cada pixel de objeto não rotulado, iniciar BFS e rotular componente inteiro.
4. Calcular estatísticas: quantidade, tamanho maior, menor e média dos componentes.
5. Visualizar: original, binária, rotulada (colormap).
6. Salvar resultados em dois formatos:
   - Escala de cinza (`art8lab1.png`): rótulos mapeados para intervalo 0–255.
   - Colorida (`art8lab2.png`): rótulos mapeados via colormap `nipy_spectral`.

### Principais Funções
- `carregar_e_preprocessar_imagem()`: lê e binariza.
- `rotular_componente_bfs(...)`: BFS rotula um componente — usa fila e vizinhos.
- `executar_rotulacao_completa(...)`: varre toda a imagem e chama BFS para cada novo componente.
- `criar_visualizacao_comparativa(...)`: gera 3 subplots (original, binária, rotulada).
- `salvar_resultados(...)`: normaliza rótulos e salva imagens de saída.
- `main()`: orquestra execução.

### Observações
- Threshold definido para evidenciar objetos na imagem de teste.
- Uso de colormap para melhorar interpretação visual.

---
## 🔍 Detalhamento — contagem_obj_Threshold.py
### Fluxo
1. Carregar imagem `clc3.png`.
2. Binarizar com regra específica da atividade: `pixel <= THRESHOLD → 1`, senão 0.
3. Salvar imagem binária (`clc3thr1.png`).
4. Rotular componentes com BFS (4-conectividade).
5. Exibir estatísticas e visualizações: original, binária, rotulada.
6. Retornar número total de objetos.

### Principais Funções
- `carregar_imagem_original()`: leitura e estatísticas iniciais.
- `aplicar_threshold(...)`: aplica regra de binarização e relata distribuição (pixels objeto vs fundo).
- `salvar_imagem_binaria(...)`: salva arquivo binário como imagem 8 bits (0/255).
- `rotular_componente_bfs(...)`: igual lógica do outro script.
- `encontrar_todos_componentes(...)`: percorre toda a imagem e rotula componentes.
- `mostrar_resultados_visuais(...)`: exibe as três visões (inclui normalização para cores).
- `main()`: executa pipeline completo.

### Diferenças em Relação ao Outro Script
- Regra de threshold invertida: aqui objeto = `pixel <= T` (conforme especificado).
- Salva somente versão binária simples (não gera versão colorida com colormap).

---
## 🧮 Fórmulas e Lógicas Essenciais
- Binarização genérica: `imagem_binaria = np.where(imagem_array > T, 1, 0)` (ou variante <= conforme regra).
- Vizinhos 4-conectados: `[(-1,0),(1,0),(0,-1),(0,1)]`.
- Normalização de rótulos para 8 bits: `(matriz_rotulos * 255 // numero_componentes)`.
- Percentual de pixels objeto: `(pixels_objeto / total_pixels) * 100`.

---
## 🚀 Passo a Passo de Execução
Pré-requisitos:
- Python 3.8+ instalado.
- Dependências: `numpy`, `pillow`, `matplotlib`.

### Windows (CMD)
```cmd
cd "C:\Users\SEU_USUARIO\OneDrive\Área de Trabalho\Processamento Digital de Imagem"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt   (ou: pip install numpy pillow matplotlib)
cd Trabalho02
python rotulacao_comp_conexos.py
python contagem_obj_Threshold.py
```

### Linux / macOS
```bash
cd /caminho/para/Processamento\ Digital\ de\ Imagem
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd Trabalho02
python3 rotulacao_comp_conexos.py
python3 contagem_obj_Threshold.py
```

### Dicas
- Rode dentro da pasta `Trabalho02` para garantir que as imagens sejam encontradas.
- Se quiser salvar figuras ao invés de exibir: substituir `plt.show()` por `plt.savefig("nome.png")`.
- Ajuste `THRESHOLD_BINARIZACAO` ou `THRESHOLD` para observar impacto da binarização.

---
## 🔧 Personalizações Sugestivas
- Adicionar 8-conectividade: incluir diagonais como vizinhos para comparar resultados.
- Filtro de pré-processamento: aplicar suavização antes do threshold para reduzir ruído.
- Métricas de componente: calcular circularidade ou bounding boxes.
- Exportar para CSV: salvar estatísticas de tamanho dos componentes.

---
## ⚠️ Observações Importantes
- Threshold mal escolhido pode unir objetos distintos ou fragmentar um único objeto.
- 4-conectividade ignora diagonais — pode gerar mais componentes que 8-conectividade.
- Rotulação é sensível a ruídos isolados (pixels únicos viram componentes de 1 pixel).
- Use visualização colorida para validar se a segmentação faz sentido para a aplicação.

---
## 🧪 Testes Recomendados
- Contar componentes com diferentes limiares e comparar estabilidade do resultado.
- Implementar versão com 8-conectividade e comparar número de componentes.
- Medir tempo de execução para imagens maiores (otimizar BFS se necessário).

---
## ✅ Resumo Comparativo
| Aspecto                | Rotulação (art8)                          | Contagem (clc3)                             |
|------------------------|-------------------------------------------|---------------------------------------------|
| Regra de threshold     | pixel > T → objeto                        | pixel ≤ T → objeto                          |
| Saídas geradas         | Imagem binária + 2 rotuladas (cinza/cor)  | Imagem binária + contagem                   |
| Estatísticas           | Total, maior, menor, média                | Total                                       |
| Visualizações          | 3 subplots + colormap                     | 3 subplots (sem colormap avançado)          |
| Conectividade          | 4                                        | 4                                           |

---
## 📌 Próximos Passos Sugeridos
- Implementar rotulação recursiva e comparar desempenho vs BFS.
- Adicionar remoção de componentes pequenos (ruído) por tamanho mínimo.
- Integrar cálculo de área e perímetro para cada rótulo.
- Criar módulo utilitário reutilizável para rotulação entre atividades.

---
_Fim do documento — Trabalho 02._

