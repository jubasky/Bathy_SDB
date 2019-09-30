# -*- coding: utf-8 -*-
from qgis.core import *
from PyQt4 import QtCore, QtGui
import traceback
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time
from classConfig import Config


class WLerPontos(QtCore.QObject):
    """Classe Worker para extrair pontos xyzirgb dos patches"""
    def __init__(self, cdi):
        QtCore.QObject.__init__(self)

        if cdi <= 0:
            raise ValueError('Esperado: inteiro >0, recebido: {} '.format(cdi))

        self.Config = Config('config.ini')
        self.cdi = cdi
        self.layer = None
        self.killed = False


    def run(self):
        ret = None
        conn = None
        try:
            # extrair pontos xyz da tabela patches
            total_pontos = 0

            tempo1 = time.time()
            # ------------------- Lê dados da tabela patches_info correspondentes ao registo seleccionado
            conn = psycopg2.connect(self.Config.Conn)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            prof_max = -6000
            prof_min = 20
            nome_dataset = ''
            sql = 'select codigo from patches_info where id=' + str(self.cdi) + ';'
            print "sql=" + sql

            cur.execute(sql)
            resultado = cur.fetchall()

            if len(resultado) > 0:
                nome_dataset = resultado[0][0]

            conn.close()

            conn = psycopg2.connect(self.Config.Conn)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            sql = "DELETE FROM public.pontos;"
            sql = sql +  "INSERT INTO public.pontos (id, cdi, geom, z) "
            sql = sql + "SELECT  f_pontoscdi.id, f_pontoscdi.cdi, "
            sql = sql + "f_pontoscdi.pt, f_pontoscdi.z "
            sql = sql + "FROM f_pontoscdi(" + str(self.cdi) +  ") f_pontoscdi(n, id, cdi, pt, z);"

            cur.execute(sql)
            conn.close()
            tempo2 = time.time()
            print('tempo2-tempo1=', (tempo2 - tempo1))

            print("classWlerPontos: CDI_DB : cdi=", self.cdi)
            uri = QgsDataSourceURI()
            uri.setConnection(self.Config.Host, self.Config.Port, self.Config.Db, self.Config.User,self.Config.Passwd)
            uri.setSrid('4326')
            uri.setDataSource("public", "pontos", "geom", "", "n")
            lyrPontos = QgsVectorLayer(uri.uri(),  str(self.cdi) + " - *", "postgres")

            if self.killed is True:
                return

            strTemp = self.Config.Path + "/data/pts_" + nome_dataset
            writer = QgsVectorFileWriter.writeAsVectorFormat(lyrPontos, r"" + strTemp  + ".shp",
                                                             "utf-8", None, "ESRI Shapefile")

            shapefile = strTemp  + ".shp"
            print('classWlerPontos: gravada shapefile ' + shapefile)

            if self.killed is False:
                ret = shapefile

        except Exception, e:
            # emitir erro de volta para objecto que pediu o serviço
            self.error.emit(e, traceback.format_exc())
            print e.message

        self.finished.emit(ret)

    def kill(self):
        self.killed = True

    finished = QtCore.pyqtSignal(object)
    error = QtCore.pyqtSignal(Exception, basestring)