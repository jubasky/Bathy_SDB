from pyproj import Proj, transform

def converter_simples(x_in, y_in, epsg_1, epsg_2):
    print ('class: converterCSV_WGS84: converter_simples ---------------------------------------')
    inProj = Proj(init='epsg:' + str(epsg_1))
    outProj = Proj(init='epsg:' + str(epsg_2))
    print ('inProj=', epsg_1, ' outProj=', epsg_2, ' ---------------------------------------')

    # Transformar coordenadas (PROJ4)
    # print("x,y = ", x,y)
    x2, y2 = transform(inProj, outProj, x_in, y_in)

    return x2, y2

y = 37.0 + 15.91237758 / 60
x = 7.0 + 37.57637413 /60

x, y = converter_simples(-x, y, 4326, 32629)
print(x, y)
