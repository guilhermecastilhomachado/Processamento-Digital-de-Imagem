# Processamento Digital de Imagem — Resumo e Guia do Projeto

Bem-vindo(a)! Este repositório reúne materiais e códigos das atividades (Trabalho01–Trabalho05) e resumos das aulas (Aula01–Aula11). Abaixo você encontra um panorama com objetivos, links úteis e como executar.

## Sumário
- [Configuração rápida (Windows CMD)](#configuração-rápida-windows-cmd)
- [Trabalhos (1 a 5)](#trabalhos-1-a-5)
- [Resumos das Aulas (1 a 11)](#resumos-das-aulas-1-a-11)
- [Imagens de exemplo (links rápidos)](#imagens-de-exemplo-links-rápidos)
- [Dependências](#dependências)

## Configuração rápida (Windows CMD)
```cmd
cd "C:\Users\SEU_USUARIO\OneDrive\Área de Trabalho\Processamento Digital de Imagem"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Trabalhos (1 a 5)

- Trabalho01 — Reamostragem (DPI) e Quantização (bits)
  - Pasta: [Trabalho01/](Trabalho01/)
  - Explicação: [Trabalho01/explicacao.md](Trabalho01/explicacao.md)
  - Scripts: [reamostragem.py](Trabalho01/reamostragem.py), [quantizacao.py](Trabalho01/quantizacao.py)
  - Executar:
    ```cmd
    cd Trabalho01
    python reamostragem.py
    python quantizacao.py
    ```

- Trabalho02 — Rotulagem de Componentes e Contagem de Objetos
  - Pasta: [Trabalho02/](Trabalho02/)
  - Explicação: [Trabalho02/explicacao.md](Trabalho02/explicacao.md)
  - Scripts: [rotulacao_comp_conexos.py](Trabalho02/rotulacao_comp_conexos.py), [contagem_obj_Threshold.py](Trabalho02/contagem_obj_Threshold.py)
  - Executar:
    ```cmd
    cd Trabalho02
    python rotulacao_comp_conexos.py
    python contagem_obj_Threshold.py
    ```

- Trabalho03 — Histograma e Equalização Manual
  - Pasta: [Trabalho03/](Trabalho03/)
  - Explicação: [Trabalho03/explicacao.md](Trabalho03/explicacao.md)
  - Script: [histograma.py](Trabalho03/histograma.py)
  - Executar:
    ```cmd
    cd Trabalho03
    python histograma.py
    ```

- Trabalho04 — Filtragem Espacial (Média e Gaussiano)
  - Pasta: [Trabalho04/](Trabalho04/)
  - Explicação: [Trabalho04/explicacao.md](Trabalho04/explicacao.md)
  - Scripts: [filtro_medio.py](Trabalho04/filtro_medio.py), [filtro_gaussiano.py](Trabalho04/filtro_gaussiano.py)
  - Executar:
    ```cmd
    cd Trabalho04
    python filtro_medio.py
    python filtro_gaussiano.py
    ```

- Trabalho05 — Filtros de Realce (Sobel, Laplaciano, Unsharp, Highboost)
  - Pasta: [Trabalho05/](Trabalho05/)
  - Explicação: [Trabalho05/explicacao.md](Trabalho05/explicacao.md)
  - Script: [filtros_de_realce.py](Trabalho05/filtros_de_realce.py)
  - Executar:
    ```cmd
    cd Trabalho05
    python filtros_de_realce.py
    ```

## Resumos das Aulas (1 a 11)
Os resumos estão em [Resumo Geral das Aulas de PDI/](Resumo%20Geral%20das%20Aulas%20de%20PDI/):
- [Aula 1](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula1.md)
- [Aula 2](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula2.md)
- [Aula 3](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula3.md)
- [Aula 4](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula4.md)
- [Aula 5](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula5.md)
- [Aula 6](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula6.md)
- [Aula 7](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula7.md)
- [Aula 8](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula8.md)
- [Aula 9](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula9.md)
- [Aula 10](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula10.md)
- [Aula 11](Resumo%20Geral%20das%20Aulas%20de%20PDI/aula11.md)

## Imagens de exemplo (links rápidos)
- Trabalho02: [art8lab1.png](Trabalho02/art8lab1.png) · [art8lab2.png](Trabalho02/art8lab2.png) · [clc3thr1.png](Trabalho02/clc3thr1.png)
- Trabalho03: 
  [imagem_equalizada.png](Trabalho03/imagem_equalizada.png) ·
  [imagem_equalizada2.png](Trabalho03/imagem_equalizada2.png) ·
  [imagem_equalizada3.png](Trabalho03/imagem_equalizada3.png) ·
  [imagem_equalizada4.png](Trabalho03/imagem_equalizada4.png) ·
  [imagem_equalizada5.png](Trabalho03/imagem_equalizada5.png) ·
  [imagem_equalizada6.png](Trabalho03/imagem_equalizada6.png)
- Entradas úteis:
  - Trabalho01: [ctskull-256.tif](Trabalho01/ctskull-256.tif) · [relogio.tif](Trabalho01/relogio.tif)
  - Trabalho02: [art8.png](Trabalho02/art8.png) · [clc3.png](Trabalho02/clc3.png)
  - Trabalho04: [ben2.png](Trabalho04/ben2.png) · [sta2.png](Trabalho04/sta2.png)
  - Trabalho05: [cln1.gif](Trabalho05/cln1.gif)

## Dependências
- Arquivo [requirements.txt](requirements.txt) cobre: numpy, pillow, matplotlib.
- Exemplos opcionais nos resumos:
  - SciPy (Aula 10): `pip install scipy`
  - scikit-image (Aula 11): `pip install scikit-image`

> Observações:
> - As pastas `Listas de Exercicios/` e `Slides das Aulas/` estão no `.gitignore`.
> - Execute os scripts dentro da pasta de cada trabalho para evitar problemas com caminhos relativos.

