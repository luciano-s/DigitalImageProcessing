import math
class Img():
    PGM = ['P2', 'P5']
    PPM = ['P3', 'P6']

    def __init__(self, width, height, Maxval, format, pixels):
        self.width  = width
        self.height = height
        self.Maxval = Maxval
        self.format = format
        self.pixels = pixels


    def read_PGM(file, format):

        
        size = file.readline().split(' ')
        

        print(size)
        Maxval = int(file.readline())
        width = int(size[0])
        height = int(size[1])
        matrix = [[0 for i in range(0, width)] for j in range(0, height)]

                
        for i in range(0, height):
                for j in range(0, width):
                    try:
                        matrix[i][j] = int(file.readline())

                    except:
                        with open('log.txt', 'a') as f:
                            f.write('Error during conversion -> image {0}'.format(file))
                        pass
                        
                    
        return Img(width, height, Maxval, format, matrix)

    @classmethod
    def get_pixels_PPM(cls, file):
        m = file.readlines()
        row_list = []
        pixels = []
        for row in m:
            row_list = row.split(' ')

            for pixel_value in row_list:
               
                abracaa=0
                try:
                    pixels.append(int(pixel_value))
                except:
                    with open('log.txt', 'a') as f:
                        f.write('Conversion error ASCII Char: {0}'.format(ord(pixel_value)))
        return pixels

    @classmethod
    def read_PPM(cls, file, format):
        
        width, height = file.readline().split(' ')
        width  = int(width)
        height = int(height)
        matrix = [[[0 for i in range(0, width)] for j in range(0, height)] for i in range(0, 3)]

        Maxval = int(file.readline())
        
        pixels = Img.get_pixels_PPM(file)

        cont = 0

        for j in range(0, height):
            for k in range(0, width):
                for i in range(0, 3):
                    try:
                        matrix[i][j][k] = pixels[cont]
                        cont+=1
                    except:
                        print(f'i: {i}\nj: {j}\nk:{k}\ncont: {cont}\n')
                        input()

        return Img(width, height, Maxval, format, matrix)

        
    @classmethod
    def load_image(cls, file):

        new_img = None

        with open(file, 'r' ) as file_1:

            format_file = file_1.readline().split('\n')[0]
            comment = file_1.readline()
            # print(f'Comentário{comment}')
            # print(format_file)
            # input()

            if format_file in cls.PGM:            
                new_img = Img.read_PGM(file_1, format_file)
                
            elif format_file in cls.PPM:
                new_img = Img.read_PPM(file_1, format_file)
            

        return new_img


    @classmethod
    def save_image(cls, img, filename):
        with open(filename, 'w') as f:

            if img.format in cls.PGM:

                f.write(str(img.format)+'\n')
                f.write('# CREATOR:  Luciano Simeao Jr\n')
                f.write(str(img.width)+' '+str(img.height)+'\n')
                f.write(str(img.Maxval)+'\n')
            
                for i in range(0, img.height):
                        for j in range(0, img.width):
                            f.write(str(img.pixels[i][j])+'\n')
            
            if img.format in cls.PPM:
                
                space =' '
                f.write(str(img.format)+'\n')
                f.write(str(img.width)+' '+str(img.height)+'\n')
                f.write(str(img.Maxval)+'\n')
                cont = 0
                for j in range(0, img.height):
                    for k in range(0, img.width):
                        for i in range(0, 3):
                            try:
                                f.write(str(img.pixels[i][j][k])+space)
                                space = ' '
                                cont+=1
                            except:
                                print(f'i > {i}\nj > {j}\nk > {k}')
                        if cont == 70:
                            space = '\n'
                            cont = 0


    def extract_channel(self, channel):
        if channel in ['r', 'R', 'c', 'C', 'h', 'H']:
            channel = 0
        elif channel in ['g', 'G', 'm', 'M', 's', 'S']:
            channel = 1
        else:
            channel = 2

        matrix = [[0 for i in range(0, self.width)] for j in range(0, self.height)]

        for i in range(0, self.height):
                for j in range(0, self.width):
                        matrix[i][j] = self.pixels[channel][i][j]

        return Img(self.width, self.height, self.Maxval, 'P2', matrix)

    @classmethod
    def create_rgb_img(cls, img_1, img_2, img_3):
        print(type(img_1))
        print(type(img_2))
        print(type(img_3))
        input()
        Maxval = max(max(img_1.Maxval, img_2.Maxval), img_3.Maxval)
        width = img_1.width
        height = img_2.height

        matrix = [[[0 for i in range(0, width)] for j in range(0, height)] for i in range(0, 3)]

        for i in range(0, height):
            for j in range(0, width):
                matrix[0][i][j] = img_1.pixels[i][j]
                matrix[1][i][j] = img_2.pixels[i][j]
                matrix[2][i][j] = img_3.pixels[i][j]

        return Img(width, height, Maxval, 'P3', matrix)

    @classmethod
    def add(cls, img_1, img_2):
        valid = lambda x: x if 0 <= x <= 255 else ( 0 if  x < 0 else 255) 
        new_img = Img.generate_matrix(img_1.height, img_1.width)

        for i in range(0, img_1.height):
            for j in range(0, img_1.width):
                new_img[i][j] = valid(img_1.pixels[i][j] + img_2.pixels[i][j])
        return Img(
            img_1.width, img_1.height, valid(img_1.Maxval+img_2.Maxval), 
            img_1.format, new_img
         )

    @classmethod
    def subtract(cls, img_1, img_2):
        new_img = Img.copy(img_1)

        for i in range(0, img_1.height):
            for j in range(0, img_1.width):
                new_img.pixels[i][j] = img_1.pixels[i][j] - img_2.pixels[i][j]


    def lighten(self, intensity):
        new_img = Img(self.width, self.height, self.Maxval, self.format)
        new_img.pixels = [[0 for i in range(0, width)] for j in range(0, height)]

        for i in range(0, height):
            for j in range(0, width):
                if (self.pixels[i][j] + intensity) > self.Maxval:
                    new_img[i][j] = self.Maxval
                else:
                    new_img[i][j] =  self.pixels[i][j]+intensity

        return new_img


    def darken(self, intensity):
        new_img = Img(self.width, self.height, self.Maxval, self.format, self.pixels)
        new_img.pixels = [[0 for i in range(0, self.width)] for j in range(0, self.height)]

        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.pixels[i][j] - intensity) < 0:
                    new_img.pixels[i][j] = 0
                else:
                    new_img.pixels[i][j] =  self.pixels[i][j]-intensity

        return new_img        


    def rotate(self, degree):
        

        if degree == 180:
            new_img = Img(self.width, self.height, self.Maxval, self.format, self.pixels)
            new_img.pixels = [[0 for i in range(0, self.width)] for j in range(0, self.height)]
            
            for i in range(0, self.height):
                for j in range(0, self.width):
                  
                    new_img.pixels[self.height-i-1][self.width-j-1] = self.pixels[i][j]
            return new_img
        
        elif degree == 90:
            matrix = [[0 for i in range(0, self.height)] for j in range(0, self.width)]
            new_img = Img(self.height, self.width, self.Maxval, self.format, matrix)
            
            # print(new_img.width)
            # print(new_img.height)
            # input()
            
            for i in range(0, self.height):
                for j in range(0, self.width):
                    try:               
                        new_img.pixels[self.width-j-1][i] = self.pixels[i][j]
                    except:
                        print(f'Width: {self.width}')
                        print(f'Height: {self.height}')
                        print(i)
                        print(j)
                        # input()
            return new_img


        elif degree == 270:
            new_img = Img(self.width, self.height, self.Maxval, self.format, self.pixels)
            new_img.pixels = [[0 for i in range(0, self.width)] for j in range(0, self.height)]
            
            for i in range(0, self.height):
                for j in range(0, self.width):
                    new_img.pixels[self.height-i-1][self.width-j-1] = self.pixels[i][j]   

            new_img_2 = Img(self.height, self.width, self.Maxval, self.format, self.pixels)
            new_img_2.pixels = [[0 for i in range(0, self.height)] for j in range(0, self.width)]
            
            for i in range(0, self.height):
                for j in range(0, self.width):
                    new_img_2.pixels[self.width-j-1][i] = new_img.pixels[i][j]

            return new_img_2

        
    @classmethod
    def copy(cls, img):
        new_img = Img(img.width, img.height, img.Maxval, img.format)
        
        if img.format in img.PGM:
            new_img.pixels = [[0 for i in range(0, img.width)] for j in range(0, img.height)]
        
        elif img.format in img.PPM:
                new_img.pixels = [[[0 for i in range(0, img.width)]
                for j in range(0, img.height)] for z in range(3)]
        
        return new_img

            
    def flip(self, type="horizontal"):
        """
            Takes a matrix as input and a flip type
            returning a new matrix flipped
        """
        m = [[0 for i in range(0, self.width)] for j in range(0, self.height)]
        k = self.width-1
        if type == "horizontal":
            for i in range(self.height):
                k = self.width-1
                for j in range(self.width):
                    m[i][j] = self.pixels[i][k]
                    k-=1

        return Img(self.width, self.height, self.Maxval,self.format, m)
    

    def highlight(self, a, b, intensity, reduce=False, r=0):
        m = [[0 for i in range(0, self.width)] for j in range(0, self.height)]

        # useful lambda functions
        valid_zero = lambda x: 0 if x < 0 else x
        valid_255  = lambda x: 255 if 255 < x else x
        valid_interval = lambda a, b: (a, b) if a < b else (b, a)
        
        a, b = valid_interval(a, b)

        if reduce:
            for i in range( self.height ):
                for j in range( self.width ):
                    
                    if a <= self.pixels[i][j] <= b:
                        m[i][j] = valid_255(intensity)
                            
                    else:
                        m[i][j] = valid_zero(r)
                        
        else:
            for i in range( self.height ):
                for j in range( self.width ):
                    
                    if a <= self.pixels[i][j] <= b:
                        m[i][j] = valid_255(intensity)
                        
                    else:
                        m[i][j] = self.pixels[i][j] 
                                  
            
        return Img(self.width, self.height, self.Maxval, self.format, m)


    def gama_t(self, gamma, c):
        m = [[0 for i in range(0, self.width)] for j in range(0, self.height)]
        
        # deals with negative c
        c = c if 0 < c else 1
        
        # useful lambda functions
        normalizer = lambda x: x/255
        s = lambda r,c,g: int((c*r**g)*255)
        

        for i in range( self.height ) :
            for j in range( self.width ):
                m[i][j] = s( normalizer(self.pixels[i][j]), c, gamma )
                
        return Img(self.width, self.height, self.Maxval, self.format, m)
    

    def generate_histogram_list(self):
        l = []

        for i in range(self.height):
            for j in range(self.width):
                l.append(self.pixels[i][j])
        l.sort()

        i = 0
        frequency_list = []
        length = len(l)

        while i < length:
            index = l.count(l[i])
            frequency_list.append( (l[i], index) )
            i += index
        
        return frequency_list


    def histogram_equalization(self, frq_list):
        m = [[0 for i in range(0, self.width)] for j in range(0, self.height)]

        cte = 255.0/(self.width * self.height)
        
        
        # frq -> ( elem, freq )
        

        final_list = []
        p = 0
        for t in frq_list:
            p = (p + t[1]) 

            final_list.append( (t[0],  int(cte*p)) )

        
        for i in range(self.height):
            for j in range(self.width):
                m[i][j] = self.find_pixel(self.pixels[i][j], final_list)
        
        return Img(self.width, self.height, self.Maxval, self.format, m)


    def find_pixel(self, p, lista):
        for l in lista:
            if p == l[0]:
                return l[1]

    @classmethod
    def generate_matrix(cls, height, width):
        m = [[0 for i in range(0, width)] for j in range(0, height)]
        return m

    @classmethod
    def populate(cls, m, height, width, values):
        index = 0
        for i in range(height):
            for j in range(width):
                m[i][j] = values[index]
                index +=1
        return m

    @classmethod
    def chose_filter(cls, type, N=0):
        filter = []
        if type == 0:
            filter = Img.generate_matrix(3, 3)
            filter = Img.populate(filter, 3, 3, values=[0,-1 ,0, -1, 4, -1, 0, -1, 0])
        elif type == 1:
            filter = Img.generate_matrix(3, 3)
            filter = Img.populate(filter, 3, 3, values=[-1,-1,-1,-1,8,-1,-1,-1,-1])
        elif type == 'media':
            filter = Img.generate_matrix(N, N)
            v = [1 for x in range(N*N)]
            filter = Img.populate(filter, N, N, values=v)

        return filter

    @classmethod
    def apply_filter(cls, f, w, x, y):                    
        a = len(w)
        r = 0
        
        for s in range(a):
            for t in range(a):
                r += f[x+s][y+t] * w[s][t]
        
        return r


    def laplaciano(self, type):
        new_img = Img.generate_matrix(self.height, self.width)
        filter = Img.chose_filter(type)
        inc = len(filter)//2
        m = Img.generate_matrix(self.height+(2*(inc)), self.width + (2*(inc)))
        m = self.add_border(m, inc)
        valid = lambda x: x if 0 <= x <= 255 else ( 0 if  x < 0 else 255) 

        for i in range(self.height):
            for j in range(self.width):
                new_img[i][j] = valid(Img.apply_filter(m, filter, i, j))
        
        return Img(self.width, self.height, self.Maxval, self.format, new_img) 


    def media(self, type, n=3):
        new_img = Img.generate_matrix(self.height, self.width)
        filter = Img.chose_filter(type='media', N=n)
        inc =  len(filter)//2
        m = Img.generate_matrix(self.height+(2*(inc)), self.width+(2*(inc)))

        m = self.add_border(m, inc)

        valid = lambda x: x if 0 <= x <= 255 else (0 if  x < 0 else 255) 

        for i in range(self.height):
            for j in range(self.width):
                new_img[i][j] = int( 
                    valid(
                        Img.apply_filter(m, filter, i, j)/(n*n) 
                    )
                )   
        
        return Img(self.width, self.height, self.Maxval, self.format, new_img)


    def add_border(self, m, inc):
        
        for i in range(self.height):
            for j in range(self.width):
                m[i+inc][j+inc] = self.pixels[i][j]
                   
        return m

    def binarizacao(self, k):
        m = Img.generate_matrix(self.height, self.width)
        for i in range(self.height):
            for j in range(self.width):
                if self.pixels[i][j] < k:
                    m[i][j] = 0
                else:
                    m[i][j] = 255
        return Img(self.width, self.height, self.Maxval, self.format, m)


    def rgb_to_cmy(self):
        validate = lambda x: x if 0 <= x <= 255 else (0 if  x < 0 else 255) 
        m = [[[validate(255 - self.pixels[k][i][j]) for i in range(self.width)]
         for j in range(self.height)] for k in range(0, 3)]
        return Img(self.width, self.height, 255, self.format, m)
    

    def rgb_to_hsi(self):
        H = lambda r, g ,b: 81.15*(math.acos((.5*((r-g) + (r-b)))/math.sqrt((r-g)**2 + (r-b)*(g-b))))\
        if b<=g else 255 *( (math.cos((
        2*math.pi - math.acos((.5*((r-g) + (r-b)))/math.sqrt((r-g)**2 + (r-b)*(g-b)))) + 2*math.pi)\
        + 1 ) ) / (2)

        S = lambda r, g, b: 1 - 3 * min(r, g, b)

        I = lambda r, g, b: (r+g+b)/(3*255)

        normalizer = lambda x, s, t: x/(x+s+t)

        v = lambda x: x if 0 <= x <= 255 else(0 if x < 0 else 255)

        m = [[[0 for i in range(self.width)] for j in range(self.height)] for k in range(0, 3)]
        for i in range(self.width):
            for j in range(self.height):
                r = normalizer(self.pixels[0][i][j],self.pixels[1][i][j], self.pixels[2][i][j])
                g = normalizer(self.pixels[1][i][j],self.pixels[0][i][j], self.pixels[2][i][j])
                b = normalizer(self.pixels[2][i][j],self.pixels[1][i][j], self.pixels[0][i][j])

                try:
                    m[0][i][j] = int(H(r, g, b))
                except:
                    m[0][i][j] = 0
                m[1][i][j] = int(255 * S(r, g, b))
                m[2][i][j] = int(255 * I(
                    self.pixels[0][i][j], self.pixels[1][i][j], self.pixels[2][i][j] 
                ))
        
        return Img(self.width, self.height, 255, self.format, m)

    @classmethod
    def get_rgb_from_hsi(cls, h, s, i):
        validate = lambda x: x if 0 <= x <= 255 else (0 if  x < 0 else 255) 

        h_deg = math.degrees(h)
        temp_1 = i * (1 + ((s * math.cos(h))/math.cos(math.radians(60-h_deg))))
        temp_2 = i * (1-s)
        temp_3 = 3 * i - (temp_1+temp_2)
        while 360 < h_deg:
            h_deg-=360 
        if 0 <= h_deg < 120:
            r, b, g = temp_1, temp_2, temp_3
        elif 120 <= h_deg < 240:
            g, r, b = temp_1, temp_2, temp_3
        elif 240 <= h_deg < 360:
            b, g, r = temp_1, temp_2, temp_3
        return validate(int(r)), validate(int(g)), validate(int(b))


    def hsi_to_rgb(self):
        m = [[[0 for i in range(self.width)] for j in range(self.height)] for k in range(0, 3)]
        

        for i in range(self.height):
            for j in range(self.width):
                H, S, I = self.pixels[0][i][j], self.pixels[1][i][j], \
                self.pixels[2][i][j]

                m[0][i][j], m[1][i][j], m[2][i][j] = Img.get_rgb_from_hsi(H,S,I)

        return Img(self.width, self.height, 255, self.format, m)


    @classmethod
    def join_channels(cls, img_1, img_2,img_3):
        m = [[[0 for i in range(img_1.width)]for j in range(img_1.height)] for k in range(0, 3)]
        ch_1, ch_2, ch_3 = img_1.pixels, img_2.pixels, img_3.pixels
        for i in range(img_1.height):
            for j in range(img_1.width):
                m[0][i][j], m[1][i][j], m[2][i][j] = ch_1[i][j], ch_2[i][j],\
                 ch_3[i][j]
        
        return Img(img_1.width, img_1.height, 255, 'P3', m)
