# Explicação — Trabalho 05: Filtros de Realce (Sobel, Laplaciano, Unsharp Masking, Highboost)

Este documento explica detalhadamente o funcionamento do script `filtros_de_realce.py`, os conceitos teóricos e fornece um guia passo a passo para execução em qualquer máquina.

Arquivo principal:
- filtros_de_realce.py — Implementa diversos filtros de realce reutilizando a convolução manual da atividade anterior.
Imagem de entrada:
- cln1.gif — usada como base para aplicar os filtros. Se não estiver presente, o código gera uma imagem sintética.

## Conceitos gerais
- Realce: aumentar a percepção de detalhes, bordas ou contraste local sem alterar demais a estrutura global.
- Derivadas em imagens: diferenças entre intensidades vizinhas destacam transições (bordas).
- Convolução: operação aplicada com um kernel que extrai, combina ou realça padrões locais.

## Estrutura do código
1) Carregamento de imagem (ou geração sintética):
   - carregar_imagem(): abre a imagem e converte para tons de cinza; se não encontrada, chama criar_imagem_sintetica().
   - criar_imagem_sintetica(): gera uma imagem com formas simples (quadrado, círculo, gradiente) e ruído — útil para testar filtros.

2) Funções utilitárias:
   - normalizar_imagem(): assegura que os valores finais fiquem em [0,255] e converte para uint8.
   - aplicar_padding(): adiciona zeros nas bordas para permitir convolução sem reduzir tamanho.
   - aplicar_convolucao_2d(): implementação manual da convolução reaproveitada da atividade anterior.

3) Filtro de Sobel:
   - criar_filtros_sobel(): define as máscaras 3x3 para derivada em X (bordas verticais) e Y (bordas horizontais).
   - aplicar_filtro_sobel(imagem): aplica as duas máscaras e calcula a magnitude do gradiente: sqrt(Gx² + Gy²).
   - Resultado: três imagens — derivada X, derivada Y e magnitude (bordas completas).

   Conceito: O Sobel aproxima derivadas de primeira ordem, enfatizando transições suaves e reduzindo ruído via pesos [-1 -2 -1].

4) Filtro Laplaciano:
   - criar_filtro_laplaciano(): cria a máscara [[0,1,0],[1,-4,1],[0,1,0]]. É a derivada de segunda ordem (∇²f).
   - aplicar_filtro_laplaciano(imagem): aplica a máscara e depois soma o resultado à imagem original com fator c = -1 (porque o centro é negativo), reconstruindo o fundo e realçando bordas.

   Conceito: A segunda derivada destaca pontos onde há mudança brusca de intensidade (bordas) em todas as direções (isotrópico). Porém, amplifica ruído.

5) Unsharp Masking:
   - criar_filtro_gaussiano_simples(): cria um kernel Gaussiano aproximado 5x5 (mais eficiente que gerar via fórmula exata para este contexto).
   - aplicar_unsharp_masking(imagem, k):
     Passos:
       1. Suaviza a imagem: s(x,y)
       2. Calcula máscara: g_mask = f - s
       3. Realça: g = f + k * g_mask
     Quando k = 1 → unsharp clássico.

   Conceito: Remove detalhes suaves para isolar alta frequência (bordas) e reintroduz esses detalhes multiplicados por k.

6) Highboost Filtering:
   - aplicar_highboost_filtering(imagem, k): igual ao unsharp, mas com k > 1 (ex.: k = 2.0) para realce mais forte.

   Conceito: Intensifica ainda mais o componente de alta frequência, deixando bordas mais marcadas.

7) Efeito atenuado (k < 1):
   - aplicar_efeito_atenuado(imagem, k): variante do unsharp com k < 1. Realce muito sutil, preservando características naturais.

8) Visualização:
   - visualizar_resultados_sobel(): mostra original, derivada X, derivada Y e magnitude.
   - visualizar_resultados_realce(): mostra original e os quatro métodos: Laplaciano, Unsharp (k=1), Highboost (k=2), Atenuado (k=0.5).

9) Discussão dos resultados:
   - discutir_resultados(): imprime comparação qualitativa entre métodos, incluindo intensidade de realce, amplificação de ruído e recomendações de uso.

## Comparação resumida dos filtros
- Sobel: Bom equilíbrio entre detecção de bordas e resistência ao ruído; fornece direção das bordas.
- Laplaciano: Realce agressivo, detecta bordas em todas as direções, mas amplifica ruído fortemente.
- Unsharp Masking (k=1): Realce natural, preserva tons médios, adequado para fotografia e pós-processamento.
- Highboost (k>1): Realce mais intenso; útil quando a imagem está “lavada” ou perderá nitidez na impressão.
- k < 1 (Atenuado): Realce mínimo; indicado para imagens sensíveis (ex.: médicas) onde artefatos são indesejados.

## Passo a passo para executar (Windows, macOS e Linux)

Pré-requisitos:
- Python 3.8+ instalado.
- Pacotes: numpy, pillow, matplotlib.

Passos em Windows (CMD):
1) Abrir o Prompt de Comando.
2) Navegar até a pasta raiz do projeto:
   cd "C:\Users\SEU_USUARIO\OneDrive\Área de Trabalho\Processamento Digital de Imagem"
3) Criar ambiente virtual:
   python -m venv venv
4) Ativar ambiente:
   venv\Scripts\activate
5) Instalar dependências:
   pip install numpy pillow matplotlib
6) Entrar na pasta Trabalho05:
   cd Trabalho05
7) Executar o script:
   python filtros_de_realce.py

Passos em Linux/macOS (Terminal):
1) cd /caminho/para/Processamento\ Digital\ de\ Imagem
2) python3 -m venv venv
3) source venv/bin/activate
4) pip install numpy pillow matplotlib
5) cd Trabalho05
6) python filtros_de_realce.py

Observações:
- Se `cln1.gif` não estiver na pasta, o script cria uma imagem sintética automaticamente.
- As janelas de gráfico abrirão mostrando os resultados; feche-as para prosseguir.
- Para salvar em arquivos ao invés de exibir, você pode substituir plt.show() por plt.savefig("nome.png") nos métodos de visualização.

## Personalizações
- Alterar IMAGEM_ENTRADA para qualquer outra imagem em escala de cinza (ou será convertida).
- Ajustar valores de k em highboost ou unsharp para controlar intensidade (ex.: k=3 para realce mais forte; k=0.3 para efeito quase imperceptível).
- Substituir o kernel Gaussiano por outro (exato) caso queira experimentos mais precisos.

## Solução de problemas
- ModuleNotFoundError: confirme se instalou as dependências dentro do ambiente virtual ativo.
- Imagem não encontrada: coloque `cln1.gif` na pasta ou deixe o gerador sintético atuar.
- Excesso de ruído no Laplaciano: faça um pré-suavizamento (aplicar Gaussiano antes).
- Resultado muito forte no Highboost: reduza k gradualmente (ex.: 2.0 → 1.5 → 1.2).

## Conceitos matemáticos essenciais
- Gradiente: vetor das derivadas parciais (Sobel aproxima). Indica direção e intensidade da maior variação.
- Segunda derivada (Laplaciano): detecta mudanças bruscas na primeira derivada; acentua bordas finas.
- Máscara de suavização (Gaussiano aproximado): reduz alta frequência para permitir isolamento de detalhes.
- Máscara de alta frequência: diferença entre imagem original e suavizada; contém contornos e detalhes finos.

## Recomendações práticas
- Para destacar bordas: Laplaciano ou magnitude do Sobel.
- Para melhorar nitidez natural de fotos: Unsharp (k=1).
- Para impressão ou imagens pouco contrastadas: Highboost (k>=2).
- Para imagens sensíveis (radiografias, exames): k<1 ou apenas Sobel leve.

## Referência das fórmulas usadas
- Magnitude do gradiente: M(x,y) = sqrt(Gx(x,y)^2 + Gy(x,y)^2)
- Unsharp/Highboost: g = f + k*(f - s) = (1 + k)f - k*s
- Laplaciano (máscara): aproxima ∇²f = f_xx + f_yy

---
Este guia cobre todo o funcionamento do script e como reproduzir os resultados. Ajuste parâmetros e explore imagens diferentes para entender melhor o impacto de cada técnica.

