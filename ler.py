# -*- coding: utf-8 -*-



m = 0

with open('C:/Users/m/Downloads/M2017.dxf', 'r') as f:
    for line in f:
        a = str(line)
        b = a.strip()
        if b == 'AcDbPoint':
            print '*' + b + '*'
            m += 1
print('FIM:', m)

