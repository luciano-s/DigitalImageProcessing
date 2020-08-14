from img import Img
import matplotlib.pyplot as plt

def load():
    try:
        file = input('Insira o caminho para a imagem: ')
        img = Img.load_image(file)
        if img != None:
            print("Imagem carregada com sucesso!")
        return img
    except:
        print(f'Erro ao abrir imagem')
        exit()


def save(new_img):
    file_name = 'img/'
    file_name += input('Insira o nome do arquivo para salvar a nova imagem: ')
    Img.save_image(new_img, file_name)
    print(f'Imagem salva com sucesso em {file_name}\n\n\n')


def fatiamento_niveis():
    img = load()
    new_img = None
    a = int(input("Insira o 1º valor do intervalo: "))
    b = int(input("Insira o 2º valor do intervalo: "))
    intensity = int(input('Insira o novo valor da intensidade do pixel: '))
    op = input('Haverá redução dos pixels fora do intervalo?[s/n] ')
    if op in ['s', 'S']:
        reduce = True
        r = int(input('Insira o novo valor dos pixels fora do intervalo: '))
        print('Processando . . ')
        new_img = img.highlight(a, b, intensity, reduce, r)
    else:
        print('Processando . . ')
        new_img = img.highlight(a, b, intensity)
    save(new_img)
    

def transformacao_gama():
    img = load()

    g = float(input('Insira o valor de Gamma: '))
    c = float(input('Insira o valor de c: '))

    new_img = img.gama_t(g, c)
    save(new_img)
    


def flip_horizontal():
    img = load()
    new_img = img.flip()
    save(new_img)

def process_hist_tuple(hist_tuple):
    l  = []
    for x in hist_tuple:
        i = x[1]
        while i:
            l.append(x[0])
            i-=1
    return l

def equalizacao_histograma():
    img = load()
    frq_list = img.generate_histogram_list()
    x = process_hist_tuple(frq_list)
    new_img = img.histogram_equalization(frq_list)
    new_frq_list = new_img.generate_histogram_list()
    y = process_hist_tuple(new_frq_list)
    plt.hist(x, bins=255)
    plt.show()
    plt.hist(y, bins=255)
    plt.show()
    save(new_img)


def menu():
    op1 =   "|------------------------------|\n"
    op1 +=  "|01 - Fatiamento de níveis     |\n"
    op1 +=  "|------------------------------|\n"
    op1 +=  "|02 - Transformação Gama       |\n"
    op1 +=  "|------------------------------|\n"
    op1 +=  "|03 - Flip horizontal          |\n"
    op1 +=  "|------------------------------|\n"
    op1 +=  "|04 - Equalização de Histograma|\n"
    op1 +=  "|------------------------------|\n"
    op1 +=  "|05 - Filtro Laplaciano        |\n"
    op1 +=  "|------------------------------|\n"
    op1 +=  "|06 - Somar Imagens            |\n"
    op1 +=  "|------------------------------|\n"
    op1 +=  "|07 - Filtro Média             |\n"
    op1 +=  "|------------------------------|\n"
    op1 +=  "|08 - Binarização              |\n"
    op1 +=  "|------------------------------|\n"
    op1 +=  "|09 - Histograma da Imagem     |\n"
    op1 +=  "|------------------------------|\n"
    op1 +=  "|10 - Conversão para CMY e HSI |\n"
    op1 +=  "|------------------------------|\n"
    # op1 +=  "|11 - Conversão HSI para RGB   |\n"
    # op1 +=  "|------------------------------|\n"
    op1 +=  "|S - Sair                      |\n"
    op1 +=  "|------------------------------|\n"
    op1 +="Digite sua escolha: "
    op = str(input(op1))
    print()
    return op


def filtro_laplaciano():
    op = '1 - Filtro 1 (elemento central = 4)\n'
    op +='2 - Filtro 2 (elemento central = 8)\n'
    op +="Digite sua escolha: "
    escolha = str(input(op)) 
    img = load()
    x = lambda x:0 if x == '1' else 1    
    new_img = img.laplaciano(x(escolha))
    save(new_img)


def add_images():
    img_1 = load()
    img_2 = load()

    new_img = Img.add(img_1, img_2)

    save(new_img)

def filtro_media():
    n = int(input('Insira o valor do parâmetro n do filtro: '))
    img = load()

    new_img = img.media(type='media', n=n)
    
    save(new_img)


def binarizacao():
    img = load()
    k = int(input('Insira o parâmetro k: '))
    new_img = img.binarizacao(k)
    save(new_img)

def generate_histogram():
    img = load()
    frq_list = img.generate_histogram_list()
    x = process_hist_tuple(frq_list)
    new_img = img.histogram_equalization(frq_list)
    new_frq_list = new_img.generate_histogram_list()
    y = process_hist_tuple(new_frq_list)
    plt.hist(x, bins=255)
    plt.show()


def split_channels():
    img = load()
    r_img = img.extract_channel('r')
    g_img = img.extract_channel('g')
    b_img = img.extract_channel('b')
    print('Imagem canal R:')
    save(r_img)
    print('Imagem canal G:')
    save(g_img)
    print('Imagem canal B:')
    save(b_img)
    
    cmy_img = img.rgb_to_cmy()
    c_img = cmy_img.extract_channel('c')
    m_img = cmy_img.extract_channel('m')
    y_img = cmy_img.extract_channel('y')
    print('Imagem canal C:')
    save(c_img)
    print('Imagem canal M:')
    save(m_img)
    print('Imagem canal Y:')
    save(y_img)

    hsi_img = img.rgb_to_hsi()
    h_img = hsi_img.extract_channel('h')
    s_img = hsi_img.extract_channel('s')
    i_img = hsi_img.extract_channel('i')
    print('Imagem canal H:')
    save(h_img)
    print('Imagem canal S:')
    save(s_img)
    print('Imagem canal I:')
    save(i_img)


def join_channels():
    print('Será solicitado três imagens (uma para cada canal):')
    img_1 = load()
    img_2 = load()
    img_3 = load()
    new_img = Img.join_channels(img_1, img_2, img_3)
    rgb_img = new_img.hsi_to_rgb()
    save(rgb_img)

    
if __name__ == "__main__":
    while(True):
        var = menu()
        if var in ['s', 'S']:
            break
        if var == '1':
            fatiamento_niveis()
        elif var == '2':
            transformacao_gama()
        elif var == '3':
            flip_horizontal()        
        elif var == '4':
            equalizacao_histograma()    
        elif var == '5':
            filtro_laplaciano()
        elif var == '6':
            add_images()
        elif var == '7':
            filtro_media()
        elif var == '8':
            binarizacao()
        elif var == '9':
            generate_histogram()
        elif var == '10':
            split_channels()
        # elif var == '11':
        #     join_channels()



    
    