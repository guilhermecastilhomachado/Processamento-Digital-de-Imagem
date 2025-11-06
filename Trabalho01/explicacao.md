# README / explicacao.md — Trabalho 01: Reamostragem (DPI) e Quantização

Este documento descreve detalhadamente os dois requisitos da Atividade Avaliativa 1:
1. Reamostragem de pixels (redução de DPI) — arquivo `reamostragem.py`
2. Quantização de níveis de cinza (redução de bits) — arquivo `quantizacao.py`

Inclui objetivos, conceitos principais, bibliotecas usadas, explicação das funções, passo a passo para executar em qualquer máquina (Windows, Linux, macOS) e observações práticas.

---
## 🎯 Objetivos Gerais
- Demonstrar o efeito da REDUÇÃO DA RESOLUÇÃO ESPACIAL (DPI) sobre os detalhes da imagem.
- Demonstrar o efeito da REDUÇÃO DA RESOLUÇÃO DE INTENSIDADE (bits) sobre suavidade e posterização.

---
## 📁 Estrutura dos Scripts
- `reamostragem.py`: Implementa reamostragem manual (Nearest Neighbor) de uma imagem de alta resolução simulada (`relogio.tif`).
- `quantizacao.py`: Implementa quantização manual da imagem (`ctskull-256.tif`) para vários números de bits (7 → 1).
- Imagens auxiliares: `relogio.tif`, `ctskull-256.tif` (ou imagens sintéticas geradas se ausentes).

---
## 🧪 Conceitos Principais
### Reamostragem (DPI)
- DPI (Dots Per Inch): número de pixels por polegada; mede resolução espacial.
- Reduzir DPI = diminuir número TOTAL de pixels (informação espacial). Não muda intensidade dos pixels preservados.
- Fator de escala: `escala = DPI_novo / DPI_original`.
- Nova dimensão: `dim_nova = dim_original * escala`.
- Nearest Neighbor: pixel na nova imagem recebe valor do pixel mais próximo na original (pode gerar blocos).

### Quantização (Bits por Pixel)
- Bits por pixel definem quantos níveis de cinza: `L = 2^k`.
- Reduzir bits = agrupar intervalos de intensidades em menos categorias.
- Posterização: faixas artificiais onde transições suaves viram degraus visíveis.
- Trade-off: menos bits = menor armazenamento, porém menos fidelidade visual.

---
## 📦 Bibliotecas Utilizadas
Ambos os scripts usam:
- `numpy`: criação e manipulação de arrays; operações matemáticas.
- `PIL.Image` (Pillow): carregamento e salvamento de imagens (conversão para escala de cinza).
- `matplotlib.pyplot`: visualização (figuras comparativas, histogramas, zoom).
- `numpy.random` (implícito): geração de ruído em imagens sintéticas.
- `os` (apenas se expandir salvamento condicional — não obrigatório atualmente).

Obs: Nenhuma função pronta de reamostragem ou quantização automática é usada; tudo é feito manualmente.

---
## 🔍 Explicação Detalhada — Requisito 1 (Reamostragem)
Arquivo: `reamostragem.py`

### Fluxo Geral
1. Carrega ou gera imagem de entrada (alta resolução simulada: 1250 DPI).
2. Calcula novas dimensões para cada DPI alvo (300, 150, 72).
3. Reamostra usando Nearest Neighbor.
4. Exibe comparações visuais (original e reamostradas + zoom central).
5. Analisa redução de pixels e perda de detalhes.

### Principais Funções
- `carregar_imagem(caminho)`: abre imagem e converte para escala de cinza; se não existir, chama `criar_imagem_sintetica()`.
- `criar_imagem_sintetica()`: desenha relógio (círculo, ponteiros, marcações) para simular cena rica em detalhes.
- `calcular_dimensoes_reamostragem(dimensao_original, dpi_original, dpi_novo)`: aplica fórmula do fator de escala e mostra cálculo.
- `reamostrar_imagem_nearest_neighbor(imagem, nova_altura, nova_largura)`: percorre cada pixel novo, mapeia coordenada proporcional na original, arredonda e copia valor.
- `aplicar_reamostragem_dpi(imagem_original, dpi_novo)`: integra cálculo das dimensões + reamostragem + estatísticas.
- `visualizar_resultados(...)`: mostra original + versões reamostradas com dimensões e porcentagem de redução.
- `visualizar_zoom_comparacao(...)`: recorta região central para destacar perda de detalhes finos.
- `analisar_resultados()`: imprime análise qualitativa (qualidade mantida vs degradada conforme DPI).
- `main()`: orquestra execução dos passos.

### Por que Nearest Neighbor?
- Simples de implementar manualmente.
- Evidencia claramente blocagem e perda de detalhes em resoluções menores.

### Observações da Saída
- 300 DPI: maioria dos detalhes ainda visível.
- 150 DPI: detalhes finos começam a desaparecer.
- 72 DPI: adequada para tela/web, mas muita perda de nitidez e formas suaves.

---
## 🔍 Explicação Detalhada — Requisito 2 (Quantização)
Arquivo: `quantizacao.py`

### Fluxo Geral
1. Carrega imagem (TC craniana) ou gera sintética (se ausente).
2. Para cada valor de bits alvo (7→1):
   - Calcula número de níveis (`2^bits`).
   - Aplica agrupamento de intensidades via passo.
   - Registra estatísticas e progresso.
3. Gera visualizações: imagens quantizadas, histogramas, zoom local.
4. Analisa efeitos (posterização, perda de transições suaves).

### Principais Funções
- `carregar_imagem(caminho)`: lê imagem e mostra parâmetros (dimensões, bits originais).
- `criar_imagem_sintetica()`: gera cena simulada de tomografia com estruturas diferenciadas para evidenciar efeitos da quantização.
- `calcular_niveis_quantizacao(bits)`: retorna `2^bits` e imprime fórmula.
- `quantizar_imagem(imagem, bits_alvo)`: algoritmo manual pixel a pixel:
  - Passo = 256 / L (L = 2^bits).
  - Grupo = valor_original / passo.
  - Novo valor = grupo * passo (limitado a 255).
- `aplicar_quantizacao_detalhada(imagem, bits_alvo)`: exemplifica num processo com pixel central antes de chamar `quantizar_imagem`.
- Visualizações:
  - `visualizar_resultados(...)`: original + 7 quantizações lado a lado.
  - `visualizar_histogramas(...)`: histogramas com o número de bins igual aos níveis.
  - `visualizar_zoom_comparacao(...)`: recorte central ampliado para evidenciar degraus.
- `analisar_resultados(...)`: compara níveis teóricos e valores únicos reais; descreve degradacão conforme bits.

### Diferença em Relação a Versões com OpenCV
- Aqui NÃO se usa `cv2.resize` nem `cv2.convertScaleAbs`; manipulação é totalmente manual.
- Explicação anterior (`explicacao2.md`) referia-se a versão baseada em OpenCV; esta documentação corresponde ao código ATUAL (`quantizacao.py`).

### Observações da Saída
- ≥6 bits: efeito quase imperceptível ao olho humano.
- 4–5 bits: leve posterização em áreas suaves.
- ≤3 bits: contornos artificiais e forte perda de gradientes.
- 1 bit: imagem binária (apenas preto e branco) — contexto específico (fax/documentos).

---
## 🧮 Fórmulas Importantes
- Níveis por bits: `L = 2^k`.
- Passo de quantização (imagem original 8 bits): `passo = 256 / L`.
- Mapeamento aproximado do grupo: `valor_quantizado = floor(valor_original / passo) * passo`.
- Escala DPI: `nova_dim = dim_original * (DPI_novo / DPI_original)`.

---
## 🚀 Passo a Passo de Execução
Pré-requisitos:
- Python 3.8 ou superior instalado.
- Pacotes: `numpy`, `pillow`, `matplotlib` (instalar via `pip`).

### Windows (CMD)
```cmd
cd "C:\Users\SEU_USUARIO\OneDrive\Área de Trabalho\Processamento Digital de Imagem"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt  (ou: pip install numpy pillow matplotlib)
cd Trabalho01
python reamostragem.py
python quantizacao.py
```

### Linux / macOS (Terminal)
```bash
cd /caminho/para/Processamento\ Digital\ de\ Imagem
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # ou libs separadas
cd Trabalho01
python3 reamostragem.py
python3 quantizacao.py
```

### Dicas
- Execute dentro da pasta `Trabalho01` para garantir que nomes relativos de imagens sejam encontrados.
- Se a imagem não existir, o script gera versão sintética (informado no console).
- Para salvar figuras ao invés de exibir, substituir `plt.show()` por `plt.savefig("nome.png")` dentro das funções de visualização.

---
## 🔧 Personalizações
- Ajustar listas: `DPI_ALVOS` ou `BITS_ALVOS` para testar outros cenários.
- Substituir imagens: colocar arquivos na pasta e alterar `IMAGEM_ENTRADA`.
- Otimização de desempenho: substituir laços pixel a pixel por operações vetorizadas (exercício futuro).

---
## ⚠️ Observações e Boas Práticas
- Reamostragem Redutora é IRREVERSÍVEL — mantenha a original.
- Quantização agressiva elimina nuances usadas em diagnóstico (ex: exames médicos não devem ser convertidos para poucos bits).
- O olho humano distingue ~100–200 tons: 8 bits é confortável; abaixo de 5 bits começa a deteriorar.
- Sempre valide visualmente os efeitos antes de aplicar em produção.

---
## 🧪 Testes Recomendados
- Compare zoom de regiões com textura fina (sulcos, bordas) em diferentes DPIs.
- Verifique histogramas das imagens quantizadas para confirmar redução de níveis.
- Calcule diferença absoluta média entre imagem original e quantizada para cada `bits` (pode ser adicionada como exercício extra).

---
## ✅ Resumo Final
| Aspecto            | Reamostragem (DPI)                   | Quantização (Bits)                 |
|--------------------|--------------------------------------|------------------------------------|
| Informação perdida | Espaço (detalhes geométricos)        | Intensidade (tons de cinza)        |
| Reversibilidade    | Não                                  | Não                                |
| Artefato típico    | Blocagem / pixelização               | Posterização / bandas              |
| Parâmetro chave    | Fator de escala (DPI_novo / DPI_orig)| Bits alvo (k)                      |
| Uso comum          | Ajuste para exibição / impressão     | Compressão / redução de ruído seletiva |

---
## 📌 Próximos Passos Sugeridos
- Implementar interpolação bilinear para comparar com Nearest Neighbor.
- Vetorizar quantização usando operações NumPy para ganho de desempenho.
- Adicionar métricas objetivas (MSE, PSNR) às análises.

---
_Fim do documento — Trabalho 01._
