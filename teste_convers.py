__author__ = 'm'
from pyproj import Proj, transform
import fileinput

a= 2147483647
b= -2147483647

print type(a)
print type(b)

fich_1 ="C:/data/teste_conv.txt"
inProj = Proj(init='epsg:' + str(4326))
outProj = Proj(init='epsg:' + str(27493))
separador = ','

for line in fileinput.input([ fich_1 ]):
    variaveis=line.split(separador)
    x = float(variaveis[0])
    y = float(variaveis[1])
    x2,y2 = transform(inProj,outProj,x,y)
    print(x2,y2)
fileinput.close()
