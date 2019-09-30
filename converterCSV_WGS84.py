# -*- coding: utf-8 -*-
from pyproj import Proj, transform

class ConverterCSV_WGS84:
    """ Classe para conversão de coordenadas xy(valores separados por strSeparador) para longlat wgs84 """

    def __init__(self):
        self.ficheiro = ""
        self.fich_sample = ""
        self.separador = ","
        self.num_linhas = 0
        self.divisor = 0
        self.espacamento = 1
        self.positivo = 1
        self.x_min = 19999999.9
        self.x_max = -19999999.9
        self.y_min = 19999999.9
        self.y_max = -19999999.9
        self.z_min = 19999999.9
        self.z_max = -19999999.9

    def set_ficheiro_csv(self, fich):
        self.ficheiro = fich

    def set_separador(self, sep):
        self.separador = sep

    def set_positivo(self, valor):
        self.positivo = valor

    def projectar(self,longitude, latitude):
        print ('projectar')
        return 'projectar'


    def converter3(self, ignorar_linha, separador, fich_1, epsg_1, fich_2, epsg_2, n1, n2, n3, n4, n5, n6, n7):

        # ------------------------------------------------------- Conversão de coordenadas para WGS84 longlat

        inProj = Proj(init='epsg:' + str(epsg_1))
        outProj = Proj(init='epsg:' + str(epsg_2))
        print ('inProj=', inProj, ' outProj=', outProj, ' ---------------------------------------')
        print ('class: converterCSV_WGS84: converter3 -------- espacamento=', self.espacamento)
        print ('class: converterCSV_WGS84: converter3 -------- fich. origem=', fich_1, ' fich. destino =', fich_2)
        # FALTA FAZER: determinar se dados têm info de reflectividade e RGB
        # se não tiver coloca os valores a zero por defeito

        # ----------------------------------- determinar nº de variaveis por linha (colunas)
        variaveis = []
        with open(fich_1, 'r') as f:
            for line in f:
                variaveis = line.split(separador)
                break
        if len(variaveis) < 3:
            print('NUM DE VARIAVEIS < 3 !!!!!!!!!!!!!!!!!!!!! do ficheiro csv', fich_1)
            return []

        # ------------------------------ se o ficheiro de destino já existir, é apagado
        with open(fich_2, 'w') as fout:
            m = 0
            # se o dados a importar estiverem em WGS84 LL, não é necessário converter
            if epsg_1 == epsg_2:
                with open(fich_1, 'r') as fin:
                    if ignorar_linha > 0:
                        next(fin)
                    for line in fin:
                        linha = line.lstrip(separador)
                        linha = linha.replace(separador+separador,separador)
                        variaveis = linha.split(separador)
                        # print("variaveis:",variaveis)
                        x = float(variaveis[n1])
                        y = float(variaveis[n2])
                        z = float(variaveis[n3]) * self.positivo
                        xs = "%.7f" % (x)
                        ys = "%.7f" % (y)
                        zs = "%.3f" % (z)
                        # reflectividade
                        i = "0"
                        # RGB
                        r_color = "0"
                        g_color = "0"
                        b_color = "0"
                        # Passar para string, definindo nº de casas decimais (resolução 0.01)

                        # max + min
                        if self.x_min > x:
                            self.x_min = x
                        if self.x_max < x:
                            self.x_max = x
                        if self.y_min > y:
                            self.y_min = y
                        if self.y_max < y:
                            self.y_max = y
                        if self.z_min > z:
                            self.z_min = z
                        if self.z_max < z:
                            self.z_max = z

                        fout.write(xs + ',' + ys + ',' + zs + ',' + i + ',' + r_color + ',' + g_color + ',' + b_color + '\n')
                        m += 1

            else:
                # dados a importar não estão em WGS84 LL, é necessário converter
                print('converter 3, n1, n2, n3, n4, n5, n6, n7:', n1, n2, n3, n4, n5, n6, n7)

                with open(fich_1, 'r') as fin:
                    if ignorar_linha > 0:
                        next(fin)
                    for line in fin:
                        variaveis = line.split(separador)
                        # print 'variaveis', variaveis
                        # R = raw_input()

                        x = float(variaveis[n1])
                        y = float(variaveis[n2])
                        z = float(variaveis[n3])*self.positivo
                        # ------------------ reflectividade
                        i = "0"
                        # ------------------ RGB
                        r_color = "0"
                        g_color = "0"
                        b_color = "0"
                        # -------------------------------------------Transformar coordenadas (PROJ4)
                        x2, y2 = transform(inProj, outProj, x, y)

                        # ------------------- Passar para string truncando à 7a casa decimal
                        xs = "%.7f" % (x2)
                        ys = "%.7f" % (y2)
                        zs = "%.3f" % (z)

                        # max + min
                        if self.x_min > x2:
                            self.x_min = x2
                        if self.x_max < x2:
                            self.x_max = x2
                        if self.y_min > y2:
                            self.y_min = y2
                        if self.y_max < y2:
                            self.y_max = y2
                        if self.z_min > z:
                            self.z_min = z
                        if self.z_max < z:
                            self.z_max = z

                        fout.write(xs + ',' + ys + ',' + zs + ',' + i + ',' + r_color + ',' + g_color + ',' + b_color + '\n')
                        m += 1
                    print(" converter3: convertido de epsg1 para epsg2:", epsg_1, epsg_2)

        MaxMin = [self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max]

        return MaxMin

    def converter_simples(self, x_in, y_in, epsg_1, epsg_2):
        print ('class: converterCSV_WGS84: converter_simples ---------------------------------------')
        inProj = Proj(init='epsg:' + str(epsg_1))
        outProj = Proj(init='epsg:' + str(epsg_2))
        print ('inProj=', epsg_1, ' outProj=', epsg_2, ' ---------------------------------------')

        # Transformar coordenadas (PROJ4)
        # print("x,y = ", x,y)
        x2, y2 = transform(inProj, outProj, x_in, y_in)

        return x2, y2
