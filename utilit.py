# -*- coding: utf-8 -*-
__author__ = 'm'
import fileinput

# ------------------------------iniciar var
variaveis=''
separador =","
# fich_1 = "C:\mikado_V3.3.3\lists\crs_SDN_L05_55.xml"
fich_1 = "C:/MapX/scripts/crs_SDN_L10_3.xml"
# determinar nome do ficheiro de destino:
print(fich_1)
fich_2=fich_1[0:-3]+"csv"
print "fich_1=" + fich_1
print "fich_2=" + fich_2

f = open(fich_2,'w')
variaveis=[]
 # determinar nº de variaveis por linha (colunas) nos
for line in fileinput.input([ fich_1 ]):
    a=line.strip('\n')

    b=a.find('key=')
    if b>-1:

        c=a.find("key=")
        d=a.find("label")
        variaveis.append(a[c+14:d-3])

        c=a.find("label=")
        d=a.find("short")
        variaveis.append(a[c+7:d-3])
        print("variaveis[0]=",variaveis[0])
        print("variaveis[1]=",variaveis[1])


        f.write(variaveis[0] + ', ' + variaveis[1] + '\n')
        variaveis=[]
fileinput.close()
f.close()
