# script para compilar forms qt tipo *.ui par *.py

from PyQt4 import uic

# fin = open('FormImportFile.ui','r')
# fout = open('FormImportFile.py','w')
#
# fin = open('FormConfig.ui','r')
# fout = open('FormConfig.py','w')
#
fin = open('formPesquisa.ui','r')
fout = open('FormPesquisa.py','w')
#
# fin = open('main_window.ui','r')
# fout = open('main_window.py','w')

uic.compileUi(fin,fout,execute=False)
fin.close()
fout.close()