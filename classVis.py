# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.mlab as ml
import visvis
from classDB import DB
from classConfig import Config
import psycopg2
class Vis():
    def __init__(self,nome, cdi,id):

        self.nome = nome
        self.cdi = cdi
        self.id = id
        self.Config = Config('config.ini')
        print('Vis: cdi=', cdi)
        self.ler_dados()

    def ler_dados(self):

        # ---  determina tipo de layer (pesquisa_patches, cdi_hull, cdi_patches, pontos, etc.)
        # ---  e chama a função adequada para preparação do ficheiro ascii a passar ao objecto
        # ---  VisPy para vusualização 3D

        print ('classVis: ler_dados(): nome do conjunto de dados = ', self.nome)

        if self.nome == 'pesquisa':
            print 'Pesquisa'
            self.lerPesquisa()
        if self.nome[0:3] == 'CDI':
            print 'CDI', "patches_info"
            # extrair xyz para ficheiro
            self.lerPatches()
        if self.nome[0:3] == 'pat':
            print 'Patches'
            self.lerPatches()
        if self.nome[0:3] == 'Poi':
            print 'points'
            self.lerPoints()

        x, y, z = np.genfromtxt('c:/MapX/data/3d.csv', delimiter=',', unpack=True, usecols=(0, 1, 2))
        # x,y,z = np.genfromtxt('c:/data/pts3d.csv',delimiter=';', skiprows=1,unpack=True, usecols=(0,1,3))
        # x,y,z = np.genfromtxt('c:/data/teste4.csv',delimiter=',', unpack=True, usecols=(0,1,2)

        #print z
        #print x[0], y[0], z[0]



        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        zmin = min(z)
        zmax = max(z)




        # passar valores de z para escala de 0 a 1
        # vai ser necessario compensar isto com um factor de
        # sobreelevacao de 10000 !! ver abaixo:
        z -= min(z)
        z /= max(z)

        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        zmin = min(z)
        zmax = max(z)
        # z *= 2
        print('min e max de x,y,z:', xmin, xmax, ymin, ymax, zmin, zmax)

        # definir resolucao dos pontos para visualizacao
        xi = np.linspace(xmin, xmax,num=200)
        yi = np.linspace(ymin, ymax,num=200)
        # print xi, yi

        X, Y = np.meshgrid(xi, yi)

        Z = ml.griddata(x, y, z, xi, yi)

        # definir resolucao da grid para visualizacao
        xig = np.linspace(xmin, xmax,num=20)
        yig = np.linspace(ymin, ymax,num=20)
        # print xi, yi
        Xg, Yg = np.meshgrid(xig, yig)
        Zg = ml.griddata(x, y, z, xig, yig)
        # Z*=-1

        # --------------------------------- VisVis
        f = visvis.gca()
        a = visvis.cla()
        a.cameraType = '2d'

        sobre_elev = abs((xmax-xmin)/(zmax-zmin))*0.2
        f.daspect = 1,1,sobre_elev # z x 10000
        # draped colors
        # print ('Z =',Z)
        m = visvis.surf(xi,yi,Z)
        #nm = visvis.grid(xi,yi,Z)
        m.colormap = visvis.CM_JET
        #nm.colormap = visvis.CM_COOL
        visvis.ColormapEditor(f)
        visvis.colorbar()

        # Create text labels
        label1 = visvis.Label(a, 'This is a Label')
        label1.position = 490, 2
        label1.bgcolor = (0.5, 1, 0.5)

        app = visvis.use()
        # NESTE CONTEXTO NÃO É NECESSARIO
        # app.Run()

    def lerPesquisa(self):
        print('ler pesquisa')
        fich_saida = self.Config.Path + '/data/3d.csv'
        sql = """
        SELECT patches_sel.cdi,patches_sel.id, st_x(st_centroid(geometry(patches_sel.pa))) AS x,
        st_y(st_centroid(geometry(patches_sel.pa))) AS y,
        pc_patchavg(patches_sel.pa, 'z'::text)::double precision AS z
        FROM patches_sel;"""

        db_acess = DB()
        db_acess.set_connection(self.Config.Conn)
        db_acess.ligar()
        ver = db_acess.ler_sql(sql)
        db_acess.desligar()

        prof_min = -6000.0
        prof_max = 0.0
        n = 0

        if len(ver) == 0:
            return

        with open(fich_saida, 'w') as fout:
            for linha in ver:
                lista = []

                a = str(linha)
                a = a.strip('()')
                lista = a.split(',')
                # print a
                # print lista

                # rr = raw_input('ooo')

                x = lista[2]
                y = lista[3]
                z = lista[4]

                # print x,y
                fout.write(x + ',' + y + ',' + z + ',' + "'" + self.cdi + "'" + '\n')
                n += 1
            print(a, lista)
            print(n, ' pontos lidos')


    def lerPatches(self):
        print('classVis: LerPatches')
        fich_saida = self.Config.Path + '/data/3d.csv'

        print self.Config.Path
        print fich_saida

        sql = "select cdi,id, st_x(pp) as x, st_y(pp) as y, prof as z "
        sql = sql + "from v_patches where "
        sql = sql + "cdi=" + str(self.cdi) + ";"

        db_acess = DB()
        db_acess.set_connection(self.Config.Conn)
        db_acess.ligar()
        ver = db_acess.ler_sql(sql)
        db_acess.desligar()

        prof_min = -6000.0
        prof_max = 0.0
        n = 0

        if len(ver)==0:
            return

        with open(fich_saida, 'w') as fout:
            for linha in ver:
                lista = []

                a = str(linha)
                a = a.strip('()')
                lista = a.split(',')
                # print a
                # print lista

                # rr = raw_input('ooo')

                x = lista[2]
                y = lista[3]
                z = lista[4]

                # print x,y
                fout.write(x + ',' + y + ',' + z + ',' + "'" + self.cdi + "'" + '\n')
                n+=1
            print(a,lista)
            print(n, ' pontos lidos')

    def lerPoints(self):
        print('classVis: LerPoints')
        fich_saida = self.Config.Path + '/data/3d.csv'
        print('Path:', self.Config.Path, ' fich_saida:', fich_saida,' nome:', self.nome, ' cdi:', self.cdi, ' id:', self.id)


        # ---------------------------1º passo, criar estrutura de dados em memoria com o resultado da query v_pontos
        sql = "SELECT f_pontos.n, f_pontos.cdi, f_pontos.id, "
        sql = sql + "ST_AsText(ST_SetSRID(f_pontos.pt, 4326)) as geom, f_pontos.z "
        sql = sql + "FROM f_pontos(" + str(self.cdi) + ", " + str(self.id) + ") f_pontos(n, id, cdi, pt, z);"

        db_acess = DB()
        db_acess.set_connection(self.Config.Conn)
        db_acess.ligar()
        ver = db_acess.ler_sql(sql)
        db_acess.desligar()

        prof_min = -6000.0
        prof_max = 0.0
        n = 0

        if len(ver)==0:
            return

        with open(fich_saida, 'w') as fout:
            for linha in ver:
                lista = []
                a = str(linha)
                lista = a.split(',')
                # print lista[3]
                b = str(lista[3])

                c = b[8:]
                c = c[:-2]
                # print c
                xy = c.split(' ')
                x = str(xy[0])
                y = str(xy[1])

                c = lista[4][10:]
                c = c[:-3]
                d = str(float(c))

                if prof_max > d:
                    prof_max = d

                if prof_min < d:
                    prof_min = d

                fout.write(x + ',' + y + ',' + d + ',' + "'" + self.cdi + "'" + '\n')
                n+=1

            print('x,y,d:',x,y,d)
            print(a,lista)
            print(n, ' pontos lidos')


