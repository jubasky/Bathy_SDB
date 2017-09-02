# -*- coding: utf-8 -*-
# --- 10/01/2017 - 14h59m
# -------- Funções da classe original "classTreeVMenuProvider" já não utilizadas (por enquanto)

def Livraria(self):
    pass

    # testes expeditos de carregar layers com sql
    # sql = "(SELECT f_pontos.n,f_pontos.id, f_pontos.cdi, ST_SetSRID(f_pontos.pt, 4326) as geom, "
    # sql = sql + "f_pontos.z FROM f_pontos(2, 23910293) f_pontos(n, id, cdi, pt, z))"
    # print sql
    #
    # uri.setSrid('4326')
    # lyrPatches = QgsVectorLayer(uri.uri(), "v_pts", "postgres")
    # QgsMapLayerRegistry.instance().addMapLayer(lyrPatches)
    # mapa_patches_list.append(QgsMapCanvasLayer(lyrPatches))


def showGrid_back(self):
    # --------------- Criar memory layer com grelha de partições

    layer = QgsVectorLayer("Polygon?crs=EPSG:4326&field=id:integer", "Grid", "memory")
    provider = layer.dataProvider()
    layer.setLayerName('grid')
    QgsMapLayerRegistry.instance().addMapLayer(layer)
    fields = provider.fields()
    features = []

    longitude = [-10.0, -5, 0]
    latitude = [36.0, 38.0, 40.0, 43.0]

    p = 0
    for m in range(0, 1):
        x1 = str(longitude[m])
        x2 = str(longitude[m + 1])
        for n in range(0, 3):
            p += 1
            y1 = str(latitude[n])
            y2 = str(latitude[n + 1])
            feature = QgsFeature()
            strPol = "POLYGON((" + x1 + " " + y1 + "," + x1 + " " + y2 + "," + x2 + " " + y2 + "," + x2 + " " + y1 + "," + x1 + " " + y1 + "))"
            print strPol
            feature.setGeometry(QgsGeometry.fromWkt(strPol))
            feature.setFields(fields)
            feature.setAttribute("id", p)
            features.append(feature)

    x1 = '-32.0'
    x2 = '-10.0'
    y1 = '36.0'
    y2 = '43.0'
    feature = QgsFeature()
    strPol = "POLYGON((" + x1 + " " + y1 + "," + x1 + " " + y2 + "," + x2 + " " + y2 + "," + x2 + " " + y1 + "," + x1 + " " + y1 + "))"
    print strPol
    feature.setGeometry(QgsGeometry.fromWkt(strPol))
    feature.setFields(fields)
    feature.setAttribute("id", p + 1)
    features.append(feature)

    x1 = '-32.0'
    x2 = '-5.0'
    y1 = '30.0'
    y2 = '36.0'
    feature = QgsFeature()
    strPol = "POLYGON((" + x1 + " " + y1 + "," + x1 + " " + y2 + "," + x2 + " " + y2 + "," + x2 + " " + y1 + "," + x1 + " " + y1 + "))"
    print strPol
    feature.setGeometry(QgsGeometry.fromWkt(strPol))
    feature.setFields(fields)
    feature.setAttribute("id", p + 2)
    features.append(feature)
    strtemp = 'N. de poligonos lidos = '
    print(strtemp + str(len(features)))

    x1 = '-180.0'
    x2 = '-5.0'
    y1 = '30.0'
    y2 = '36.0'
    feature = QgsFeature()
    strPol = "POLYGON((" + x1 + " " + y1 + "," + x1 + " " + y2 + "," + x2 + " " + y2 + "," + x2 + " " + y1 + "," + x1 + " " + y1 + "))"
    print strPol
    feature.setGeometry(QgsGeometry.fromWkt(strPol))
    feature.setFields(fields)
    feature.setAttribute("id", p + 2)
    features.append(feature)
    strtemp = 'N. de poligonos lidos = '
    print(strtemp + str(len(features)))

    provider.addFeatures(features)
    layer.updateExtents()


def lerPontosCDI_Sql(self, cdi):
    print ('lerPontosCDI_Sql  cdi = ', cdi)
    uri = QgsDataSourceURI()
    uri.setConnection(self.Config.Host, self.Config.Port, self.Config.Db, self.Config.User, self.Config.Passwd)
    sql = "(SELECT f_pontoscdi.n, f_pontoscdi.id, f_pontoscdi.cdi, st_SetSRID(f_pontoscdi.pt, 4326) as pt, f_pontoscdi.z "
    sql = sql + "FROM f_pontoscdi(" + str(cdi) + ") f_pontoscdi(n, id, cdi, pt, z))"
    print sql

    uri = QgsDataSourceURI()
    uri.setConnection(self.Config.Host, self.Config.Port, self.Config.Db, self.Config.User, self.Config.Passwd)

    uri.setDataSource("public", sql, "pt", "")
    lyrGrid = QgsVectorLayer(uri.uri(), "grid", "postgres")
    # self.applySymbologyFixedDivisionsMarker(lyrGrid,'z')

    map_layer = QgsMapCanvasLayer(lyrGrid)
    map_layer.setVisible(True)
    QgsMapLayerRegistry.instance().addMapLayer(lyrGrid)


def lerPontosCDI(self, cdi):
    # 1º passo, criar estrutura de dados em memoria com o resultado da query v_pontos
    sql = "SELECT f_pontoscdi.n, f_pontoscdi.id, f_pontoscdi.cdi, "
    sql = sql + "ST_AsText(f_pontoscdi.pt) as geom, f_pontoscdi.z "
    sql = sql + "FROM f_pontoscdi(" + str(cdi) + ") f_pontoscdi(n, id, cdi, pt, z);"

    conn = psycopg2.connect(self.Config.Conn)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    ver = cur.fetchall()

    layer = QgsVectorLayer("Point?crs=EPSG:4326&field=id:integer&field=cdi:integer&field=z:double", "Point ",
                           "memory")
    provider = layer.dataProvider()
    layer.setLayerName('point_cdi_' + str(cdi).strip(' '))
    QgsMapLayerRegistry.instance().addMapLayer(layer)
    fields = provider.fields()
    features = []

    for linha in ver:
        lista = []
        a = str(linha)
        lista = a.split(',')
        b = str(lista[3])
        feature = QgsFeature()
        c = b[8:]
        c = c[:-2]
        xy = c.split(' ')
        x = xy[0]
        y = xy[1]
        feature.setGeometry(QgsGeometry.fromWkt("POINT (" + x + " " + y + ")"))
        feature.setFields(fields)
        feature.setAttribute("id", int(lista[1]))
        feature.setAttribute("cdi", int(lista[2]))
        c = lista[4][9:]
        c = c[:-1]
        feature.setAttribute("z", c)
        features.append(feature)

    print(len(features), ' pontos lidos')
    cur.close()
    conn.close()

    provider.addFeatures(features)
    layer.updateExtents()


def lerPontosCDI_DB(self, cdi):
    conn = psycopg2.connect(self.Config.Conn)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    sql = "DELETE FROM public.pontos;"
    sql = sql + "INSERT INTO public.pontos (id, cdi, geom, z) "
    sql = sql + "SELECT  f_pontoscdi.id, f_pontoscdi.cdi, "
    sql = sql + "f_pontoscdi.pt, f_pontoscdi.z "
    sql = sql + "FROM f_pontoscdi(" + str(cdi) + ") f_pontoscdi(n, id, cdi, pt, z);"

    print(sql)
    try:
        cur.execute(sql)

    except:
        print('erro ººººººººººººººººººººººººººººººº')
    finally:
        cur.close()
        conn.close()

    print("classTreeVMenuProvider  lerPontosCDI_DB : cdi=", cdi)
    uri = QgsDataSourceURI()
    uri.setConnection(self.Config.Host, self.Config.Port, self.Config.Db, self.Config.User, self.Config.Passwd)

    uri.setSrid('4326')
    uri.setDataSource("public", "pontos", "geom", "", "n")

    lyrPatches = QgsVectorLayer(uri.uri(), str(cdi) + " - *", "postgres")
    # featuresA = [feat for feat in lyrPatches.getFeatures()]
    print('*********************************** featuresA')

    writer = QgsVectorFileWriter.writeAsVectorFormat(lyrPatches, r"C:/MapX/Data/hoppla.shp", "utf-8", None,
                                                     "ESRI Shapefile")
    shapefile = "C:/MapX/Data/hoppla.shp"
    layerB = QgsVectorLayer(shapefile, "world_vector", "ogr")

    # # Duplicar layerA (na BD) para layerB (em memoria)
    # layerB = QgsVectorLayer("Point?crs=epsg:4326&index=yes", "LayerB", "memory")
    # attr = lyrPatches.dataProvider().fields().toList()
    # layerB_data = layerB.dataProvider()
    # layerB_data.addAttributes(attr)
    # layerB.updateFields()
    # layerB_data.addFeatures(featuresA)
    # layerB.updateExtents()
    # featuresB = [feat for feat in layerB.getFeatures()]

    self.applySymbologyFixedDivisionsMarker(layerB, 'z')
    # renderer = self.definirRendererP(lyrPatches)
    # lyrPatches.setRendererV2(renderer)


    QgsMapLayerRegistry.instance().addMapLayer(layerB)
    map_layer = QgsMapCanvasLayer(layerB)
    map_layer.setVisible(True)

    self.window.setLayerSet([map_layer])
