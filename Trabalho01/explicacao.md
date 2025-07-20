- A reamostragem não muda os valores de pixels (como brilho ou cor), mas sim o **número total de pixels**. Estamos criando uma nova matriz de pixels que é menor que a original. O processo não altera os valores de cor ou brilho dos pixels existentes, mas sim seleciona quais deles serão representados na nova matriz, menor.

- Para isso usamos alguns conceitos importante, por exemplo:
    1. Calcula o novo tamanho da imagem utilizando a formula:
        # nova dimensão = dimensão original * (DPI alvo / DPI original)
        Separadamente fica:
        fator_de_escala  = dpi_alvo / DPI_ORIGINAL
        
        nova_largura = round(largura_original * fator_de_escala )
        nova_altura = round(altura_original * fator_de_escala )

    2. Agora vamos gerar a reamostragem para a imagem original:
        Criamos uma matriz para linha e coluna:
        imagem_reamostrada = np.zeros((nova_altura, nova_largura), dtype=imagem_original.dtype)

        Calculamos o fator de escala:
        fator_escala_x = largura_original / nova_largura
        fator_escala_y = altura_original / nova_altura

        e por fim, percorremos a linha e coluna para encontrar o pixel correspondente na imagem original:
        
        x_original = int(pixel_x_novo * fator_escala_x)
        y_original = int(pixl_y_novo * fator_escala_y)

    3. Quando eu conseguir as informações de x_original e y_original eu consigo pegar os valores na imagem original e passar para a nova imagem que estou criando:
    imagem_reamostrada[pixl_y_novo, pixel_x_novo] = imagem_original[y_original, x_original]
