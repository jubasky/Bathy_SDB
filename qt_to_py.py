# script para compilar forms qt tipo *.ui par *.py

from PyQt4 import uic
fin = open('FormNewDatabase.ui','r')
fout = open('FormNewDatabase.py','w')
uic.compileUi(fin,fout,execute=False)
fin.close()
fout.close()