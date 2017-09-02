# -*- coding: utf-8 -*-

from qgis.gui import *
from qgis.core import *
from qgis.core import QgsRasterLayer
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QFileInfo
from PyQt4.QtGui import QMessageBox
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import random
from classWLerPontos import WLerPontos
from classConfig import Config
from classDB import DB
from classVis import Vis


class TreeVMenuProvider(QgsLayerTreeViewMenuProvider):

    def __init__(self, view, window):

        QgsLayerTreeViewMenuProvider.__init__(self)
        # --------------------------------------------------- Ler constantes a partir de config.ini
        self.Config = Config('config.ini')

        self.view = view
        self.window = window
        self.cdi_anterior = ''

        self.num_pesquisas = 0

    def createContextMenu(self):
        if not self.view.currentLayer():
            return None

        m = QtGui.QMenu()
        m.addAction("Zoom", self.showExtent)
        m.addAction("Info", self.showInfo)
        m.addAction("Ver patches E local", self.showPatches)
        m.addAction("Ver patches E global", self.showPatchesGlobal)

        m.addAction("Ver pontos", self.showPontosCDI)
        m.addAction("Remover", self.removerLayer)
        m.addAction("Reler data", self.reloadLayers)
        m.addAction("Grid", self.showGrid)
        m.addAction("Apagar", self.apagarLayer)
        m.addAction("Seleccao", self.seleccao)
        m.addAction("3d", self.vis3d)


        return m

    def vis3d(self):
        iter = self.view.currentLayer().getFeatures()
        nm = self.view.currentLayer().name()
        print nm[0:3]
        for feature in iter:
            attrs = feature.attributes()
            cdi = str(attrs[0])
            id = str(attrs[1])
            break

        b = Vis(nm,cdi,id)



    def mostrarResultado(self):
        # -------------------------------------------------------- Ler resultado de pesquisa e mostrar na tree view
        uri = QgsDataSourceURI()

        uri.setConnection(self.Config.Host, self.Config.Port, self.Config.Db, self.Config.User, self.Config.Passwd)
        uri.setDataSource("public", "patches_sel", "pa", "", "id")
        lyrResultado = QgsVectorLayer(uri.uri(), "pesquisa", "postgres")
        renderer = self.definirRendererS(True)
        lyrResultado.setRendererV2(renderer)
        map_layer = QgsMapCanvasLayer(lyrResultado)
        map_layer.setVisible(True)
        QgsMapLayerRegistry.instance().addMapLayer(lyrResultado)
        # r = self.view.currentLayer().extent()
        r = lyrResultado.extent()

        # QMessageBox.information(None, "Extent", r.toString())
        self.window.setExtent(r)
        self.window.zoomToSelected()
        self.window.refresh()

    def seleccao(self):
        iter = self.view.currentLayer().getFeatures()
        for feature in iter:
            attrs = feature.attributes()
            cdi = str(attrs[0])
            cdi2 = str(attrs[1])
            print('seleccao: cdi, cdi2:', cdi, cdi2)




    def apagarLayer(self):
        iter = self.view.currentLayer().getFeatures()
        for feature in iter:
            attrs = feature.attributes()
            cdi = str(attrs[0])
            cdi2 = str(attrs[1])
            break

        print('apagar cdi:', cdi)
        # ----------------- Confirmar apagar layer da BD
        reply = QMessageBox.question(self.window, 'Continue?',
                                     'Your message here', QMessageBox.Yes, QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            # --------------- ligar à base de dados
            db_acess = DB()
            db_acess.set_connection(self.Config.Conn)
            db_acess.ligar()
            db_acess.execute_sql('delete from patches_info where id=' + str(cdi) + ";")
            db_acess.execute_sql('delete from patches where cdi=' + str(cdi) + ";")
            db_acess.execute_sql('delete from cdi_equip where cdi=' + str(cdi) + ";")
            db_acess.execute_sql('delete from cdi_param where cdi=' + str(cdi) + ";")
            db_acess.desligar()
            db_acess.set_connection(self.Config.Conn)
            db_acess.ligar()
            db_acess.execute_sql('delete from cdi where id=' + str(cdi) + ";")
            db_acess.desligar()
            db_acess = None



    def showGrid(self):

        # -------------------------------------------------------- Ler grid da BD e mostrar na tree view
        uri = QgsDataSourceURI()

        uri.setConnection(self.Config.Host,self.Config.Port, self.Config.Db, self.Config.User, self.Config.Passwd)
        uri.setDataSource("public", "grid", "geom","", "id")
        lyrGrid = QgsVectorLayer(uri.uri(),  "grid"  , "postgres")
        renderer = self.definirRendererS(True)
        lyrGrid.setRendererV2(renderer)
        map_layer = QgsMapCanvasLayer(lyrGrid)
        map_layer.setVisible(True)
        QgsMapLayerRegistry.instance().addMapLayer(lyrGrid)


    def showPontosCDI(self):

        iter = self.view.currentLayer().getFeatures()
        for feature in iter:
            attrs = feature.attributes()
            cdi = int(attrs[0])
            cdi2 = attrs[1]
        self.ini1 = time.time()

        self.lerPontosCDI_DB_Wk(cdi)

    # ----------------------------- Função para ler pontos com objecto "thread"
    def lerPontosCDI_DB_Wk(self,cdi):
        print('---------------- lerPontosCDI_DB_Wk')
        # --------------------------------------- criar leitor de pontos numa nova thread
        LeitorPontos = WLerPontos(cdi)
        thread = QtCore.QThread()
        LeitorPontos.moveToThread(thread)
        # --------------------------------------- responder aos eventos do leitor de pontos
        LeitorPontos.finished.connect(self.LeitorPontosFinished)
        LeitorPontos.error.connect(self.LeitorPontosError)

        thread.started.connect(LeitorPontos.run)
        thread.start()
        self.thread = thread
        self.LeitorPontos = LeitorPontos
        self.cdi = cdi

    def LeitorPontosFinished(self, ret):
        # --------- Limpar objecto LeitorPontos e respectiva "thread"

        # print('................Tempo em seg.:', (self.ini2-self.ini1))
        self.LeitorPontos.deleteLater()
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()

        if ret is not None:
            # ----------------- devolve shapefile criada localmente
            shapefile = ret
            layerB = QgsVectorLayer(shapefile, "pts_" + str(self.cdi), "ogr")
            self.applySymbologyFixedDivisionsMarker(layerB,'z')
            QgsMapLayerRegistry.instance().addMapLayer(layerB)
            map_layer = QgsMapCanvasLayer(layerB)
            map_layer.setVisible(True)
            self.window.setLayerSet([map_layer])
        else:
            # notify the user that something went wrong
            print('Erroooooooooooooooooo')

    def LeitorPontosError(self, e, exception_string):
        print(u' "thread" LeitorPontos  provocou uma excepção ! :\n'.format(exception_string))

    def lerPontos(self, cdi, id):

        # ---------------------------1º passo, criar estrutura de dados em memoria com o resultado da query v_pontos
        sql = "SELECT f_pontos.n,  f_pontos.cdi, f_pontos.id, "
        sql = sql + "ST_AsText(ST_SetSRID(f_pontos.pt, 4326)) as geom, f_pontos.z "
        sql = sql + "FROM f_pontos(" + str(cdi) + ", " + str(id) + ") f_pontos(n, id, cdi, pt, z);"

        conn = psycopg2.connect(self.Config.Conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(sql)
        ver = cur.fetchall()

        layer = QgsVectorLayer("Point?crs=EPSG:4326&field=id:integer&field=cdi:integer&field=z:double", "Point " + str(id), "memory")
        provider = layer.dataProvider()

        fields = provider.fields()
        features = []
        prof_min = -13000.0
        prof_max = 0.0

        for linha in ver:
            lista =[]
            a=str(linha)
            lista = a.split(',')
            # print lista[3]
            b = str(lista[3])

            c = b[8:]
            c = c[:-2]
            # print c
            xy = c.split(' ')
            x=xy[0]
            y=xy[1]
            # print x,y
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromWkt("POINT ("+x+" "+y+")"))
            feature.setFields(fields)

            feature.setAttribute("cdi", int(lista[2]))
            feature.setAttribute("id", int(lista[1]))
            c = lista[4][10:]
            c = c[:-3]
            d = float(c)

            if prof_max > d:
                prof_max =d

            if prof_min < d:
                prof_min = d

            feature.setAttribute("z", c)
            features.append(feature)

        print(len(features), ' pontos lidos' )
        cur.close()
        conn.close()

        # -------------------------------
        provider.addFeatures(features)

        layer.updateExtents()
        # ---------------------------------------------- ler max e min de prof
        # ----------------------------------------------------------- ligar à BD
        db_acess = DB()
        db_acess.set_connection(self.Config.Conn)
        db_acess.ligar()
        ver = db_acess.ler_sql("select prof_max,prof_min FROM patches_info WHERE id = '" + str(cdi) + "' ;")
        db_acess.desligar()
        db_acess = None

        if len(ver):
            # print("prof_max===",ver)
            prof_max, prof_min = ver[0]
            print("prof_max===", prof_max, "prof_min===", prof_min)

        # self.applySymbologyFixedDivisionsMarker(layer,'z')
        self.applySymbologyMinMaxMarker(layer,prof_max, prof_min,'z' )
        QgsMapLayerRegistry.instance().addMapLayer(layer)

    def reloadLayers(self):

        QgsMapLayerRegistry.instance().removeAllMapLayers()
        self.window.refresh()
        self.MostrarMapa()

    def removerLayer(self):
        # r = self.view.currentLayer().name()
        # print ('Remover layer', r)
        # QgsMapLayerRegistry.instance().removeMapLayer(self.view.currentLayer().id())
        # names = [layer.name() for layer in QgsMapLayerRegistry.instance().mapLayers().values()]
        # print(names)

        n =0
        for nn in self.view.selectedLayers():
            n+=1
            print n, nn.name()
            QgsMapLayerRegistry.instance().removeMapLayer(nn.id())
        self.window.refresh()


    def showExtent(self):
        r = self.view.currentLayer().extent()
        # QMessageBox.information(None, "Extent", r.toString())
        self.window.setExtent(r)
        self.window.refresh()

    def showInfo(self):
        iter = self.view.currentLayer().getFeatures()
        for feature in iter:
            attrs = feature.attributes()


        r = 'Cdi:' + str(attrs[0]) +'\n' + 'Num:' + str(attrs[1])
        QMessageBox.about(None, "Info", r)

    def showPatches(self):
        self.modo = 'local'
        print 'showPatches'
        nome = self.view.currentLayer().name()

        if nome == "pesquisa":
            self.num_pesquisas +=1

            iter = self.view.currentLayer().getFeatures()
            for feature in iter:
                attrs = feature.attributes()
                cdi = str(attrs[1])
                codigo = attrs[1]
                print cdi
                break

            uri = QgsDataSourceURI()
            uri.setConnection(self.Config.Host, self.Config.Port, self.Config.Db, self.Config.User, self.Config.Passwd)
            print('cdi:', cdi)

            self.modo_patches = False
            strSql = 'cdi > 0'
            print strSql
            uri.setDataSource("public", "vv_patches_sel", "geom", strSql, "id")
            uri.setSrid('4326')
            self.modo_patches = True
            lyrPatches = QgsVectorLayer(uri.uri(), "pt:" + str(cdi)+ str(self.num_pesquisas), "postgres")
            campo = 'prof'
            # ---------------------------------------------- ler max e min de prof
            # ----------------------------------------------------------- ligar à BD
            db_acess = DB()
            db_acess.set_connection(self.Config.Conn)
            db_acess.ligar()
            ver = db_acess.ler_sql("select min(PC_PatchMin(pa, 'z')) as prof_max, max(PC_PatchMax(pa, 'z')) as prof_min FROM patches_sel;")
            db_acess.desligar()
            db_acess = None
            prof_max, prof_min = ver[0]
            print prof_max, prof_min
            # self.applySymbologyFixedDivisions(lyrPatches, campo)
            self.applySymbologyMaxMinDivisions(lyrPatches, prof_max, prof_min, campo)

            map_layer = QgsMapCanvasLayer(lyrPatches)
            map_layer.setVisible(True)
            # self.window.refresh()
            QgsMapLayerRegistry.instance().addMapLayer(lyrPatches)
            self.cdi_anterior = cdi
            self.window.refresh()

        else:

            iter = self.view.currentLayer().getFeatures()
            for feature in iter:
                attrs = feature.attributes()
                cdi = str(attrs[0])
                codigo = attrs[1]
                print cdi
                break

            uri = QgsDataSourceURI()
            uri.setConnection(self.Config.Host, self.Config.Port, self.Config.Db, self.Config.User, self.Config.Passwd)
            print('cdi:', cdi)

            self.modo_patches = False
            strSql = 'cdi = ' + cdi
            print('LerCdi.', cdi)
            uri.setDataSource("public", "vv_patches", "geom", strSql, "id")

            uri.setSrid('4326')
            self.modo_patches = True
            lyrPatches = QgsVectorLayer(uri.uri(),  "patches:" + str(codigo) , "postgres")
            campo = 'prof'
            # ---------------------------------------------- ler max e min de prof
            # ----------------------------------------------------------- ligar à BD
            db_acess = DB()
            db_acess.set_connection(self.Config.Conn)
            db_acess.ligar()
            ver = db_acess.ler_sql("select prof_max,prof_min FROM patches_info WHERE id = '" + str(cdi) + "' ;")
            db_acess.desligar()
            db_acess = None


            if len(ver):
                # print("prof_max====",ver)
                prof_max, prof_min= ver[0]
                print("prof_max====", prof_max, "prof_min====", prof_min)

                # -----------------,---------------------------- criar e aplicar Renderer FixedDivisions (em função da prof)
                # self.applySymbologyFixedDivisions(lyrPatches, campo)
                if self.modo == 'global':
                    self.applySymbologyFixedDivisions(lyrPatches, campo)
                else:
                    self.applySymbologyMaxMinDivisions(lyrPatches, prof_max, prof_min,campo)

                map_layer = QgsMapCanvasLayer(lyrPatches)
                map_layer.setVisible(True)
                # self.window.refresh()
                QgsMapLayerRegistry.instance().addMapLayer(lyrPatches)
                self.cdi_anterior = cdi
                self.window.refresh()
                self.window.repaint()



    def showPatchesGlobal(self):
        self.modo ='global'
        iter = self.view.currentLayer().getFeatures()
        for feature in iter:
            attrs = feature.attributes()
            cdi = str(attrs[0])
            cdi2 = str(attrs[1])
            break

        uri = QgsDataSourceURI()
        uri.setConnection(self.Config.Host, self.Config.Port, self.Config.Db, self.Config.User, self.Config.Passwd)
        print('cdi:', cdi, 'cdi_anterior:', self.cdi_anterior)

        self.modo_patches = False

        strSql = 'cdi = ' + cdi
        print('LerCdi.', cdi)
        uri.setDataSource("public", "vv_patches", "geom", strSql, "id")
        uri.setSrid('4326')
        self.modo_patches = True
        lyrPatches = QgsVectorLayer(uri.uri(),  "patches:" + str(cdi2) , "postgres")
        campo = 'prof'
        # ---------------------------------------------- ler max e min de prof
        # ----------------------------------------------------------- ligar à BD
        db_acess = DB()
        db_acess.set_connection(self.Config.Conn)
        db_acess.ligar()
        ver = db_acess.ler_sql("select prof_max,prof_min FROM patches_info WHERE id = '" + str(cdi) + "' ;")
        db_acess.desligar()
        db_acess = None


        if len(ver):
            # print("prof_max====",ver)
            prof_max, prof_min= ver[0]
            print("prof_max====", prof_max, "prof_min====", prof_min)

            # -----------------,---------------------------- criar e aplicar Renderer FixedDivisions (em função da prof)
            # self.applySymbologyFixedDivisions(lyrPatches, campo)
            if self.modo == 'global':
                self.applySymbologyFixedDivisions(lyrPatches, campo)
            else:
                self.applySymbologyMaxMinDivisions(lyrPatches, prof_max, prof_min,campo)

            map_layer = QgsMapCanvasLayer(lyrPatches)
            map_layer.setVisible(True)
            # self.window.refresh()
            QgsMapLayerRegistry.instance().addMapLayer(lyrPatches)
            self.cdi_anterior = cdi
            self.window.refresh()
            self.window.repaint()


    def MostrarMapa(self):

        print('MostrarMapa')
        # ------------------------------------------------------------------------- mapa base raster
        fileName = self.Config.Path + "/data/NE1_HR_LC_SR_W_DR.tif"
        fileInfo = QFileInfo(fileName)
        baseName = fileInfo.baseName()
        baseName = "world_raster"
        self.lyrRaster = QgsRasterLayer(fileName, baseName)
        self.lyrRaster.setCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId))
        if not self.lyrRaster.isValid():
            print "Layer failed to load!"
        else:
            QgsMapLayerRegistry.instance().addMapLayer(self.lyrRaster)
        # ------------------------------------------------------------------------ mapa base vectorial
        shapefile = self.Config.Path + "/data/ne_50m_admin_0_countries.shp"
        self.lyrMapaVector = QgsVectorLayer(shapefile, "world_vector", "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(self.lyrMapaVector)
        # ------------------- identificar todos os datasets presentes na tabela patches
        # ------------------- prever alteração para mostrar a geometria (bounding boxes)
        # ------------------- dos registos de metadados
        lista_cdis=[]
        lista_codigos = []
        conn = None
        try:
            conn = psycopg2.connect(self.Config.Conn)
            cur = conn.cursor()
            # -------------------------------------------------------------
            cur.execute("SELECT id, codigo FROM patches_info ORDER BY id")
            ver = cur.fetchall()
            for linha in ver:
                a = str(linha)
                a = a.replace("'", "")
                a = a.replace("(", "")
                a = a .replace(")", "")
                campos = a.split(",")
                lista_cdis.append(campos[0])
                lista_codigos.append(campos[1])
            print lista_cdis

        except:
            QMessageBox.about(None, "Info", u'Não foi possível ligar à BD ' + self.Config.Db)
            print("erro ao ligar à BD:")
            return

        finally:
            if conn:
                conn.close()

        # --------------------------------------- Verifica se existem dados para mostrar. Se não existirem avisa !
        if len(lista_cdis) == 0:
            QMessageBox.about(None, "Info", u'Não existem dados na BD ' + self.Config.Db)

        else:
            mapa_patches_list = []
            print('+++++++++++++++',lista_cdis)

            for n in range(len(lista_cdis)):
                uri = QgsDataSourceURI()
                cdis = 'id = ' + lista_cdis[n]
                print(cdis)
                uri.setConnection(self.Config.Host, self.Config.Port, self.Config.Db, self.Config.User, self.Config.Passwd)
                uri.setDataSource("public", "patches_info", "geom", cdis, "id")
                uri.setSrid('4326')
                lyrPatches = QgsVectorLayer(uri.uri(), "CDI:" + lista_codigos[n] , "postgres")
                renderer = self.definirRendererS(False)
                lyrPatches.setRendererV2(renderer)
                QgsMapLayerRegistry.instance().addMapLayer(lyrPatches)

                if n == 0:
                    extent = lyrPatches.extent()
                else:
                    extent.combineExtentWith(lyrPatches.extent())

                mapa_patches_list.append(QgsMapCanvasLayer(lyrPatches))

            self.window.setExtent(extent)
            self.window.setLayerSet(mapa_patches_list)

        self.window.refresh()
        self.modo_patches = False

    def definirRendererP(self, myVectorLayer):
        print("myVectorLayer.geometryType=", myVectorLayer.geometryType())
        myTargetField = 'z'
        myRangeList = []
        myOpacity = 1
        # Make our first symbol and range...
        myMin = -6000.0
        myMax = -3000.0
        myLabel = 'Group 1'
        myColour = QtGui.QColor('#ffee00')
        mySymbol1 = QgsSymbolV2.defaultSymbol(myVectorLayer.geometryType())
        #mySymbol1.setColor(myColour)

        #mySymbol1.setAlpha(myOpacity)
        myRange1 = QgsRendererRangeV2(myMin, myMax, mySymbol1, myLabel)
        myRangeList.append(myRange1)
        #now make another symbol and range...
        myMin = -3000.0
        myMax = 20.0
        myLabel = 'Group 2'
        myColour = QtGui.QColor('#00eeff')
        mySymbol2 = QgsSymbolV2.defaultSymbol(myVectorLayer.geometryType())
        # mySymbol2.setColor(myColour)
        # mySymbol2.setAlpha(myOpacity)
        myRange2 = QgsRendererRangeV2(myMin, myMax, mySymbol2, myLabel)
        myRangeList.append(myRange2)

        myRenderer = QgsGraduatedSymbolRendererV2('', myRangeList)
        myRenderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
        myRenderer.setClassAttribute(myTargetField)
        symbol = QgsMarkerSymbolV2.createSimple({'name': 'square', 'color': 'red'})
        myRenderer = QgsSingleSymbolRendererV2(symbol)

        return myRenderer


    def definirRendererS(self, border):

        myStyle = QgsStyleV2().defaultStyle()

        randomColor = QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255))

        if border:
            symbol_ok = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '255,0,0,255', 'style_border':'yes'})
        else:
            symbol_ok = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '255,0,0,255', 'style_border':'no'})

        symbol_ok.setColor(randomColor)
        # ------------------- definir rampa de cores  #RdBu

        numberOfClasses=1
        myRenderer = QgsSingleSymbolRendererV2(symbol_ok)


        return myRenderer

    def definirRendererPatchesTV(self):

        myStyle = QgsStyleV2().defaultStyle()
        defaultColorRampNames = myStyle.colorRampNames()
        ramp = myStyle.colorRamp(defaultColorRampNames[16])
        # ------------------ criar simbolo (quadrado) para representar patches, sem line border !
        symbol_ok = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '255,0,0,255', 'style_border':'no'})
        # ------------------- definir rampa de cores  #RdBu

        numberOfClasses=10
        myRenderer = QgsGraduatedSymbolRendererV2()
        myRenderer.setInvertedColorRamp(True)
        myRenderer.setSourceSymbol(symbol_ok)
        myRenderer.setClassAttribute('-prof')
        myRenderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
        myRenderer.updateClasses(self.lyrPatches,QgsGraduatedSymbolRendererV2.EqualInterval,numberOfClasses)

        myRenderer.updateColorRamp(ramp)

        return myRenderer

    def definirRendererPatchesD(self):

        lista=[-6000,-3000,-1000,-500,-300,-100,-50, -30,-10,50]
        myTargetField = 'prof'
        myRangeList = []
        myOpacity = 1
        for n in range(0,9):
            myMin = lista[n]
            myMax = lista[n+1]
            myLabel = str(myMin) + ' ' + str(myMax)
            myColour = QtGui.QColor(n*25,0,160 + n*10)

            mySymbol1 = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '255,0,0,255', 'style_border':'no'})
            mySymbol1.setColor(myColour)
            mySymbol1.setAlpha(myOpacity)
            myRange1 = QgsRendererRangeV2(myMin, myMax, mySymbol1, myLabel)
            myRangeList.append(myRange1)

        myRenderer = QgsGraduatedSymbolRendererV2('', myRangeList)
        myRenderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
        myRenderer.setClassAttribute(myTargetField)

        return myRenderer



    def makeSymbologyForRange(self, layer, min , max, title, color):
        symbol = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '255,0,0,255', 'style_border':'no'})
        symbol.setColor(color)
        range = QgsRendererRangeV2( min, max, symbol, title )
        return range

    def applySymbologyFixedDivisions( self, layer, field ):
        rangeList = []
        rangeList.append(self.makeSymbologyForRange( layer, -6000.00, -3000.00, '-6000 -3000', QtGui.QColor("#00007f") ) )
        rangeList.append( self.makeSymbologyForRange( layer, -3000.00, -1000.00, '-3000 -1000', QtGui.QColor("#0000e2") ) )
        rangeList.append( self.makeSymbologyForRange( layer, -1000.00, -200.00, '-1000 -200', QtGui.QColor("#0000ff") ) )
        rangeList.append( self.makeSymbologyForRange( layer, -200.00, -100.00, '-200 -100', QtGui.QColor("#0a61ff") ) )
        rangeList.append( self.makeSymbologyForRange( layer, -100.00, -50.00, '-100 -50', QtGui.QColor("#00aaff") ) )
        rangeList.append( self.makeSymbologyForRange( layer, -50.00, 0.00, '-50 0', QtGui.QColor("#ffaa7f") ) )
        rangeList.append( self.makeSymbologyForRange( layer, 0.00, 10000.00, '0 10000', QtGui.QColor("#ff5500") ) )
        renderer = QgsGraduatedSymbolRendererV2( field, rangeList )
        renderer.setMode( QgsGraduatedSymbolRendererV2.Custom )
        layer.setRendererV2( renderer )

    # -------- renderer para criar classes de valores adaptados aos min e max dos dados
    def applySymbologyMaxMinDivisions( self, layer, min, max, field):
        rangeList = []
        num_niveis = 7
        amplitude_prof = abs(max - min)
        inc_prof = amplitude_prof/ num_niveis
        rangeColor = []
        rangeColor.append(QtGui.QColor("#00007f"))
        rangeColor.append(QtGui.QColor("#0000e2"))
        rangeColor.append(QtGui.QColor("#0000ff"))
        rangeColor.append(QtGui.QColor("#0a61ff"))
        rangeColor.append(QtGui.QColor("#00aaff"))
        rangeColor.append(QtGui.QColor("#ffaa7f"))
        rangeColor.append(QtGui.QColor("#ff5500"))

        for n in range(1,num_niveis+1):
            a = min+(n-1)*inc_prof
            b = min+(n)*inc_prof
            if a>10 and b>10:
                a = round(a / 10, 0) * 10
                b = round(b/10,0)*10
            else:
                a = round(a ,2)
                b = round(b, 2)

            rangeList.append(self.makeSymbologyForRange(layer,a, b, str(a) + " " + str(b), rangeColor[n-1]))

        rangeList.append( self.makeSymbologyForRange( layer, b, 10000.00, str(b) + ' 10000', QtGui.QColor("#740932") ) )

        renderer = QgsGraduatedSymbolRendererV2( field, rangeList )
        renderer.setMode( QgsGraduatedSymbolRendererV2.Custom )
        layer.setRendererV2( renderer )

    def makeSymbologyForRangeMK(self, layer, min , max, title, color):
        symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
        symbol.setColor(color)
        symbol.setSize(1.1)
        symbol.symbolLayer(0).setOutlineColor(color)

        range = QgsRendererRangeV2( min, max, symbol, title )
        return range

    def applySymbologyFixedDivisionsMarker( self, layer, field ):
        rangeList = []
        rangeList.append(self.makeSymbologyForRangeMK(layer, -6000.00, -3000.00, '-6000 -3000', QtGui.QColor("#00007f")))
        rangeList.append( self.makeSymbologyForRangeMK(layer, -3000.00, -1000.00, '-3000 -1000', QtGui.QColor("#0000e2")))
        rangeList.append( self.makeSymbologyForRangeMK(layer, -1000.00, -200.00, '-1000 -200', QtGui.QColor("#0000ff")))
        rangeList.append( self.makeSymbologyForRangeMK(layer, -200.00, -100.00, '-200 -100', QtGui.QColor("#0a61ff")))
        rangeList.append( self.makeSymbologyForRangeMK(layer, -100.00, -50.00, '-100 -50', QtGui.QColor("#00aaff")))
        rangeList.append( self.makeSymbologyForRangeMK(layer, -50.00, 0.00, '-50 0', QtGui.QColor("#ffaa7f")))
        rangeList.append( self.makeSymbologyForRangeMK(layer, 0.00, 10.00, '0 10', QtGui.QColor("#ff5500")))

        renderer = QgsGraduatedSymbolRendererV2(field, rangeList)
        renderer.setMode(QgsGraduatedSymbolRendererV2.Custom)

        layer.setRendererV2(renderer)

    def applySymbologyMinMaxMarker( self, layer, max, min, field ):
        rangeList = []
        num_niveis = 7
        amplitude_prof = abs(max - min)
        inc_prof = amplitude_prof / num_niveis
        rangeColor = []
        rangeColor.append(QtGui.QColor("#00007f"))
        rangeColor.append(QtGui.QColor("#0000e2"))
        rangeColor.append(QtGui.QColor("#0000ff"))
        rangeColor.append(QtGui.QColor("#0a61ff"))
        rangeColor.append(QtGui.QColor("#00aaff"))
        rangeColor.append(QtGui.QColor("#ffaa7f"))
        rangeColor.append(QtGui.QColor("#ff5500"))

        print('max, min=',max, min)

        for n in range(1, num_niveis + 1):
            a = max + (n - 1) * inc_prof
            b = max + (n) * inc_prof
            if a > 10 and b > 10:
                a = round(a / 10, 0) * 10
                b = round(b / 10, 0) * 10
            rangeList.append(self.makeSymbologyForRangeMK(layer, a, b, str(a) + " " + str(b), rangeColor[n - 1]))

        rangeList.append(self.makeSymbologyForRangeMK(layer, b, 10000.00, str(b) + ' 10000', QtGui.QColor("#740932")))

        renderer = QgsGraduatedSymbolRendererV2(field, rangeList)
        renderer.setMode(QgsGraduatedSymbolRendererV2.Custom)

        layer.setRendererV2(renderer)

    # ----------------------------------- preparar visualização da prof por gradação de cores
    def definirRendererPatches(self):

        myStyle = QgsStyleV2().defaultStyle()
        defaultColorRampNames = myStyle.colorRampNames()
        ramp = myStyle.colorRamp(defaultColorRampNames[16])
        # ------------------ criar simbolo (quadrado) para representar patches, sem line border !
        symbol_ok = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '255,0,0,255', 'style_border':'no'})
        # ------------------- definir rampa de cores  #RdBu

        numberOfClasses=10
        myRenderer = QgsGraduatedSymbolRendererV2()
        myRenderer.setInvertedColorRamp(True)
        myRenderer.setSourceSymbol(symbol_ok)
        myRenderer.setClassAttribute('-prof')
        myRenderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
        myRenderer.updateClasses(self.lyrPatches,QgsGraduatedSymbolRendererV2.EqualInterval,numberOfClasses)

        myRenderer.updateColorRamp(ramp)

        return myRenderer

