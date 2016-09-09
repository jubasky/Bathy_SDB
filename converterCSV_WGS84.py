# -*- coding: utf-8 -*-
__author__ = 'm'
# Classe para conversão de coordenadas
# de ficheiro xyzi (valores separados por strSeparador)
# para longlat wgs84
from pyproj import Proj, transform
from osgeo import ogr
from osgeo import osr
import fileinput

class ConverterCSV_WGS84():
    fich_sample=""
    ficheiro="teste.csv"
    separador=","
    num_linhas=0
    divisor=0

    def set_ficheiro_csv(self, fich):
        self.ficheiro=fich

    def set_separador(self,sep):
        self.separador=sep

    def resumo(self,fich_1, epsg_1,epsg_2):
        # determinar nome do ficheiro de destino:

        self.fich_sample=fich_1[0:-3]+"smp"
        print "fich_ini=" + fich_1
        print "fich_sample="+ self.fich_sample

        # determinar num de linhas, max e minimos
        min_x=8000000
        min_y=min_x
        min_z=min_x
        max_x=-8000000
        max_y=max_x
        max_z=max_x
        n=0

        for line in fileinput.input([ fich_1 ]):
                n+=1

                variaveis=line.split(',')
                x=float(variaveis[0])
                y=float(variaveis[1])
                z=float(variaveis[2])

                if min_x > x:
                    min_x = x
                if max_x < x:
                    max_x = x
                if min_y > y:
                    min_y = y
                if max_y < y:
                    max_y = y
                if min_z > z:
                    min_z = z
                if max_z < z:
                    max_z = z

        self.num_linhas=n
        fileinput.close()

        print u" nº de linhas= ______________________________", self.num_linhas

        # calcular valor pelo qual vou dividir o total de linhas
        # de forma a encontrar sempre só 1000 amostras no maximo
        self.divisor=1
        for m in range(12,4,-1):
            if self.num_linhas >10**m:
                self.divisor=10**(m-3)
                break

        # preparar conversão de coordenadas
        inputEPSG = epsg_1
        outputEPSG = epsg_2
        inSpatialRef = osr.SpatialReference()
        inSpatialRef.ImportFromEPSG(inputEPSG)
        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(outputEPSG)
        # criar transformação de coordenadas
        coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
        point = ogr.Geometry(ogr.wkbPoint)

        # se o nº total de pontos for menor que 10000
        # utiliza todos os pontos do ficheiro original para
        # pré-visualização, senão, procede a sub-amostragem (max 1000pts)
        if self.divisor<9900:
            f = open(self.fich_sample,'w')

            f.write("x,y,z"+"\n")
            for line in fileinput.input([ fich_1 ]):
                variaveis=line.split(',')
                x=float(variaveis[0])
                y=float(variaveis[1])
                z=float(variaveis[2])
                i="0"
                # criar geometria
                point.AddPoint_2D(x, y)
                # Transformar
                point.Transform(coordTransform)
                # Passar para string
                xs= "%.6f" % (point.GetX())
                ys= "%.6f" % (point.GetY())
                zs= "%.3f" % (z)
                # limpar point
                point.Empty()
                f.write(xs + ',' + ys + ',' + zs  +  '\n')

            f.close()
            fileinput.close()
        else:
            n=0
            m=self.divisor
            f = open(self.fich_sample,'w')
            f.write("x,y,z"+"\n")
            for line in fileinput.input([ fich_1 ]):
                n+=1
                if n == m:
                    variaveis=line.split(',')
                    x=float(variaveis[0])
                    y=float(variaveis[1])
                    z=float(variaveis[2])
                    # criar geometria
                    point.AddPoint_2D(x, y)
                    # Transformar
                    point.Transform(coordTransform)
                    # Passar para string
                    xs= "%.6f" % (point.GetX())
                    ys= "%.6f" % (point.GetY())
                    zs= "%.3f" % (z)
                    # limpar point
                    point.Empty()
                    f.write(xs + ',' + ys + ',' + zs  +  '\n')
                    m+=self.divisor

            f.close()
            fileinput.close()

    def resumo2(self,fich_1, epsg_1,epsg_2):
        # determinar nome do ficheiro de destino:

        self.fich_sample=fich_1[0:-3]+"smp"

        print('classe: converterCSV_WGS84:  ----------------------------------------resumo2')
        print "fich_ini=" + fich_1

        print "fich_sample="+ self.fich_sample

        # determinar num de linhas, max e minimos
        min_x=8000000
        min_y=min_x
        min_z=min_x
        max_x=-8000000
        max_y=max_x
        max_z=max_x
        n=0

        for line in fileinput.input([ fich_1 ]):
                n+=1

                variaveis=line.split(',')
                x=float(variaveis[0])
                y=float(variaveis[1])
                z=float(variaveis[2])

                if min_x > x:
                    min_x = x
                if max_x < x:
                    max_x = x
                if min_y > y:
                    min_y = y
                if max_y < y:
                    max_y = y
                if min_z > z:
                    min_z = z
                if max_z < z:
                    max_z = z

        self.num_linhas=n
        fileinput.close()

        print u" nº de linhas= ______________________________", self.num_linhas

        # calcular valor pelo qual vou dividir o total de linhas
        # de forma a encontrar sempre só 1000 amostras no maximo
        # if n> 1000:

        self.divisor=1

        if n>1000:
            for m in range(4,12,1):
                if self.num_linhas >10**m:
                    self.divisor=10**(m-2)
                    break
        print('.......................................divisor=', self.divisor)
        print( u".................................... nº de linhas=", self.num_linhas)


        # preparar conversão de coordenadas
        inProj = Proj(init='epsg:' + str(epsg_1))
        outProj = Proj(init='epsg:' + str(epsg_2))

        # se o nº total de pontos for menor que 10000
        # utiliza todos os pontos do ficheiro original para
        # pré-visualização, senão, procede a sub-amostragem (max 1000pts)

        f = open(self.fich_sample,'w')
        m=0
        mm=0
        n_step=self.divisor
        f.write("x,y,z"+"\n")

        if inProj==outProj:

            for line in fileinput.input([ fich_1 ]):
                m+=1
                if m % n_step==0:
                    mm+=1
                    variaveis=line.split(',')
                    x=float(variaveis[0])
                    y=float(variaveis[1])
                    z=float(variaveis[2])
                    i="0"

                    # Transformar
                    x2,y2 = transform(inProj,outProj,x,y)
                    # print x2,y2
                    # Passar para string
                    xs= "%.7f" % (x2)
                    ys= "%.7f" % (y2)
                    zs= "%.3f" % (z)

                    f.write(xs + ',' + ys + ',' + zs  +  '\n')
            fileinput.close()

        else:

            for line in fileinput.input([ fich_1 ]):
                m+=1
                if m % n_step==0:
                    mm+=1
                    variaveis=line.split(',')
                    x=float(variaveis[0])
                    y=float(variaveis[1])
                    z=float(variaveis[2])
                    i="0"
                    # Passar para string, com casas decimais adequadas (~1cm)
                    xs= "%.7f" % (x)
                    ys= "%.7f" % (y)
                    zs= "%.3f" % (z)

                    f.write(xs + ',' + ys + ',' + zs  +  '\n')
            fileinput.close()


        f.close()

        print("..............................total de pontos             m=",m)
        print("..............................total de pontos amostrados mm=",mm)

    def converter(self,fich_1, epsg_1, fich_2,epsg_2):
        # conversão de coordenadas para WGS84 longlat + prof + reflectividade (0 por defeito)
        # ref. bibliografica:
        # http://gis.stackexchange.com/questions/78838/how-to-convert-projected-coordinates-to-lat-lon-using-python
        #http://stackoverflow.com/questions/8009882/how-to-read-large-file-line-by-line-in-python

        # Sistemas de Referência:
        # datum etrs89
        #inputEPSG = 3763
        #outputEPSG = 4326

        inputEPSG = epsg_1
        outputEPSG = epsg_2
        inSpatialRef = osr.SpatialReference()
        inSpatialRef.ImportFromEPSG(inputEPSG)
        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(outputEPSG)

        # criar transformação de coordenadas
        coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
        # determinar se tem info de reflectividade,
        # se não tiver coloca o valor 0 (zero) por defeito
        for line in fileinput.input([ fich_1 ]):
            variaveis=line.split(',')
            break
        fileinput.close()

        # determinar nome do ficheiro de destino:

        fich_final=fich_1[0:-3]+"bt1"
        print "fich_1=" + fich_1
        print "fich_final="+ fich_final

        point = ogr.Geometry(ogr.wkbPoint)

        f = open(fich_final,'w')
        m=0
        if len(variaveis) < 4:

            for line in fileinput.input([ fich_1 ]):
                variaveis=line.split(',')
                x=float(variaveis[0])
                y=float(variaveis[1])
                z=float(variaveis[2])
                i="0"
                # criar geometria
                point.AddPoint_2D(x, y)
                # Transformar
                point.Transform(coordTransform)
                # Passar para string
                xs= "%.3f" % (point.GetX())
                ys= "%.3f" % (point.GetY())
                zs= "%.3f" % (z)
                # limpar point
                point.Empty()

                f.write(xs + ',' + ys + ',' + zs + ',' + i + '\n')
                #verificar que point.GetPointCount() devolve apenas 1
                #print "point count=" ,point.GetPointCount()
                m+=1
        else:

            for line in fileinput.input([ self.ficheiro ]):
                variaveis = line.split(',')
                x = float(variaveis[0])
                y = float(variaveis[1])
                z = float(variaveis[2])
                ii  =float(variaveis[3])
                ii = round(ii,2)
                i = long(ii)


                # criar geometria

                point.AddPoint_2D(x, y)
                point.Transform(coordTransform)

                xs= "%.9f" % (point.GetX())
                ys= "%.9f" % (point.GetY())
                zs= "%.3f" % (z)
                i_s=str(i)
                # apagar objecto point
                point.Empty()

                f.write(xs + ',' + ys + ',' + zs + ',' + i_s + '\n')
                #verificar que point.GetPointCount() devolve apenas 1
                #print "point count=" ,point.GetPointCount()
                m+=1

        fileinput.close()
        f.close()

        print x,y,z,i
        print line
        print u"nº de linhas", m

    def converter2(self,fich_1, epsg_1, fich_2,epsg_2):
        # conversão de coordenadas para WGS84 longlat + prof + reflectividade (0 por defeito)
        # ref. bibliografica:
        # http://gis.stackexchange.com/questions/78838/how-to-convert-projected-coordinates-to-lat-lon-using-python
        #http://stackoverflow.com/questions/8009882/how-to-read-large-file-line-by-line-in-python

        print ('converterCSV_WGS84: converter2  --------------------------------------')
        inProj = Proj(init='epsg:' + str(epsg_1))
        outProj = Proj(init='epsg:' + str(epsg_2))

        # determinar se tem info de reflectividade,
        # se não tiver coloca o valor 0 (zero) por defeito
        for line in fileinput.input([ fich_1 ]):
            variaveis=line.split(',')
            break
        fileinput.close()

        # determinar nome do ficheiro de destino:

        fich_final=fich_1[0:-3]+"bt1"
        print "fich_1=" + fich_1
        print "fich_final="+ fich_final

        f = open(fich_final,'w')
        m=0

        if len(variaveis) < 4:

            for line in fileinput.input([ fich_1 ]):
                variaveis=line.split(',')
                x=float(variaveis[0])
                y=float(variaveis[1])
                z=float(variaveis[2])
                i="0"

                # Transformar
                x2,y2 = transform(inProj,outProj,x,y)
                # print x2,y2
                # Passar para string
                xs= "%.3f" % (x2)
                ys= "%.3f" % (y2)
                zs= "%.3f" % (z)

                f.write(xs + ',' + ys + ',' + zs + ',' + i + '\n')
                #verificar que point.GetPointCount() devolve apenas 1
                #print "point count=" ,point.GetPointCount()
                m+=1

        else:
            print('NUM DE VARIAVEIS >=4 !!!!!!!!!!!!!!!!!!!!! do ficheiro csv', fich_1)

        fileinput.close()
        f.close()

        print x,y,z,i
        print line
        print u"nº de linhas", m

    def converter3(self,fich_1, epsg_1, fich_2,epsg_2,n1,n2,n3):

        """ conversão de coordenadas para WGS84 longlat + prof + reflectividade (0 por defeito) + R,G,B """

        # ref. bibliografica:
        # http://gis.stackexchange.com/questions/78838/how-to-convert-projected-coordinates-to-lat-lon,-using-python
        # http://stackoverflow.com/questions/8009882/how-to-read-large-file-line-by-line-in-python

        print ('class: converterCSV_WGS84: converter3 ---------------------------------------')
        inProj = Proj(init='epsg:' + str(epsg_1))
        outProj = Proj(init='epsg:' + str(epsg_2))
        print ('inProj=', epsg_1,' outProj=' , epsg_2,' ---------------------------------------')

        # determinar se tem info de reflectividade,
        # se não tiver coloca o valor 0 (zero) por defeito
        for line in fileinput.input([ fich_1 ]):
            variaveis=line.split(',')
            break
        fileinput.close()

        # determinar nome do ficheiro de destino:

        fich_final=fich_1[0:-3]+"bt1"
        print "fich_1=" + fich_1
        print "fich_final="+ fich_final

        f = open(fich_final,'w')
        m=0

        if len(variaveis) < 5:

            for line in fileinput.input([ fich_1 ]):
                variaveis=line.split(',')
                x=float(variaveis[n1])
                y=float(variaveis[n2])
                z=float(variaveis[n3])
                # reflectanci
                i="0"
                # RGB
                r_color="0"
                g_color="0"
                b_color="0"

                #
                # Transformar
                x2,y2 = transform(inProj,outProj,x,y)
                # print x2,y2
                # Passar para string
                xs= "%.7f" % (x2)
                ys= "%.7f" % (y2)
                zs= "%.3f" % (z)

                f.write(xs + ',' + ys + ',' + zs + ',' + i  + ',' + r_color + ',' + g_color +  ',' + b_color + '\n')
                #verificar que point.GetPointCount() devolve apenas 1
                #print "point count=" ,point.GetPointCount()
                m+=1

        else:
            print('NUM DE VARIAVEIS >=5 !!!!!!!!!!!!!!!!!!!!! do ficheiro csv', fich_1)

        fileinput.close()
        f.close()

        print x,y,z,i
        print line
        print u"nº de linhas", m
