# Explicação — Trabalho 04: Filtros de Média e Gaussiano

Este documento explica, em detalhes, o que cada script faz, os conceitos por trás, e traz um passo a passo para executar em qualquer máquina (Windows, macOS ou Linux).

Arquivos deste trabalho:
- filtro_medio.py — Implementa e compara filtros de média 3x3, 7x7 e 15x15.
- filtro_gaussiano.py — Implementa filtro Gaussiano e analisa o impacto de sigma (σ) e do tamanho da máscara.
- ben2.png e sta2.png — Imagens de entrada usadas pelos scripts.


## Conceitos principais

- Convolução 2D: operação que aplica um “kernel” (máscara) sobre a imagem, multiplicando elemento a elemento a vizinhança do pixel e somando os resultados para formar o novo valor do pixel.
- Padding (preenchimento): bordas adicionadas (com zeros) para que o resultado da convolução tenha o mesmo tamanho da imagem original.
- Normalização do kernel: ajustar os coeficientes do kernel para que sua soma seja 1, preservando o brilho médio da imagem.


## filtro_medio.py — O que o código faz

1) Carregamento e preparação
- carregar_imagem(caminho): abre a imagem, converte para tons de cinza e retorna um array numpy em float64.
- normalizar_imagem(img): limita valores para [0,255] e converte para uint8 para visualização.
- aplicar_padding(imagem, tamanho_kernel): adiciona bordas de zeros do tamanho metade do kernel.

2) Criação do filtro de média
- criar_filtro_media(tamanho): cria uma matriz tamanho×tamanho com todos os valores iguais, depois divide todos pelo número total de elementos (tamanho*tamanho) para que a soma do kernel seja 1.
  - Ex.: 3×3 → cada célula = 1/9; 7×7 → 1/49; 15×15 → 1/225.

3) Convolução manual
- aplicar_convolucao_2d(imagem, kernel):
  - Faz o padding na imagem.
  - Para cada posição (i, j), extrai a região da imagem com o mesmo tamanho do kernel, multiplica elemento a elemento e soma (np.sum(regiao * kernel)).
  - Preenche a imagem de saída com esse valor.

4) Aplicação do filtro e comparação
- aplicar_filtro_media(imagem, tamanho): cria o kernel, aplica a convolução e normaliza o resultado.
- comparar_filtros_media: aplica 3×3, 7×7 e 15×15 e mostra lado a lado: Original, Média 3×3, 7×7 e 15×15.

5) Discussão dos resultados
- Descreve o efeito de cada tamanho de máscara em termos de suavização/borramento e perda de detalhes.

Resumo do efeito:
- Quanto maior a máscara de média, maior o borramento e menor a preservação de detalhes finos.


## filtro_gaussiano.py — O que o código faz

1) Carregamento, normalização e padding
- Mesmo fluxo do script de média.

2) Função Gaussiana 2D
- funcao_gaussiana_2d(x, y, sigma): implementa a fórmula
  G(x, y) = (1 / (2πσ²)) * exp( - (x² + y²) / (2σ²) )
- σ (sigma) controla a “largura” da Gaussiana: σ pequeno → menos borramento; σ grande → mais borramento.

3) Construção do kernel Gaussiano
- criar_filtro_gaussiano(tamanho, sigma):
  - Garante que o tamanho seja ímpar (3, 5, 7, …) para existir um centro.
  - centro = tamanho // 2.
  - Para cada posição (i, j) do kernel, calcula as coordenadas relativas ao centro:
    - x = i - centro; y = j - centro
    - Aplica a função Gaussiana com essas coordenadas relativas: filtro[i, j] = funcao_gaussiana_2d(x, y, sigma)
  - Normaliza o kernel para que a soma seja 1 (preserva brilho).

Por que x = i - centro e y = j - centro?
- A Gaussiana é centrada na origem (0, 0). Quando construímos o kernel, queremos que o maior peso esteja no centro do kernel.
- Ao subtrair o índice do centro, estamos “movendo a origem” para o meio da máscara:
  - No centro: i = centro e j = centro → x = 0 e y = 0 → G(0,0) é o valor máximo.
  - À medida que nos afastamos do centro, |x| e |y| aumentam e G(x,y) decai suavemente.
- Isso garante simetria radial e pesos coerentes com a distância ao centro, condição essencial para um desfoque Gaussiano correto.

4) Convolução e aplicação do filtro
- aplicar_convolucao_2d: mesma lógica do script de média.
- aplicar_filtro_gaussiano: cria o kernel Gaussiano, aplica a convolução e normaliza o resultado.

5) Experimentos e conclusão
- comparar_efeito_tamanho_mascara: varia o tamanho do kernel com σ fixo.
- comparar_efeito_sigma: varia σ com tamanho do kernel fixo.
- comparar_casos_extremos: compara combinações “extremas”.
- discutir_resultados_gaussiano: discute qual parâmetro afeta mais.

Conclusão (como mostrado pelo código):
- A variação de σ impacta mais o resultado do que apenas aumentar o tamanho da máscara. A máscara precisa ser grande o suficiente para “conter” a Gaussiana (regra prática: tamanho ≳ 6σ), mas o quanto a imagem é borrada é determinado principalmente por σ.


## Passo a passo para executar (Windows, macOS e Linux)

Pré-requisitos
- Python 3.8+ instalado.
- Pacotes: numpy, pillow, matplotlib.

Passos (Windows — CMD)
1) Abrir o Prompt de Comando.
2) Navegar até a pasta do repositório.
3) Criar e ativar um ambiente virtual.
4) Instalar dependências (use o arquivo requirements.txt na raiz ou instale manualmente numpy pillow matplotlib).
5) Entrar na pasta Trabalho04.
6) Executar um dos scripts:
   - python filtro_medio.py
   - python filtro_gaussiano.py

Observações importantes
- Execute os scripts dentro da pasta Trabalho04 para que os arquivos ben2.png e sta2.png sejam encontrados pelos nomes relativos.
- As janelas de gráficos (matplotlib) se abrirão com as comparações.
- Se nada aparecer, verifique se seu ambiente permite janelas gráficas (em ambientes remotos/sem display pode ser necessário salvar as figuras em arquivo ao invés de exibir na tela).

Dicas de uso
- Ajuste TAMANHOS_FILTRO e VALORES_SIGMA no topo dos scripts para testar outros valores.
- Para imagens próprias, adicione o arquivo na mesma pasta e inclua o nome na lista IMAGENS_ENTRADA.


## Solução de problemas comuns
- FileNotFoundError: verifique se está rodando a partir da pasta Trabalho04 e se os arquivos ben2.png/sta2.png existem.
- “Module not found” (numpy/pillow/matplotlib): instale as dependências no ambiente virtual ativo.
- Janela não abre: em alguns ambientes a janela do matplotlib pode ficar atrás de outras; minimize outras janelas ou use plt.savefig(...) para salvar as figuras.


## Referências rápidas
- Filtro de Média: kernel com todos os coeficientes iguais cuja soma é 1. Suaviza ruído, mas borra bordas.
- Filtro Gaussiano: pesos proporcionais a uma Gaussiana centrada; suavização mais “natural”, com controle por σ.

